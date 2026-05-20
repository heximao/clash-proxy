# Clash 规则提供者仓库

本仓库包含通过 jsDelivr 提供的 Clash `rule-provider` YAML 文件。

## 🛠 Developer Workflow

- **No Build/Test**: 本仓库没有自动化测试或构建步骤。
- **Verification**: 提交前请确保 YAML 有效。使用 `DOMAIN-SUFFIX`（连字符），而非 `DOMAIN_SUFFIX`（下划线）。
- **Deployment**: 文件通过文件名引用，格式为 `https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml`。

## 📁 File Structure & Conventions

- **File Format**: 每个 `.yaml` 文件必须以 `payload:` 作为根键开始。
- **Naming**: 新文件请使用 `CapitalCase.yaml`（例如 `SocialMedia.yaml`）。
- **Deprecation**: 退役文件请改名加上 `弃用`（例如 `ServiceName弃用.yaml`），而不是立即删除。
- **Rule Types**:
  - `DOMAIN-SUFFIX,example.com`（大多数网站首选）
  - `DOMAIN-KEYWORD,keyword`
  - `IP-CIDR,1.1.1.1/32,no-resolve`
  - `PROCESS-NAME,BinaryName`（谨慎使用，主要针对桌面应用）

## ✍️ Coding Style

- **Grouping**: 使用注释按服务/类别分组规则：
  ```yaml
  # === Service Name ===
  - DOMAIN-SUFFIX,example.com
  ```
- **Ordering**: 将相关规则放在一起。虽然不强制按字母顺序，但优先考虑可读性。
- **Exceptions**: `Proxy.yaml` 和 `Direct.yaml` 是用于杂项规则的 catch-all 文件。大型特定服务（Apple、Google、Microsoft）有各自的文件。

## 使用示例（Clash 配置）

在 Clash 的主配置中使用 `rule-providers` 引用本仓库的规则：

```yaml
rule-providers:
  example-rules:
    type: http
    behavior: classical
    url: https://cdn.jsdelivr.net/gh/heximao/clash-proxy/SocialMedia.yaml
    path: ./SocialMedia.yaml
    interval: 86400
```

## 验证与调试

- 确保每个 `.yaml` 文件以 `payload:` 作为根键。
- 使用 `yamllint` 或 `yamllint <file>` 检查格式（如已安装）。
- 用 Python 快速检测语法错误：

```bash
python -c "import sys,yaml; yaml.safe_load(sys.stdin)" < SocialMedia.yaml
```

## 贡献指南

- 先 fork 本仓库并在个人仓库中修改或新增文件。
- 提交前务必校验 YAML 格式与 `payload:` 根键。
- 提交 PR 时请在 PR 描述中说明变更来源与验证方法。

> 注意：对仓库内容的讨论/改进请优先使用 PR；维护者不希望直接通过 Issues 提交规则。 
