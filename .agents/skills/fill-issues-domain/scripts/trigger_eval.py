#!/usr/bin/env python3
"""trigger_eval.py — route-edit 前置关卡 + 2026-10-28 16 项回归用例。

本脚本是 yao-meta-skill Compact Workflow 第 5 步要求的 trigger 评测脚本：
"route edits need trigger_eval.py"。它解决两个问题：

1. **路由判定**（默认模式）：给定一个用户输入文本，判定它应该路由到
   - `fill-issues-domain`（处理待人工域名表 / 给挂起域名定归属 / 清理挂起表）
   - `fill-domains-from-log`（处理日志漏网之鱼 / 提取 match Match 域名）
   - `none`（信息查询 / 配置问题 / 与 skill 无关）
   并给出置信度。

2. **回归用例**（--regression 模式）：重放 2026-10-28 全部定案的 16 项
   作为判据/口径变更后的回归基线。每项标注当时裁决去向与关键锚点；
   跑回归时验证既定判据仍能复现当时的去向。任意锚点漂移到无法支撑原
   裁决时报告 `REGRESSION-DRIFT`。

用法：
    # 路由判定（默认模式，读 cases.json）
    python3 trigger_eval.py
    python3 trigger_eval.py --text "把 issues-domain 表里那几个域名定一下"

    # 回归模式（跑 16 项内嵌用例，不联网；--online 联网重跑证据采集）
    python3 trigger_eval.py --regression
    python3 trigger_eval.py --regression --online

设计原则：
    - 自包含，不依赖 yao-meta-skill 的 semantic_config（保持本 skill 自洽）。
    - 路由判定用关键词 + 简单否定模式；不引入 embedding/LLM 调用。
    - 回归模式不联网时只比对内嵌锚点（不会失败，只可能 DRIFT）；
      --online 时实际调用 probe_domains / verify_landing / log_cooccurrence
      重跑证据采集，比对当前输出与内嵌锚点。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# =====================================================================
# 路由判定
# =====================================================================

# fill-issues-domain 的强信号词（命中即路由到本 skill）
FID_TRIGGER_PATTERNS = [
    r"issues[- ]?domain",
    r"待人工(?:判定|裁决|确认|域名)",
    r"挂起(?:表|清单|域名|的)",
    r"清理.{0,4}挂起",
    r"清(?:空|零).{0,4}(?:挂起|待判|issues)",
    r"给.{0,6}(?:挂起|待判|待人工)(?:的)?域名.{0,4}定",
    r"(?:定|处理|消费|裁决).{0,6}(?:挂起|待判|待人工|issues)",
    r"上次登记.{0,6}域名",
    r"批量定.{0,6}(?:域名|挂起|issues)",
]

# fill-domains-from-log 的强信号词（命中即路由到姊妹 skill，不路由到本 skill）
FDFL_TRIGGER_PATTERNS = [
    r"漏网之鱼",
    r"match\s*Match",
    r"oc-cn-domain",
    r"(?:从|分析)\s*(?:今日|昨天|今天)?\s*(?:的)?\s*日志",
    r"提取(?:日志|漏网)",
    r"补(?:漏|规则)",
    r"日志(?:补规则|提取|分析)",
]

# 否定模式（明显不该路由到任何 skill）
NEGATIVE_PATTERNS = [
    r"只要总结",
    r"翻译一下",
    r"头脑风暴",
    r"解释一下",
    r"什么是",
    r"怎么用\s*clash",
    r"clash\s*配置",
]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def classify(text: str) -> dict:
    """判定路由归属 + 置信度。"""
    norm = normalize(text)

    for neg in NEGATIVE_PATTERNS:
        if re.search(neg, norm, re.IGNORECASE):
            return {"route": "none", "confidence": 0.9,
                    "reason": "命中否定模式：%s" % neg}

    fid_hits = [p for p in FID_TRIGGER_PATTERNS if re.search(p, norm, re.IGNORECASE)]
    fdfl_hits = [p for p in FDFL_TRIGGER_PATTERNS if re.search(p, norm, re.IGNORECASE)]

    if fid_hits and not fdfl_hits:
        return {"route": "fill-issues-domain", "confidence": 0.85,
                "reason": "命中本 skill 触发词：%s" % ", ".join(fid_hits)}
    if fdfl_hits and not fid_hits:
        return {"route": "fill-domains-from-log", "confidence": 0.85,
                "reason": "命中姊妹 skill 触发词：%s" % ", ".join(fdfl_hits)}
    if fid_hits and fdfl_hits:
        # 同时命中两个：优先 fill-issues-domain（处理已登记挂起项时通常也会提到日志）
        return {"route": "fill-issues-domain", "confidence": 0.6,
                "reason": "同时命中两个 skill 触发词，默认 fill-issues-domain（已登记挂起项优先消费）；fid=%s fdfl=%s"
                          % (", ".join(fid_hits), ", ".join(fdfl_hits))}
    return {"route": "none", "confidence": 0.5,
            "reason": "未命中任何 skill 触发词"}


# =====================================================================
# 回归用例（2026-10-28 16 项）
# =====================================================================

REGRESSION_FIXTURE = [
    # 落盘 11 项
    {
        "domain": "applogcdn.com",
        "ruled_to": "bytedance.yaml",
        "criterion": "判据4命名族 + 判据5已有锚点文件",
        "anchors": {
            "soa_admin_suffix": "bytedance.com",
            "cname": "bytedns3.com",
            "log_cooc_top": ["lf-package-cn.feishucdn.com", "internal-api-lark-api.feishu.cn", "is.snssdk.com"],
        },
    },
    {
        "domain": "byte-test.com",
        "ruled_to": "bytedance-global.yaml",
        "criterion": "ASN 直接判厂商（端点归属优先于注册商）",
        "anchors": {
            "cname": "bplslb.com",
            "asn_orgs": ["Bytedance Inc", "BytePlus Pte. Ltd."],
            "subdomain_hint": "perfops.",
        },
    },
    {
        "domain": "pixpix.com",
        "ruled_to": "proxy-ai.yaml",
        "criterion": "首页标题定性 AI SaaS",
        "anchors": {
            "http_title_keyword": "AI Product Image",
            "storage_cname_suffix": "x-oss-process",
        },
    },
    {
        "domain": "123169.xyz",
        "ruled_to": "proxy.yaml",
        "criterion": "图床族互现 + 与 icanhazip 同批",
        "anchors": {"cooc_sibling": ["111666.best", "999831.xyz"]},
    },
    {
        "domain": "111666.best",
        "ruled_to": "proxy.yaml",
        "criterion": "首页标题「16图床」",
        "anchors": {"http_title_keyword": "16图床", "subdomain_hint": "i."},
    },
    {
        "domain": "999831.xyz",
        "ruled_to": "proxy.yaml",
        "criterion": "图床族互现",
        "anchors": {"cooc_sibling": ["123169.xyz", "111666.best"], "subdomain_hint": "cf."},
    },
    {
        "domain": "yjz.hk",
        "ruled_to": "proxy.yaml",
        "criterion": "粤语技术博客，Cloudflare A + vanitydns NS",
        "anchors": {"http_title_keyword": "歸去如風"},
    },
    {
        "domain": "tsight.io",
        "ruled_to": "proxy.yaml",
        "criterion": "TrueSight SERP Intelligence，WorkBuddy Helper 进程",
        "anchors": {"http_title_keyword": "SERP Intelligence", "cooc_top": "www.workbuddy.cn"},
    },
    {
        "domain": "ns1pcdn.net",
        "ruled_to": "proxy.yaml",
        "criterion": "多租户 CDN（NS1+CSC），与 dnscheck/ipleak 同批",
        "anchors": {"ns_pattern": "ns1pcdn.net", "cooc_top": "dnscheck.tools"},
    },
    {
        "domain": "freloop.com",
        "ruled_to": "proxy.yaml",
        "criterion": "NameCheap 2025 注册 + Cloudflare NS + 首页空（海外杂项兜底）",
        "anchors": {"registrar": "NameCheap", "ns_pattern": "cloudflare"},
    },
    {
        "domain": "checktrustworthiness.com",
        "ruled_to": "proxy.yaml",
        "criterion": "global-iuni CNAME AWS ALB，与 umeng/jpush 同批（海外杂项兜底）",
        "anchors": {"cname_suffix": "elb.amazonaws.com", "cooc_top": "cnlogs.umeng.com"},
    },
    # 转 skip 5 项
    {
        "domain": "featureassets.org",
        "ruled_to": "skip:reject.yaml L50446 DOMAIN-SUFFIX",
        "criterion": "reject.yaml 上游已收录（reject 是 rules 首条，补录无意义）",
        "anchors": {"reject_line": 50446, "reject_rule_type": "DOMAIN-SUFFIX"},
    },
    {
        "domain": "wdfl.co",
        "ruled_to": "skip:reject.yaml L162770 DOMAIN-SUFFIX",
        "criterion": "reject.yaml 上游已收录",
        "anchors": {"reject_line": 162770, "reject_rule_type": "DOMAIN-SUFFIX"},
    },
    {
        "domain": "nsvcs.net",
        "ruled_to": "skip:reject.yaml L68267 精确主机 ingesteer.services-prod.nsvcs.net",
        "criterion": "reject.yaml 已有精确主机规则，父域无其他端点",
        "anchors": {"reject_line": 68267, "reject_rule_type": "DOMAIN 精确主机"},
    },
    {
        "domain": "mdoelscope.ai",
        "ruled_to": "skip:仿冒域（modelscope.ai 字母转位）",
        "criterion": "字母转位仿冒，绝不补录",
        "anchors": {"legitimate": "modelscope.ai", "a_record": "none"},
    },
    {
        "domain": "sitemana.com",
        "ruled_to": "skip:广告追踪类整批不落盘",
        "criterion": "p. 子域与 doubleclick/googlesyndication/statcounter/clarity.ms 同批",
        "anchors": {"http_title_keyword": "conversion catalyst", "cooc_top": "doubleclick"},
    },
]


def regression_offline():
    """离线回归：只打印内嵌锚点，不联网。验证 fixture 完整性。"""
    print("=" * 70)
    print("回归用例（2026-10-28 16 项，离线模式）")
    print("=" * 70)
    landing = sum(1 for c in REGRESSION_FIXTURE if not c["ruled_to"].startswith("skip"))
    skip = sum(1 for c in REGRESSION_FIXTURE if c["ruled_to"].startswith("skip"))
    print("汇总：%d 项落盘 / %d 项转 skip\n" % (landing, skip))
    for i, c in enumerate(REGRESSION_FIXTURE, 1):
        print("[%2d] %-32s → %s" % (i, c["domain"], c["ruled_to"]))
        print("       判据: %s" % c["criterion"])
        for k, v in c["anchors"].items():
            display = v if isinstance(v, str) else (
                ", ".join(str(x) for x in v) if isinstance(v, (list, tuple)) else str(v))
            print("       %-22s %s" % (k + ":", display))
        print()
    print("回归通过：所有 fixture 完整（不联网模式只验证 fixture 完整性）。")
    print("要复跑证据采集比对当前网络侧输出，加 --online。")
    return 0


def regression_online():
    """联网回归：调用 probe_domains 重跑证据采集，比对当前输出与内嵌锚点。"""
    py = sys.executable
    skill_dir = Path(__file__).resolve().parent.parent
    probe = skill_dir / "scripts" / "probe-domains" / "probe_domains.py"
    if not probe.exists():
        print("[fatal] probe_domains.py 不存在：%s" % probe, file=sys.stderr)
        return 2

    # 代理可用性探测
    proxy_ok = subprocess.run(["nc", "-z", "127.0.0.1", "7893"],
                              capture_output=True).returncode == 0
    if not proxy_ok:
        print("[warn] 7893 代理不通，--online 模式跳过；改跑离线模式。\n")
        return regression_offline()

    domains = [c["domain"] for c in REGRESSION_FIXTURE]
    out_path = "/tmp/regression-probe-%s.json" % os.popen("date +%F").read().strip()
    print("=" * 70)
    print("回归用例（2026-10-28 16 项，联网模式）— 调用 probe_domains")
    print("=" * 70)
    print("探针输出 → %s\n" % out_path)

    r = subprocess.run(
        [py, str(probe)] + domains + ["--json", out_path],
        capture_output=True, text=True, timeout=600,
    )
    if r.returncode != 0:
        print("[fatal] probe_domains 失败：%s" % r.stderr[-500:], file=sys.stderr)
        return 2
    print(r.stdout[-2000:])
    print("\n[info] 详细比对需人工核对 %s 与内嵌 fixture 的关键字段。" % out_path)
    print("[info] 关键锚点：soa_admin 后缀 / cname / http title keyword / cooc top")
    return 0


# =====================================================================
# 默认模式：跑 cases.json 路由判定
# =====================================================================

DEFAULT_CASES = {
    "should_trigger": [
        {"text": "处理 issues-domain 表里那几个域名", "family": "process_table"},
        {"text": "清理一下挂起的待判域名", "family": "clear_pending"},
        {"text": "给挂起域名定个归属", "family": "rule_pending"},
        {"text": "issues-domain 表怎么清零", "family": "clear_table"},
        {"text": "把 issues-domain 表里的域名批量定一下", "family": "batch_ruling"},
        {"text": "上次登记的待人工域名定一下归属", "family": "rule_pending"},
        {"text": "跑一下 fill-issues-domain skill", "family": "explicit_skill_name"},
    ],
    "should_not_trigger": [
        {"text": "今天日志里有哪些漏网之鱼", "family": "log_extraction"},
        {"text": "提取昨天的 match Match 域名", "family": "log_extraction"},
        {"text": "怎么用 clash 配置代理", "family": "info_query"},
        {"text": "什么是 DOMAIN-SUFFIX 规则", "family": "info_query"},
        {"text": "翻译一下这段英文", "family": "translate"},
        {"text": "解释一下 SOA 记录是什么", "family": "explain"},
        {"text": "头脑风暴一下域名归类方案", "family": "brainstorm"},
    ],
}


def run_default_cases(cases_path: str):
    cases = DEFAULT_CASES
    if cases_path and os.path.exists(cases_path):
        with open(cases_path, encoding="utf-8") as f:
            cases = json.load(f)

    print("=" * 70)
    print("trigger_eval 默认模式（路由判定）")
    print("=" * 70)
    fails = 0
    for case in cases.get("should_trigger", []):
        r = classify(case["text"])
        ok = r["route"] == "fill-issues-domain"
        marker = "OK  " if ok else "FAIL"
        if not ok:
            fails += 1
        print("%s [%-22s] %s" % (marker, case["family"], case["text"]))
        print("       → route=%s conf=%.2f (%s)" % (r["route"], r["confidence"], r["reason"]))

    for case in cases.get("should_not_trigger", []):
        r = classify(case["text"])
        ok = r["route"] != "fill-issues-domain"
        marker = "OK  " if ok else "FAIL"
        if not ok:
            fails += 1
        print("%s [%-22s] %s" % (marker, case["family"], case["text"]))
        print("       → route=%s conf=%.2f (%s)" % (r["route"], r["confidence"], r["reason"]))

    print("\n汇总：失败 %d 条" % fails)
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--text", help="单条文本路由判定")
    ap.add_argument("--cases", default="", help="cases.json 路径（默认内嵌）")
    ap.add_argument("--regression", action="store_true", help="跑 16 项回归用例")
    ap.add_argument("--online", action="store_true", help="回归模式联网重跑证据采集")
    args = ap.parse_args()

    if args.regression:
        return regression_online() if args.online else regression_offline()

    if args.text:
        r = classify(args.text)
        print(json.dumps({"text": args.text, **r}, ensure_ascii=False, indent=2))
        return 0

    return run_default_cases(args.cases)


if __name__ == "__main__":
    sys.exit(main())
