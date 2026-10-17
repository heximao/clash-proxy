#!/usr/bin/env python3
"""从 ClashX Meta 日志中提取未被本仓库 yaml 规则覆盖的目标并去重。

覆盖两类未覆盖目标：
1. match Match —— 落入漏网之鱼兜底策略组（未命中任何规则）
2. match RuleSet(oc-cn-domain) —— 命中外部 OpenClash CN 域名规则集（通常走 DIRECT）

用法：
    python3 extract_match_domains.py <log文件或目录> [更多路径...]

- 目录会递归收集其中的 *.log
- 只匹配 info 级别行；dial 报错行（`match Match/`、`match RuleSet/xxx`）天然不匹配
- 顺带聚合每个目标对应的发起进程名（日志行中源地址后的 `(进程名)` 字段），
  用于辅助判断域名归属（如 Electron=Trae、trustd=macOS 证书校验）
- 输出五段：match Match 域名 / match Match 裸 IP / oc-cn-domain 域名 /
  oc-cn-domain 裸 IP / 进程提示 `目标: 进程A(N), 进程B(M)`
"""
import ipaddress
import re
import sys
from collections import Counter
from pathlib import Path

LINE_RE = re.compile(r"--> (\S+):\d+ match (Match|RuleSet\(oc-cn-domain\)) using")
PROC_RE = re.compile(r"\(([^()]+)\) -->")


def collect_logs(paths):
    for p in map(Path, paths):
        if p.is_dir():
            yield from sorted(p.rglob("*.log"))
        else:
            yield p


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    buckets = {  # category -> (domains, ips)
        "match-match": (set(), set()),
        "oc-cn-domain": (set(), set()),
    }
    procs = {}  # target -> Counter(process names)
    for log in collect_logs(sys.argv[1:]):
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            m = LINE_RE.search(line)
            if not m:
                continue
            host, category = m.group(1).strip("."), m.group(2)
            key = "match-match" if category == "Match" else "oc-cn-domain"
            pm = PROC_RE.search(line)
            if pm:
                procs.setdefault(host, Counter())[pm.group(1)] += 1
            try:
                ipaddress.ip_address(host)
                buckets[key][1].add(host)
            except ValueError:
                if "." in host:  # 过滤 monitor_browser / kwrt 等无 TLD 伪域名
                    buckets[key][0].add(host.lower())
    mm, oc = buckets["match-match"], buckets["oc-cn-domain"]
    print("# match-match domains")
    print("\n".join(sorted(mm[0])))
    print("# match-match ips")
    print("\n".join(sorted(mm[1])))
    print("# oc-cn-domain domains")
    print("\n".join(sorted(oc[0])))
    print("# oc-cn-domain ips")
    print("\n".join(sorted(oc[1])))
    print("# process-hints")
    for target in sorted(procs):
        hint = ", ".join(f"{p}({n})" for p, n in procs[target].most_common())
        print(f"{target}: {hint}")


if __name__ == "__main__":
    main()
