# Method Workflow

Use this reference when a paper contains reusable synthesis, fabrication, device setup, characterization, computation, or data-analysis methods. The goal is to build `<OBSIDIAN_VAULT>\\04-Methods` as a durable method library rather than producing one method file per material.

## What Counts As A Method

Create or update a method note for reusable procedural knowledge:

- Materials synthesis: hydrothermal, solvothermal, sol-gel, co-precipitation, electrodeposition, ALD, CVD, annealing, etching, doping, ligand exchange
- Device and apparatus setup: electrochemical cells, flow cells, reactors, in-situ/operando holders, fixtures, membranes, gas/liquid handling
- Characterization and testing: electrochemical protocols, cycling/stability tests, spectroscopy workflows, in-situ methods
- Computation and data-analysis: DFT/MD workflows, fitting routines, normalization, metric calculation, uncertainty handling

Do not create a method note for a purely descriptive result, a common instrument name, or a one-off detail that cannot transfer to another paper.

## Deduplication Rule

Before creating a note, search `<OBSIDIAN_VAULT>\\04-Methods` by method family, synonyms, equipment, and key operations. Compare the new method against existing notes using this method_fingerprint:

```text
method_family + mechanism + key_operations + equipment + parameter_window + output_structure
```

Do not create a new method note when the same method_fingerprint already exists and the paper only changes material names, precursors, substrate, dopant, solvent, concentration, temperature, time, or target product. Update the existing note's `文献变体` table instead.

Create a new note only when at least one of these changes the method identity:

- Different mechanism, such as hydrothermal crystallization vs vapor deposition
- Different essential equipment, such as H-cell vs flow cell
- Different operation sequence that changes the result, such as seed-mediated growth vs one-pot synthesis
- Different output structure class, such as powder nanoparticles vs supported membrane electrode
- Different purpose, such as synthesis route vs testing protocol

## Naming

Name method notes by general reusable method, not by one material:

| Better | Avoid unless truly unique |
|---|---|
| `Hydrothermal Nanosheet Synthesis.md` | `Material-A Synthesis.md` |
| `Solvothermal Oxide Preparation.md` | `Specific Sample Preparation.md` |
| `Two-Electrode Flow Cell Assembly.md` | `This Paper Flow Cell.md` |
| `Operando Spectroscopy Cell.md` | `Specific Catalyst Setup.md` |

Use aliases for common material-specific names.

## Method Note Template

Save method notes to:

```text
<OBSIDIAN_VAULT>\\04-Methods\\<General Method Name>.md
```

Use this structure:

```markdown
---
type: method
method_family: synthesis | device | characterization | computation | data-analysis
method_fingerprint: "<family> | <mechanism> | <key operations> | <equipment> | <parameter window> | <output structure>"
aliases: []
tags: [method]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# General Method Name

## 一句话定义

## 适用场景

## 核心原理

## 标准流程

1. ...

## 关键参数窗口

| 参数 | 常见范围 | 影响 | 风险 |
|---|---|---|---|
| ... | ... | ... | ... |

## 可替换变量

| 变量 | 可替换项 | 不应改变的条件 | 注意事项 |
|---|---|---|---|
| Material / precursor | ... | ... | ... |

## 文献变体

| 论文 | 材料/装置 | 条件差异 | 结果/用途 | 备注 |
|---|---|---|---|---|
| [[Paper Note]] | ... | ... | ... | ... |

## 常见坑点

## 相关方法

- [[Related Method]]

## 相关论文

- [[Paper Note]]
```

## Paper Note Link Pattern

In the paper note, add method links under `可复用方法与装置`:

```markdown
## 可复用方法与装置

- [[General Synthesis Method]] - This paper changes the precursor or parameter window while preserving the same method fingerprint.
- [[General Testing Protocol]] - This paper uses the same testing logic but changes the electrolyte, normalization basis, or operating window.
```

If no reusable method appears, write a short sentence saying no new transferable method was extracted. Do not force a method note.

## Common Merge Examples

- Two papers using the same synthesis mechanism, equipment, and operation sequence usually belong in one method note; add each paper as a `文献变体`.
- Two routes with different essential equipment or growth mechanisms should become separate method notes.
- Two testing setups can be separate notes when the cell/reactor architecture changes the measured behavior.
- A sample-specific recipe can stay inside the paper note when it is not reusable beyond that material or device.

## Quality Gate

Before finishing a paper note:

- Check whether the Methods/Experimental/Supporting Information section contains a reusable method.
- Search existing method notes before creating a new one.
- Prefer updating `文献变体` over making near-duplicate notes.
- Link the method note from the paper note.
- Keep the method note general enough that the next similar paper can extend it.


