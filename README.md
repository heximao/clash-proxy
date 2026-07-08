# clash-proxy 精准分流域名规则集

一套长期维护的域名规则集，可在 mihomo / Clash 系列代理软件中引用，实现代理的精准分流。

## 使用建议

- **按需引用**：推荐引用个人常用的规则即可，例如需要精准控制访问`OpenAI`时使用的代理，只引用`openai.yaml`即可，其余规则集不引用，为`openai`分配策略（代理）组之后，再为`Match`设置一个兜底策略（代理）组即可。

## 支持软件

- OpenClash
- Clash for Android
- ClashX Meta
- Clash Verge
- Shadowrocket（小火箭）
- Stash
- Surge
- Potatso

> 在绕过中国大陆场景下，无需全局代理。只需在代理软件配置文件的 `rules` 末尾将 `MATCH` 规则指向一个专用的"漏网之鱼"策略组，并将该策略组分配至 PROXY 或 DIRECT；同时创建一个 PROXY 策略组，将本仓库的 `proxy` 规则集分配给它，即可实现对未命中规则域名的精准分流控制。

## 规则文件

| 文件 | 说明 |
|------|------|
| **apple.yaml** | Apple 服务（App Store、iCloud 等） |
| **bilibili.yaml** | 哔哩哔哩（B 站、B23、BiliBili 国际版等） |
| **claude.yaml** | Claude / Anthropic |
| **crypto.yaml** | 加密货币交易所与钱包 |
| **direct-ai.yaml** | 可直连的 AI 服务 |
| **direct.yaml** | 可直连的域名 |
| **dns.yaml** | DNS 服务器 |
| **fin-media.yaml** | 财经媒体与数据 |
| **fin-tech.yaml** | 金融科技工具 |
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
| **reject.yaml** | 广告/追踪/恶意软件拦截（自动同步，勿手动编辑） |
| **social.yaml** | Reddit、Discord、Pinterest 等 |
| **spotify.yaml** | Spotify |
| **streaming.yaml** | Netflix、Disney+、HBO 等 |
| **telegram.yaml** | Telegram |
| **us-bank.yaml** | 美国银行 |
| **us-broker.yaml** | 美股券商，建议优先直连 |
| **us-payment.yaml** | 美国支付（PayPal、Wise 等） |
| **wechat.yaml** | 微信（国内域名，可直连） |
| **x.yaml** | Twitter / X |
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

### OpenClash

```yaml
rule-providers:
  google:                                                                      # 规则集名称，可自定义
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml
    path: ./rule_provider/google.yaml                                          # 规则集文件存放目录，Openclash安装在OpenWRT的完整默认目录是/etc/openclash/rule_provider 
    interval: 86400                                                            # 自动更新时间，单位秒，86400 = 24 小时
```

### Clash Verge

```yaml
rule-providers:
  google:
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml
    path: ./ruleset/google.yaml
    interval: 86400
```



## 反馈

欢迎通过 [Issues](https://github.com/heximao/clash-proxy/issues) 提出建议或反馈。