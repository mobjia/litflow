# Entity Note Workflow

Use this workflow whenever a paper note contains reusable concepts or important researchers/teams. It exists to prevent paper notes from linking `[[Concept]]` or `[[Person]]` names without actually creating the target notes.

Default locations:

```text
<OBSIDIAN_VAULT>\02-Concepts\
<OBSIDIAN_VAULT>\03-People\
```

## Default New-Paper Mode

Default new-paper reading is lightweight and current paper only:

- Extract concept/person candidates only from the current paper.
- Check existing `02-Concepts` and `03-People` only for same names, obvious aliases, and target files referenced by the current paper note.
- Create or update notes needed by the current paper.
- Verify current-paper links exist.
- do not scan all historical paper notes.
- Do not run broad semantic comparison across the full concept/person library.

This keeps routine reading token-efficient while preventing new omissions.

## Entity Note Gate

Do not finish the paper note until the entity gate passes.

For every paper, complete a small candidate table during reading:

| candidate | type | evidence in paper | action | target file |
|---|---|---|---|---|
| concept or person name | concept / person | where it appears and why it matters | create / update / skip | file path or reason |

The table can stay in the working notes; it does not need to be copied into the final paper note unless useful. The final paper note should include only the compact `实体链接检查` summary.

## Concept Candidates

Create or update a `02-Concepts` note when the item is reusable across papers:

- A mechanism, reaction pathway, transport process, design principle, metric, model, material class, fabrication logic, or characterization idea.
- A term the user will likely search again when reading the next paper.
- A concept that helps compare papers, methods, or innovation clusters.

Skip common background words unless the paper uses them in a field-specific or unusual way.

Save concept notes to:

```text
<OBSIDIAN_VAULT>\02-Concepts\<ConceptName>.md
```

Before creating a file, deduplicate by checking existing filenames, aliases, Chinese/English variants, singular/plural forms, and near-synonyms already described in `references/concept-glossary.md`.

## People Candidates

Create or update a `03-People` note for:

- Corresponding authors and likely PIs.
- First authors who recur across multiple papers or define an important route.
- Labs, teams, or authors associated with a key method, material system, device, or mechanism.
- Researchers the user may plausibly want to track, compare, contact, or cite in a review.

Do not create notes for every coauthor in a long list.

Save people notes to:

```text
<OBSIDIAN_VAULT>\03-People\<Person Name>.md
```

Before creating a file, deduplicate by checking initials, full names, Chinese/English variants, affiliations, ORCID/profile clues if available, and existing aliases.

## Required Actions

For each candidate, choose exactly one action:

- `create`: make a new concept/person note because no equivalent note exists.
- `update`: append this paper to an existing note under related papers, representative work, route preference, or evidence.
- `skip`: do not create a note, with a short reason.

If no new concept/person notes are created, still verify that important existing links are updated when relevant. If no concept or people notes are created or updated, record a short reason such as "all candidates already existed", "no reusable concepts beyond routine background", or "PDF did not identify a PI/team clearly enough".

## Link Verification

After writing the paper note:

1. Extract wikilinks from `关键概念链接`, `人物与团队`, the metadata table's corresponding-author field, and the `实体链接检查` section.
2. Ignore paper-note links, method links, innovation-index links, and image embeds.
3. For each concept link, verify target files exist in `<OBSIDIAN_VAULT>\02-Concepts\`.
4. For each person/team link, verify target files exist in `<OBSIDIAN_VAULT>\03-People\`.
5. If a target is missing, create/update it before the paper note is considered complete.

In short: verify target files exist, not merely that the link text looks plausible.

## Subagent Rule

If a subagent drafts the paper note, the main agent remains responsible for the Entity Note Gate. A subagent may propose candidate entities, but the main agent must deduplicate, create/update the target files, and verify the final links. Do not accept a delegated paper note as complete just because it mentions concept/person names.

## Entity Backfill Mode

Backfill is non-default. Use this mode only when the user explicitly asks to repair,回溯, scan old papers, check previous notes, or fill missing `02-Concepts` / `03-People` entries.

Goal: scan existing paper notes in `<OBSIDIAN_VAULT>\01-Papers\`, identify missing target files, and repair the vault without rereading every PDF from scratch unless the paper note lacks enough evidence.

## Explicit Backfill Triggers

Run backfill only for requests like:

- "回溯检查 02/03"
- "扫描旧文献，补建概念条目"
- "修复人物库"
- "检查最近 10 篇文献的概念和人物"
- "对这个文件夹做 Entity Backfill Mode"

If the user is simply asking for a normal new-paper reading, do not start backfill.

Prefer bounded scopes. Ask for or infer a practical scope before a large repair:

- local: one named paper note or a few specified notes.
- folder/date/window: a specified folder, recent N notes, or a topic subset.
- full vault: all `<OBSIDIAN_VAULT>\01-Papers\` notes; do this only when the user clearly asks for full-library repair.

In all backfill modes, user specifies the scope or explicitly accepts the inferred scope.

Backfill steps:

1. List the target paper notes, or scan all Markdown files in `<OBSIDIAN_VAULT>\01-Papers\` if the user asks for a broad repair.
2. Extract wikilinks from `关键概念链接`, `人物与团队`, corresponding-author metadata rows, and any `实体链接检查` section.
3. Classify links as concept, person/team, paper, method, innovation index, or image embed. Do not treat every wikilink as a missing entity.
4. For concept/person links, check whether the corresponding file exists in `<OBSIDIAN_VAULT>\02-Concepts\` or `<OBSIDIAN_VAULT>\03-People\`.
5. For missing target files, use the paper-note context to create a minimal but useful note. If the paper note lacks enough context, mark it `待补证据` and quote the paper title/section that needs checking.
6. For existing target files, update the related-paper or representative-work section instead of creating duplicates.
7. Produce a repair summary: created, updated, skipped, and needs manual source checking.

Backfill should be conservative. It is better to create a short grounded note with `待补证据` than to invent details from a thin paper summary.

## Minimal Final Summary

At the end of a reading task, mention only the useful outcome:

- Paper note saved.
- Concept notes created/updated.
- People notes created/updated.
- Any skipped entity category and why.

Avoid dumping the whole candidate table unless the user asks for audit details.


