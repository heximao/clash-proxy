#!/usr/bin/env python3
"""批量查证待判定域名的网络侧证据（RDAP / SOA / NS / A / CNAME / HTTP 标题）。

用法：
    python3 probe_domains.py <domain> [<domain> ...] [--json /tmp/out.json] [--no-http]

输出每域名一段，字段含义：
    SOA(邮箱)  权威区 SOA 的 rname 字段——厂商自建权威 DNS 时常直接暴露母公司域
               （如 dnsadmin.bytedance.com ⇒ 字节），是最硬的归属锚点
    NS         委托的权威 NS，可暴露 DNS 服务商（volc-dns / nsone / awsdns / alidns）
    RDAP       registrar + 注册/变更日期 + registrar/registrant 实体
    A / CNAME  gethostbyname 被 fake-ip 污染，一律走 DoH
    HTTP       首页状态 + <title>，是「这个域到底做什么服务」最快的一手证据

环境约定：
    - DoH 直连（--noproxy '*'）；RDAP 与 HTTP 走代理（rdap.org 直连返空）
    - 本机 dig 返回 198.18.x fake-ip，不可用于 A 记录判定，故一律 DoH
    - 代理不通时 RDAP/HTTP 会如实报 ERR，不阻塞其余字段
"""
import argparse
import json
import os
import re
import subprocess
import sys

PROXY = os.environ.get("PROBE_PROXY", "http://127.0.0.1:7893")
PY = sys.executable


def curl(args, timeout=25):
    """返回 (stdout, ok)。curl 非 0 退出但有 body 时仍算 ok。"""
    try:
        r = subprocess.run(["curl", "-s", "--max-time", str(timeout)] + args,
                           capture_output=True, text=True, timeout=timeout + 5)
        return r.stdout.strip(), bool(r.stdout.strip())
    except Exception as e:  # noqa: BLE001
        return "ERR:%s" % e, False


def doh(name, rrtype, use_authority=False, timeout=12):
    """Cloudflare DoH，直连。

    默认只取 Answer（A/CNAME/NS 的真实记录）；SOA 在区顶点常落在 Authority 段，
    故 use_authority=True 时回退取 Authority。混在一起会把 SOA 串误当成 A 记录。
    """
    url = ("https://cloudflare-dns.com/dns-query?name=%s&type=%s" % (name, rrtype))
    out, ok = curl(["--noproxy", "*", "-H", "accept: application/dns-json", url], timeout)
    if not ok:
        return []
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return []
    ans = [a.get("data", "") for a in d.get("Answer", [])]
    if not ans and use_authority:
        ans = [a.get("data", "") for a in d.get("Authority", [])]
    return ans


def rdap(domain, retries=3):
    for _ in range(retries):
        out, ok = curl(["-x", PROXY, "-L", "https://rdap.org/domain/%s" % domain], 30)
        if ok and out.startswith("{"):
            try:
                d = json.loads(out)
            except json.JSONDecodeError:
                continue
            info = {"status": d.get("status", [])}
            for e in d.get("events", []):
                if e.get("eventAction") in ("registration", "last changed"):
                    info[e["eventAction"]] = (e.get("eventDate") or "")[:10]
            ents = []
            for ent in d.get("entities", []):
                roles = ent.get("roles", [])
                if not ({"registrar", "registrant"} & set(roles)):
                    continue
                name = ""
                v = ent.get("vcardArray")
                if v and len(v) > 1:
                    for item in v[1]:
                        if item[0] == "fn":
                            name = item[3]
                            break
                ents.append("%s:%s" % ("/".join(roles), name))
            info["entities"] = ents
            return info
    return {"error": "RDAP 无响应（重试 %d 次）" % retries}


def http_title(domain):
    for scheme in ("https", "http"):
        code, ok = curl(["-x", PROXY, "-L", "-o", "/dev/null", "-w", "%{http_code}",
                         "%s://%s/" % (scheme, domain)], 15)
        if not ok or code.strip() in ("000", "000000"):
            continue
        body, _ = curl(["-x", PROXY, "-L", "%s://%s/" % (scheme, domain)], 15)
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        title = re.sub(r"\s+", " ", m.group(1)).strip()[:100] if m else "-"
        return "%s %s | title=%s" % (scheme, code.strip(), title)
    return "无响应"


def soa_admin(soa_records):
    """SOA data 形如 'ns1.volc-dns.com. dnsadmin.bytedance.com. serial refresh retry expire min'。"""
    for rec in soa_records:
        parts = rec.split()
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None, None


def probe(domain, want_http=True):
    res = {"domain": domain}
    soa = doh(domain, "SOA", use_authority=True)
    res["soa"] = soa
    res["soa_mname"], res["soa_admin"] = soa_admin(soa)
    res["ns"] = doh(domain, "NS")
    res["rdap"] = rdap(domain)
    res["a"] = doh(domain, "A")
    res["cname"] = doh(domain, "CNAME")
    res["http"] = http_title(domain) if want_http else "(skipped)"
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domains", nargs="+")
    ap.add_argument("--json", default="")
    ap.add_argument("--no-http", action="store_true")
    a = ap.parse_args()

    rows = []
    for d in a.domains:
        r = probe(d, want_http=not a.no_http)
        rows.append(r)
        print("=" * 66)
        print("##", d)
        print("  SOA(邮箱): %s" % (r["soa_admin"] or "-"))
        print("  NS       : %s" % (" ; ".join(r["ns"]) if r["ns"] else "-"))
        print("  A        : %s" % (" ; ".join(r["a"])[:120] if r["a"] else "-"))
        if r["cname"]:
            print("  CNAME    : %s" % " ; ".join(r["cname"])[:120])
        rd = r["rdap"]
        if "error" in rd:
            print("  RDAP     : %s" % rd["error"])
        else:
            print("  RDAP     : 注册 %s | 变更 %s | %s | %s" % (
                rd.get("registration", "-"), rd.get("last changed", "-"),
                ", ".join(rd.get("entities", [])) or "无实体",
                ", ".join(rd.get("status", [])) or "-"))
        print("  HTTP     : %s" % r["http"])
        sys.stdout.flush()

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print("\nJSON → %s" % a.json)


if __name__ == "__main__":
    main()
