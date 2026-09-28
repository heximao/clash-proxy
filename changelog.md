# 更新记录

## 2026-09-29 find_duplicates.py 退出码反映重复检查结果

- 脚本原先无论是否存在重复都以退出码 0 结束，无法在 shell / CI 中作为门禁；现改为：**无重复退出 0，存在跨文件或文件内重复退出 1**（两种情况下报告均照常生成）。
- 终端新增重复数量汇总输出（跨文件重复规则数、文件内重复条目数）。
- 同步更新 `scripts/README.md` 与本地 `AGENTS.md` 的自检闭环说明。

## 2026-09-29 scripts/duplicates.json 取消版本跟踪并加入 .gitignore

- `find_duplicates.py` 生成的 `scripts/duplicates.json` 体积约 17MB 且为可随时再生成的本地产物，改用 `git rm --cached` 取消跟踪（本地文件保留），并在 `.gitignore` 中忽略。
- `scripts/DUPLICATES.md` 仍保留版本跟踪；同步更新 `scripts/README.md` 说明。

## 2026-09-29 scripts 目录补充 README，重复报告输出路径移至 scripts/

- 新增 `scripts/README.md`：说明 `find_duplicates.py`、`merge_reject_from_loyalsoldier.py`、`normalize_yaml_comments.py` 三个脚本的用途、用法、输出产物、运行目录要求及与每日 GitHub Actions 的关系。
- `find_duplicates.py` 生成的 `DUPLICATES.md`、`duplicates.json` 由仓库根目录改为输出到脚本所在的 `scripts/` 目录（`Path(__file__).parent`），扫描范围仍为仓库根目录。
- 已通过 `git mv` 将现有两份报告迁移至 `scripts/`，保留重命名历史。

## 2026-09-29 漏网之鱼日志归类（log/ 子目录 clashx 日志全量提取）

数据来源：`log/` 下 19 个子目录中的 clashx_*.log 与 clashx_mihomo.log，提取落入兜底 `match Match`（漏网之鱼）规则的目标，去重后共 **183 个**（域名 169 + 裸 IP 14）。经 whois 归属查询与进程上下文核对后分类如下：

### tencent-global.yaml（腾讯海外 AI）
- `workbuddy.ai`（www.workbuddy.ai 884 次，WorkBuddy AI 主站）
- `codebuddy.ai`（www / download，CodeBuddy 国际版）

### apple.yaml
- `IP-CIDR,17.57.145.0/24`（apsd 推送）
- `IP-CIDR,17.253.0.0/16`（timed NTP 时间同步）

### google.yaml
- `google.co.jp`（www / accounts，DOMAIN-SUFFIX,google.com 不覆盖日本 ccTLD）
- `a.run.app`（Cloud Run，同时覆盖原 antigravity 更新器子域）

### microsoft.yaml
- `playwright.dev`（cdn.playwright.dev）

### firefox.yaml
- `mozilla-backup.org`（aus5 / firefox-settings / content-signature / versioncheck 等）
- `firefox-portal-detection.com`（captive portal 探测）

### meta.yaml
- `facebook.net`（connect.facebook.net）

### crypto.yaml
- `hyperliquid.xyz`（app / api-ui）
- `coingecko.com`、`coinyep.com`（行情数据）
- `web3modal.org`、`privy.io`、`magic.link`（Web3 钱包/认证）

### proxy-ai.yaml
- `newapi.ai`、`newapi.pro`（NewAPI 网关文档）
- `parallel.ai`（search）、`cua.ai`、`keenable.ai`、`flova.ai`、`lobehub.com`、`manus.space`、`agentlane.com`、`ccswitch.io`、`skills.sh`、`skill-history.com`、`browse.sh`

### github.yaml
- `star-history.com`（api）

### fin-media.yaml
- `sec.gov`（美国证监会）
- `tradingcode.net`、`trading-strategies.academy`（交易学习）
- `biggo.com`（finance.biggo.com 比价）

### bytedance.yaml
- `visactor.io`（字节开源可视化）

### hk-broker.yaml
- `wbrks.com`（长桥 CDN，Longbridge Pro SG Helper 进程确认；与已有 wbkrs.com/lbkrs.com 同族）
- `usmartglobal.com`（hk.usmartglobal.com，uSMART）

### us-broker.yaml
- `ibkr.com`（t.ibkr.com，盈透）

### streaming.yaml
- `live-video.net`、`twitchcdn.net`、`pscp.tv`（Twitch 视频分发）

### proxy.yaml
- 证书验证：`lencr.org`（Let's Encrypt OCSP，ye/ye1/ye2/x1/x2）、`crt.sectigo.com`、`ocsp.comodoca4.com`（trustd 系统证书校验；本机直连测试受 TUN 干扰无法确认可直连，先按代理处理）
- 开发者工具：`pythonhosted.org`（PyPI 文件）、`astral.sh`（uv）、`open-vsx.org`（CodeBuddy CN 扩展仓库）、`rgpub.io`
- 文档/状态页平台：`gitbook.io`、`statuspage.io`
- AWS：`awswaf.com`、`on.aws`
- 网站功能组件：`easychat.co`、`omnichat.ai`、`smartlook.cloud`（smartlook.com 已在 reject）、`cdn-ukwest/privacyportal-uk.onetrust.com`、`cdn.cookielaw.org`、`cmp.osano.com`、`cdp.customer.io`、`blacklist.tampermonkey.net`（均为精确 DOMAIN，避免遮蔽 reject 中的追踪子域）
- Docker：`prodregistryv2.org`（registry 别名）
- Riot：`lolesports.com`
- 杂项站点：`manyvids.com`（成人）、`numuki.com`（游戏）、`printfriendly.com`、`split-tool.com`、`xiaowan.hk`、`cdnfonts.com`、`bootstrapcdn.com`、`sublimetext.com`、`sublimehq.com`、`gfis.info`、`aisecmatrix.org`、`api.sunbreak.com`、`cvs.prohost.org`

### direct.yaml
- `60s-api.viki.moe`（docs，实测直连 200）
- `cdn.ripperhe.com`（Bob 翻译作者 CDN）
- `IP-CIDR,192.0.32.59/32`（whois.iana.org，本机 whois 命令）

### reject.yaml（手动补录段，未改动上游条目）
- `hibchr.com`、`antpeak.com`、`zorvian.com`、`premzon.com`（NameCheap+Cloudflare 无主体、Chrome 后台加载的疑似追踪域名，如误杀可从该段删除）

### 跳过项（日志时间早于规则更新，现已被 reject.yaml 覆盖）
`etahub.com`、`analytics.tiktok.com`、`analytics-ipv6.tiktokw.us`、`appier.net`、`go-mpulse.net`、`akstat.io`、`siteintercept.qualtrics.com`、`sdk-api-v1.singular.net`、`browser-intake-datadoghq.com`、`cloudflareinsights.com`、`cdn.debugbear.com`、`a.tampermonkey.net`、`smartlook.com`、`beyondwickedmapping.org`、`featureassets.org`、`ingesteer.services-prod.nsvcs.net`、`gssprt.jp`、`player.stats.live-video.net`

### 未处理裸 IP（任播/云厂商 IP，加 /32 属过拟合，暂不处理）
Fastly（151.101.0/64/128/192.223）、Cloudflare（104.21.17.214、172.67.178.84）、AWS（35.84.53.85、44.233.186.238、52.37.99.5、54.151.0.246）、阿里云（47.243.118.180）、腾讯云（43.160.158.125）、192.34.234.30、203.119.87.74

验证：16 个文件 `yaml.safe_load` 全部通过；`find_duplicates.py` 无新增跨文件重复；覆盖率审计 169/169 域名已覆盖。
