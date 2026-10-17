# clash-proxy 项目长期笔记

## 目录结构
`.workbuddy/skills`、`.workbuddy/memory` 是指向 `.agents/skills`、`.agents/memory` 的**单向符号链接**，同一份文件两个路径等价。文档写 `.agents/...` 即为正确，不要"修正"。`Skill` 工具加载 `fill-domains-from-log` 会报 "Cannot find skill" → 直接 Read `.agents/skills/fill-domains-from-log/SKILL.md`。
**scripts/ 自 2026-10-17 起为子目录结构**（每脚本一目录一 README）：`scripts/find-duplicates/`、`scripts/merge-reject-from-loyalsoldier/`、`scripts/normalize-yaml-comments/`。`find-duplicates/find_duplicates.py` 扫描根已锚定仓库根、**任意目录可运行**，报告（DUPLICATES.md / duplicates.json）在脚本旁；另两个脚本仍须**仓库根目录执行**（依赖 cwd）。旧平铺路径已全部失效，见到的旧引用一律按此映射。

## 归属判定判据（按可信度排序）
1. **同标签 TLD 变体**：库内已有该品牌标签任一 TLD（如 `browserleaks.com`）→ `.net`/`.org` 零歧义补录。**grep 必须按品牌标签而非全域名**，否则会漏掉锚点。标签须**逐字符相同**，形近/字母转位（`mdoelscope.ai` vs `modelscope.ai`）是仿冒域，绝不补录。
2. **同厂商兄弟域 + 文件内既有成组约定**：`intercom.io`+`intercomcdn.com` 组 → 补 `sentry-cdn.com`；`pornhub.yaml` 的「主域+同名 CDN」组 → 补 `xvideos.net`。
3. **「品牌 + 固定后缀」成对先例**（2026-10-17 新增）：同文件分组内已有「主域 + 同品牌衍生域」成对并存（`volces.com` + `volccdn.com`、`doubao.com`）→ 同结构的 `doubaocdn.com` 属零歧义补录。
4. **命名族归属 > 进程证据**：`byte*` 族（byteimg/bytetos/bytedanceapi/bytescm/bytetcc）支持 `bytednsdoc`；`bdstatic.com` 支持 `bdimg.com`。进程证据只能加分不能单独定案（`volceapplog.com` 疑火山但仅 firefox 进程 → 留人工）。
5. **品牌字面在域内 + 该厂商文件已落盘**：`servicewechat.com` / `wechat.com` → `wechat.yaml`（已有 weixin.com）。**无锚点文件即新增厂商文件**（`logitech.io`、`asus.com`）→ 一律留人工，即便品牌明确。
6. **`*.tencent.com` 精确子域**属零歧义安全区；禁止 `DOMAIN-SUFFIX,tencent.com` 主域（与 hk-bank 的 `tpns.hk.tencent.com` 冲突）。
7. **裸 IP 判据 = 同厂商 IP 分组已存在**，非"同主域"：`17.57.0.147` → apple.yaml「apsd」组（已有 `17.57.145.0/24`）。加前先确认无更宽既有网段。
8. **精确主机规则 ≠ 主域覆盖**：`DOMAIN,cdn.ripperhe.com` 不代表覆盖 `ripperhe.com`。判定前必须回看命中行规则类型。

## 已裁决结论（勿再问、勿收录）
- 无主端点不归类：`antpeak.com` / `hibchr.com` / `zorvian.com`。
- reject 上游已收录（跳过不加不问）：`clarity.ms`、`jpush.cn`、`jiguang.cn`、`etahub.com`、`cloudflareinsights.com`、`go-mpulse.net`、`akstat.io`。
- **伪域名 / 探针族整批跳过不计入待判**：`wpad`、`monitor_browser`、`*.dotnxdomain.net` / `*.dashnxdomain.net` / `*.starnxdomain.net`（NextDNS + DNSSEC `root-key-sentinel-*` 探针）。
- **广告/追踪类整批不落盘**：归 reject.yaml 上游且**禁止核对 reject.yaml**，故只记录不判断（Chrome 浏览一日可产出 40+ 个 ad-tech 主域）。
- 微信主域 `weixin.com` / `wechat.com` → `wechat.yaml`（非 tencent）。`spacelama.com` → tencent（用户直接指定）。
- 海外 → `proxy.yaml`；国内经 RDAP/NS 确认 → `direct.yaml`；`macked.site` 是 Mac 资源站→proxy。
- 中国移动系（10086.cn / chinamobile.com / cmcc-cs.cn / komect.com / miguvideo.com / 10085.cn / cmicapm.com 等）→ direct.yaml 中国移动组。WPS 系（wps.cn / wpscdn.cn / qwps.cn / ksosoft.com）→ direct.yaml。
- Agent 自用查询端点（rdap.org / verisign.com / crt.sh 等）→ direct.yaml「域名查询 / RDAP」组。
- 长期挂起待人工（无锚点）：`logitech.io`、`oceanengine.com`、`ntp.org.cn`、`yhgfb-cn-static.com`、`applogcdn.com`、`temu.com`、`photon.codes`、`mdoelscope.ai`（仿冒）。

## 文档 / README 改动约定（2026-10-17 用户裁决；分支制度当日当晚取消）
**2026-10-17 当晚用户裁决取消分支制度**：所有改动（含 README、scripts、AGENTS.md 等）一律**直接在 main 上修改、提交、推送**，本地只保留 main（`feature/workbuddy-add-log-domain` 已删）。**保留的核心约束**：动手前 `git fetch` + `git rev-list --left-right --count origin/main...HEAD` 双向 `0 0`，远程有新提交则 `git stash` → `git pull --rebase` → `git stash pop`；提交前再查一次；commit 后立即 push 并再校验 `0 0`。README 代码块用「生成（`/tmp/*.py`，CJK 双宽对齐）→ `yaml.safe_load` 校验 → 按板块标题 splice」流程，替换后补**引用一致性校验**（rules 引用的 provider/group、use 的订阅均已定义）。

## 环境坑
- 系统 `python3` 无 pyyaml → 用 `/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python`。
- `whois` 不可用、无 `timeout`。RDAP 走代理 `https_proxy=http://127.0.0.1:7893`，首调常空需重试 2-3 次。RDAP registrar 为空时看 NS 定归属（HICHINA/ALIDNS→国内）或 DoH 看 A 记录 IP 段。
- **git 代理 7893 状态来回翻转，每轮现场双探测**：`nc -z 127.0.0.1 7893` + `curl --noproxy '*' github.com`。禁用代理时 zsh 变量不做词分割，须 `gitx() { git -c http.proxy= -c https.proxy= "$@"; }`。
- heredoc 内联 python 被安全策略拦截 → Write 成 `/tmp/*.py` 再跑（`git commit -F -` 不受影响）。单条带内联脚本+参数的校验命令也可能被拦 → 写 `/tmp/yaml_check.py` 循环校验。

## 统计口径
- 全库统计必须剥离 `reject.yaml`（占 99.29%）。`find_duplicates.py` 已跳过它，报的是业务文件间重复，**基线 1 条**（`settings.crashlytics.com` direct/google），不要误报成新增。
- 解析规则行时 `IP-CIDR,...,no-resolve` 的 `no-resolve` 会被吞进 value，按逗号切第一段；空占位 `DOMAIN-SUFFIX,` 用允许空值的正则抓（`steam.yaml:3`）。
- **changelog 编写约束已落地 AGENTS.md（2026-10-17）**：提取须同时覆盖 `match Match using` 与 `(match Match/)` 两种行格式（10-07 曾因只取前者漏记 smallstrawberry.com）；payload 数写前用 `grep -cE '^[[:space:]]*-[[:space:]]*[^[:space:]]'` 实查；「归并主域后 N 个」要括号注明构成。

## 日志差集纪律
- **2026-10-17 起日志移动制（skill v2.3.0 用户裁决）**：源目录 `~/.config/clash.meta/logs/` 的日志 **`mv` 移入** `log/clashx-meta-log/`（先 `diff -rq` 只移「Only in 源目录」项——目标侧同名时 `mv` 会套娃塞进内部，必须避开）；本轮分析全部完成（push + 0 0）后已处理文件夹归档至同级 `log/.archive/`，未定案的留在原地。旧 cp 时代源目录残留的同名副本**不主动删**，清理由用户裁决。**注意：AGENTS.md「日志差集纪律」仍是旧 cp 口径，尚未同步，待用户裁决。**
- **changelog 有记录 ≠ 已处理完**：日志当天持续追加、跨日追加、重启新增 core 文件，须 diff 后重新提取，与 changelog 已处理主域集合对比定位增量。
- **增量可能落在「今日」目录而非「昨日」**，"默认昨日"不等于可忽略今日目录。带出的目录必须真正跑提取，不能只移入。
- 差集 ≠ 漏跑：早期运行未 cp 造成的历史缺口用 changelog 交叉核验定性（特征域名能找到落点即是复制缺口）。
- 提交信息里的数字先算准再写（2026-10-11 把 19 写成 13，已推送无法改）。

## 仓库状态
- PayPal 域名全在 `us-payment.yaml`，独立 `paypal.yaml` 已删（2026-10-11）。用户说「加到 X 文件」前必须先 grep 全库查重。
- 未修的已知问题：`proxy.yaml:784` 把 `USER-AGENT,WhatsApp*` 误写成分组注释头致 43 条归属错误；`direct.yaml` 44–179 行「腾讯云-香港」134 条实为杂项。
- `domain-distribution.html` 未被 gitignore（未跟踪未提交）。
