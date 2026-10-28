# 三处闭环、快照同步、校验、提交推送、环境坑

本 skill 第 7–10 步的展开细则，以及第 0 步同步准备的详细说明。

## 同步准备（第 0 步）

```bash
git fetch origin && git rev-list --left-right --count origin/main...HEAD   # 必须 0 0
```

同时读四处，缺一处就会重复裁定或漏判：

1. `issues-domain.md` —— 本轮处理集合。
2. `AGENTS.md`「域名归属判定判据」+「已裁决结论」—— 判据条号是留痕时必须引用的；已裁决结论避免重复问用户。
3. `.agents/skills/fill-domains-from-log/scripts/extract-match-domains/skip-list.txt` —— `manual` 段应与表一一对应。
4. `changelog.md` 最近若干条 —— 该域是否已被往期裁决过（表可能滞后于 changelog）。

**一致性核对**：`grep -c "manual:"` 应等于表内行数。不等时以 changelog 为准定位差异，修复后在 changelog 记一笔，不要静默改表。

**automation 预审消费衔接**（v2.0.0 新增）：若 `reports/pre-ruling-*.md` 存在且项数与表行数一致，直接以预审报告跳到第 4 步批量提问，跳过 L1–L4 重跑（除非用户要求重跑）。存在但项数少于表行数（表新增了挂起项）时只对增量项跑 L1–L4，合并进预审报告。预审报告消费后（用户已据其完成裁决）由交互式会话删除或归档至 `reports/archive/`。

## 三处闭环与快照同步（第 7 步）

四处必须同时改，少一处下轮就会重复出现：

1. **`issues-domain.md`**：移除已定案行，表头计数改为剩余数。表清空时保留表头 + 一行说明（去哪看定案记录），**不留定案记录段**——定案只写 changelog。
2. **`skip-list.txt`**：移除对应 `manual:` 行；转 skip 的按 `ruling-and-landing.md` 新增 `skip:` 行。落盘项直接删除、不转 `skip`（历史惯例：落盘即净出）。
3. **`changelog.md`**：顶部新条目，逐项写「去向 + 证据 + 判据」，这是唯一可追溯来源。
4. **快照同步（仅交互式会话）**：`AGENTS.md`「已裁决结论」（新增 skip 类、口径变更）+ `.agents/memory/MEMORY.md`（挂起清单、口径变更）。automation 会话写 `AGENTS.md` 会被 BLOCKED，留待交互轮。

**agent 不得自行移除行**：误登记的也要在 changelog 说明后改行，不静默删。

## 校验（第 8 步）

```bash
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains <全部本轮域名> --yaml <改动过的 yaml...>
```

必须全部满足：

- 落盘项 `OK`（恰好 1 个业务文件、0 个命中 reject）；转 skip 项 `MISSING` 且 reject 命中或 skip-list 有 `skip`。
- 无 `DUP`、无 `IN-REJECT`。
- 改动 yaml 全部 `safe_load` 通过。
- `grep -c "manual:" skip-list.txt` 等于表内剩余行数（通常都是 0）。

## changelog、提交、推送（第 9 步）

- changelog 条目结构：落盘（按文件分组，每项写证据）/ 转 skip（每项写依据）/ 校验（实查数字）/ 口径变更（若有）/ Git 说明。
- **精确 `git add` 逐文件列出**，禁用 `git add -A` / `git add .`——工作区常有未跟踪本地文件（`config.yaml`、空的 `cn.yaml`、`.DS_Store`）。
- 确认 `reject.yaml` 未被暂存：`git diff --cached --name-only | grep -x reject.yaml` 必须无输出（该文件由 bot 独占维护）。
- 提交信息中文，先算准数字再写（推上去就改不了）。
- commit 前再 fetch 校验一次 `0 0`；push 后再验 `0 0`。

## 环境坑（第 10 步）

- **`Edit` 工具删整行会吃掉换行**：把 `old_string` 写成「整行 + 下一行开头」再替换，否则相邻两行会粘连（2026-10-28 踩过）。批量删行改用 Python 按行过滤。
- **本机 `dig` 不可信**：Clash TUN fake-ip 模式下 A 记录一律返回 `198.18.x`，必须走 DoH。
- **DoH 用 Cloudflare + 直连**：`curl --noproxy '*' -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=<域>&type=<类型>'`；加 `&ct=application/dns-json` 会 400。
- **`reject.yaml` 的 grep 会骗人**：改用 Python 逐行扫（见 `evidence-collection.md` L1）。
- **没有 `timeout` 命令、没有 `whois`**（macOS），查询靠 curl `--max-time`。
- **代理状态来回翻转**：每轮现场 `nc -z 127.0.0.1 7893` 探测，不通就顺延而不是重试到卡死。
- **`config.yaml` 是本地配置**（未跟踪也未 gitignore），不参与库内查重；空文件（`cn.yaml`）不参与扫描。
- **AGENTS.md 是受保护文件**：cron / automation 会话（无交互用户）中 patch 工具直接 BLOCKED（"requires approval but no interactive user or gateway is present"，2026-10-18 实测）。automation 轮新裁决项只落 skip-list + changelog 即完整闭环；AGENTS.md「已裁决结论」清单与 `.agents/memory/MEMORY.md` 同构清单的同步延后至交互式会话。
- **Hermes python3 走代理 SSL 证书校验失败**（CA bundle 缺失）：urllib/build_opener 报 `SSLCertVerificationError`。RDAP/DoH 类外部查询一律用 `curl -sL --max-time N`（curl 用系统钥匙串正常）。
- **并发会话冲突**：同一工作区可能有用户交互会话在 automation 轮运行途中直接提交。症状：`verify_landing` 报 `DUP` 而自己确认只编辑过一处。排查法：`git diff HEAD -- <file>` + `git show HEAD:<file>` 三方状态定位——若 HEAD 版本已含该域（他人已提交），撤销本轮自己的追加、保留他人版本，并在 changelog 注明并发去重。提交前 fetch + 双向 `0 0` 的窗口检查把碰撞概率降到最低，但查重→编辑窗口内仍可能被插队。
