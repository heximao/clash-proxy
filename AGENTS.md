### clash-proxy/AGENTS.md

本文件为 Agent（Claude、Codex、Opencode、Hermes Agent）在本仓库工作提供指引。

本仓库（clash-proxy）是一个域名规则集合仓库，不是一个标准的代码仓库，本仓库无构建系统、测试套件或 linter。通过 jsDelivr CDN 分发为 Clash / OpenClash 客户端提供 YAML 域名规则文件。引用 CDN URL 格式：`https://cdn.jsdelivr.net/gh/heximao/clash-proxy/<filename>.yaml`。

本仓库的核心目的是基于真实的使用场景，将访问过的域名收集并分类，以便可以精准的使用指定代理访问各个网络。

#### 目录结构

```text
clash-proxy/
├── AGENTS.md                           # 本文件：Agent 在本仓库的工作指引
├── config.yaml                         # Mac ClashX Meta 运行配置文件的副本，与正在运行的区别是隐藏了 proxy-providers 订阅链接（未跟踪也未 gitignore）
├── *.yaml                              # 除 config.yaml 外的业务规则文件：扁平存放根目录，均以 payload: 开头
├── README.md                           # 面向使用者：CDN 引用方式、客户端配置示例、规则文件全表
├── changelog.md                        # 更新记录：每次变更后在顶部追加（见「git 操作」）
├── issues-domain.md                    # 待人工判定域名表：证据不足无法判定归属的域名登记于此（fill-domains-from-log skill 第 6b 节登记，fill-issues-domain skill 处理定案）
├── .gitignore                          # 忽略规则（log/、tmp/、工具目录等；以文件本身为准）
├── scripts/                            # 维护脚本（每个脚本独立子目录，各带自己的 README）
│   ├── find-duplicates/               # find_duplicates.py + 生成物 DUPLICATES.md（入库）/ duplicates.json（入库）
│   ├── check-coverage/                # check_coverage.py：规则级覆盖检查 + 品牌标签锚点检索（查询工具，非门禁）
│   ├── merge-reject-from-loyalsoldier/
│   └── normalize-yaml-comments/
├── .agents/                            # 项目级 Agent 数据（已纳入 git 跟踪）
│   ├── skills/
│   │   ├── fill-domains-from-log/     # 从日志提取漏网之鱼域名并分类补录的完整工作流
│   │   │   └── scripts/extract-match-domains/  # 提取脚本 + skip-list.txt（已裁决跳过项数据源）+ README
│   │   └── fill-issues-domain/        # issues-domain.md 待判定表处理流程（证据复核 → 用户裁决 → 落盘/转 skip → 三处闭环）+ 查证/校验脚本
│   └── memory/                         # 项目记忆：每日工作日志 + MEMORY.md
├── .github/workflows/
│   └── auto-merge-reject.yml           # 每日 00:20 UTC 自动合并 reject.yaml
├── tmp/                                # 临时目录
└── log/                                # 本地运行日志（已 gitignore，不入库），补充规则时"漏网之鱼"域名的数据来源
    ├── clashx-meta-log/                # ClashX Meta 日志：cp 只读复制昨天的日志进来（处理源）
    ├── openclash-log/                  # OpenClash 日志（历史遗留空目录；oc-cn-domain 命中实际来自 clashx-meta 日志）
    ├── archive/                        # 已处理完（push + 0 0）的日志文件夹归档处（归档目录唯一位置）
```

扁平存放的 40 余个 `*.yaml` 规则文件（精确数量以 [README.md](README.md) 的「规则文件」表为准，勿在本文硬编码维护），如新增或重构文件内容，需同步更新该表。

#### 目录和文件命名规则

- **文件命名**：新建或重命名文件，使用 `lowercase.yaml` 格式，多词用连字符（示例 `hk-broker.yaml`、`fin-media.yaml`）。
- **log/**：运行日志目录（流量日志和插件日志）。日志中 `match Match` 表示该域名未匹配任何规则，落入了"漏网之鱼"策略组；`match RuleSet(oc-cn-domain)` 表示命中了外部 OpenClash CN 域名规则集（通常走 DIRECT）。两类目标都说明未被本仓库 yaml 规则覆盖，需定期将这些域名归类到对应的规则文件中。归类漏网之鱼的域名时，查询域名归属用 **RDAP**（本机 `whois` 不可用，需走代理，见「常见坑」）。

#### 文件分类规则

- **大型互联网公司优先**：大型互联网公司使用独立规则文件，其次按照域名所属的服务区分（例如Apple、Google、Microsoft、AI 等）有各自专属文件。
- **proxy.yaml**：兜底存放无法直连或者直连不稳定的杂项规则
- **direct.yaml**：兜底存放可稳定直连的杂项规则。
- **-global.yaml**：同厂商的海外 / 国际版服务，与国内主文件分开维护，目前有 `alibaba`、`bytedance`、`tencent` 三对
- **-ai.yaml**：AI 服务按可直连 / 需代理拆分：`direct-ai.yaml`（直连）、`proxy-ai.yaml`（代理）；大厂 AI 优先归入厂商文件（如 `claude.yaml`、`openai.yaml`）
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
> 同步延后至交互式会话（受保护文件限制见「常见坑」），不要求逐轮一致。
>
> `manual` 项另有人类可读表格视图：根目录 [`issues-domain.md`](issues-domain.md)（待人工判定域名表，**登记**由
> fill-domains-from-log skill 第 6b 节负责，**定案处理**由 fill-issues-domain skill 负责）——证据不足无法判定归属的域名（含判据 5 无锚点厂商文件的
> 大型公司主域）登记于此留用户判定；用户定案后该行与 skip-list `manual` 项同步移除（**表只保留待判定
> 域名，定案记录以 changelog 为准**）。`skip` 类已裁决项（无主端点/广告追踪/reject 上游/伪域名）不进表。

- 无主端点不归类：`antpeak.com` / `hibchr.com` / `zorvian.com`。
- reject 上游已收录（跳过不加不问）：`clarity.ms`、`jpush.cn`、`jiguang.cn`、`etahub.com`、`cloudflareinsights.com`、`go-mpulse.net`、`akstat.io`、`featureassets.org`、`wdfl.co`、`nsvcs.net`（后三者 2026-10-28 定案：`reject.yaml` 已有 `DOMAIN-SUFFIX` 或精确主机规则，而 `reject` 是 `rules` 首条、优先级最高，再补录无意义）。
- **伪域名 / 探针族整批跳过不计入待判**：`wpad`、`monitor_browser`、`www.z` / `www.zhipin`（WorkBuddy AI Helper 截断主机名，无有效 TLD，2026-10-19 裁决入 skip-list）、`*.dotnxdomain.net` / `*.dashnxdomain.net` / `*.starnxdomain.net`（NextDNS + DNSSEC `root-key-sentinel-*` 探针）。
- **广告/追踪类整批不落盘**：归 reject.yaml 上游且**禁止核对 reject.yaml**，故只记录不判断（Chrome 浏览一日可产出 40+ 个 ad-tech 主域）。
- 微信主域 `weixin.com` / `wechat.com` → `wechat.yaml`（非 tencent）。`spacelama.com` → tencent（用户直接指定）。
- 海外 → `proxy.yaml`；国内经 RDAP/NS 确认 → `direct.yaml`；`macked.site` 是 Mac 资源站→proxy。
- 中国移动系（10086.cn / chinamobile.com / cmcc-cs.cn / komect.com / miguvideo.com / 10085.cn / cmicapm.com 等）→ direct.yaml 中国移动组。WPS 系（wps.cn / wpscdn.cn / qwps.cn / ksosoft.com）→ direct.yaml。
- Agent 自用查询端点（rdap.org / verisign.com / crt.sh 等）→ direct.yaml「域名查询 / RDAP」组。
- **issues-domain 挂起项处置规则（用户 2026-10-22 裁定，2026-10-28 修订）**：`.cn` 域名全部归 `direct.yaml`；agent 判定**高度归属国内**的域名归 `direct.yaml`；**不新建厂商文件**——海外知名公司杂项归 `proxy.yaml`；**无国内实证、无海外公司归属的域名也统一归 `proxy.yaml`，不再逐项挂起**（2026-10-28 用户裁定，取代 10-22 的「继续挂起」分支；无主端点/广告追踪/reject 上游等既有 skip 裁决优先）。（广告/追踪类整批不落盘纪律优先于本裁定。）
- 长期挂起待人工项以 [`issues-domain.md`](issues-domain.md) 表为唯一视图（2026-10-28 全部定案后现 0 项），本文不镜像清单——定案只需改表 + skip-list 两处。

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

获取、归档、差集的完整操作口径见 `SKILL.md` 第 1、2b、12 节，此处只列不可违反的四条：

- **源目录只读**：`~/.config/clash.meta/logs/` 的昨日文件夹用 `cp -R` 复制到 `log/clashx-meta-log/`，**禁止 `mv`/`rm` 源目录**——写/删 `~/.config` 触发沙箱授权弹窗，automation 无人响应会卡死。
- **只处理昨天**：当天日志仍在实时写入，留待次日处理；带出的目录必须真正跑提取，不能只 cp。
- **处理完必须归档**到 `log/archive/`（工作区内 `mv`），否则下轮重复提取。
- **changelog 有记录 ≠ 已处理完**：日志会跨日追加、重启新增 core 文件，须 diff 后与 changelog 已处理主域集合比对定位增量；早期 cp 造成的历史缺口用 changelog 交叉核验定性（特征域名能找到落点即是复制缺口）。

#### changelog 编写约束

`changelog.md` 是变更账本，也是跨轮次「已处理主域集合」的比对基准——每轮日志提取靠它判断增量，所以条目必须可核对、可复用。写入时机：commit **之前**追加到顶部（最新在前，同日按完成时间倒序），一次逻辑变更一个条目，条目是提交说明的展开版且事实一致。

域名归类类条目的九个必写要素：① 标题 `## YYYY-MM-DD <对象>：<摘要>（<轮次>）`；② 数据来源（日志目录清单 + `diff -rq` 差集结论）；③ 提取量（`match Match` / `oc-cn-domain` 各自域名数与裸 IP 数）；④ 补录明细（文件、分组、规则、判据条号或既有先例，不许只写"无歧义"）；⑤ 未收录及原因；⑥ 整批跳过（已覆盖主域按厂商系列举、历史已判定项、伪域名/探针族）；⑦ 待人工确认（附子域、进程、"连续第 N 轮"，落盘后移除并写去向）；⑧ 自检结果（重复检查数、payload 数、`yaml.safe_load`）；⑨ Git 操作链（提交号 → push 区间 → `0 0`）。

统计口径细节（两种 `match` 行格式都要覆盖、伪域名/探针族剔除、主域归并构成、payload 数实查命令）与计数纪律（列举项数 = 声称项数、提交信息数字与条目对齐）见 `SKILL.md` 第 10 节，本文不重复。广告/追踪类按批次记录（可列代表性主域），不逐一判定、不查询 reject.yaml。历史条目数量或事实有误直接修正；补记内容标注「YYYY-MM-DD 复查补记」及依据，不做无声改写。语言为中文，域名/规则/文件名/commit 号用反引号。

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
# 批量输入走 stdin 管道（推荐）：cat domains.txt | python3 scripts/check-coverage/check_coverage.py -
# 注意：`-` 与位置参数混用会吞掉 stdin 输入（2026-10-19 实测），多输入必须全部走 stdin
# --quiet 只列未覆盖项
python3 scripts/check-coverage/check_coverage.py --quiet feishu.cn itdog.cn 1.2.3.4

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
- 全库统计必须剥离 `reject.yaml`（占全库规则 99.29%）。`find_duplicates.py` 已跳过它，报的是业务文件间重复，**基线 1 条**（`settings.crashlytics.com` direct/google），不要误报成新增。另注意 `config.yaml`（未跟踪的运行配置副本）也会被扫描，其 intra-file「重复」实为策略组名 / DNS 配置值噪声（2026-10-19 实测 23 条），不是规则重复，勿当新引入误判。
- 解析规则行时 `IP-CIDR,...,no-resolve` 的 `no-resolve` 会被吞进 value，按逗号切第一段；空占位 `DOMAIN-SUFFIX,` 用允许空值的正则抓（`steam.yaml:3`）。

#### git 操作

> **背景**：`main` 由本仓库与 `auto-merge-reject.yml` 工作流共管 —— 该工作流每日 00:20 UTC 会直接向 `main` 推送 `reject.yaml` 的自动合并提交。因此远程随时可能出现新提交，且**禁止任何形式的强制推送**。git 使用的最高目标是**不丢数据、不乱历史**。

**红线禁令（任何场景不可违反）**

- 禁止 `git add .`、`git add -A`、`git add <目录>` 及 `git commit -a` / `-am` 等一切**批量暂存**——会把无关 / 未跟踪文件一网扫入；暂存一律精确到文件路径。
- 已 push 的 commit **禁止 amend / rebase**——补救只能靠 `push --force`，会重写远程历史；发现提交内容或信息有误时新建 commit 修正，并在 changelog 说明。
- **禁止 `push --force` / `--force-with-lease`** 覆盖远程，除非用户明确确认远程历史作废。
- 破坏性命令（`reset --hard` / `checkout -- <file>` / `restore` / `clean -f`）会**不可逆丢弃未提交改动**，执行前必须先 `git status` + `git diff` 确认影响范围。
- 非交互 shell 中 `git commit` 必须带 `-m`（无 `-m` 会拉起编辑器、挂死会话）；多行提交信息用 `git commit -F - <<'EOF' … EOF`。

**暂存与提交**

- 每完成一次阶段性文件改动，立即 `git add <file>`（精确到文件）；提交前用 `git diff --cached` 过目，防止误提交凭证、调试产物或无关文件。除非用户主动要求不git
- 每完成一次阶段性任务，必须同步更新 [changelog](changelog.md)（变更随该次提交显式暂存），然后 commit（附中文说明）并立即 push。
- 删除已跟踪文件用 `git rm`（同时暂存删除动作）；直接 `rm` 后必须补 `git add <file>`，否则 commit 里文件还在。
- 定时 / 周期性更新只允许 `git add -u && git commit -m "更新已有文件"`——仅暂存已跟踪文件，不引入新文件。
- 命令里含中文或空格的路径必须加引号。
- **少用 `git stash`**：本仓库流程要求阶段性改动立即 add + commit；stash 内容不显示在 `git status`，跨会话 / 跨 Agent 极易遗忘而丢失。同步远程时可用 `git stash` → `pull --rebase` → `stash pop`，但必须当场 pop 回来。

**移动 / 重命名 / 删除**

- 移动或重命名一律用 `git mv`；它只暂存改名（沿用暂存区旧内容），移动前已做的内容修改**不会随之入库**，移动后需再 `git add` 新路径补上（2026-10-19 实测踩坑）。
- macOS 文件系统大小写不敏感：仅改大小写的重命名**不要用普通 `mv`**（`git status` 可能识别不到变更），一律 `git mv`，必要时加 `-f`。

**推送、冲突与配置**

- 每完成一次 commit 必须立即 push，推送后校验 `git rev-list --left-right --count origin/main...HEAD` 为 `0 0`。
- push 被拒（远程已有新提交，如 bot 的自动合并）：`git fetch` + `git pull --rebase` 后再 push；rebase 冲突时先 `git status` 看冲突文件，**与 `reject.yaml` 的冲突一律 `git checkout --theirs reject.yaml`** 保留 bot 版本（人工改动与 bot 的 reject.yaml 几乎不会重叠，真出现先停下来汇报）。
- 修改 `.gitignore` 前必须与全局 `.gitignore_global` 对比，不能有冲突。

#### 文档 / README 改动约定

- 所有改动（含 README、scripts）直接在 main 上修改、提交、推送（本地仅保留 main）。每次动手前后按上文「git 操作」执行本地与远程一致性检查（`fetch` + 双向 `0 0`），推送后再校验一次。
- README 代码块用「生成（`/tmp/*.py`，CJK 双宽对齐）→ `yaml.safe_load` 校验 → 按板块标题 splice」流程，替换后补**引用一致性校验**（rules 引用的 provider/group、use 的订阅均已定义）。
- 面向 SEO/AI 的摘要板块，正确姿势是「压缩重述 + 独家事实 + 指针」，不是照搬正文；易漂移的数字（文件数、interval）只在一处出现，其余用指针。

#### 常见坑

- **`git commit -F - <<'EOF'`（heredoc 提交信息）可用**，但 **heredoc 内联 python 脚本会被安全策略拦截**；批量处理请先 Write 成 `/tmp/xxx.py` 再执行。单条带内联脚本+参数的校验命令也可能被拦 → 写 `/tmp/yaml_check.py` 循环校验。
- **git 代理 7893 状态来回翻转，每轮现场双探测**：`nc -z 127.0.0.1 7893` + `curl --noproxy '*' github.com`。禁用代理时 zsh 变量不做词分割，须 `gitx() { git -c http.proxy= -c https.proxy= "$@"; }`。
- **`git merge` 必须带 `-m/--no-edit`**，否则无终端下退出码 137 并留 `MERGE_HEAD`。
- **`.workbuddy/skills` 与 `.workbuddy/memory` 是指向 `.agents/` 下真实目录的符号链接**，两个路径访问的是同一份文件。项目级 skill 的实际位置是 `.agents/skills/`，记忆是 `.agents/memory/`，文档里写 `.agents/...` 路径即为正确，不要"修正"成 `.workbuddy/...`。`Skill` 工具加载 `fill-domains-from-log` 可能报 "Cannot find skill" → 直接 Read `.agents/skills/fill-domains-from-log/SKILL.md`。
- `whois` 命令不可用（`whois.iana.org` 无法解析且客户端会挂起），macOS 也**没有 `timeout` 命令**；域名注册信息查询走 RDAP（需代理 `https_proxy=http://127.0.0.1:7893`）。RDAP 首调常空需重试 2-3 次；registrar 为空时看 NS 定归属（HICHINA/ALIDNS→国内）或 DoH 看 A 记录 IP 段。
- **AGENTS.md 本身是受保护文件**：cron / automation 会话（无交互用户）中 patch 工具直接 BLOCKED（"requires approval but no interactive user or gateway is present"，2026-10-18 实测）。automation 轮新裁决项只落 skip-list + changelog 即闭环（提取脚本只读 skip-list）；本文件与 `.agents/memory/MEMORY.md` 的「已裁决结论」清单同步延后至交互式会话（fill-domains-from-log skill 第 0 节对齐检查）。

#### 仓库状态（已知事实与遗留问题）

- PayPal 域名全在 `us-payment.yaml`，独立 `paypal.yaml` 已删（2026-10-11）。用户说「加到 X 文件」前必须先用 `scripts/check-coverage/check_coverage.py` 全库查重（规则级判断，勿用 grep 子串匹配）。
- 未修的已知问题（行号会漂移，按内容定位）：`proxy.yaml` 中 `# === USER-AGENT,WhatsApp* ===` 把本应是规则的条目写成了分组注释头，致其后一批 Google 系杂项（`1e100.net`、`appspot.com` 等）全部挂错分组；`direct.yaml` 的「腾讯云-香港」组内实为杂项，名不副实。
- README 仍有用户挂起未确认的改动（两条 FAQ 未恢复、句式杂糅等），非用户明确要求不要擅自动。
- `.gitignore` 以仓库根文件为准，本文不镜像清单。`log/`、`tmp/` 是本地数据；`config.yaml` 未跟踪也未 gitignore，`git status` 恒显示 `?? config.yaml`。哪些文件入库以 `git ls-files` 实查为准。
