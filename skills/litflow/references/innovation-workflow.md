# Innovation Workflow

Use this reference when a paper contains a clear novelty claim. The goal is to build `<OBSIDIAN_VAULT>\\07-Innovations` as a lightweight 创新点聚类索引: similar innovation points go together, and each paper contributes one concise line rather than a long genealogy.

## Default Rule

Classify and cluster. do not perform deep lineage tracing by default.

The daily reading task is:

1. Identify the paper's 1-2 strongest innovation points.
2. Choose the best innovation index file.
3. Place the entry under an existing subsection when the pattern is similar.
4. Create a new subsection only when no existing pattern fits.
5. Write one sentence explaining the innovation.
6. Use `可选备注` only for short clues such as "possible prior route to check", "inspired by adjacent system design", or "lineage not traced".

Full source tracing, historical route reconstruction, and citation-chain analysis are optional review tasks, not the default deep-reading workload.

## Fixed Files

Keep exactly four high-level index files:

```text
<OBSIDIAN_VAULT>\\07-Innovations\\机制创新.md
<OBSIDIAN_VAULT>\\07-Innovations\\材料创新.md
<OBSIDIAN_VAULT>\\07-Innovations\\器件-方法创新.md
<OBSIDIAN_VAULT>\\07-Innovations\\装置-系统创新.md
```

## Category Boundaries

| File | Use for | Example subsections |
|---|---|---|
| `机制创新.md` | Why it works; reaction pathway, charge transfer, failure suppression, ion transport, catalysis mechanism | 反应路径调控, 界面电荷转移调控, 失效机制抑制, 离子传输调控 |
| `材料创新.md` | What material/structure is new; composition, morphology, defects, heterostructures, interfaces | 缺陷工程, 异质结构设计, 界面/包覆层设计, 形貌调控 |
| `器件-方法创新.md` | How it is made, tested, characterized, or analyzed; device-level method but not full system architecture | 测试协议改造, 原位表征方法, 电极制备方法, 数据处理方法 |
| `装置-系统创新.md` | How the whole setup/system is configured; cell, reactor, flow system, module, platform | 流动体系设计, 悬浮/半固态体系, 原位装置搭建, 模块化系统集成 |

## Entry Table

Use the same table shape in every subsection:

```markdown
| 论文 | 一句话创新点 | 作用对象 | 关键证据 | 关联概念/方法 | 可选备注 |
|---|---|---|---|---|---|
| [[Paper Note]] | ... | ... | Fig 2; metric=... | [[Concept]]; [[Method]] | 待追溯 |
```

同类创新点放在同一个小类. For example, multiple papers that redesign a device around a movable or distributed active phase may belong under `装置-系统创新.md` → `悬浮/半固态体系` unless their novelty is mainly material chemistry or mechanism.

## Subsection Suggestions

### 机制创新.md

- 反应路径调控
- 界面电荷转移调控
- 失效机制抑制
- 离子传输调控
- 成核/沉积行为调控

### 材料创新.md

- 缺陷工程
- 掺杂/组分调控
- 异质结构设计
- 界面/包覆层设计
- 形貌与孔结构调控

### 器件-方法创新.md

- 电极制备方法
- 测试协议改造
- 原位/operando表征方法
- 数据处理与指标定义
- 小型器件结构设计

### 装置-系统创新.md

- 流动体系设计
- 悬浮/半固态体系
- 反应器/电解槽系统
- 原位装置搭建
- 模块化系统集成

## Paper Note Link Pattern

In each paper note, keep the innovation section lightweight:

```markdown
## 创新点归类

- `装置-系统创新 / 悬浮/半固态体系`: [[装置-系统创新#悬浮/半固态体系]] - 将固定反应界面改造成可迁移或可更新的反应相，以系统结构缓解局部失效问题。
```

## Common Mistakes

- Do not force every paper into all four categories; 1-2 categories are enough.
- Do not create a new subsection for every paper. Reuse existing subsections when the innovation pattern is similar.
- Do not write a paragraph in the index table. One sentence is the point.
- Do not treat `可选备注` as mandatory lineage tracing.
- Do not duplicate method details from `04-Methods`; link method notes instead.


