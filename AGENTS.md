### clash-proxy/AGENTS.md

本文件为 Agent（Claude、Codex、Opencode、Hermes)在本仓库工作提供指引。

本仓库（clash-proxy）是一个域名规则集合仓库，不是一个标准的代码仓库，本仓库无构建系统、测试套件或 linter。通过 jsDelivr CDN 分发为 Clash / OpenClash 客户端提供 YAML 域名规则文件。引用 CDN URL 格式：`https://cdn.jsdelivr.net/gh/heximao/clash-proxy/<filename>.yaml`。

本仓库的核心目的是基于真实的使用场景，将访问过的域名收集并分类，以便可以精准的使用指定代理访问各个网络。

#### 目录结构

```text
clash-proxy/
├── config.yaml                         # Mac ClashX Meta 运行配置文件的副本，与正在运行的配置文件区别是隐藏了`proxy-providers`中的订阅链接
├── *.yaml                              # 除config.yaml,均为规则文件：扁平存放在根目录，均以 payload: 开头
├── README.md                           # 面向使用者：CDN 引用方式、客户端配置示例、规则文件全表
├── changelog.md                        # 更新记录：每次变更后在顶部追加（见 Git 工作流）
├── scripts/                            # 维护脚本（每个脚本独立子目录，各带自己的 README）
│   ├── find-duplicates/               # find_duplicates.py + 生成物 DUPLICATES.md（入库）/ duplicates.json（入库）
│   ├── check-coverage/                # check_coverage.py：规则级覆盖检查 + 品牌标签锚点检索（查询工具，非门禁）
│   ├── merge-reject-from-loyalsoldier/
│   └── normalize-yaml-comments/
├── .agents/skills/                     # 项目级 Agent Skills（已纳入 git 跟踪）
│   └── fill-domains-from-log/         # 从日志提取漏网之鱼域名并分类补录的完整工作流
│       └── scripts/extract-match-domains/  # 提取脚本 + skip-list.txt（已裁决跳过项数据源）+ README
├── .github/workflows/
│   └── auto-merge-reject.yml           # 每日 00:20 UTC 自动合并 reject.yaml
└── log/                                # 本地运行日志（已 gitignore，不入库）
                                        # 是补充规则时"漏网之鱼"域名的数据来源
```

扁平存放的 40 余个（当前 43 个）`*.yaml` 规则文件，如新增或重构文件内容，需同步更新 [README.md](README.md) 的「规则文件」表。

#### 目录和文件命名规则

- **文件命名**：新建或重命名文件，使用 `lowercase.yaml`格式，多词用连字符（示例 `hk-broker.yaml`、`fin-media.yaml`）。
- **log/**：运行日志目录（流量日志和插件日志）。日志中 `match Match` 表示该域名未匹配任何规则，落入了"漏网之鱼"策略组；`match RuleSet(oc-cn-domain)` 表示命中了外部 OpenClash CN 域名规则集（通常走 DIRECT）。两类目标都说明未被本仓库 yaml 规则覆盖，需定期将这些域名归类到对应的规则文件中。归类漏网之鱼的域名时，查询域名归属用 **RDAP**（本机 `whois` 不可用，需走代理，见「常见坑」）。

#### 文件分类规则

- **大型互联网公司优先**：大型互联网公司使用独立规则文件，其次按照域名所属的服务区分（例如Apple、Google、Microsoft、AI 等）有各自专属文件。
- **proxy.yaml**：兜底存放无法直连或者直连不稳定的杂项规则
- **direct.yaml**：兜底存放可稳定直连的存放杂项规则。
- **-global.yaml**：同厂商的海外 / 国际版服务，与国内主文件分开维护，目前有 `alibaba`、`bytedance`、`tencent` 三对
- **-ai.yaml**： AI 服务按可直连 / 需代理拆分：`direct-ai.yaml`（直连）、`proxy-ai.yaml`（代理）；大厂 AI 优先归入厂商文件（如 `claude.yaml`、`openai.yaml`）
- **占位文件**：截至 2026-10-17 全库空壳文件已清零（`paypal.yaml` 已删除、域名并入 `us-payment.yaml`；`steam.yaml`、`xhs.yaml` 已补真实规则）。如再出现仅有空占位 `DOMAIN-SUFFIX,`（无效规则）的文件，补充真实域名时直接替换占位行。
- **reject.yaml**：由 GitHub Actions 工作流维护，每日从 Loyalsoldier 上游自动生成广告域名 — 禁止编辑，为本地新发现的域名做分类时，也不要查询、核对**reject.yaml**。

#### 域名归属判定判据（按可信度排序）

为新域名定归属文件时，按以下判据逐级判断；都不满足的一律留人工，不得凭感觉归类：

1. **同标签 TLD 变体**：库内已有该品牌标签任一 TLD（如 `browserleaks.com`）→ `.net`/`.org` 零歧义补录。**标签须逐字符相同**，形近/字母转位（`mdoelscope.ai` vs `modelscope.ai`）是仿冒域，绝不补录。（锚点检索已机器化：`check_coverage.py` 对未覆盖域名自动输出 `BRAND-ANCHOR`，仍须人工确认标签逐字符相同。）
2. **同厂商兄弟域 + 文件内既有成组约定**：`intercom.io`+`intercomcdn.com` 组 → 补 `sentry-cdn.com`；`pornhub.yaml` 的「主域+同名 CDN」组 → 补 `xvideos.net`。
3. **「品牌 + 固定后缀」成对先例**：同文件分组内已有「主域 + 同品牌衍生域」成对并存（`volces.com` + `volccdn.com`、`doubao.com`）→ 同结构的 `doubaocdn.com` 属零歧义补录。
4. **命名族归属 > 进程证据**：`byte*` 族（byteimg/bytetos/bytedanceapi/bytescm/bytetcc）支持 `bytednsdoc`；`bdstatic.com` 支持 `bdimg.com`。进程证据只能加分不能单独定案（`volceapplog.com` 疑火山但仅 firefox 进程 → 留人工）。
5. **品牌字面在域内 + 该厂商文件已落盘**：`servicewechat.com` / `wechat.com` → `wechat.yaml`（已有 weixin.com）。**无锚点文件即新增厂商文件**（`logitech.io`、`asus.com`）→ 一律留人工，即便品牌明确。
6. **`*.tencent.com` 精确子域**属零歧义安全区；禁止 `DOMAIN-SUFFIX,tencent.com` 主域（与 hk-bank 的 `tpns.hk.tencent.com` 冲突）。
7. **裸 IP 判据 = 同厂商 IP 分组已存在**，非"同主域"：`17.57.0.147` → apple.yaml「apsd」组（已有 `17.57.145.0/24`）。加前先确认无更宽既有网段。
8. **精确主机规则 ≠ 主域覆盖**：`DOMAIN,cdn.ripperhe.com` 不代表覆盖 `ripperhe.com`。判定前必须回看命中行规则类型。

#### 已裁决结论（勿再问、勿收录）

> 机器可读映射（**已裁决项的运行时唯一数据源**）：`.agents/skills/fill-domains-from-log/scripts/extract-match-domains/skip-list.txt`
> （`skip`=静默跳过，`manual`=待人工可见）。**新裁决项落 changelog 时必须同步追加到该文件**，
> 用户定案的 manual 项要从文件移除。判据规则以本节为权威；下方清单是该文件的人类可读快照，
> 由**交互式会话**对齐维护（fill-domains-from-log skill 第 0 节对齐检查）——AGENTS.md 是受保护
> 文件，cron / automation 会话写它必被 BLOCKED，清单同步延后至交互式会话，不要求逐轮一致。

- 无主端点不归类：`antpeak.com` / `hibchr.com` / `zorvian.com`。
- reject 上游已收录（跳过不加不问）：`clarity.ms`、`jpush.cn`、`jiguang.cn`、`etahub.com`、`cloudflareinsights.com`、`go-mpulse.net`、`akstat.io`。
- **伪域名 / 探针族整批跳过不计入待判**：`wpad`、`monitor_browser`、`*.dotnxdomain.net` / `*.dashnxdomain.net` / `*.starnxdomain.net`（NextDNS + DNSSEC `root-key-sentinel-*` 探针）。
- **广告/追踪类整批不落盘**：归 reject.yaml 上游且**禁止核对 reject.yaml**，故只记录不判断（Chrome 浏览一日可产出 40+ 个 ad-tech 主域）。
- 微信主域 `weixin.com` / `wechat.com` → `wechat.yaml`（非 tencent）。`spacelama.com` → tencent（用户直接指定）。
- 海外 → `proxy.yaml`；国内经 RDAP/NS 确认 → `direct.yaml`；`macked.site` 是 Mac 资源站→proxy。
- 中国移动系（10086.cn / chinamobile.com / cmcc-cs.cn / komect.com / miguvideo.com / 10085.cn / cmicapm.com 等）→ direct.yaml 中国移动组。WPS 系（wps.cn / wpscdn.cn / qwps.cn / ksosoft.com）→ direct.yaml。
- Agent 自用查询端点（rdap.org / verisign.com / crt.sh 等）→ direct.yaml「域名查询 / RDAP」组。
- 长期挂起待人工（无锚点）：`logitech.io`、`logitechg.com`（Logitech G 系，2026-10-18 裁决，同 logitech.io）、`oceanengine.com`、`ntp.org.cn`、`yhgfb-cn-static.com`、`applogcdn.com`、`temu.com`、`photon.codes`、`mdoelscope.ai`（仿冒）。

#### 文件格式规则

每个 `.yaml` 规则文件**必须**以 `payload:` 作为根键开头。使用的规则类型：

- `DOMAIN-SUFFIX,example.com` — 大多数网站首选使用 `DOMAIN-SUFFIX`（连字符），**而非** `DOMAIN_SUFFIX`（下划线）。
- `DOMAIN,example.com`
- `DOMAIN-KEYWORD,keyword`
- `IP-CIDR,1.1.1.1/32,no-resolve`
- `PROCESS-NAME,BinaryName` — 谨慎使用，仅限桌面应用
- **分组**：使用 `# === Service Name ===` 注释头按服务/类别分组规则。

#### YAML 域名规则文件更新

- reject.yaml：由 GitHub Actions 工作流（`auto-merge-reject.yml`）每日 00:20 UTC 运行，调用 `scripts/merge-reject-from-loyalsoldier/merge_reject_from_loyalsoldier.py` 并自动提交 `reject.yaml` 的变更，本地禁止编辑。
- 其他YAML文件：域名更新的数据来源是真实使用场景中Mac ClashX Meta App的日志。手动或自动提取日志中 match 域名，整理到 yaml中，完成更新。

#### 日志差集纪律（从日志提取域名时必守）

- **2026-10-17 起日志 cp 复制 + 只处理昨天（skill v2.5.0+）**：源目录 `~/.config/clash.meta/logs/` 的**昨天**日志文件夹用 `cp -R` **只读复制**到 `log/clashx-meta-log/`（不删源）；**禁止 `mv`/`rm` 源目录**——写/删 `~/.config`（系统配置目录）触发沙箱授权弹窗、automation 无人响应卡死，cp 只读源不弹窗。当天日志不处理（仍被实时写入）、更早的留存源目录（累积由用户定期清理）。处理完成（push + 同步 `0 0`）后已处理文件夹归档至同级 `log/.archive/`（归档为工作区内 mv，不碰 `~/.config`）。优先用仓库已有（`log/clashx-meta-log/` 下昨天前缀文件夹存在则直接用，无则从源 cp；防 cp 套娃——目标侧同名则跳过）。
- **changelog 有记录 ≠ 已处理完**：日志当天持续追加、跨日追加、重启新增 core 文件，须 diff 后重新提取，与 changelog 已处理主域集合对比定位增量。
- **只处理昨天**：当天日志留待次日 automation 处理（作为昨天的）；不再扫描今日目录。带出的目录必须真正跑提取，不能只 cp。
- 差集 ≠ 漏跑：早期运行未 cp 造成的历史缺口用 changelog 交叉核验定性（特征域名能找到落点即是复制缺口）。
- 提交信息里的数字先算准再写。

#### changelog 编写约束

changelog.md 是变更账本（2026-10-17 起已纳入 git 跟踪，**每次提交须把 changelog.md 一并显式暂存**），同时是跨轮次「已处理主域集合」的比对基准——每轮日志提取靠它判断增量。因此**每条都必须可核对、可复用**；写不好会直接导致下一轮重复劳动或漏判。

**写入时机与位置**
- 每完成一次阶段性任务，在 commit **之前**将本次变更**追加到 changelog.md 顶部**（最新在前）；同一天多条按完成时间倒序。
- 一次逻辑变更一个条目；条目是提交说明的展开版，两者事实必须一致。

**条目结构（域名归类类变更，必写要素）**
1. **标题**：`## YYYY-MM-DD <对象>：<一句话摘要>（<branch> → <merge commit>）`。
2. **数据来源**：处理的日志目录清单 + `diff -rq` 差集结论（昨日 / 今日 / 续写增量分别说明）。
3. **提取量**：`match Match` / `oc-cn-domain` 各自的域名数与裸 IP 数，注明统计口径（见下）。
4. **补录明细**：落到哪个文件、哪个分组、什么规则、判定依据——引用「域名归属判定判据」条目号或既有先例，不要只写"无歧义"。
5. **未收录及原因**：逐个域名说明为什么不收。
6. **整批跳过**：已覆盖主域（按厂商系列举）、历史已判定项（`antpeak.com` / `hibchr.com` / `zorvian.com`、reject 上游已收录等）、伪域名 / 探针族。
7. **待人工确认**：逐个域名附子域、发起进程、遗留轮次（"连续第 N 轮"）；落盘或判定后从清单移除并写去向。
8. **自检结果**：`find_duplicates.py` 跨文件 / 文件内重复数（明确"本次新引入 0 项"及历史基线）、被编辑文件的 payload 数与 `yaml.safe_load` 结果。
9. **Git 操作链**：提交号 → push 区间 → `0 0` 确认。

**统计口径（写数字前先对齐）**
- **提取行格式**：`match Match using` 与 `(match Match/)` 错误行**两种都要覆盖**（2026-10-07 曾因只取前一种漏记一个已覆盖域；近期日志该差异仅涉及探针伪域名与已覆盖域，但口径必须写全）。
- **伪域名过滤**：`wpad`、`monitor_browser`、`postgres` 等无 TLD 主机名，以及 `*.dotnxdomain.net` / `*.dashnxdomain.net` / `*.starnxdomain.net`（NextDNS + DNSSEC `root-key-sentinel-*` 探针）整族剔除，不计入数量。
- **「归并主域后 N 个」**：按可注册主域合并后的去重数（含已覆盖项），括号注明构成（如 `oc-cn-domain 12 + match Match 6`），便于复核。
- **payload 数**：文件中 `- ` 开头的规则行数（含 IP-CIDR）；写之前用 `grep -cE '^[[:space:]]*-[[:space:]]*[^[:space:]]' <file>` 实查，不凭记忆。
- **全局数字**（全库文件数、规则总数）以提交时的仓库实际状态为准。

**计数纪律**
- 条目内列举的项数必须等于声称的项数："待人工确认 N 项"的 N = 列表子弹数；"补录 M 个域名"的 M = 明细行数。
- 提交信息里的数字与条目保持一致，**先算准再写**（历史事故：2026-10-11 提交信息把 19 项写成 13 项，已推送无法改）。

**历史条目修正**
- 复查发现往期条目的数量或事实错误：直接修正；涉及新增内容（如补记漏项）时在该处标注「YYYY-MM-DD 复查补记」及依据，不做无声改写。

**其他**
- 广告 / 追踪类按批次记录（可列代表性主域），不逐一判定、不查询 reject.yaml。
- 语言为中文；域名、规则、文件名、commit 号用反引号。

#### 常用命令

YAML文件编辑后，验证是否符合语法规则（**注意：本机系统 `python3` 无 pyyaml，必须用带 pyyaml 的解释器**）：

```bash
# 校验 YAML 语法
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
$PY -c "import sys,yaml; yaml.safe_load(sys.stdin)" < SomeFile.yaml

# 检查跨文件重复规则（报告输出至 scripts/find-duplicates/DUPLICATES.md，全量 JSON duplicates.json 已入库）
# 该脚本扫描根已锚定仓库根，任意目录可运行
python3 scripts/find-duplicates/find_duplicates.py

# 规则级覆盖检查：判断域名/IP 是否已被业务 yaml 覆盖 + 品牌标签锚点（判据1 机器化）
# 排除 reject.yaml；查询工具非门禁，退出码恒 0；任意目录可运行
python3 scripts/check-coverage/check_coverage.py feishu.cn itdog.cn 1.2.3.4

# 从 Loyalsoldier 上游合并最新拒绝规则至 reject.yaml（须在仓库根目录执行）
# 注意：本地无需手动执行，auto-merge-reject.yml 每日自动运行；仅在需要本地验证合并结果时使用
python3 scripts/merge-reject-from-loyalsoldier/merge_reject_from_loyalsoldier.py

# 将章节注释标题规范化为 `# === Title ===` 格式（须在仓库根目录执行）
python3 scripts/normalize-yaml-comments/normalize_yaml_comments.py
```

#### 编辑后重复规则自检闭环（强制）

每次新增 / 修改 / 删除任意 `.yaml` 规则后，必须执行以下闭环，确认没有引入重复规则：

1. **运行脚本** — 执行 `python3 scripts/find-duplicates/find_duplicates.py`（扫描根已锚定仓库根，任意目录可运行）。
2. **读取报告** — 读取 `scripts/find-duplicates/DUPLICATES.md`（只列重复项，Agent 读此文件即可；`scripts/find-duplicates/duplicates.json` 是全量数据。
3. **修正并重跑** — 若报告存在跨文件重复或文件内重复，调整规则归属 / 删除冗余项后重新运行脚本，直到脚本退出码为 0（即 `DUPLICATES.md` 中无任何重复条目）。
4. **语法校验** — 重复检查通过后，再用上面的 YAML 语法校验命令确认被编辑文件语法合法。

说明：脚本退出码可直接作为门禁 —— **无重复为 0，发现任意跨文件 / 文件内重复为 1**（报告两种情况下都会生成）；但退出码只表示"有无"重复，定位和修正具体规则仍需读取 `scripts/find-duplicates/DUPLICATES.md`。

**统计口径**：
- 全库统计必须剥离 `reject.yaml`（占全库规则 99.29%）。`find_duplicates.py` 已跳过它，报的是业务文件间重复，**基线 1 条**（`settings.crashlytics.com` direct/google），不要误报成新增。
- 解析规则行时 `IP-CIDR,...,no-resolve` 的 `no-resolve` 会被吞进 value，按逗号切第一段；空占位 `DOMAIN-SUFFIX,` 用允许空值的正则抓（`steam.yaml:3`）。

#### Git 工作流

> **背景**：`main` 由本仓库与 `auto-merge-reject.yml` 工作流共管 —— 该工作流每日 00:20 UTC 会直接向 `main` 推送 `reject.yaml` 的自动合并提交。因此远程随时可能出现新提交，且**禁止任何形式的强制推送**。

**分支制度已取消（2026-10-17 用户裁决）**：所有改动（yaml 规则、README、scripts、AGENTS.md 等文档）**一律直接在 main 上修改、提交、推送**，不再先切 feature 分支、不再 `--no-ff` 合并；本地只保留 `main` 一个分支。由于 main 与 bot 共管、远程随时可能出现新提交，**「动手前先确认本地与远程一致」是最核心的约束**，任何文件修改都必须按以下顺序执行：

1. **编辑前 fetch + 比对** — 修改任何文件前，先 `git fetch origin`，再用 `git rev-list --left-right --count origin/main...HEAD` 确认本地与远程双向均为 `0`（左侧非 0 即远程有新提交）。
   - 远程有新提交时：`git stash` → `git pull --rebase` → `git stash pop`，同步后再开始修改。
   - `git pull --rebase` 在存在未暂存改动时会直接失败，此时必须先 `git stash`。
   - 出现冲突先解决冲突再继续，**禁止 `git push --force` / `--force-with-lease`**。
2. **编辑本地文件** — 进行修改。
   - 文件移动 / 重命名一律使用 `git mv <旧路径> <新路径>`，禁止手动删旧建新（易丢失 git 历史并残留 untracked 文件）。
   - 每完成一次阶段性的文件改动，必须立即显式暂存：`git add <file>`。**禁止使用 `git add .`、`git add -A` 或类似批量跟踪命令**——会把无关文件带入暂存区，导致仓库文件混乱（`.agents/`、`AGENTS.md`、`changelog.md` 等已不在 .gitignore 中，误用批量跟踪的后果比以前更严重）。
   - 编辑完成后、暂存提交前，**先读一遍 `changelog.md`**（已纳入 git 跟踪，但跨轮次比对基准的地位不变），确认目标域名是否已被往期记录判定为「reject.yaml 上游已收录」——这类域名不应重复加入业务规则文件。
3. **提交前再 fetch + 比对** — 暂存完成后、commit 之前，再次 `git fetch origin` 并比对 `origin/main...HEAD`（双向 `0` 才可提交）；期间远程又有新提交则按第 1 步同步后重来。
4. **更新 changelog 并提交** —
   - 每完成一次阶段性任务，**必须先在 `changelog.md` 顶部追加本次变更记录**（写法见「changelog 编写约束」；已纳入 git 跟踪，**提交时与改动文件一并显式暂存**），然后再 commit。
   - 提交信息（commit message）使用中文，**一次逻辑变更一个提交**；暂存时显式列出文件，**禁止 `git add .` / `git add -A`**。
   - **禁止在提交中包含 `reject.yaml`**，该文件由 bot 独占维护，人工提交带上它会与上游自动合并产生冲突。
   - **按时定期更新的特例**：如需定时 / 周期性更新文件，只允许 `git add -u && git commit -m "更新已有文件"`——仅暂存已跟踪文件的修改，不做批量跟踪、不引入新文件。
5. **立即推送并确认同步** — 每完成一次 `commit`，**必须立即 `push`**。推送后确认 `git rev-list --left-right --count origin/main...HEAD` 输出 `0 0`。

#### 文档 / README 改动约定

- 所有改动（含 README、scripts）与 Git 工作流一致：**直接在 main 上修改、提交、推送**（2026-10-17 起取消分支制度，本地仅保留 main）；每次动手前后按 Git 工作流第 1、3 步执行本地与远程一致性检查，推送后校验 `0 0`。
- README 代码块用「生成（`/tmp/*.py`，CJK 双宽对齐）→ `yaml.safe_load` 校验 → 按板块标题 splice」流程，替换后补**引用一致性校验**（rules 引用的 provider/group、use 的订阅均已定义）。
- 面向 SEO/AI 的摘要板块，正确姿势是「压缩重述 + 独家事实 + 指针」，不是照搬正文；易漂移的数字（文件数、interval）只在一处出现，其余用指针。

#### 常见坑

- **`git commit -F - <<'EOF'`（heredoc 提交信息）可用**，但 **heredoc 内联 python 脚本会被安全策略拦截**；批量处理请先 Write 成 `/tmp/xxx.py` 再执行。单条带内联脚本+参数的校验命令也可能被拦 → 写 `/tmp/yaml_check.py` 循环校验。
- **git 代理 7893 状态来回翻转，每轮现场双探测**：`nc -z 127.0.0.1 7893` + `curl --noproxy '*' github.com`。禁用代理时 zsh 变量不做词分割，须 `gitx() { git -c http.proxy= -c https.proxy= "$@"; }`。
- **`git merge` 必须带 `-m/--no-edit`**，否则无终端下退出码 137 并留 `MERGE_HEAD`。
- **`.workbuddy/skills` 与 `.workbuddy/memory` 是指向 `.agents/` 下真实目录的符号链接**，两个路径访问的是同一份文件。项目级 skill 的实际位置是 `.agents/skills/`，记忆是 `.agents/memory/`，文档里写 `.agents/...` 路径即为正确，不要"修正"成 `.workbuddy/...`。`Skill` 工具加载 `fill-domains-from-log` 可能报 "Cannot find skill" → 直接 Read `.agents/skills/fill-domains-from-log/SKILL.md`。
- **本机系统 `python3` 没有 pyyaml**，YAML 语法校验需用带 pyyaml 的解释器：`/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python`。
- `whois` 命令不可用（`whois.iana.org` 无法解析且客户端会挂起），macOS 也**没有 `timeout` 命令**；域名注册信息查询走 RDAP（需代理 `https_proxy=http://127.0.0.1:7893`）。RDAP 首调常空需重试 2-3 次；registrar 为空时看 NS 定归属（HICHINA/ALIDNS→国内）或 DoH 看 A 记录 IP 段。
- **AGENTS.md 本身是受保护文件**：cron / automation 会话（无交互用户）中 patch 工具直接 BLOCKED（"requires approval but no interactive user or gateway is present"，2026-10-18 实测）。automation 轮新裁决项只落 skip-list + changelog 即闭环（提取脚本只读 skip-list）；本文件与 `.agents/memory/MEMORY.md` 的「已裁决结论」清单同步延后至交互式会话（fill-domains-from-log skill 第 0 节对齐检查）。

#### 仓库状态（已知事实与遗留问题）

- PayPal 域名全在 `us-payment.yaml`，独立 `paypal.yaml` 已删（2026-10-11）。用户说「加到 X 文件」前必须先用 `scripts/check-coverage/check_coverage.py` 全库查重（规则级判断，勿用 grep 子串匹配）。
- 未修的已知问题：`proxy.yaml:784` 把 `USER-AGENT,WhatsApp*` 误写成分组注释头致 43 条归属错误；`direct.yaml` 44–179 行「腾讯云-香港」134 条实为杂项。
- `domain-distribution.html` 未被 gitignore（未跟踪未提交）。
- README 仍有用户挂起未确认的改动（两条 FAQ 未恢复、L100 句式杂糅等），非用户明确要求不要擅自动。

#### .gitignore

以下文件或目录已 gitignore ，如果与.gitignore文件有冲突，以.gitignore文件为准

```text
.claude/
.omc/
.trae/
.workbuddy-ai/
.workbuddy/
.codebuddy/
log/
```

注：2026-10-17 用户裁决，`.agents/`、`AGENTS.md`、`CLAUDE.md`、`changelog.md`、`scripts/find-duplicates/duplicates.json` **均已纳入 git 跟踪**（`CLAUDE.md` 以指向 `AGENTS.md` 的符号链接形式跟踪）；`.omc/` 维持忽略不跟踪。提交时仍须显式列文件（`git add -A` / `git add .` 依旧禁止），且 `changelog.md` 变更须随对应提交入库。
