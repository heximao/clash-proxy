#!/usr/bin/env python3
"""按日志共现语境反推域名所属应用。

待判定表里的域名往往只剩「一个子域 + 一个进程名」的线索，单看域名判不出归属。
同一应用通常在同一秒内打出一串请求，因此把目标域名命中时刻 ±N 秒内的其它域名
统计出来，共现最高的几个往往就是它所属产品簇（例：`sitemana` 与 doubleclick /
googlesyndication / statcounter 同批 ⇒ 广告追踪；三个随机数字域互现 ⇒ 同一图床站）。

用法：
    python3 log_cooccurrence.py <domain> [<domain> ...] [--window 6] [--top 10]
    python3 log_cooccurrence.py --root ../../../../log/archive 123169.xyz sitemana.com

要点：
    - 表里登记的是主域，日志里是子域（api./i./cf./p.），一律按后缀匹配
    - 默认同时扫描 log/archive/**/clashx_core_*.log 与 log/clashx-meta-log/**（若存在）
    - 纯 IP 目标（DNS 解析器 1.1.1.1 / 8.8.8.8 等）默认过滤，--keep-resolvers 可保留
"""
import argparse
import bisect
import collections
import datetime
import glob
import os
import re
import sys

LINE = re.compile(
    r"(\d{4})年(\d{1,2})月(\d{1,2})日 (\d{1,2}):(\d{2}):(\d{2})\.(\d{3})"
    r".*?--> ([^\s:]+):(\d+)")
PROC = re.compile(r"\(([^)]*)\)\s*-->")
IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def parse_file(path):
    """返回按时间排序的 [(epoch, domain, process)]。"""
    events = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if "-->" not in line:
                continue
            m = LINE.search(line)
            if not m:
                continue
            y, mo, d, h, mi, s, _ms, dom, _port = m.groups()
            try:
                ts = datetime.datetime(int(y), int(mo), int(d),
                                       int(h), int(mi), int(s)).timestamp()
            except ValueError:
                continue
            pn = PROC.search(line)
            events.append((ts, dom, pn.group(1) if pn else "-"))
    events.sort(key=lambda x: x[0])
    return events


def owner_of(dom, targets):
    for t in targets:
        if dom == t or dom.endswith("." + t):
            return t
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domains", nargs="+")
    ap.add_argument("--root", default="log/archive", help="归档日志根目录")
    ap.add_argument("--also", default="log/clashx-meta-log", help="额外扫描目录（存在则加）")
    ap.add_argument("--window", type=int, default=6, help="共现时间窗（秒）")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--keep-resolvers", action="store_true")
    args = ap.parse_args()

    roots = [args.root]
    if args.also and os.path.isdir(args.also):
        roots.append(args.also)
    files = []
    for r in roots:
        files += sorted(glob.glob(os.path.join(r, "**", "clashx_core_*.log"),
                                  recursive=True))
    if not files:
        sys.exit("未找到日志：%s" % ", ".join(roots))

    targets = args.domains
    subs = {t: collections.Counter() for t in targets}
    proc = {t: collections.Counter() for t in targets}
    ctx = {t: collections.Counter() for t in targets}

    for fp in files:
        events = parse_file(fp)
        if not events:
            continue
        times = [e[0] for e in events]
        for ts, dom, pn in events:
            t = owner_of(dom, targets)
            if not t:
                continue
            subs[t][dom] += 1
            proc[t][pn] += 1
            lo = bisect.bisect_left(times, ts - args.window)
            hi = bisect.bisect_right(times, ts + args.window)
            for j in range(lo, hi):
                co = events[j][1]
                if args.keep_resolvers or not IPV4.match(co):
                    if owner_of(co, targets) != t:
                        ctx[t][co] += 1

    for t in targets:
        total = sum(subs[t].values())
        print("=" * 66)
        print("## %s | 命中 %d 次 | 进程 %s" % (
            t, total, dict(proc[t].most_common(3)) or "-"))
        if not total:
            print("   （归档日志中无命中——可能日志未归档，或该域只在当前日志命中）")
            continue
        for d, c in subs[t].most_common(5):
            print("   子域 %-45s %d" % (d, c))
        for d, c in ctx[t].most_common(args.top):
            print("   共现 %-45s %d" % (d, c))


if __name__ == "__main__":
    main()
