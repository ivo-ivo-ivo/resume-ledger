# resume-ledger · 简历账本

从**事实账本**生产简历、JD 定向版和项目作品集，文档里的每一个数字都能对回一条你本人确认过的来源。它是一个 Agent Skill，可在 Claude Code、Codex CLI、Gemini CLI、Cursor 以及任何读 `SKILL.md` 的工具里使用。中英文都支持。

市面上的"AI 改简历"大多从 JD 出发往上凑。这套反过来：先把你做过的事连同口径和来源记进账本，再写；脚本会拒绝任何数字不在账本里的草稿。

## 怎么运转

1. `init` 在你自己的目录里建项目：账本、规则、内容、版本登记。你的任何信息都不会进这个仓库。
2. 模型分轮问你。每条新事实要有口径、来源、你的角色边界和状态（live / pilot / planned）。前后说法有冲突时摆出来问你，不替你选。
3. 事实用 `fact_add.py` 追加（自动编号、拒绝重复）。你填 `rules.md`：红线词、禁用与允许写法、脱敏替换表。
4. 内容一个版本一个 Markdown。定向版先做 JD 命中表：要求 → 账本行 → 命中 / 部分 / 缺口。缺口不用文案填。
5. `check.py` 出 HTML 与 PDF、逐数对账、扫红线词与格式、读回页数。三项全过才算完成。
6. 盲投版由脚本派生，不手改。版本登记记录投递与反馈，这是唯一的学习来源。

作品集同样适用，只有一处不同：口径可以与简历独立，但每个数字仍要有 scope 为 `portfolio` 的账本行。

## 兼容性

| 工具 | 安装方式 | 状态 |
| --- | --- | --- |
| Claude Code | 插件市场或 `npx skills add` | 安装已验证；触发评测进行中（见 `evals/`） |
| Codex CLI、Cursor、Gemini CLI、Copilot、Windsurf 等遵循 Agent Skills 标准的工具 | `npx skills add` 装入 `.agents/skills/` | 按标准可装；未逐一验证 |
| 没有 shell 的网页聊天 | 把 `SKILL.md` 与参考文件作为指令粘贴 | 退化模式见 `SKILL.md`；未验证 |

状态：v0.1。在你的工具里能用或不能用，请开 issue 告诉我们。

## 安装

```bash
npx skills add ivo-ivo-ivo/resume-ledger
claude plugin marketplace add ivo-ivo-ivo/resume-ledger && claude plugin install resume-ledger@resume-ledger
gemini extensions install https://github.com/ivo-ivo-ivo/resume-ledger
```

依赖：Python 3.10+，`pip install markdown pypdf`（macOS 请用 venv），Chrome / Chromium / Edge 出 PDF。没有 shell 的工具里会退化为人工核对模式，并明说。

## 三分钟上手

```bash
S=<skills/resume-ledger/scripts 的路径>
python3 $S/init.py --lang zh --name 你的名字 --dir ~/my-resume
cd ~/my-resume
python3 $S/fact_add.py --topic 岗位 --fact "……" --number "……" --definition "……" --source "口述 2026-10-16"
python3 $S/check.py content/general.md
```

或者直接对你的 agent 说"帮我按这个 JD 写简历"，让 skill 来驱动。

## 示例

两套完整的虚构走查：[`examples/zh`](examples/zh/README.md)（小张）和 [`examples/en`](examples/en/README.md)（Maya Chen）。第一轮口述里各埋了五处常见错误，示范冲突检查和数字对账怎么抓出来。

## 隐私

账本是个人数据。`init.py` 写的 `.gitignore` 会把口述原文挡在 git 外；整个项目目录都应私有。skill 不会把你的事实复制到自己的目录里。

## 许可证

代码 MIT；文档、参考与示例 CC BY 4.0。见 `LICENSE` 与 `LICENSE-docs`。
