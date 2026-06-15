# clash-proxy 精准分流域名规则集

一套长期维护的域名规则集，可在 mihomo / Clash 系列代理软件中引用，实现代理的精准分流。

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

| 分类 | 文件 | 说明 |
|------|------|------|
| **通用** | `proxy.yaml` | 需代理的杂项域名 |
| | `direct.yaml` | 可直连的域名 |
| | `reject.yaml` | 广告/追踪/恶意软件拦截（自动同步，勿手动编辑） |
| **社交通讯** | `telegram.yaml` | Telegram |
| | `meta.yaml` | Facebook、Instagram、WhatsApp、Threads |
| | `x.yaml` | Twitter / X |
| | `line.yaml` | LINE |
| | `social.yaml` | Reddit、Discord、Pinterest 等 |
| **流媒体** | `youtube.yaml` | YouTube |
| | `streaming.yaml` | Netflix、Disney+、HBO 等 |
| | `spotify.yaml` | Spotify |
| | `pornhub.yaml` | Pornhub |
| **AI** | `direct-ai.yaml` | 可直连的 AI 服务 |
| | `proxy-ai.yaml` | 需代理的 AI 服务 |
| | `openai.yaml` | OpenAI（ChatGPT、API 等） |
| | `claude.yaml` | Claude / Anthropic |
| **开发者** | `github.yaml` | GitHub 及相关开发工具 |
| **系统服务** | `apple.yaml` | Apple 服务（App Store、iCloud 等） |
| | `microsoft.yaml` | Microsoft 服务（Office、Azure 等） |
| | `google.yaml` | Google 服务 |
| | `nvidia.yaml` | NVIDIA 服务 |
| **金融** | `crypto.yaml` | 加密货币交易所与钱包 |
| | `hk-broker.yaml` | 港美股券商（TradingView、长桥、IBKR 等） |
| | `us-broker.yaml` | 美股券商 |
| | `hk-bank.yaml` | 香港银行（汇丰、ZA、WeLab 等） |
| | `fin-media.yaml` | 财经媒体与数据 |
| **网络** | `dns.yaml` | DNS 服务器 |

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
  google:
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/google.yaml
    path: ./ruleset/google.yaml
    interval: 86400
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

## 更新机制

- 主要规则文件不定期手动更新
- `reject.yaml` 由 GitHub Actions 每日自动同步 [Loyalsoldier](https://github.com/Loyalsoldier) 上游规则

## 反馈

欢迎通过 [Issues](https://github.com/heximao/clash-proxy/issues) 提出建议或反馈。
