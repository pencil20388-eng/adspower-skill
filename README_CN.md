[README_CN.md](https://github.com/user-attachments/files/28037305/README_CN.md)
# 🌐 AdsPower Skill — 让 Claude Code 管理你的指纹浏览器

[English](./README.md) | **中文**

一个 [Claude Code 技能](https://code.claude.com/docs/en/skills)，让 Claude 通过自然语言操控 [AdsPower](https://www.adspower.net/) 指纹浏览器。

> "帮我批量创建 50 个浏览器配置文件" → 搞定。
> "把这个 CSV 里的代理绑到所有配置文件上" → 搞定。
> "打开每个配置文件，访问谷歌，截个图，关掉" → 搞定。

兼容 **Claude Code**、**Codex CLI**、**Cursor**、**Gemini CLI** 等支持 SKILL.md 标准的 AI 编程工具。

## 能做什么

| 你说 | Claude 做 |
|---|---|
| "创建 20 个配置文件" | 调用 AdsPower API 批量创建，自动随机指纹 |
| "从这个 CSV 绑定代理" | 读取代理列表，逐个更新配置文件 |
| "打开配置文件 X 检查指纹" | 打开浏览器，连接 Selenium/Playwright，访问 BrowserScan |
| "导出我活动组的 cookie" | 查询组内所有配置文件，导出 cookie 数据 |
| "我有哪些配置文件" | 列出所有配置文件的 ID、名称、分组、代理状态 |

## 安装

### Claude Code

```bash
# 在你的项目目录下
mkdir -p .claude/skills
git clone https://github.com/pencil20388-eng/adspower-skill.git .claude/skills/adspower
```

### 其他 AI 编程工具

把 `adspower/` 文件夹复制到你的工具读取 skills 的目录。

## 前置条件

- 已安装 [AdsPower](https://www.adspower.net/download) 并运行（需付费版，有 API 权限）
- 已生成 API Key（AdsPower → 自动化 → API → 生成）
- Python 3.8+，已安装 `requests` 包

## 使用方式

安装好之后，直接用自然语言跟 Claude 说就行：

```
> 在 "美国活动" 分组里创建 30 个浏览器配置文件，代理从 proxies.csv 里读

> 打开配置文件 h1abc123，访问 amazon.com，等 10 秒，截图，然后关掉

> 显示所有没有配置代理的配置文件

> 导出 "欧洲账号" 分组里所有配置文件的 cookie
```

Claude 会自动调用 AdsPower Local API 来执行这些操作。

## 覆盖的 API 端点

| 端点 | 功能 |
|---|---|
| `GET /api/v1/status` | 检查 API 是否运行 |
| `GET /api/v1/browser/start` | 打开浏览器配置文件 |
| `GET /api/v1/browser/stop` | 关闭浏览器配置文件 |
| `POST /api/v1/user/create` | 创建新配置文件 |
| `POST /api/v1/user/update` | 更新配置文件（代理、指纹等） |
| `GET /api/v1/user/list` | 查询配置文件列表 |
| `POST /api/v1/group/create` | 创建分组 |

## 更多资源

- 📦 [AdsPower 自动化脚本合集](https://github.com/pencil20388-eng/awesome-adspower-automation) — 开箱即用的脚本、模板和教程
- 📖 [AdsPower API 文档](https://localapi-doc-en.adspower.com/)
- 🌐 [AdsPower 官网](https://www.adspower.net/)

## 开源协议

[MIT](LICENSE)

---

**⭐ 觉得有用就给个 Star 吧！**
