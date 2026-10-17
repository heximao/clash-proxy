#!/usr/bin/env python3
"""规则级查重/覆盖检查：判断给定域名或 IP 是否已被本仓库业务 yaml 规则覆盖。

取代旧流程里 `grep -l "$d" *.yaml` 的子串匹配（会误命中 xxxx53.com，
也会漏掉品牌标签锚点），本脚本按规则类型精确判断：

- DOMAIN-SUFFIX：域名本身或其任一父域等于该值 → 覆盖
- DOMAIN：仅精确主机名命中 → 覆盖（注意：不代表主域覆盖，AGENTS.md 判据 8）
- DOMAIN-KEYWORD：关键词是域名子串 → 报告为 KEYWORD（弱证据，由调用者判断）
- IP-CIDR：IP 落入网段 → 覆盖（含 no-resolve 附加参数的行）

对未覆盖域名额外做「品牌标签锚点」扫描（AGENTS.md 判据 1）：库内存在与
待判域名可注册主域 SLD 标签**逐字符相同**的其他 TLD 变体规则 → 报告
BRAND-ANCHOR（如待判 browserleaks.net、库内已有 browserleaks.com）。

用法：
    python3 check_coverage.py <域名或IP> [更多...]
    cat domains.txt | python3 check_coverage.py -
    python3 check_coverage.py --quiet feishu.cn itdog.cn   # 只列未覆盖项

排除 reject.yaml（bot 独占维护，禁止核对）。
扫描根已锚定仓库根，任意目录可运行。退出码恒为 0（查询工具，非门禁）。
"""
import ipaddress
import re
import sys
from pathlib import Path

out_dir = Path(__file__).resolve().parent
root = out_dir.parent.parent
EXCLUDED = {"reject.yaml"}
RULE_RE = re.compile(r"^\s*-\s*(.+)$")

# 与 extract-match-domains 保持一致的启发式二级 TLD 表
MULTI_TLDS = {
    "com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "ac.cn", "mil.cn",
    "com.hk", "com.tw", "com.sg", "com.au", "com.br", "com.mx", "com.ru",
    "com.tr", "com.ua", "com.vn", "co.uk", "org.uk", "co.jp", "co.kr",
    "co.in", "co.nz", "co.za", "com.ar", "com.co", "com.my", "com.ph",
}


def registrable(host: str) -> str:
    labels = host.split(".")
    if len(labels) <= 2:
        return host
    if ".".join(labels[-2:]) in MULTI_TLDS:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def sld_label(host: str) -> str:
    return registrable(host).split(".")[0]


def build_index():
    suffix_map = {}    # value -> [(file, line, raw)]
    domain_map = {}
    keyword_map = {}
    ip_nets = []       # (network, file, line, raw)
    skipped = 0
    files = sorted(p for p in root.glob("*.yaml") if p.name not in EXCLUDED)
    for p in files:
        for ln_no, line in enumerate(
            p.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            m = RULE_RE.match(line)
            if not m:
                continue
            raw = m.group(1).strip()
            parts = [x.strip() for x in raw.split(",")]
            rtype = parts[0].upper()
            value = parts[1] if len(parts) > 1 else ""
            if rtype == "DOMAIN-SUFFIX" and value:
                suffix_map.setdefault(value.lower(), []).append((p.name, ln_no, raw))
            elif rtype == "DOMAIN" and value:
                domain_map.setdefault(value.lower(), []).append((p.name, ln_no, raw))
            elif rtype == "DOMAIN-KEYWORD" and value:
                keyword_map.setdefault(value.lower(), []).append((p.name, ln_no, raw))
            elif rtype == "IP-CIDR" and value:
                try:
                    ip_nets.append(
                        (ipaddress.ip_network(value, strict=False), p.name, ln_no, raw)
                    )
                except ValueError:
                    skipped += 1
            else:
                skipped += 1
    return suffix_map, domain_map, keyword_map, ip_nets, skipped, files


def check_domain(d, suffix_map, domain_map, keyword_map):
    """返回 (covered_hits, keyword_hits, brand_anchors)。

    covered_hits: [(kind, value, [(file, line, raw)])]
    brand_anchors: [(anchor_value, [(file, line, raw)])]
    """
    d = d.lower().strip(".")
    covered, keywords, anchors = [], [], []

    # 精确 DOMAIN 命中
    if d in domain_map:
        covered.append(("DOMAIN", d, domain_map[d]))

    # DOMAIN-SUFFIX 覆盖：自身及逐级父域
    labels = d.split(".")
    for i in range(len(labels)):
        cand = ".".join(labels[i:])
        if cand in suffix_map:
            covered.append(("DOMAIN-SUFFIX", cand, suffix_map[cand]))

    # DOMAIN-KEYWORD（弱证据）
    for kw, hits in keyword_map.items():
        if kw in d:
            keywords.append((kw, hits))

    # 品牌标签锚点（判据 1）：未覆盖时才扫
    if not covered:
        label = sld_label(d)
        if label:
            seen = set()
            for value, hits in list(suffix_map.items()) + list(domain_map.items()):
                if value == d or value in seen:
                    continue
                try:
                    other = sld_label(value)
                except IndexError:
                    continue
                if other == label:
                    seen.add(value)
                    anchors.append((value, hits))
    return covered, keywords, anchors


def check_ip(ip_str, ip_nets):
    """返回 [(net, file, line, raw)]：包含该 IP 的所有既有网段。"""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return None
    return [t for t in ip_nets if ip in t[0]]


def fmt_hits(hits):
    return "; ".join(f"{f}:{ln} ({raw})" for f, ln, raw in hits)


def main():
    args = [a for a in sys.argv[1:] if a != "--"]
    quiet = False
    if "--quiet" in args:
        quiet = True
        args.remove("--quiet")
    if not args or args == ["-"]:
        args = [ln.strip() for ln in sys.stdin if ln.strip()]

    suffix_map, domain_map, keyword_map, ip_nets, skipped, files = build_index()
    print(f"# loaded {len(files)} yaml files, "
          f"{len(suffix_map)} suffix / {len(domain_map)} domain / "
          f"{len(keyword_map)} keyword rules / {len(ip_nets)} ip-cidr "
          f"(unparsed {skipped}, reject.yaml excluded)")
    print()

    n_covered = n_uncovered = n_anchor = 0
    for item in args:
        item = item.strip().lower()
        if not item:
            continue
        ip_hits = check_ip(item, ip_nets)
        if ip_hits is not None:
            if ip_hits:
                n_covered += 1
                print(f"{item} => COVERED")
                for net, f, ln, raw in ip_hits:
                    print(f"  - {raw} @ {f}:{ln}")
            else:
                n_uncovered += 1
                print(f"{item} => UNCOVERED (ip)")
            continue

        covered, keywords, anchors = check_domain(
            item, suffix_map, domain_map, keyword_map
        )
        if covered:
            n_covered += 1
            if not quiet:
                print(f"{item} => COVERED")
                for kind, value, hits in covered:
                    print(f"  - {kind},{value} @ {fmt_hits(hits)}")
        else:
            n_uncovered += 1
            if quiet:
                print(f"{item} => UNCOVERED")
            else:
                print(f"{item} => UNCOVERED")
            for kw, hits in keywords:
                print(f"  - DOMAIN-KEYWORD,{kw} @ {fmt_hits(hits)} (弱证据，自行判断)")
            for value, hits in anchors:
                n_anchor += 1
                print(f"  - BRAND-ANCHOR: {value} @ {fmt_hits(hits)} "
                      f"(判据1 同标签 TLD 变体)")

    print()
    print(f"# summary: covered {n_covered}, uncovered {n_uncovered} "
          f"(brand-anchor {n_anchor})")


if __name__ == "__main__":
    main()
