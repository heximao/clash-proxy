# clash-proxy 为代理软件实现精准分流的互联网域名规则集

clash-proxy 的域名来自真实的网络访问请求，按厂商与服务分类整理，可在 mihomo / Clash 系列代理软件中引用，实现网络请求的精准分流控制。

## 支持软件或插件

- OpenClash
- Clash for Android
- ClashX Meta
- Clash Verge
- Shadowrocket（小火箭）
- Stash
- Surge
- Potatso
- 其他同类型软件或插件

> 🌟 本项目长期更新，域名基于真实的网络访问请求，不断更新补充，推荐直接引用，无需 Fork 单独维护，对你有帮助，欢迎点 [Star](https://github.com/heximao/clash-proxy) 支持，如果需要为某个规则补充域名，请提[Issues](https://github.com/heximao/clash-proxy/issues) 。

## 规则文件

| 文件 | 说明 |
|------|------|
| **alibaba-global.yaml** | 阿里巴巴海外服务（ModelScope 国际版等） |
| **alibaba.yaml** | 阿里巴巴 / 阿里系服务（淘宝、天猫、高德、ModelScope 等） |
| **apple.yaml** | Apple 服务（App Store、iCloud 等） |
| **baidu.yaml** | 百度 |
| **bilibili.yaml** | 哔哩哔哩（B 站、B23、BiliBili 国际版等） |
| **bytedance-global.yaml** | 字节跳动海外服务（Trae 国际版、TikTok 等） |
| **bytedance.yaml** | 字节跳动（抖音、飞书、豆包、火山引擎、Trae CN 等） |
| **claude.yaml** | Claude / Anthropic |
| **crypto.yaml** | 加密货币交易所与钱包 |
| **direct-ai.yaml** | 可直连的 AI 服务 |
| **direct.yaml** | 可直连的域名 |
| **dns.yaml** | DNS 服务器 |
| **fin-media.yaml** | 财经媒体与数据 |
| **fin-tech.yaml** | 金融科技工具 |
| **firefox.yaml** | Firefox / Mozilla |
| **github.yaml** | GitHub 及相关开发工具 |
| **google.yaml** | Google 服务 |
| **hk-bank.yaml** | 香港银行（汇丰、ZA、WeLab 等） |
| **hk-broker.yaml** | 港股券商，建议使用代理 |
| **line.yaml** | LINE |
| **meta.yaml** | Facebook、Instagram、WhatsApp、Threads |
| **microsoft.yaml** | Microsoft 服务（Office、Azure 等） |
| **netease-music.yaml** | 网易云音乐 |
| **nvidia.yaml** | NVIDIA 服务 |
| **openai.yaml** | OpenAI（ChatGPT、API 等） |
| **pornhub.yaml** | Pornhub |
| **proxy-ai.yaml** | 需代理的 AI 服务 |
| **proxy.yaml** | 需代理的杂项域名 |
| **reject.yaml** | 广告/追踪/恶意软件拦截（推荐设置 reject） |
| **social.yaml** | Reddit、Discord、Pinterest 等 |
| **spotify.yaml** | Spotify |
| **steam.yaml** | Steam 游戏平台（待补充） |
| **streaming.yaml** | Netflix、Disney+、HBO 等 |
| **telegram.yaml** | Telegram |
| **tencent-global.yaml** | 腾讯海外服务 |
| **tencent.yaml** | 腾讯（QQ、腾讯云等） |
| **us-bank.yaml** | 美国银行，建议优先直连 |
| **us-broker.yaml** | 美股券商，建议优先直连 |
| **us-payment.yaml** | 美国支付（PayPal、Wise 等） |
| **wechat.yaml** | 微信（国内域名，可直连） |
| **x.yaml** | Twitter / X |
| **xhs.yaml** | 小红书 / RedNote |
| **youtube.yaml** | YouTube |

## 使用建议

- **按需引用，不必大而全**：只需引用你个人常用、需要精准控制策略（代理）组的规则集即可，无需把本仓库所有规则全部引用。访问没有引用的域名时，请求会自动落到 `MATCH` 兜底规则，由你为 `MATCH` 设置的策略（代理）组统一处理。这样配置更精简，也更容易维护。
- **示例**：如果你只想精准控制 `OpenAI` 的访问代理，那只就只引用 `openai.yaml`，为它单独分配一个策略（代理）组，再为 `MATCH` 设置一个兜底策略（代理）组即可。

## 引用方式

CDN URL 模式，将 `<name>` 替换为实际文件名：

```
https://cdn.jsdelivr.net/gh/heximao/clash-proxy/<name>.yaml
```

例如引用 Google 规则：

```
https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml
```

## 配置示例

打开你正在使用的代理软件配置文件（通常叫 `config.yaml`），除了 `dns` 等块外，还包含以下 4 类内容：

| 配置块 | 它是什么 | 说明 |
|--------|---------|--------|
| `proxy-providers` | 订阅集合 | 你从"机场"买来的节点列表，软件会定时自动更新 |
| `proxy-groups` | 策略组 | 流量的"出口选择器"：命中规则的流量，走这里选定的节点 |
| `rule-providers` | 规则集 | 一份域名清单（本仓库的 `.yaml` 就是规则集）：规定哪些域名归哪个策略组管 |
| `rules` | 规则 | 分拣表：从上往下依次比对，**命中即停**；都没命中就走最后的 `MATCH` 兜底 |

四者的分工：`rule-providers` 提供"清单"，`rules` 按清单分拣流量，`proxy-groups` 决定流量从哪个出口出去，`proxy-providers` 提供出口（节点）本身。


下面是一份最精简的配置：引用本仓库的 `google.yaml`，让 Google 走「Google」策略组代理访问，中国流量直连，其余兜底。进阶玩法请查阅 mihomo 官方文档。

```yaml
proxy-providers:                                                       # 订阅集合块：放你的机场节点列表
  airport:                                                             # 给订阅起个名字（后面会引用，可改）
    type: http                                                         # 订阅类型：通过网址获取
    url: https://你的机场订阅链接                                        # ★ 全篇唯一必改：换成你自己的订阅链接
    path: ./proxy_provider/airport.yaml                                # 节点列表下载后保存在本地哪个文件
    interval: 3600                                                     # 更新间隔：3600 秒 = 1 小时
    health-check:                                                      # 健康检查：自动测出节点是否还能用
      enable: true                                                     # 开关：打开
      url: http://www.gstatic.com/generate_204                         # 测试地址：能打开就说明网络通
      interval: 300                                                    # 每 300 秒（5 分钟）检测一次
proxy-groups:                                                          # 策略组块：决定流量从哪个出口走
  - name: Google                                                       # 策略组名字（可改，如「谷歌」「出国」）
    type: select                                                       # select = 在下面的节点里手动挑一个
    proxies:                                                           # 固定可选节点：
    - DIRECT                                                           # DIRECT = 直连，不走代理
    - PROXY                                                            # PROXY = 用订阅里的默认节点
    use:                                                               # 再把订阅里的全部节点加进来：
    - airport                                                          # 引用上面名为 airport 的订阅
rule-providers:                                                        # 规则集块：本仓库提供的域名清单
  google:                                                              # 规则集名字（可改）
    type: http                                                         # 类型：通过网址获取
    behavior: classical                                                # classical = 标准域名规则，照抄即可
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml   # 本仓库 google.yaml 的地址
    path: ./rule_provider/google.yaml                                  # 规则文件下载后保存在本地哪个文件
    interval: 86400                                                    # 更新间隔：86400 秒 = 24 小时
rules:                                                                 # 规则块：从上往下依次匹配，命中即停
  - RULE-SET,google,Google                                             # Google 域名 → 走 Google 策略组
  - GEOIP,CN,DIRECT                                                    # 中国 IP → 直连
  - MATCH,PROXY                                                        # 兜底：以上都没命中 → 走 PROXY
```

网络请求是怎么被分流的：

#### 例 1：访问 google.com

1. 浏览器输入 `google.com`，请求首先交给代理软件；
2. 软件拿这个域名先去比对 `google.yaml` 规则集——**命中**，google.com 就在清单里；
3. 流量转交「Google」策略组，走你在组里选中的那个机场节点；
4. 机场节点替你去访问 google.com，再把结果传回来。谷歌服务器只看到节点的 IP，看不到你的真实 IP。

#### 例 2：访问 baidu.com

1. 浏览器输入 `baidu.com`，请求交给代理软件；
2. 软件拿这个域名先去比对 google 规则集——没命中（百度不在 Google 清单里），继续往下；
3. 软件接着拿域名比到 `GEOIP,CN`：软件把 baidu.com 解析成 IP 地址，发现这个 IP 属于中国大陆；
4. 流量走 DIRECT——不经过代理，直接连百度的服务器。百度服务器看到的是你本地的真实 IP，请求不经过代理，不消耗代理流量。

#### 例 3：访问 facebook.com

1. 浏览器输入 `facebook.com`，请求交给代理软件；
2. 软件拿这个域名先去比对 google 规则集——没命中；
3. 软件接着拿域名比到 `GEOIP,CN`：软件把 facebook.com 解析成 IP 地址，发现这个 IP 不属于中国大陆，没命中；
4. 一路落到最后的 `MATCH,PROXY`——这是兜底规则，前面所有规则都没中的流量都归它管；流量走 PROXY（默认代理节点），正常打开 Facebook。

> 注意例 3：facebook.com 并没有自己的规则，走的是兜底。这份最精简配置只引用了 `google.yaml`，除 Google 外的海外网站一律落入 `MATCH,PROXY`。想给 Facebook（或 YouTube、OpenAI）单独指定策略，需要在 `rule-providers` 中增加对应规则集，再在 `rules` 中加一行 `RULE-SET,名字,策略组名`。

## 常见问题

**Q1：没有"机场"和订阅链接，能用吗？**

不能。"机场"是代理服务商的俗称，需自行解决，对方会提供一个订阅链接。本仓库只提供域名分类规则，不提供节点。

**Q2：代理软件提示"规则集下载失败 / 加载失败"？**

先确认当前网络能打开 `https://cdn.jsdelivr.net`（浏览器直接访问测试）；打不开时临时开启全局代理，更新一次配置后再关。规则每 24 小时自动更新（`interval: 86400`），也可在软件里手动"更新配置"立即刷新。

**Q3：按示例配好了，Google 还是打不开？**

按顺序排查：① 在策略组里换一个节点；② 确认订阅链接没填错、节点列表已更新；③ 确认配置已保存并"应用"（部分软件需重新加载配置才生效）。

如果你是小白，懒得折腾上述的配置文件（`config.yaml`），本项目提供付费代写个性化定制的配置文件（`config.yaml`），如有需要，请在 [Issues](https://github.com/heximao/clash-proxy/issues) 联系。（本项目不提供代理节点、机场订阅）

## 反馈

欢迎通过 [Issues](https://github.com/heximao/clash-proxy/issues) 提出建议或反馈。

## 关键词

Clash 规则集、Clash 规则、Clash 分流规则、mihomo 规则集、OpenClash 规则、ClashX Meta 规则、Clash Verge 规则、Clash for Android 规则、Stash 规则、Shadowrocket 规则、Surge 规则、域名规则集、rule-provider、RULE-SET、规则订阅、精准分流、智能分流、代理规则推荐、广告过滤规则、去广告域名、追踪域名拦截、Google 规则、ChatGPT 规则、OpenAI 规则、YouTube 规则、Telegram 规则、TikTok 规则、Netflix 规则、GitHub 规则、港美股券商规则、香港银行规则、美国银行规则、clash rules、mihomo rules、clash rule provider、openclash ruleset

## 项目速览

**clash-proxy** 是一个长期维护的 Clash / mihomo 域名规则集：将真实网络访问中遇到的域名按厂商与服务分类，整理为 40 余个 yaml 规则文件，通过 jsDelivr CDN 分发（`https://cdn.jsdelivr.net/gh/heimao/clash-proxy/<name>.yaml`），供 OpenClash、ClashX Meta、Clash Verge、Clash for Android、Stash 等代理软件以 `rule-providers` 订阅方式引用，实现指定域名走指定策略的精准分流。

核心事实：

- **数据来源真实**：域名来自代理软件运行日志中未命中任何规则的请求，经归属判定后归类补录，而非凭空罗列；
- **规则形态**：全部为域名级规则（以 `DOMAIN-SUFFIX` 为主），在 `rules` 中以 `RULE-SET,名字,策略组` 引用，自上而下、命中即停；
- **兜底不漏**：未引用的规则集不会导致域名"漏掉"，未命中流量自动落入 `MATCH`，由用户自行指定兜底策略；
- **更新机制**：客户端按 `interval` 定时拉取规则文件（示例配置为 86400 秒即 24 小时）；`reject.yaml` 广告/追踪拦截列表由 GitHub Actions 每日自动合并上游更新；
- **边界**：本项目仅提供域名分类规则，不提供代理节点与机场订阅。

适用人群：不希望全局代理，需要让 Google、YouTube、OpenAI 等海外服务走代理，同时让国内网站及银行、券商等站点按需直连或代理的 Clash / mihomo 用户。
