# check-coverage

规则级查重/覆盖检查：判断给定域名或 IP 是否已被本仓库业务 yaml 规则覆盖，
并自动扫描「品牌标签锚点」（AGENTS.md 域名归属判定判据 1）。

取代旧流程中 `grep -l "$d" *.yaml` 的子串匹配——子串匹配会把 `53.com` 误判成
命中 `xxxx53.com`，也会漏掉品牌标签锚点（如待判 `browserleaks.net`、库内已有
`browserleaks.com`）。

## 用法

```bash
# 直接传参
python3 scripts/check-coverage/check_coverage.py feishu.cn itdog.cn 1.2.3.4

# 管道（extract-match-domains 的 registrable 段输出可直接喂入）
python3 .agents/skills/fill-domains-from-log/scripts/extract-match-domains/extract_match_domains.py <日志> \
  | awk '/^# registrable/{f=1;next} /^# public-ips/{f=0} f && !/^（无）/{print $1}' \
  | python3 scripts/check-coverage/check_coverage.py -

# 只列未覆盖项（--quiet 抑制 COVERED 明细）
python3 scripts/check-coverage/check_coverage.py --quiet a.com b.cn
```

## 判定逻辑

| 规则类型 | 判定 |
|---|---|
| `DOMAIN-SUFFIX` | 域名本身或任一父域等于该值 → **COVERED** |
| `DOMAIN` | 精确主机名命中 → **COVERED**（≠ 主域覆盖，判据 8） |
| `DOMAIN-KEYWORD` | 关键词子串命中 → 报告为弱证据，不算覆盖 |
| `IP-CIDR` | IP 落入网段 → **COVERED**（`no-resolve` 附加参数已剥离） |

未覆盖域名额外输出 **BRAND-ANCHOR**：库内存在可注册主域 SLD 标签逐字符相同的
其他 TLD 规则（判据 1 的机器化检索）。形近/字母转位（`mdoelscope.ai` vs
`modelscope.ai`）标签不同，天然不会误报。

## 说明

- 排除 `reject.yaml`（bot 独占维护，禁止核对）。
- 扫描根已锚定仓库根（根目录扁平 `*.yaml`），任意目录可运行。
- 退出码恒为 0——这是查询工具不是门禁；门禁仍用 find-duplicates。
- 解析为行级正则（与 find-duplicates 一致），不依赖 pyyaml，
  系统 `python3` 可直接运行。
