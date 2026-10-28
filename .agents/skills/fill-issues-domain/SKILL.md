---
name: fill-issues-domain
version: v2.0.0
agent_created: true
maturity: production
description: 处理 clash-proxy 仓库的 issues-domain.md 待人工判定域名表——把采集侧（fill-domains-from-log）查不出归属的域名逐项复核证据（先查 reject.yaml 覆盖，再查库内品牌锚点，再补 RDAP/DoH/SOA/ASN/首页标题/日志共现），整理成分组候选方案交用户批量裁决，然后按定案执行落盘 yaml、转 skip-list 或保留挂起，并完成表清空、三处闭环、changelog 定案记录、AGENTS.md 与 MEMORY.md 快照同步、自检与提交推送。当用户要求处理 issues-domain、清理待人工域名表、给挂起域名定归属、或询问表里剩下的域名怎么定时使用。
---

# 处理待人工判定域名表（issues-domain）

`issues-domain.md`（仓库根）是 clash-proxy 的「待人工判定域名」表：采集侧查不出归属的域名攒在这里，等用户定夺。本 skill 负责把这张表**清零**——复核证据、补查、汇总方案、用户裁决、执行落盘、闭环提交。

**与 `fill-domains-from-log` 的分工**：那边负责「发现 + 登记」（第 6b 节），本 skill 负责「消费 + 定案」。判定依据本身仍以 `AGENTS.md`「域名归属判定判据」+「已裁决结论」为权威，本 skill 不重复定义判据，只规定**怎么查、怎么问、怎么落、怎么收**。

全程在仓库根 `/Users/saibopika/clash-proxy` 执行。

## 处理流程（必须按序）

```text
 0. 同步准备：git fetch → 0 0；读四处核对表行数 == skip-list manual 数
      ↓
 1. 建立本轮清单（表内全部行，按登记日期升序）
      ↓
 2. 五层证据采集（细则见 references/evidence-collection.md）：
    L1 reject.yaml 覆盖 → 命中即 skip
    L2 库内品牌锚点 → 有锚点直接落盘
    L3 网络查证（probe-domains：SOA/NS/ASN/CNAME/首页标题）
    L4 日志共现（log-cooccurrence：反推产品簇）
    L5 兜底：无主端点/国内杂项/海外杂项口径
      ↓
 3. 汇总裁决表（域名 | 证据 | 建议去向 | 置信度），按主题分组 ≤4 组
      ↓
 4. 交用户批量裁决（AskUserQuestion，≤4 问，每问含「继续挂起」）
      ↓
 5. 按定案执行：落盘 / 转 skip / 保留挂起（细则见 references/ruling-and-landing.md）
      ↓
 6. 三处闭环 + 快照同步 + 校验 + changelog/提交/推送（references/closure-and-commit.md）
```

**automation 预审模式（v2.0.0 新增）**：cron 轮不提问、不动表、不落盘，只跑 L1–L4 生成 `reports/pre-ruling-YYYY-MM-DD.md`（gitignore）留交互轮消费。细则见 `references/automation-pre-ruling.md`。

## 第 0 步：同步准备与一致性核对

```bash
git fetch origin && git rev-list --left-right --count origin/main...HEAD   # 必须 0 0
```

读四处（`issues-domain.md` / `AGENTS.md` 判据+已裁决 / `skip-list.txt` manual 段 / `changelog.md` 近期）+ 一致性核对（`grep -c "manual:"` == 表行数）+ automation 预审消费衔接（`reports/pre-ruling-*.md`）的细则见 `references/closure-and-commit.md`。

## 脚本入口

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python

# L1 reject 覆盖 + 第 6 步最终校验（落点唯一性/reject/skip-list/safe_load）
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains <域名...> [--yaml <改动过的 yaml...>]

# L3 网络查证（SOA/NS/A/CNAME/RDAP/首页标题）
$PY .agents/skills/fill-issues-domain/scripts/probe-domains/probe_domains.py \
    <域名...> --json /tmp/probe-$(date +%F).json

# L4 日志共现（±N 秒共现反推产品簇）
$PY .agents/skills/fill-issues-domain/scripts/log-cooccurrence/log_cooccurrence.py \
    <域名...> --top 10

# 路由前置关卡 + 16 项回归
$PY .agents/skills/fill-issues-domain/scripts/trigger_eval.py [--regression|--text "..."]
```

## 关键约束（细则见 references）

- **行只许因用户定案移除**；agent 不得自行删行。
- **automation 预审模式不动表、不动 skip-list、不写 changelog 定案段、不写 AGENTS.md**。
- **不要用 `grep -c` 统计 `reject.yaml`**，用 `verify_landing.py` 逐行扫；**本机 `dig` 不可信**（fake-ip），走 DoH。
- **AGENTS.md 受保护**：automation 写它必被 BLOCKED；**精确 `git add`**，禁用 `git add -A`；commit 后立即 push 校验 `0 0`。
- **不新建厂商文件**；落盘 `DOMAIN-SUFFIX,<主域>`（连字符）。

## references

- `evidence-collection.md` — L1–L5 证据采集 + SOA/ASN/首页标题判读
- `ruling-and-landing.md` — 汇总/提问/落盘/转 skip/保留挂起
- `closure-and-commit.md` — 第 0 步同步准备 + 三处闭环 + 校验 + 提交推送 + 环境坑
- `automation-pre-ruling.md` — v2.0.0 预审模式 + 并发保护 + 16 项回归用例
