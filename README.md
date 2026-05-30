这是一个长期维护的自用域名 / IP 规则集（`rule-provider`）。

- 优先通过 fork + PR 的方式同步更新，请勿直接提交 Issues。
- 可 fork 到自己的仓库后引用，或直接在配置中引用本仓库的文件。

引用 URL（将 name 替换为实际的文件名）：

https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml

在 Clash 配置中使用 `rule-providers` 的示例：

```yaml
rule-providers:
	my-rules:
		type: http
		behavior: classical
		url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml
		path: ./my-rules.yaml
		interval: 86400
```

注意：每个 `.yaml` 文件应以 `payload:` 作为根键开始（见仓库中各文件）。

快速校验建议：

- 使用 `yamllint` 或 `yamllint <file>` 进行格式检查（如已安装）。
- 使用 Python 快速解析检测语法错误：

```bash
python -c "import sys,yaml; yaml.safe_load(sys.stdin)" < name.yaml
```

如需帮助或改进建议，请 fork 并提交 PR，维护者会合并或给予反馈。
