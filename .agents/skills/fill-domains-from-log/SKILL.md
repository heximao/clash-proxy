---
name: fill-domains-from-log
version: v2.4.1
description: 从 ClashX Meta 日志提取漏网之鱼（match Match）及 oc-cn-domain 外部规则集命中的域名，本地查重与进程名粗判后**自主裁决归属**（证据不足时自主调用 RDAP/DoH，不再经用户确认），分类补录到 clash-proxy 规则 yaml 并执行重复检查自检闭环。日志获取采用移动制：将 ~/.config/clash.meta/logs 下的日志移入仓库 log/clashx-meta-log/，本轮分析全部完成（push 并确认 0 0）后将已处理日志归档至同级的 log/.archive/。Git 侧自 2026-10-17 起取消分支制度：每轮开头先 fetch 并把本地 main 追上远程、确认与远程双向 0 0，全部改动直接在 main 上完成并提交，commit 前再查一次同步状态，随后立即 push main 并确认 0 0。当用户要求补漏域名、归类漏网之鱼、分析日志补规则、整理 match Match 或 oc-cn-domain 域名时使用。
---

# 从日志补漏域名

在 clash-proxy 仓库中将 ClashX Meta 日志里未被本仓库 yaml 规则覆盖的目标归类到合适的规则文件。覆盖两类：

- `match Match` —— 未命中任何规则，落入"漏网之鱼"兜底策略组
- `match RuleSet(oc-cn-domain)` —— 命中外部 OpenClash CN 域名规则集（通常走 DIRECT），同样说明本仓库规则未覆盖

全程在仓库根目录 `/Users/saibopika/clash-proxy` 执行命令。

## 处理流程（必须按序执行）

```text
 0. ★ 同步准备（每轮开头必做，详见第 0 节）★
      git fetch origin → main 追上远程 → 确认与远程双向 0 0
      ↓
 1. 准备日志（移动：~/.config/clash.meta/logs → log/clashx-meta-log/）
      ↓
 2. 提取 + 去重 + 过滤伪域名
      ↓
 3. 归并主域
      ↓
 4. 批量查现有规则（grep *.yaml）+ 读历史 changelog + 进程名粗判
   —— 本步骤禁止任何外部查询 ——
      ↓
 5. ★ 自主裁决归属（证据足直接定；不足进 6）★
      ↓
   ┌── 证据充分 ─────────────────┐
   │                            ↓
   └── 证据不足 → 6. 自主 RDAP / DoH 查询 → 据结果定夺
                              ↓
 7. 按自主裁决结论分类到规则文件
      ↓
 8. 编辑格式（payload: 开头、DOMAIN-SUFFIX、# === 分组 ===）
      ↓
 9. 自检闭环：find_duplicates.py + yaml语法校验
      ↓
10. 更新 changelog → 在 main 上提交（显式列文件，不推远程）
      ↓
11. push main → 确认 0 0
      ↓
12. 归档已处理日志（log/clashx-meta-log/ → log/.archive/）
```

**两条核心原则：**

1. **归属判断自主裁决（2026-10-17 起取消 review 关卡）。** 粗判 + 必要时 RDAP/DoH 即为判断依据，每个决定须**留痕**（AGENTS.md 判据条号 / 进程名 / 域名语义 / RDAP 结果），写入 changelog 可追溯。证据不足且查询无结论的按既定规则兜底（无主端点不归类、国内杂项归 `direct.yaml`、海外杂项归 `proxy.yaml`），不强行归类、不凭感觉。用户主动介入给归属时以用户为准，但默认不主动询问用户。
2. **动手前必须确认本地与远程一致。** main 与 `auto-merge-reject.yml` 工作流共管（每日 00:20 UTC 自动推送 `reject.yaml`），远程随时可能出现新提交；每轮开头和每次 commit 前都必须 fetch + 双向 `0 0` 校验，否则可能在过期基线上做查重判断。所有编辑直接在 main 上进行（2026-10-17 起取消分支制度）。

## 0. 同步准备（每轮开头必做，不可跳过）

本仓库的 `main` 由 `auto-merge-reject.yml` 工作流共管（每日 00:20 UTC 自动推送 `reject.yaml`），远程随时可能出现新提交；本地只保留 `main` 一个分支（2026-10-17 起取消分支制度，所有改动直接在 main 上进行）。**动手分析日志之前必须先完成同步准备**，否则可能在过期的代码基线上做查重判断。

执行：

```bash
cd /Users/saibopika/clash-proxy

# 1. 取远程引用（安全，不动工作区）
git fetch origin

# 2. 本地 main 追上远程 main
git checkout main
git status                                    # 有未暂存改动 → 先 git stash
git pull --rebase origin main
git stash pop                                 # 仅 stash 过才需要

# 3. 确认落位：与远程双向同步
git rev-list --left-right --count origin/main...HEAD   # 必须输出 0  0
git status -sb                                # 工作区干净（未跟踪文件不影响）
```

判定与异常处理：

- `git pull --rebase` 在存在未暂存改动时会直接失败，此时**必须先 `git stash`**，不要用 `git checkout --` 丢弃改动。
- rebase 出现冲突时先解决冲突再 `git rebase --continue`；无法判断时 `git rebase --abort` 回到操作前状态并汇报。
- **禁止 `git push --force` / `--force-with-lease` 任何形式**，会抹掉 bot 的自动合并提交。
- 第 3 步不是 `0  0` 就不算完成，必须继续同步；走到第 1 步时若 HEAD 不在 main 上，先 `git checkout main`。

## 1. 准备日志

- 日志源目录：`/Users/saibopika/.config/clash.meta/logs`，其中日志文件夹命名格式为 `YYYY-MM-DD_HH-MM-SS`。
- 若用户未指定日期，默认处理**昨天**的文件夹（多个同名日期前缀时全部处理）。
- **移动而非复制**（2026-10-17 起）：把待处理文件夹从源目录**移入**仓库 `log/clashx-meta-log/`：
  ```bash
  mv /Users/saibopika/.config/clash.meta/logs/<YYYY-MM-DD_HH-MM-SS> log/clashx-meta-log/
  ```
  移动制下源目录不保留已迁移日志，天然消除"源目录与仓库副本出现差集"的复制缺口问题。
- **⚠️ mv 套娃坑**：目标侧已存在同名文件夹时，`mv` 会把源文件夹**塞进目标文件夹内部**而不报错。移动前必须先 `diff -rq /Users/saibopika/.config/clash.meta/logs log/clashx-meta-log` 比对，**只移入"Only in 源目录"的文件夹**；双侧同名的跳过不移（视为已迁移）。
- **历史遗留**：2026-10-17 之前采用 `cp -R` 复制，源目录曾残留大量与仓库同名的旧副本，当日已由用户清理完毕；现移动制下源目录日常只留当日未移入的新日志。
- `log/clashx-meta-log/` 下已有、但尚未归档（上轮中断遗留或本轮移入）的日志直接纳入本轮提取范围；处理完成后按第 12 节归档。

## 2. 提取与去重

用本 skill 自带脚本提取，输出五段：match Match 域名、match Match 裸 IP、oc-cn-domain 域名、oc-cn-domain 裸 IP、进程提示（`目标: 进程名(次数)`），已完成去重并过滤无 TLD 伪域名：

```bash
python3 .agents/skills/fill-domains-from-log/scripts/extract_match_domains.py <日志文件或目录>
```

手工核对时等价命令：

```bash
# match Match
grep -oE -- '--> [^ ]+ match Match using' <log> | sed -E 's/--> ([^:]+):[0-9]+ match Match using/\1/' | sort -u
# oc-cn-domain
grep -oE -- '--> [^ ]+ match RuleSet\(oc-cn-domain\) using' <log> | sed -E 's/--> ([^:]+):[0-9]+ match RuleSet\(oc-cn-domain\) using/\1/' | sort -u
```

只提取 info 级别的 `... using` 行；忽略 `match Match/`、`match RuleSet/oc-cn-domain` 等斜杠形式的 dial 报错行（同一目标已含于 info 行）。

日志行格式：`[TCP] 源地址(进程名) --> 目标:端口 match <Match|RuleSet(oc-cn-domain)> using 策略组`。进程名位于源地址后的圆括号内，可有可无。

## 3. 过滤

以下目标不归类：

- 无 TLD 的伪域名（脚本已过滤），如 `monitor_browser`、`kwrt`、`lan`、`local`、`localhost`。
- 局域网 / 保留 IP 段地址。
- 明显的本地服务主机名。

## 4. 批量查重 + 粗判归属（不做外部查询）

**这一阶段禁止调用任何外部查询（RDAP / DoH / wayback / urlscan / WebSearch）**，只靠本地证据做粗判，为第 5 步自主裁决提供素材。

1. **批量查现有规则**：把提取结果归并到主域（`xx.yy.cn` 取 `yy.cn`，`a.b.com` 取 `b.com`），然后一次性扫描：
   ```bash
   for d in <主域列表>; do hit=$(grep -l "$d" *.yaml 2>/dev/null | grep -v '^reject.yaml$' | tr '\n' ' '); echo "$d => ${hit:-NONE}"; done
   ```
   已有 `DOMAIN-SUFFIX` 覆盖的主域**整批跳过**（规则集先于本地 yaml 匹配，不代表规则缺失），不逐个处理。**禁止查询、核对 `reject.yaml`**。
2. **读历史 changelog**：`changelog.md` 已纳入 git 跟踪、持续维护。里面可能已记录某域「reject.yaml 上游已收录」（如 `clarity.ms`、`jpush.cn`、`jiguang.cn`），这类**直接跳过，不加也不问**。必须先读。
3. **进程名粗判**：脚本 process-hints 段给出每个目标的发起进程，这是第一手线索：
   - `Trae CN Helper` / `TRAE SOLO CN Helper` / `DoubaoIme` → 字节系（Trae / 豆包）
   - `Feishu` / `Lark Helper` → 飞书系
   - `wpsoffice` / `wpscloudsvr` → 金山办公 WPS
   - `trustd` → macOS 证书校验，目标多为 OCSP / CRL 端点
   - `mihomo` / `OrbStack Helper` → 内核 / 基础设施自身流量
   - `Google Chrome Helper` / `firefox` → **无产品指向，归属由第 5/6 步自主裁决；证据不足走 RDAP**
4. **给出粗判结论并记录**：每个未覆盖主域写一行「主域 → 建议归属文件 + 判断依据（进程名 / 域名语义 / 已有同类分组 / AGENTS.md 判据条号）」。证据充分的标记为 `可定`，证据不足的标记为 `待查`（进入第 6 节 RDAP/DoH）。**禁止在本步发起任何外部查询。**

## 5. 自主裁决归属（留痕，可追溯）

**本步骤取代旧版 review 关卡（2026-10-17 起取消用户确认环节）。** 粗判完成后，由 agent 自主裁决归属，不再用 `AskUserQuestion` 向用户提问。

裁决规则：

- **证据充分（`可定`）**：粗判依据明确（命中 AGENTS.md 判据条号、或进程名+域名语义双佐证、或同文件已有同类分组）→ 直接定归属文件，进入第 7 步落盘。
- **证据不足（`待查`）**：进入第 6 节自主调用 RDAP / DoH / wayback 查询；查询有结论的据结果定夺，无结论的按既定兜底规则处理（见下）。
- **已裁决项直接跳过**：AGENTS.md「已裁决结论」、changelog 记录的「reject.yaml 上游已收录」（如 `clarity.ms`、`jpush.cn`、`jiguang.cn`、`etahub.com` 等）、伪域名/探针族——不查、不收、不归类。
- **无主端点兜底**：Cloudflare NS + RDAP 无注册商实体 + 首页 429/空 + 直连超时 + 仅浏览器进程且无产品指向（典型 `antpeak.com` / `hibchr.com` / `zorvian.com`）→ 不归类，记 changelog「待人工」。
- **杂项兜底**：国内经 RDAP/NS 确认归 `direct.yaml`；海外归 `proxy.yaml`；归属仍完全无法判定的记 changelog「待人工」并跳过落盘，不强行归类。

**留痕要求**：每个归类决定在 changelog 写明依据（判据条号 / 进程名 / RDAP 结果），未归类项写明原因。这是自主模式下唯一的可追溯手段，不可省略。

**用户介入通道**：默认不主动询问用户；若用户在对话中主动给出归属（如「zhipin.com → 猎聘」），以用户输入为准，不再自行论证或改判。

## 6. RDAP / DoH 查询（自主调用，针对证据不足项）

**前置条件：第 5 步自主裁决中标记为 `待查` 的项。** 不再以"用户答不确定"为触发条件，由 agent 自主判断证据是否充分。

- **本机 `whois` 命令不可用**：`whois.iana.org` 无法解析，客户端会挂起而非报错；macOS 也**没有 `timeout` 命令**（`timeout: command not found`）。不要再尝试 `timeout 30 whois <domain>`。
- **RDAP（首选）**：`https_proxy=http://127.0.0.1:7893 curl -sL --max-time 20 https://rdap.org/domain/<domain>` — **必须走代理**（直连返回空）。首次调用常返回空响应，需重试 2–3 次（间隔 3s）。返回 JSON 中 `registrar` 为空数组 + `nameservers` 为 Cloudflare NS（`ALEC.NS.CLOUDFLARE.COM`）通常意味着注册信息完全隐私保护。
- **批量 RDAP**：写成 `/tmp/rdap.py` 循环 + 重试执行（heredoc 内联 python 会被安全策略拦截，见第 15 节环境坑）。
- **DoH 存活检查**：`https_proxy=http://127.0.0.1:7893 curl -s "https://cloudflare-dns.com/dns-query?name=<domain>&type=A" -H "Accept: application/dns-json"` — `"Status":3`（NXDOMAIN）= 域名已失效，不归类。适合一次批量筛多个主域。
- **辅助判**：`https://archive.org/wayback/available?url=<domain>` 查历史快照（走代理，高频会 429）；`urlscan.io` 搜索结果常直接暴露归属（如 `cmicapm.com` → China Mobile Group Guangdong）。
- **查询结果据以定夺并留痕**：拿到 RDAP/外部证据后，结论与粗判不同或仍有歧义时，按查询结果修正裁决，不再回问用户。查询无结论的（隐私保护 + 首页 429/空 + 直连超时 + 仅浏览器进程）按第 5 节「无主端点兜底」处理——不归类，记 changelog「待人工」。
- **判定"无主端点"的标准**：Cloudflare NS + RDAP 无注册商实体 + 首页 429 或空响应 + 直连超时 + 发起进程仅浏览器且无产品指向 → 判定为无主广告/追踪端点。典型样例：antpeak.com / hibchr.com / zorvian.com（2026-10-04）。**这类默认不归类，记 changelog「待人工」；不主动询问用户。**

## 7. 分类到规则文件（按自主裁决结论执行）

**前提：第 5 步自主裁决完成，第 6 步（证据不足项）已查清。按自主裁决结论执行，留痕已写入 changelog 草稿。**

按以下优先级判定（细则以 AGENTS.md 为准）：

| 域名特征 | 目标文件 |
|---|---|
| 大型互联网公司主域 | 对应厂商文件：`google.yaml`、`apple.yaml`、`microsoft.yaml`、`meta.yaml`、`bytedance.yaml`、`alibaba.yaml`、`tencent.yaml` 等 |
| 大厂海外 / 国际版服务 | 对应 `-global.yaml`（`alibaba-global`、`bytedance-global`、`tencent-global`） |
| 大厂 AI 服务 | 优先归入厂商专属 AI 文件（如 `claude.yaml`、`openai.yaml`）；无专属文件的按可直连 / 需代理归 `direct-ai.yaml` / `proxy-ai.yaml` |
| 无法直连或直连不稳定的杂项 | `proxy.yaml` |
| 可稳定直连的杂项 | `direct.yaml` |
| 特定领域服务 | 对应主题文件（`streaming.yaml`、`telegram.yaml`、`github.yaml` 等） |

判断要点：

- 日志中走代理节点不代表必须归代理文件；按服务性质判断（如 Let's Encrypt 证书端点 `lencr.org` 可直连归 `proxy.yaml` 或 `direct.yaml` 的证书验证分组需按实际情况定）。
- **oc-cn-domain 类别**的域名命中外部 OpenClash CN 域名规则集且通常走 DIRECT，说明其为国内可达服务，多为国内大厂子域（字节系 `zijieapi.com`、`doubao.com`、`feishu.cn`、`byteimg.com` 等，腾讯系 `qq.com`、`weixinbridge.com` 等）——优先归入对应厂商文件，杂项归 `direct.yaml`。**高频场景：oc-cn-domain 提取出的域名主域往往已被现有 `DOMAIN-SUFFIX` 规则覆盖（如 `*.feishu.cn` 已有 `DOMAIN-SUFFIX,feishu.cn`），这是 Clash 规则集评估优先级导致——规则集先于本地 yaml 匹配，不代表规则缺失。应先批量查重主域（`grep -rl <主域> *.yaml`），已覆盖的整批跳过，不逐个处理。**
- **不要用厂商主域一次性兜底**：`DOMAIN-SUFFIX,tencent.com` 这类主域会与其它文件里的子域分组产生语义冲突（如 hk-bank.yaml 的 `tpns.hk.tencent.com`），厂商主域很宽时改用精确子域。
- 已收录的域名不重复添加；若已有文件中的归属明显合理，沿用即可。
- **禁止编辑 `reject.yaml`**。
- 全库空壳占位文件已清零（2026-10-17）；如再出现仅有无效占位行 `DOMAIN-SUFFIX,` 的文件，补充真实域名时直接替换该占位行。

## 8. 编辑格式

- 文件必须以 `payload:` 开头；规则用 `DOMAIN-SUFFIX,example.com`（连字符，不用下划线），可选 `DOMAIN,`、`DOMAIN-KEYWORD,`、`IP-CIDR,x.x.x.x/32,no-resolve`。
- 分组注释头格式：`# === 名称（YYYY-MM-DD 漏网之鱼补录）===`，归入文件内已有的同类分组时直接追加到该分组下。
- 若因补录使文件性质变化（如占位文件有了真实内容），同步更新 README.md「规则文件」表中该文件的描述。

## 9. 自检闭环（强制）

每次编辑任意 `.yaml` 后必须执行：

1. 运行 `python3 scripts/find-duplicates/find_duplicates.py`（扫描根已锚定仓库根，任意目录可跑），读取 `scripts/find-duplicates/DUPLICATES.md`。
2. 若存在本次编辑**新引入**的重复，调整归属或删除冗余后重跑。编辑前已存在的历史重复（多为与 `reject.yaml` 重复，或既有的跨文件重复）不在本次处理范围，在汇报中说明即可。
3. 语法校验每个被编辑文件（注意用带 pyyaml 的解释器，见第 15 节）：
   `/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python -c "import yaml; yaml.safe_load(open('<file>.yaml'))"`

## 10. 更新 changelog 并在 main 上提交

**前提：第 5 步自主裁决已完成、第 9 步自检闭环已通过。确认 `git rev-parse --abbrev-ref HEAD` 输出 `main`、且与远程双向 `0 0` 再提交。**

0. **先写 changelog**：在 `changelog.md` 顶部追加本轮条目（已纳入 git 跟踪，**提交时须一并显式暂存**；格式见第 13 节）。
1. 再次确认工作区范围，只暂存本次改动的文件（**不要 `git add -A` / `git add .`**，工作区仍有未跟踪本地文件——`domain-distribution.html`、`log/` 等）：
   ```bash
   git status -sb
   git add direct.yaml github.yaml README.md scripts/find-duplicates/DUPLICATES.md changelog.md   # 显式列出，changelog.md 变更随提交入库
   ```
2. **确认 `reject.yaml` 未被暂存**（`git diff --cached --name-only | grep -x reject.yaml` 必须无输出）。该文件由 bot 独占维护，人工提交带上它会与上游自动合并冲突。
3. 提交信息用中文，一次逻辑变更一个提交，格式示例：
   ```
   漏网之鱼归类：trae.ai 归入 bytedance-global.yaml

   Co-Authored-By: WorkBuddy <noreply@workbuddy.cn>
   ```
4. **提交前再同步检查一次**：`git fetch origin && git rev-list --left-right --count origin/main...HEAD`，双向 `0 0` 才继续；远程又有新提交则按第 0 节同步后重来。
5. 本步不推远程，推送统一在第 11 步。

## 11. push main 并确认同步

```bash
# 1. 推送前最后确认一次远程状态（bot 可能在提交期间推了新提交）
git fetch origin
git rev-list --left-right --count origin/main...HEAD   # 左侧为 0 才能推

# 2. push（若被拒说明 bot 刚推了新提交，重新同步后再 push，禁止强推）
git push origin main

# 3. 门禁：必须输出 0  0
git rev-list --left-right --count origin/main...HEAD
```

冲突与异常处理：

- **push 被拒（non-fast-forward）**：说明 bot 在本地提交期间推了新提交。`git pull --rebase origin main` 同步后重新校验自检闭环再 push，**不要 `git push --force` / `--force-with-lease`**，会抹掉 bot 的自动合并提交。
- rebase 出现冲突时先 `git status` 看冲突文件；与 `reject.yaml` 的冲突一律 `git checkout --theirs reject.yaml` 保留 bot 版本（人工改动与 bot 的 reject.yaml 几乎不会重叠，真出现先停下来汇报）。
- 第 3 步不是 `0  0` 就不算完成，汇报里必须明确指出未同步。

## 12. 归档已处理日志

**前提：第 11 步 push 已完成、同步确认 `0 0`、changelog 条目已按第 10 步写入并随提交入库（hash 回填按既有纪律顺延下轮）。** 归档是本轮流程的收尾动作，未归档不算完成。

```bash
mkdir -p log/.archive
mv log/clashx-meta-log/<已处理文件夹> log/.archive/
```

- 只归档本轮**确认处理完成**的文件夹；上轮中断遗留、本轮未能定案（留待人工）的日志**留在 `log/clashx-meta-log/` 原地**，待后续轮次处理完再归档。
- **仍在被写入的文件夹不归档**（v2.4.1 护栏）：若 ClashX Meta 进程仍在运行、对应会话日志文件夹的 core/mihomo 日志 mtime 接近当前时间（`pgrep -fl ClashX` 看进程 + `ls -lT log/clashx-meta-log/<folder>/` 看 mtime），说明 app 会话未结束、mihomo 内核 fd 仍指向该目录继续写入。此时归档（mv 到 `.archive/`）会让后续写入落入 `.archive/`、污染「已处理完不再动」语义并使下轮 diff 找不到今日日志。**留原地**，待 app 重启生成新时间戳文件夹、该文件夹停止增长后再归档。
- `.archive/` 与 `clashx-meta-log/` 同级（即 `log/.archive/`），同被 `.gitignore` 的 `log/` 规则覆盖，不会入库。
- 归档后 `log/clashx-meta-log/` 应只剩未处理项；下一轮的待处理集合 = 源目录新增 + `log/clashx-meta-log/` 未归档存量。
- 归档情况（哪些文件夹移入了 `.archive/`）记入当日 memory 日志。

## 13. 填写更新记录

push 并确认 `0 0` 后，确认本轮条目已按第 10 步写入 `changelog.md` 顶部并已随提交入库（若第 10 步遗漏，此处补写并在下轮补提交；条目格式如下）：

```markdown
## YYYY-MM-DD 漏网之鱼归类：<一句话摘要>

- 数据来源：<日志路径>，提取未被本仓库规则覆盖的目标去重后共 N 个（`match Match` x 个、`oc-cn-domain` y 个）：<列表>。
- <每个归类决定：规则、目标文件、归属依据>
- <未归类项及原因：伪域名、已收录、自主裁决不归类（无主端点/证据不足待人工）等>
- 重复检查结果与语法校验结论。
- Git：main 提交 <hash> 已推送，同步 0 0。
```

同时把本轮经验追加到 `.agents/memory/YYYY-MM-DD.md`（若该轮产生了新的归属判定经验，再更新 `.agents/memory/MEMORY.md`），并按第 12 节完成日志归档。

## 14. 硬性约束

- **禁止跳过第 0 步同步准备（本地与远程一致性检查）。** 在旧基线上做查重与规则判断会得出错误结论。
- **自主裁决须留痕**：每个归类决定在 changelog 写明依据（AGENTS.md 判据条号 / 进程名 / RDAP 结果 / 同文件同类分组），未归类项写明原因；证据不足且查询无结论的按兜底规则处理（无主端点不归类、国内杂项归 `direct.yaml`、海外杂项归 `proxy.yaml`），不强行归类、不凭感觉。
- **第 4 步只做本地查重和粗判，禁止外部查询**；RDAP/DoH/wayback 等外部查询集中在第 6 节按需自主发起。
- **禁止编辑 `reject.yaml`**，**禁止在提交中包含 `reject.yaml`**。
- **禁止任何形式的强制推送**（`--force` / `--force-with-lease`）。
- **禁止 `git add -A` / `git add .` 等批量跟踪**，只显式暂存本次改动文件；commit 后必须立即 push 并校验 `0 0`。
- **禁止跳过日志归档（第 12 节）**：push 并确认 `0 0` 后必须把本轮已处理日志移入 `log/.archive/`，否则下轮会对同一批日志重复提取。
- 用户主动介入给归属时（对话中直接给出），以用户输入为准，不再自行论证或改判；默认不主动询问用户。

## 15. 环境坑（本机实测）

- 系统 `python3` **无 pyyaml**。YAML 语法校验必须用：
  `/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python -c "import yaml; yaml.safe_load(open('<file>.yaml'))"`
- `timeout` 命令不存在（macOS），`whois` 不可用（见第 6 节）。
- **`mv <源文件夹> <已存在同名文件夹的目标目录>` 不报错，而是把源塞进目标内部**（套娃）。移动日志前必须 diff 确认目标侧无同名文件夹（见第 1 节）。
- **heredoc 内联 python 会被安全策略误判为系统级工具并直接拒绝执行**（提示"该命令属于系统级工具（如 WSL、wmic、sc、reg、schtasks）"）。必须先用 Write 写成 `/tmp/xxx.py`，再 `python3 /tmp/xxx.py`。
- `scripts/find-duplicates/find_duplicates.py` 已排除 reject.yaml，报告中的重复项**均为真实业务文件之间的重复**，可直接作为门禁使用。
- Git 提交用 heredoc（`git commit -F - <<'EOF'`）可用，不会被安全策略拦截；只有 python 内联脚本会被误判。
- **`.workbuddy/skills` 与 `.workbuddy/memory` 是指向 `.agents/` 下真实目录的符号链接**，两个路径访问的是同一份文件。`Skill` 工具加载本 skill 会报 "Cannot find skill"（符号链接对加载器不生效），需要时直接 Read `.agents/skills/fill-domains-from-log/SKILL.md`。

