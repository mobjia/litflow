# LitFlow

LitFlow is an agent skill for deep academic paper reading, figure extraction, and Obsidian knowledge-base writing. It is designed for Codex, Hermes, and other `SKILL.md`-compatible assistants that support skill folders with references, scripts, and assets.

中文说明见下方：[中文介绍](#中文介绍)。

## What It Does

- Triage papers before deep reading by type: research, review, theory, perspective, or method.
- Read full academic PDFs and produce structured Chinese Obsidian notes.
- Extract and QA key figures, tables, schemes, and mechanism diagrams.
- Create paper notes with summaries, logic maps, key data, figure interpretation, limitations, and reusable ideas.
- Maintain linked Obsidian knowledge folders for papers, concepts, people, methods, and innovation indexes.
- Support batch reading, cross-paper comparison, literature review synthesis, and backfill repair for missing concept or people notes.

## Is It Ready To Use?

Yes, as a skill package: install the whole `skills/litflow` folder and invoke `$litflow`.

On first use, the agent will still need your local configuration:

- Your Obsidian vault path.
- Optional Zotero storage path if you use Zotero.
- Permission before installing missing Python packages or external PDF/OCR tools.

## Repository Layout

```text
litflow-skill/
├── README.md
├── LICENSE
└── skills/
    └── litflow/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        ├── references/
        └── scripts/
```

`agents/openai.yaml` is optional Codex/OpenAI UI metadata. Hermes and other compatible agents can ignore it.

## Install

### Codex

Install from GitHub with Codex's GitHub skill installer:

```bash
install-skill-from-github.py --repo <your-github-user>/<your-repo> --path skills/litflow
```

Or copy the skill folder manually:

```text
skills/litflow -> <CODEX_HOME>/skills/litflow
```

If `CODEX_HOME` is not set, Codex usually falls back to:

```text
~/.codex/skills/litflow
```

Restart Codex after copying the folder.

### Hermes

Copy the same folder into your Hermes skills directory:

```text
skills/litflow -> <HERMES_SKILLS_DIR>/litflow
```

Then restart or refresh Hermes so it can discover the skill.

### Other Compatible Agents

Use the folder at `skills/litflow` as the installable skill. The required entry point is `SKILL.md`; bundled helper content lives in `references/`, `scripts/`, and `assets/`.

## First Use

Ask your agent with an explicit skill invocation:

```text
Use $litflow to deeply read this PDF and save a Chinese Obsidian note.
```

On first use, the agent should ask for your own local paths instead of assuming any machine-specific path:

- `OBSIDIAN_VAULT`: your Obsidian vault path
- `ZOTERO_STORAGE`: optional Zotero storage path
- `ATTACHMENTS_DIR`: usually `<OBSIDIAN_VAULT>\99-Attachments`

## Suggested Obsidian Structure

```text
<OBSIDIAN_VAULT>\
  00-Inbox\
  01-Papers\
  02-Concepts\
  03-People\
  04-Methods\
  05-MOC\
  06-Templates\
  07-Innovations\
  99-Attachments\
```

## Dependencies

Core dependencies:

- Python 3.10+
- PyMuPDF for PDF text extraction, page rendering, and figure cropping
- Pillow for image checks and crop QA

Optional tools:

- Obsidian for Markdown notes, wikilinks, and the optional CSS snippet
- Zotero if your PDFs live in Zotero storage
- Poppler, PDFFigures2, GROBID, Docling, PaddleOCR, or cloud PDF extraction tools for difficult figure/OCR cases

LitFlow instructs the agent to ask before installing packages, plugins, or external tools.

## Privacy Notes

Do not commit private PDFs, unpublished manuscripts, Obsidian vault contents, Zotero storage, `.env` files, API keys, or machine-specific absolute paths. The skill uses placeholder variables such as `<OBSIDIAN_VAULT>` so each user can configure their own local setup.

## 中文介绍

LitFlow 是一个通用 agent skill，用于论文精读、图表提取和 Obsidian 知识库沉淀。它适用于 Codex、Hermes，以及其他兼容 `SKILL.md` 结构的智能体。

### 主要功能

- 论文分诊：先判断论文类型，包括 research、review、theory、perspective、method。
- 中文精读笔记：生成结构化 Obsidian Markdown 笔记。
- 图表提取：从 PDF 中裁剪关键图、表、scheme、机制图，并要求进行视觉 QA。
- 知识库沉淀：维护 `01-Papers`、`02-Concepts`、`03-People`、`04-Methods`、`07-Innovations` 等目录。
- 批量阅读：支持文件夹级批量分诊、批量精读和跨论文综述。
- 回溯修复：在用户明确要求时，补建旧笔记中缺失的概念、人名、方法和创新点索引。

### 是否开箱即用？

是，但这里的“开箱即用”指的是：把整个 `skills/litflow` 文件夹安装到对应 agent 的 skills 目录后，即可用 `$litflow` 调用。

首次使用时仍需要用户提供本机配置：

- Obsidian vault 路径。
- 如果使用 Zotero，需要提供 Zotero storage 路径。
- 如果缺少 `PyMuPDF`、`Pillow` 或外部 OCR/PDF 工具，agent 会先征求许可再安装或调用。

### 安装方式

Codex 可以从 GitHub 安装：

```bash
install-skill-from-github.py --repo <你的 GitHub 用户名>/<仓库名> --path skills/litflow
```

也可以手动复制：

```text
skills/litflow -> <CODEX_HOME>/skills/litflow
```

Hermes 用户复制同一个文件夹：

```text
skills/litflow -> <HERMES_SKILLS_DIR>/litflow
```

安装后重启或刷新对应 agent。

### 使用示例

```text
Use $litflow to deeply read this PDF and save a Chinese Obsidian note.
```

中文也可以这样说：

```text
请使用 $litflow 精读这篇 PDF，并保存为中文 Obsidian 笔记。
```

### 隐私提醒

不要把私人 PDF、未发表论文、Obsidian vault、Zotero storage、`.env`、API key 或个人电脑绝对路径提交到公开仓库。LitFlow 使用 `<OBSIDIAN_VAULT>` 这类占位符，让每个用户在本机配置自己的路径。

## License

MIT
