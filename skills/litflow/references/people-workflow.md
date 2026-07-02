# People Workflow

Use `03-People` to build a researcher and lab map from literature reading.

## Entity Note Gate

People-note work is part of the required Entity Note Gate. If a paper has a corresponding author, PI, recurring first author, important lab, or route-defining team, the paper note is not complete until the relevant `03-People` file is created or updated and the wikilink target is verified.

If no people note is created or updated, record the reason in the working checklist or the paper note's `实体链接检查` section, such as "all important people already had notes" or "no identifiable PI/team from the PDF".

## When to Create a People Note

Create or update a people note for:

- Corresponding authors and PIs
- First authors who appear repeatedly
- Researchers the user may contact
- Authors associated with a key method, material system, or technical route
- Labs that anchor a literature-review section

Do not create notes for every coauthor in a long author list.

## File Name

Save to:

```text
<OBSIDIAN_VAULT>\03-People\<Person Name>.md
```

If Chinese and English names both appear, use the most searchable publication name as the file name and add aliases.

## Template

```markdown
---
type: person
name: "Person Name"
aliases: ["中文名", "Other Name Variant"]
role: "PI / corresponding author / first author / researcher"
affiliation: "Institution"
fields: [field-1, field-2]
email: ""
website: ""
scholar: ""
orcid: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Person Name

## 一句话定位

这个人主要做什么方向，为什么值得在当前知识库里追踪。

## 研究方向

- Direction 1
- Direction 2

## 代表工作

- [[Paper Note Name]] - 这篇工作解决了什么问题，贡献是什么。

## 技术路线/方法偏好

总结其团队常用材料体系、表征方法、模型、反应体系或应用场景。

## 可能联系点

适合在什么问题上联系；如果是潜在合作/套磁对象，记录切入点。

## 关联人物/团队

- [[Collaborator Name]]
```

## Update Rules

- Merge name variants into one note; do not create duplicates.
- Add new papers under `代表工作`, not as separate repeated biography paragraphs.
- Keep claims grounded in paper evidence unless verified from official profile pages.
- If contact details are not in the PDF, leave them blank instead of guessing.
- For uncertain PI/corresponding-author status, write `待确认`.

## How Paper Notes Should Link People

In each paper note:

```markdown
## 人物与团队

- [[Person Name]] - 通讯作者，团队长期关注...
- [[First Author]] - 第一作者，本文负责/代表工作待确认。
```

Use the People note to accumulate "who did what" across papers. This turns `03-People` into a field map rather than a static address book.


