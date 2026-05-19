# Clash Rule-Provider Repository

Repository containing Clash `rule-provider` YAML files served via jsDelivr.

## 🛠 Developer Workflow

- **No Build/Test**: There are no automated tests or build steps.
- **Verification**: Ensure YAML is valid before committing. Use `DOMAIN-SUFFIX` (hyphen), not `DOMAIN_SUFFIX` (underscore).
- **Deployment**: Files are referenced by filename via `https://cdn.jsdelivr.net/gh/heximao/clash-proxy/name.yaml`.

## 📁 File Structure & Conventions

- **File Format**: Every `.yaml` file must start with `payload:` as the root key.
- **Naming**: Use `CapitalCase.yaml` for new files (e.g., `SocialMedia.yaml`).
- **Deprecation**: Rename files to include `弃用` (e.g., `ServiceName弃用.yaml`) instead of deleting them immediately.
- **Rule Types**:
  - `DOMAIN-SUFFIX,example.com` (Preferred for most sites)
  - `DOMAIN-KEYWORD,keyword`
  - `IP-CIDR,1.1.1.1/32,no-resolve`
  - `PROCESS-NAME,BinaryName` (Use sparingly, primarily for desktop apps)

## ✍️ Coding Style

- **Grouping**: Group rules by service/category using comments:
  ```yaml
  # === Service Name ===
  - DOMAIN-SUFFIX,example.com
  ```
- **Ordering**: Keep related rules together. No strict alphabetical ordering is enforced, but readability is preferred.
- **Exceptions**: `Proxy.yaml` and `Direct.yaml` are catch-all files for miscellaneous rules. Large specific services (Apple, Google, Microsoft) have their own files.
