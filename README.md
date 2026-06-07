这是一个长期维护的自用域名 / IP 规则集（`rule-provider`）。

- 可直接在代理软件配置文件中引用本仓库的规则文件，也推荐通过 Issues 提出建议或反馈。
- 引用 URL（将 name 替换为实际的文件名）：

https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml

在 Clash 配置中使用 `rule-providers` 的示例：

```yaml
rule-providers:
	my-rules:         #my-rules可自定义
		type: http
		behavior: classical
		url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml
		path: ./my-rules.yaml
		interval: 86400
```