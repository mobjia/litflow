# Obsidian Note Design Style

Use this reference when writing final paper notes or review notes. The goal is not decoration; it is readable hierarchy, fast review, and long-term knowledge reuse.

## Design Principles

- Make the first screen useful: title, summary callout, metadata table, and speed-read card should tell the reader why the paper matters.
- Make the page feel like a research card, not a copied abstract. Use a strong opening summary, visual logic map, compact tables, and figure interpretation.
- Use tables for comparison and facts; use prose for reasoning.
- Keep paragraphs short: 3-6 lines each in Obsidian reading view.
- Use callouts sparingly. Prefer `[!summary]`, `[!note]`, `[!important]`, and `[!question]`.
- Do not overuse bold text. Bold only the core claim, metric, or contrast.
- Do not create decorative separators everywhere. Use sections and tables as the structure.
- Keep wikilinks meaningful. Link concepts, people, and closely related papers; do not link every noun.
- Figures should breathe: one figure, then one interpretation callout. Avoid stacking many images without explanation.

## Preferred Paper Note Layout

```markdown
# Paper Title

> [!summary] 一句话总览
> 2-3 句说明问题、策略、结论。让没读过论文的人立刻知道它为什么重要。

> [!important] 读这篇文章要抓住的主线
> **问题** → **策略** → **证据** → **结论**：一行写出论文的逻辑链。

| 项目 | 信息 |
|---|---|
| 作者 | ... |
| 年份/期刊 | ... |
| 机构 | ... |
| 通讯/PI | [[Person Name]] |
| DOI | ... |
| 关键词 | `keyword-1` `keyword-2` |

## 速读卡

| 维度 | 内容 |
|---|---|
| 核心问题 | ... |
| 研究策略 | ... |
| 关键结果 | ... |
| 主要创新 | ... |
| 局限/疑问 | ... |

## 逻辑地图

```mermaid
flowchart LR
  A["领域瓶颈"] --> B["本文策略"]
  B --> C["关键实验"]
  C --> D["核心证据"]
  D --> E["结论/启发"]
```

## 研究背景与内容

Use coherent prose. Explain the field bottleneck first, then the paper's specific question.

## 研究策略

Explain the design logic and experimental route. Avoid turning this into a protocol list unless the paper itself is method-heavy.

## 创新点

| 创新点 | 证据/数据 | 为什么重要 |
|---|---|---|
| ... | ... | ... |

## 关键图表

### Fig 1 - Short Title
![[Author_Year_Fig1.png]]
> [!note] 图表解读
> 解释这张图的核心信息、看图顺序、它支撑的结论。

## 关键数据

| 指标 | 数值 | 条件/对照 | 意义 |
|---|---:|---|---|
| ... | ... | ... | ... |

## 不足与评价

Use `[!question]` for the most important unresolved issue if helpful.

## 关键概念链接

- [[Concept]] - why it matters here.

## 人物与团队

- [[Person Name]] - role and research direction.

## 可复用启发

- 可借鉴的实验设计：
- 可迁移的方法/材料：
- 后续可以追的问题：
```

## Figure Section Rules

- Put no more than 1-2 figures back-to-back without commentary.
- Use short figure headings: `Fig 2 - Performance comparison`, not full captions.
- The image itself should contain the original full caption when possible.
- The callout below the image should explain the figure in the user's own knowledge system, not merely repeat the caption.
- Use `[!note] 图表解读` for ordinary figures and `[!important] 关键证据` for the single most important figure.

## Optional CSS Snippet

For a more polished Obsidian reading view, copy `assets/obsidian-snippets/literature-reading.css` into `.obsidian/snippets/` and enable it in Settings → Appearance → CSS snippets.

The note should include:

```yaml
cssclasses: [paper-note, literature-card]
```

The Markdown must still look good without CSS; the snippet is enhancement only.

## Tables

Use tables only when they improve scanning:

- Metadata
- Speed-read card
- Innovation/evidence
- Key metrics
- Cross-paper comparison

Avoid wide tables with long paragraphs. If a cell becomes longer than 2 lines, move that content to prose.

## Literature Review Layout

For review notes:

```markdown
# Review Title

> [!summary] 综述主线
> 用 3-4 句说明这组论文围绕什么核心矛盾展开，以及本文综述采用什么逻辑线。

## 逻辑框架

Use Mermaid, ASCII, or a compact numbered chain if it clarifies the argument.

## 技术路线演进

| 路线 | 代表论文 | 核心思想 | 优势 | 瓶颈 |
|---|---|---|---|---|

## 横向对比

| Paper | System | Method | Key Metric | Limitation |
|---|---|---|---:|---|

## 设计原则

Use prose plus a short table if needed.

## 未解决问题

> [!question] Open question
> ...
```

## Bad Patterns to Avoid

- A long wall of prose before any summary.
- Many headings with only one sentence under each.
- Images without interpretation.
- A giant bullet list pretending to be deep reading.
- Too many callouts, which makes every block compete for attention.
- Captions repeated verbatim in Markdown when the cropped image already contains them.


