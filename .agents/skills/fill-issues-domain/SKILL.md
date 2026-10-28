---
name: fill-issues-domain
version: v1.0.0
agent_created: true
description: 处理 clash-proxy 仓库的 issues-domain.md 待人工判定域名表——把采集侧（fill-domains-from-log）查不出归属的域名逐项复核证据（先查 reject.yaml 覆盖，再查库内品牌锚点，再补 RDAP/DoH/SOA/ASN/首页标题/日志共现），整理成分组候选方案交用户批量裁决，然后按定案执行落盘 yaml、转 skip-list 或保留挂起，并完成表清空、三处闭环、changelog 定案记录、AGENTS.md 与 MEMORY.md 快照同步、自检与提交推送。当用户要求处理 issues-domain、清理待人工域名表、给挂起域名定归属、或询问表里剩下的域名怎么定时使用。
---

# 处理待人工判定域名表（issues-domain）

`issues-domain.md`（仓库根）是 clash-proxy 的「待人工判定域名」表：采集侧查不出归属的域名攒在这里，等用户定夺。本 skill 负责把这张表**清零**——复核证据、补查、汇总方案、用户裁决、执行落盘、闭环提交。

与 `fill-domains-from-log` 的分工：那边负责「发现 + 登记」（其第 6b 节），本 skill 负责「消费 + 定案」。判定依据本身仍以 `AGENTS.md`「域名归属判定判据」+「已裁决结论」为权威，本 skill 不重复定义判据，只规定**怎么查、怎么问、怎么落、怎么收**。

全程在仓库根 `/Users/saibopika/clash-proxy` 执行。

## 处理流程（必须按序）

```text
 0. 同步准备：git fetch → 0 0；读四处（表 / AGENTS.md / skip-list / 最近 changelog）
    并核对「表内行数 == skip-list manual 数」
      ↓
 1. 建立本轮清单（表内全部行，按登记日期升序）
      ↓
 2. 逐项证据采集，按「便宜且决定性」排序，先做 L1 再上网：
    L1 reject.yaml 覆盖（verify-landing）→ 命中即 skip，不再查归属
    L2 库内品牌锚点（check-coverage / 标签 grep）→ 有锚点直接落盘
    L3 网络查证（probe-domains：SOA 邮箱 / NS / ASN / CNAME / 首页标题）
    L4 日志共现（log-cooccurrence：反推所属产品簇）
    L5 仍无结论 → 按现行口径兜底或保留挂起
      ↓
 3. 汇总裁决表（域名 | 证据 | 建议去向 | 置信度），按主题分组（≤4 组）
      ↓
 4. 交用户批量裁决（AskUserQuestion，≤4 问，每问含「继续挂起」选项）
      ↓
 5. 按定案执行：落盘 yaml / 转 skip-list / 保留挂起
      ↓
 6. 三处闭环：issues-domain.md 移除行 / skip-list 移除 manual / changelog 写定案
      ↓
 7. 快照同步：AGENTS.md 已裁决结论 + MEMORY.md（交互式会话动作）
      ↓
 8. 校验：yaml.safe_load + 落点唯一性 + manual 计数
      ↓
 9. changelog → 精确 add → commit → push → 0 0
```

## 0. 同步准备与一致性核对

```bash
git fetch origin && git rev-list --left-right --count origin/main...HEAD   # 必须 0 0
```

同时读四处，缺一处就会重复裁定或漏判：

1. `issues-domain.md` —— 本轮处理集合。
2. `AGENTS.md`「域名归属判定判据」+「已裁决结论」—— 判据条号是留痕时必须引用的；已裁决结论避免重复问用户。
3. `.agents/skills/fill-domains-from-log/scripts/extract-match-domains/skip-list.txt` —— `manual` 段应与表一一对应。
4. `changelog.md` 最近若干条 —— 该域是否已被往期裁决过（表可能滞后于 changelog）。

**一致性核对**：`grep -c "manual:"` 的数量应与表内行数相等。不等时以 changelog 为准定位差异，修复后在 changelog 记一笔，不要静默改表。

## 1. 建立本轮清单

表内全部行即本轮集合（`#`、域名、登记日期、命中子域、进程、已查证据、存疑点）。命中子域/次数是历史实证，**不必重新统计**，但若本轮日志有新命中，可顺带更新该列。

## 2. 证据采集（按层推进，命中即停）

### L1 先查 reject.yaml 覆盖（最容易被跳过、也最省力）

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains <域名...>
```

`config.yaml` 的 `rules` 第一条就是 `RULE-SET,reject,REJECT`，**`reject.yaml` 命中的域名补录到任何业务文件都永不生效**。因此先查覆盖：命中即直接转 skip，查归属是白做功。

2026-10-28 轮 16 项中有 3 项（`featureassets.org` / `wdfl.co` / `nsvcs.net`）早已被 reject 上游收录，正是这一步省掉的。注意 `DOMAIN-SUFFIX,ingesteer.services-prod.nsvcs.net` 这类**精确主机**规则也算覆盖了主域的对应子域——父域无其他端点时按不落盘处理。

**不要用 `grep -c` 多模式统计 `reject.yaml`**（10MB / 24 万行，`-c` 与 `-n` 会给出矛盾结果，2026-10-28 实测），用脚本或 Python 逐行扫。

### L2 库内品牌锚点

```bash
$PY scripts/check-coverage/check_coverage.py <主域...>
```

`BRAND-ANCHOR` 命中说明库内已有该品牌其它 TLD/兄弟域，按 AGENTS.md 判据 1–5 直接落盘。**标签须逐字符相同**，字母转位/形近是仿冒域（`mdoelscope.ai` ↔ `modelscope.ai`），绝不补录。

### L3 网络查证

```bash
$PY .agents/skills/fill-issues-domain/scripts/probe-domains/probe_domains.py \
    <域名...> --json /tmp/probe-$(date +%F).json
```

代理不可用（`nc -z 127.0.0.1 7893` 失败）时不要无限重试：把该项标记「下轮重试」原样留在表里，本轮按无结论处理，正常收尾。

### L4 日志共现

```bash
$PY .agents/skills/fill-issues-domain/scripts/log-cooccurrence/log_cooccurrence.py \
    <域名...> --top 10
```

传主域即可（脚本按后缀匹配子域）。命中 0 次通常是该域只在未归档的当天日志里出现，先把日志 cp 归档再跑。

### L5 兜底

查完仍无结论时，按下文「现行归属口径」处理。**只有用户明确要求保留观察时才留在表里**。

## 3. 三类证据怎么读

### SOA 管理员邮箱 = 最硬锚点

`probe-domains` 输出的 `SOA(邮箱)` 取的是权威区 SOA 的 rname 字段。厂商自建权威 DNS 时它直接暴露母公司域：

| 实测 | 结论 |
|---|---|
| `applogcdn.com` → `ns1.volc-dns.com. dnsadmin.bytedance.com.` | 字节（该轮据此定 `bytedance.yaml`） |
| NS 为 `*-m.ns1pcdn.net` + NS1 | 多租户 CDN，无品牌指向 → 无锚点 |

### ASN 直接判厂商，注册商不是判据

CNAME 跳到云厂商 SLB 域名后，A 记录 IP 的 ASN 往往就是答案：

```bash
curl -s --max-time 10 "https://ipwho.is/<ip>" | $PY -c "import json,sys;c=json.load(sys.stdin)['connection'];print(c['asn'],c['org'])"
```

`perfops.byte-test.com` → CNAME `bplslb.com` → `71.18.228.101` AS396986 Bytedance Inc / `101.47.92.142` AS150436 BytePlus ⇒ 字节海外。**这条证据直接推翻了「阿里云注册 + alidns NS 不符字节惯例」的旧挂起理由**——注册商/NS 只是旁证，端点归属优先。

`ipinfo.io` 与 `rdap.org/ip` 走代理常返空，用 `ipwho.is`。

### 首页标题 = 最快的服务定性

| 实测 | 定性 |
|---|---|
| `111666.best` → 「16图床，永久免费，无需登录的图床」 | 图床（`i.` 子域即图片域） |
| `pixpix.com` → 「PixPix — AI Product Image & Video Generator for E-commerce」 | AI SaaS → `proxy-ai.yaml` |
| `sitemana.com` → 「Your conversion catalyst」+ 与 doubleclick 同批 | 广告追踪 → skip |

`403 Just a moment...` / `429` 多为 Cloudflare 挑战或反爬，**不代表无主**，只说明该端点在防抓取。

## 4. 汇总裁决表

一行一项：`域名 | 证据（可复述的关键字段） | 建议去向 | 置信度`。然后**按主题分组**——用户裁决要批量问，分组决定了能压成几个问题（例如「图床族三项」「同一应用的两个端点」「广告追踪类」）。

分两类呈现：**已可闭环**（证据无歧义，只需确认）与**待你定夺**（需要用户价值判断：这东西对他有没有用、该不该走代理）。

## 5. 交用户批量裁决

用 `AskUserQuestion`，硬约束：

- **≤4 个问题**，每问覆盖同主题的多个域名（把 16 项压成 4 问是常态）。
- 每个问题的选项**必须包含「继续挂起」**，用户有权不裁决。
- 证据细节放正文表格，选项只写去向（`归 direct.yaml` / `归 proxy.yaml` / `继续挂起`）。
- 证据无歧义的一组，第一问就请用户整批确认，不要逐项问。

不要替用户决定「这个服务他用不用得上」——那是他的取舍，不是判据问题。

## 6. 执行定案

### 落盘

- 规则名用 `DOMAIN-SUFFIX,<主域>`（连字符），整域归并，不写子域。
- 分组注释头格式：`# === 名称（YYYY-MM-DD 漏网之鱼补录）===`；**归入文件内已有同类分组时直接追加到该分组下**，并把该分组头里的日期列表补齐。
- 追加位置在 payload 末尾或对应分组内，保持文件既有缩进（两空格 + `- `）。
- 不要为单个域名新建厂商文件（AGENTS.md 明确禁止）；海外知名厂商已有文件的才进厂商文件。

### 转 skip

在 `skip-list.txt` 末尾追加本轮日期段，写 `skip:<原因>`，原因必须能自证（reject 行号、判据条号、同批域名）：

```text
# --- YYYY-MM-DD 交互轮：issues-domain N 项全部定案（M 项 skip，K 项落盘）---
#     落盘：<域> → <file>.yaml；……（明细见 changelog）
<域> skip:reject.yaml 上游已收录（DOMAIN-SUFFIX L50446，reject 规则优先级最高，补录无意义）
```

### 保留挂起

行原样留在表里，在「存疑点」列补一句「本轮用户裁定继续挂起（YYYY-MM-DD）」，changelog「待人工」段同步记一笔。

## 7. 三处闭环与快照同步

四处必须同时改，少一处下轮就会重复出现：

1. **`issues-domain.md`**：移除已定案行，表头计数改为剩余数。表清空时保留表头 + 一行说明（去哪看定案记录），**不留定案记录段**——定案只写 changelog。
2. **`skip-list.txt`**：移除对应 `manual:` 行；转 skip 的按上节新增 `skip:` 行。落盘项直接删除、不转 `skip`（历史惯例：落盘即净出）。
3. **`changelog.md`**：顶部新条目，逐项写「去向 + 证据 + 判据」，这是唯一可追溯来源。
4. **快照同步（仅交互式会话）**：`AGENTS.md`「已裁决结论」（新增 skip 类、口径变更）+ `.agents/memory/MEMORY.md`（挂起清单、口径变更）。automation 会话写 `AGENTS.md` 会被 BLOCKED，留待交互轮。

**agent 不得自行移除行**：误登记的也要在 changelog 说明后改行，不静默删。

## 8. 校验

```bash
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains <全部本轮域名> --yaml <改动过的 yaml...>
```

必须全部满足：

- 落盘项 `OK`（恰好 1 个业务文件、0 个命中 reject）；转 skip 项 `MISSING` 且 reject 命中或 skip-list 有 `skip`。
- 无 `DUP`、无 `IN-REJECT`。
- 改动 yaml 全部 `safe_load` 通过。
- `grep -c "manual:" skip-list.txt` 等于表内剩余行数（通常都是 0）。

## 9. changelog、提交、推送

- changelog 条目结构：落盘（按文件分组，每项写证据）/ 转 skip（每项写依据）/ 校验（实查数字）/ 口径变更（若有）/ Git 说明。
- **精确 `git add` 逐文件列出**，禁用 `git add -A` / `git add .`——工作区常有未跟踪本地文件（`config.yaml`、空的 `cn.yaml`、`.DS_Store`）。
- 确认 `reject.yaml` 未被暂存：`git diff --cached --name-only | grep -x reject.yaml` 必须无输出（该文件由 bot 独占维护）。
- 提交信息中文，先算准数字再写（推上去就改不了）。
- commit 前再 fetch 校验一次 `0 0`；push 后再验 `0 0`。

## 10. 环境坑

- **`Edit` 工具删整行会吃掉换行**：把 `old_string` 写成「整行 + 下一行开头」再替换，否则相邻两行会粘连（2026-10-28 踩过）。批量删行改用 Python 按行过滤。
- **本机 `dig` 不可信**：Clash TUN fake-ip 模式下 A 记录一律返回 `198.18.x`，必须走 DoH。
- **DoH 用 Cloudflare + 直连**：`curl --noproxy '*' -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=<域>&type=<类型>'`；加 `&ct=application/dns-json` 会 400。
- **`reject.yaml` 的 grep 会骗人**：改用 Python 逐行扫（见 L1）。
- **没有 `timeout` 命令、没有 `whois`**（macOS），查询靠 curl `--max-time`。
- **代理状态来回翻转**：每轮现场 `nc -z 127.0.0.1 7893` 探测，不通就顺延而不是重试到卡死。
- **`config.yaml` 是本地配置**（未跟踪也未 gitignore），不参与库内查重；空文件（`cn.yaml`）不参与扫描。
