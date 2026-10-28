#!/usr/bin/env python3
"""定案闭环校验：落点唯一性 + reject 上游覆盖 + skip-list 一致性 + yaml 语法。

用法（务必用带 pyyaml 的解释器）：
    /Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python \
        verify_landing.py --domains applogcdn.com byte-test.com ... \
        --yaml bytedance.yaml proxy.yaml

判定口径：
    OK       恰好落在 1 个业务 yaml（落盘项应为此状态）
    MISSING  业务 yaml 里都没有（转 skip 项应为此状态，且 reject 命中或 skip-list 有记录）
    DUP      落在多个业务 yaml —— 必须消除
    IN-REJECT 声称落盘但 reject.yaml 里也有 —— reject 是 rules 首条，落盘不会生效

注意：不要用 `grep -c` 统计 reject.yaml（10MB 文件上多模式 -c 会给出与 -n 不一致的结果），
本脚本用 Python 逐行扫描，结果可复现。
"""
import argparse
import glob
import os
import sys

import yaml


def load_payload(path):
    try:
        d = yaml.safe_load(open(path, encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return None, str(e)
    p = d.get("payload")
    if not isinstance(p, list):
        return None, "payload 不是列表"
    return p, None


def scan_all(business_files, targets):
    landing = {t: [] for t in targets}
    for f in business_files:
        if os.path.getsize(f) == 0:  # 本地空壳文件（如未落内容的 cn.yaml）不算库
            continue
        payload, err = load_payload(f)
        if payload is None:
            print("  [warn] %s 解析失败：%s" % (f, err))
            continue
        for item in payload:
            if not isinstance(item, str) or "," not in item:
                continue
            val = item.split(",")[1]
            if val in landing:
                landing[val].append(f)
    return landing


def scan_reject(targets):
    hits = {t: [] for t in targets}
    if not os.path.exists("reject.yaml"):
        return hits
    with open("reject.yaml", "r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            for t in targets:
                if t in line:
                    hits[t].append((i, line.strip()[:100]))
    return hits


def scan_skiplist(path, targets):
    mode = {t: None for t in targets}
    if not os.path.exists(path):
        return mode
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith("#") or " " not in line:
            continue
        dom, _, rest = line.partition(" ")
        if dom in mode:
            mode[dom] = rest.split(":")[0]
    return mode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", nargs="+", required=True)
    ap.add_argument("--yaml", nargs="*", default=[], help="需做 safe_load 校验的文件")
    ap.add_argument("--skip-list",
                    default=".agents/skills/fill-domains-from-log/scripts/"
                            "extract-match-domains/skip-list.txt")
    ap.add_argument("--expect", default="auto", choices=["auto", "landing", "skip"],
                    help="landing=全部应在业务 yaml；skip=全部应不在业务 yaml")
    args = ap.parse_args()

    business = [f for f in sorted(glob.glob("*.yaml"))
                if f not in ("reject.yaml", "config.yaml")]
    landing = scan_all(business, args.domains)
    reject = scan_reject(args.domains)
    skip = scan_skiplist(args.skip_list, args.domains)

    bad = 0
    print("%-30s %-9s %-28s %-8s %s" % ("domain", "verdict", "business yaml", "reject", "skip-list"))
    print("-" * 96)
    for t in args.domains:
        files = landing[t]
        in_reject = "yes" if reject[t] else "no"
        if len(files) > 1:
            verdict = "DUP"
        elif len(files) == 1:
            verdict = "IN-REJECT" if reject[t] else "OK"
        else:
            verdict = "MISSING"
        expect = args.expect
        if expect == "auto":
            expect = "skip" if (reject[t] or skip[t] == "skip") else "landing"
        if expect == "landing" and verdict != "OK":
            bad += 1
        if expect == "skip" and not (verdict == "MISSING" and (reject[t] or skip[t] == "skip")):
            bad += 1
        print("%-30s %-9s %-28s %-8s %s" % (
            t, verdict, ",".join(files) or "-", in_reject, skip[t] or "-"))

    for f in args.yaml:
        payload, err = load_payload(f)
        if payload is None:
            print("[yaml] %-24s FAIL %s" % (f, err))
            bad += 1
        else:
            print("[yaml] %-24s OK  payload=%d" % (f, len(payload)))

    if reject:
        for t in args.domains:
            for i, l in reject[t][:3]:
                print("[reject] %s → L%d %s" % (t, i, l))

    print("\n异常项：%d" % bad)
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
