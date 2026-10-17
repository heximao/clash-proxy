# clash-proxy 精准分流域名规则集

clash-proxy是一套长期维护的域名规则集，可在 mihomo / Clash 系列代理软件中引用，实现代理的精准分流。

> 🌟 如果本项目对你有帮助，欢迎点 [Star](https://github.com/heximao/clash-proxy) 支持，也方便后续持续跟进更新。

## 使用建议

- **按需引用，不必大而全**：只需引用你个人常用、需要精准控制策略（代理）组的规则集即可，无需把本仓库所有规则全部引用。没有引用的域名不会"漏掉"——它们会自动落到 `MATCH` 兜底规则，由你为 `MATCH` 设置的策略（代理）组统一处理。这样配置更精简，也更容易维护。
- **示例**：你只想精准控制 `OpenAI` 的访问代理，那只就只引用 `openai.yaml`，为它单独分配一个策略（代理）组，再为 `MATCH` 设置一个兜底策略（代理）组即可。

## 支持软件

- OpenClash
- Clash for Android
- ClashX Meta
- Clash Verge
- Shadowrocket（小火箭）
- Stash
- Surge
- Potatso
- 其他同类型软件

> 在绕过中国大陆场景下，无需全局代理。只需在代理软件配置文件的 `rules` 末尾将 `MATCH` 规则指向一个专用的"漏网之鱼"策略组，并将该策略组分配至 PROXY 或 DIRECT；同时创建一个 PROXY 策略组，将本仓库的 `proxy` 规则集分配给它，即可实现对未命中规则域名的精准分流控制。

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
| **hk-broker.yaml** | 港美股券商（TradingView、长桥、IBKR 等），建议使用香港节点 |
| **line.yaml** | LINE |
| **meta.yaml** | Facebook、Instagram、WhatsApp、Threads |
| **microsoft.yaml** | Microsoft 服务（Office、Azure 等） |
| **netease-music.yaml** | 网易云音乐 |
| **nvidia.yaml** | NVIDIA 服务 |
| **openai.yaml** | OpenAI（ChatGPT、API 等） |
| **pornhub.yaml** | Pornhub |
| **proxy-ai.yaml** | 需代理的 AI 服务 |
| **proxy.yaml** | 需代理的杂项域名 |
| **reject.yaml** | 广告/追踪/恶意软件拦截（推荐设置reject） |
| **social.yaml** | Reddit、Discord、Pinterest 等 |
| **spotify.yaml** | Spotify |
| **steam.yaml** | Steam 游戏平台（待补充） |
| **streaming.yaml** | Netflix、Disney+、HBO 等 |
| **telegram.yaml** | Telegram |
| **tencent-global.yaml** | 腾讯海外服务 |
| **tencent.yaml** | 腾讯 / 微信 |
| **us-bank.yaml** | 美国银行（待补充） |
| **us-broker.yaml** | 美股券商，建议优先直连 |
| **us-payment.yaml** | 美国支付（PayPal、Wise 等） |
| **wechat.yaml** | 微信（国内域名，可直连） |
| **x.yaml** | Twitter / X |
| **xhs.yaml** | 小红书 / RedNote |
| **youtube.yaml** | YouTube |

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

### 第一步：先看懂 4 个概念（小白必读，约 1 分钟）

代理软件的配置文件由 4 类内容组成。看懂它们，下面的示例就是"填空题"：

| 配置块 | 它是什么 | 大白话 |
|--------|---------|--------|
| `proxy-providers` | 订阅集合 | 你从"机场"买来的节点列表，软件会定时自动更新 |
| `proxy-groups` | 策略组 | 流量的"出口选择器"：命中规则的流量，走这里选定的节点 |
| `rule-providers` | 规则集 | 一份域名清单（本仓库的 `.yaml` 就是规则集）：规定哪些域名归哪个策略组管 |
| `rules` | 规则 | 分拣表：从上往下依次比对，**命中即停**；都没命中就走最后的 `MATCH` 兜底 |

四者的分工：`rule-providers` 提供"清单"，`rules` 按清单分拣流量，`proxy-groups` 决定流量从哪个出口出去，`proxy-providers` 提供出口（节点）本身。

### 第二步：复制最精简配置

适用于 **OpenClash、ClashX Meta、Clash Verge、Clash for Android、Stash** 等 mihomo / Clash 系软件；Surge、Shadowrocket 语法不同，请使用各自软件内置的规则集功能。

下面是一份最精简的完整配置：引用本仓库的 `google.yaml`，让 Google 走代理、中国流量直连、其余兜底。**必须修改的只有一处——订阅链接**（标 ★ 那行）；其他名字不喜欢可以随便改，不改也能直接用。更多玩法请查阅 mihomo 官方文档。

```yaml
proxy-providers:                                                       # 订阅集合块：放你的机场节点列表
  airport:                                                             # 给订阅起个名字（后面会引用，可改）
    type: http                                                         # 订阅类型：通过网址获取
    url: https://你的机场订阅链接                                      # ★ 全篇唯一必改：换成你自己的订阅链接
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

### 第三步：常见问题

**Q1：这段配置粘到哪里？**

- Clash Verge / ClashX Meta / Stash：打开你正在使用的配置文件（通常叫 `config.yaml`），把上面内容合并进去。若文件里已有 `proxy-providers`、`rules` 等同名段落，只把条目添进去，**不要出现两个 `rules:`**。
- OpenClash：进入「配置文件」管理页 → 编辑正在使用的配置 → 粘贴保存 → 应用配置。
- Clash for Android：在「配置」页编辑当前配置，粘贴合并后保存并应用。

**Q2：没有"机场"和订阅链接，能用吗？**

不能。"机场"是代理服务商的俗称，需自行购买，对方会提供一个订阅链接。本仓库只提供域名分类规则，不提供节点。

**Q3：想让 YouTube、OpenAI 也走代理？**

在 `rule-providers` 里照抄一段、改个名字和链接，再在 `rules` 里加一行 `RULE-SET,名字,策略组名`：

```yaml
rule-providers:
  google:                                                              # 原有示例（不用动）
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml
    path: ./rule_provider/google.yaml
    interval: 86400
  openai:                                                              # 新增：照抄一段，改个名字和链接
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/openai.yaml
    path: ./rule_provider/openai.yaml
    interval: 86400
rules:
  - RULE-SET,google,Google
  - RULE-SET,openai,Google                                             # 新增一行：OpenAI 域名也走 Google 策略组
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

**Q4：提示"规则集下载失败 / 加载失败"？**

先确认当前网络能打开 `https://cdn.jsdelivr.net`（浏览器直接访问测试）；打不开时临时开启全局代理，更新一次配置后再关。规则每 24 小时自动更新（`interval: 86400`），也可在软件里手动"更新配置"立即刷新。

**Q5：按示例配好了，Google 还是打不开？**

按顺序排查：① 在策略组里换一个节点；② 确认订阅链接没填错、节点列表已更新；③ 确认配置已保存并"应用"（部分软件需重新加载配置才生效）。

## 反馈

欢迎通过 [Issues](https://github.com/heximao/clash-proxy/issues) 提出建议或反馈。