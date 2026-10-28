# v2.0.0 新增：automation 预审模式、并发保护、回归用例

本 skill 升级到 v2.0.0 后新增的三块能力。**默认交互式会话走原流程**；automation 轮走预审模式。

## automation 预审模式（cron 兼容）

`issues-domain.md` 表行**只许用户定案移除**，agent 不得自行删行——这是硬约束，automation 轮也不能违反。但 automation 可以做"证据预审 + 裁决建议表"，把人工裁决成本降到最低。

### 触发条件

cron / automation 轮跑 `fill-domains-from-log` 时，第 6b 节发现 `issues-domain.md` 表中有 N≥1 行（即至少一个待判域名），且代理可用（`nc -z 127.0.0.1 7893` 通过）。

### 流程

1. **同步准备**：与交互式会话相同（fetch + `0 0`）。
2. **逐项跑 L1–L4**：复用 `scripts/verify-landing/verify_landing.py` + `scripts/probe-domains/probe_domains.py` + `scripts/log-cooccurrence/log_cooccurrence.py` + `scripts/check-coverage/check_coverage.py`。L5 兜底按既定口径（无主端点不归类、国内杂项归 `direct.yaml`、海外杂项归 `proxy.yaml`）给出**建议**但不落盘。
3. **生成预审报告**：写入 `reports/pre-ruling-YYYY-MM-DD.md`（gitignore 覆盖，不入库），结构：

   ```markdown
   # issues-domain 预审报告 YYYY-MM-DD（automation 轮）

   本报告由 cron 自动生成，仅作裁决建议，**未执行任何落盘 / 转 skip / 移表行操作**。
   请交互式会话据本报告走 fill-issues-domain skill 第 5 步批量提问。

   ## 汇总（N 项）

   | 域名 | 证据 | 建议去向 | 置信度 | 备注 |
   |---|---|---|---|---|

   ## 按主题分组（≤4 组，供批量提问）

   ### 组 1：<主题>
   - ...

   ## 未决项（建议保留挂起）
   - ...
   ```

4. **不动表、不动 skip-list、不写 changelog 定案段**。只在 changelog 顶部写一条「automation 预审」段：标注预审报告路径、项数、置信度分布，**不写定案去向**。
5. **提交预审报告外的任何 yaml 改动？不要**：预审报告不入库（gitignore），其它文件不动。
6. **代理不通时顺延**：标记「下轮重试」，正常收尾，automation 不卡死。

### 与交互式会话的衔接

下一轮交互式会话跑 `fill-issues-domain` 时，第 0 步同步准备后先查 `reports/pre-ruling-*.md` 是否存在且日期为最近：

- **存在且项数与表行数一致**：直接以预审报告为输入跳到第 5 步批量提问，跳过 L1–L4 重跑（除非用户要求重跑）。
- **存在但项数少于表行数**（表新增了挂起项）：只对增量项跑 L1–L4，合并进预审报告。
- **不存在或过期**：按原流程跑。

预审报告消费后（用户已据其完成裁决）由交互式会话删除或归档至 `reports/archive/`。

### 不做的事

- ❌ 不调用 `AskUserQuestion`（automation 无交互用户）。
- ❌ 不写 `skip:` 行、不删除 `manual:` 行。
- ❌ 不动 `issues-domain.md` 表行。
- ❌ 不写 `AGENTS.md`（受保护文件，automation 写必被 BLOCKED）。
- ❌ 不调用 `verify-landing.py --expect` 强校验（无落盘动作无需校验落点）。

## 并发会话冲突保护

`fill-domains-from-log` skill 第 15 节实测过并发冲突：同一工作区可能有用户交互会话在 automation 轮运行途中直接提交。本 skill 同样需要保护。

### 触发场景

- automation 轮跑预审模式时，用户在另一个交互式会话直接给归属并落盘 → 表行已被移除、skip-list 已改、yaml 已落盘。
- automation 轮跑预审模式时，bot 推了新 `reject.yaml`（L1 覆盖判断的基线变了）。

### 保护措施

1. **预审报告开头标注"基线 commit"**：写明生成时的 `git rev-parse HEAD`，交互式会话消费时若发现 HEAD 已前进，重新对表行数与 `git log --oneline` 看是否有用户已定案。
2. **L1 reject 覆盖判断前后各 fetch 一次**：bot 的 reject.yaml 自动合并可能恰好推了新行。
3. **预审报告只读不写**：本身不修改任何已跟踪文件，所以冲突最多导致报告内容过时，不会破坏库。
4. **交互式会话消费预审报告前**：先 `git fetch` + 双向 `0 0` 校验，再 `git show HEAD:issues-domain.md` 与本地表对比，确认表未被他人改过；若被改过，重新对齐预审报告与当前表行集合。

## 回归用例固化（2026-10-28 16 项）

把 2026-10-28 全部定案的 16 项作为回归用例，固化在 `scripts/trigger_eval.py` 的 `--regression` 模式里。每项标注：

- 域名
- 当时裁决去向（落盘文件 / 转 skip 原因 / 保留挂起）
- 关键证据字段（SOA 邮箱 / ASN / 首页标题 / 共现 top1）

`--regression` 模式跑：

```bash
$PY .agents/skills/fill-issues-domain/scripts/trigger_eval.py --regression
```

预期：每项都能用既定判据复现当时的去向（即证据采集脚本输出与回归用例里记录的关键字段一致）。**不要求逐字相同**（RDAP 字段可能漂移），只要求关键锚点（SOA 邮箱后缀、ASN org 名、首页 title 关键词、共现 top3 集合）一致。任意一项锚点漂移到无法支撑原裁决时，报告 `REGRESSION-DRIFT` 并标出哪条锚点失效。

回归用例的意义：判据/口径变更（如 2026-10-22 → 2026-10-28 的兜底口径修订）后，跑一次回归看历史裁决是否仍站得住；站不住的需要在 changelog 复查补记。
