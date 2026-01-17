<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Marketplace-blueviolet?style=for-the-badge" alt="Claude Code Marketplace">
  <img src="https://img.shields.io/badge/Plugins-1-blue?style=for-the-badge" alt="1 Plugin">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Claude Code Reflection Skills</h1>

<p align="center">
  <strong>让 Claude Code 能够自我配置的元技能市场</strong>
</p>

<p align="center">
  告别手动编辑 JSON 文件，直接让 Claude 帮你搞定一切。
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="README.ru.md">Русский</a> •
  <a href="README.pt-BR.md">Português</a>
</p>

---

## 安装

```bash
# 第一步：添加市场源
/plugin marketplace add https://github.com/CodeAlive-AI/claude-code-reflection-skills.git

# 第二步：安装插件
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
```

---

## 包含内容

**claude-code-reflection-skills** 插件提供 7 个技能：

| 技能 | 功能 |
|------|------|
| **claude-mcp-manager** | 通过 MCP 服务器连接数据库、GitHub 和各类 API |
| **claude-hooks-manager** | 自动格式化、自动测试、命令日志记录 |
| **claude-settings-manager** | 配置权限、沙箱模式、模型选择 |
| **claude-subagents-manager** | 创建专门处理特定任务的子代理 |
| **claude-skills-manager** | 跨项目管理和分享技能 |
| **claude-plugins-manager** | 打包和发布自己的插件 |
| **optimizing-claude-code** | 审计仓库并优化 CLAUDE.md 配置 |

---

## 使用示例

### claude-mcp-manager

> 通过 MCP 服务器连接数据库、GitHub 和各类 API

**连接数据库**
> *"把 Claude 连接到我的 PostgreSQL 数据库"*

安装[数据库 MCP 服务器](https://github.com/modelcontextprotocol/servers)，配置连接字符串。之后就能用对话方式查询数据了。

**集成 GitHub**
> *"把 Claude 连接到 GitHub，让它能创建 PR 和管理 Issue"*

安装[官方 GitHub MCP 服务器](https://github.com/github/github-mcp-server)。Claude 可以直接创建分支、PR，处理 Issue。

**更新 API 密钥**
> *"更新 MCP 配置里的 CodeAlive API 密钥"*

编辑 `~/.claude.json` 或 `.mcp.json` 来更新密钥。轮换凭证时无需重新安装。

**批量更新服务器配置**
> *"把所有 MCP 服务器的超时时间改成 120 秒"*

批量更新 MCP 服务器配置。可以一次性调整所有服务器的超时时间、环境变量或命令参数。

---

### claude-hooks-manager

> 自动格式化、自动测试、命令日志记录

**代码自动格式化**
> *"每次编辑后对 TypeScript 文件运行 Prettier"*

添加 PostToolUse 钩子。Claude 修改的每个文件都会自动格式化，再也不用担心代码风格不一致。

**自动运行测试**
> *"Claude 编辑 Python 文件时自动运行 pytest"*

为 `*.py` 文件添加 PostToolUse 钩子。改动后立即知道有没有破坏什么。

**记录所有命令**
> *"把 Claude 执行的每条命令记录到审计文件"*

添加 PreToolUse 钩子，将命令追加到 `~/.claude/command-log.txt`。完整的操作审计记录。

**阻止危险命令**
> *"添加钩子阻止全局 rm -rf 命令"*

添加 PreToolUse 钩子，在执行前拦截危险命令。防止意外删除数据。

**要求确认**
> *"添加钩子，遇到包含 'db reset' 的命令时请求用户确认"*

添加 PreToolUse 钩子，在数据库重置等敏感操作前暂停并请求确认。

---

### claude-settings-manager

> 配置权限、沙箱模式、模型选择

**启用沙箱模式**
> *"开启沙箱模式，让 Claude 不用每条命令都请求权限"*

启用[原生沙箱](https://www.anthropic.com/engineering/claude-code-sandboxing)——权限提示减少 84%，同时保持系统安全。

**阻止访问敏感文件**
> *"禁止 Claude 读取 .env 文件和 /secrets 目录"*

添加权限拒绝规则。即使 Claude 尝试访问，敏感文件也会受到保护。

**切换模型**
> *"这个项目使用 Opus 模型"*

更新设置使用 `claude-opus-4-5`——复杂架构决策时推理能力更强。

**团队共享配置**
> *"设置项目配置，让团队所有人使用相同的 Claude 设置"*

在项目范围创建 `.claude/settings.json`。提交一次，整个团队获得一致的配置。

---

### claude-subagents-manager

> 创建专门处理特定任务的子代理

**创建代码审查员**
> *"创建一个只能读取文件的审查子代理，使用 Opus 保证质量"*

创建[自定义子代理](https://code.claude.com/docs/en/sub-agents)，配置 `tools: Read, Grep, Glob` 和 `model: opus`。深入细致的代码审查。

**创建测试运行器**
> *"创建一个运行测试并报告失败的子代理"*

创建专门运行测试套件的代理，限制工具访问以确保安全。

---

### claude-skills-manager

> 跨项目管理和分享技能

**查看可用技能**
> *"显示我所有已安装的技能"*

列出用户和项目范围的技能，包括触发条件和描述。

**在范围间移动技能**
> *"把这个技能移到用户范围，这样我到处都能用"*

在项目和用户范围之间移动技能，调整可用范围。

---

### claude-plugins-manager

> 打包和发布自己的插件

**创建插件**
> *"用我的自定义技能创建一个新插件"*

生成新插件的目录结构，包含清单文件、README 和技能目录。

**发布到 GitHub**
> *"把我的插件发布到 GitHub"*

打包插件并创建 GitHub Release，供他人安装使用。

---

### optimizing-claude-code

> 审计仓库并优化 CLAUDE.md 配置

**项目就绪审计**
> *"检查这个仓库是否为 Claude Code 做好了准备"*

运行全面审计，分析 CLAUDE.md 文件、设置、MCP 配置和项目结构。返回按优先级排序的建议（P0/P1/P2），附带具体的改进方案。

**优化 CLAUDE.md**
> *"审查我的 CLAUDE.md 并提出改进建议"*

评估记忆文件质量：结构、简洁性、@import 验证、必要章节（命令、架构、约定）。提供具体的修改建议，让项目对 AI 代理更友好。

---

## 系统要求

- Claude Code CLI 1.0.33 或更高版本
- Python 3.x（用于技能脚本）
- `gh` CLI（可选，用于插件发布功能）

---

## 目录结构

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── marketplace.json         (市场目录)
├── plugins/
│   └── claude-code-reflection-skills/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── claude-mcp-manager/
│       │   ├── claude-hooks-manager/
│       │   ├── claude-settings-manager/
│       │   ├── claude-subagents-manager/
│       │   ├── claude-skills-manager/
│       │   ├── claude-plugins-manager/
│       │   └── optimizing-claude-code/
│       ├── LICENSE
│       └── README.md
├── CLAUDE.md
├── LICENSE
└── README.md
```

---

## 了解更多

- [MCP 服务器指南](https://code.claude.com/docs/en/mcp)
- [钩子文档](https://code.claude.com/docs/en/hooks-guide)
- [自定义子代理](https://code.claude.com/docs/en/sub-agents)
- [沙箱机制](https://code.claude.com/docs/en/sandboxing)

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)

---

<p align="center">
  <sub>使用 Claude Code 构建</sub>
</p>
