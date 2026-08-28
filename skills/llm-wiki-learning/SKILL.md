---
name: llm-wiki-learning
description: "Use only when King explicitly asks Codex to write, update, organize, ingest into, diagram, or lint LLM knowledge in his Obsidian vault. Do not use for chat-only LLM teaching, explanations, paper discussion, or conceptual questions."
---

# LLM Wiki Learning

Maintain King's Obsidian LLM wiki when he explicitly requests file changes.

Default vault: `/home/kj/Documents/Obsidian/personalOS`  
Default LLM wiki root: `Knowledge/LLM/` unless user specifies otherwise.

## Trigger Boundary

- Activate only for explicit Obsidian or vault mutations: write, record, add, update, organize, ingest, diagram, or lint.
- Do not activate for chat-only learning, teaching, explanations, paper discussion, or conceptual questions.
- If no file change was requested, answer normally without this skill and do not suggest a writeback target.

## Core Stance

- Preserve source vs synthesis: raw material is not knowledge. Sources stay in `Resources/LLM/`; King's reusable understanding goes in `Knowledge/LLM/`.
- Keep graph clean: only topic pages and concept pages belong in the LLM knowledge graph. Project logs, experiment logs, paper summaries, and raw chat notes feed the graph but do not become graph nodes directly.
- Prefer minimal edits. Update existing notes/maps before creating new pages.
- Never fabricate sources. Mark uncertain claims as `待验证`.

## Read First

For vault edits, first read:

1. `AGENT.md`
2. `Knowledge/LLM Learning Roadmap.md`
3. `Knowledge/_index.md`
4. Relevant existing `Knowledge/LLM/` pages, if present

Load references only when needed:

- `references/workflow.md` for routing, writeback, ingest, lint.
- `references/note-templates.md` for topic/concept/source/project/log templates.
- `references/canvas-diagrams.md` for Mermaid rules.

## Workflow Decision

Classify the user request before acting:

| Request | Mode |
|---|---|
| "record/write/add this to my Obsidian wiki" | Concept writeback |
| "ingest/save this paper/report/source into my vault" | Source ingest |
| "write this experiment plan/result into my vault" | Experiment note |
| "organize/update my Obsidian roadmap/map" | Topic map maintenance |
| "create/update a diagram in my vault" | Visual map |
| "check/clean/lint my wiki files" | Wiki lint |

If no explicit Obsidian file change was requested, stop using this skill.

## Wiki Shape

Use this shape unless user overrides:

```text
Knowledge/LLM/
  LLM Home.md
  LLM Full Flow.md
  Source Index.md
  Topics/
    Architecture.md
    Pretraining.md
    Post-training.md
    PEFT.md
    Inference.md
    Systems.md
    Evaluation.md
    Data Engineering.md
    VLM and World Models.md
  Concepts/
    <Concept>.md
  Experiments/
    YYYY-MM-DD - <experiment>.md
Resources/LLM/
  <source notes and links>
Projects/
  LLM Phase <n> - <artifact>.md
```

Use `Knowledge/LLM/` over a new root `LLM Wiki/`, because King's vault already defines `Knowledge/` as the wiki layer.

## Routing Rules

- `LLM Home.md`: dashboard, current sprint, links, recent notes, publish queue.
- `LLM Full Flow.md`: whole lifecycle from data to deployment; big mental model, not a dump.
- `Topics/*.md`: routers for areas; include boundary, concept map, reading order, key sources, open questions.
- `Concepts/*.md`: one reusable idea only.
- `Resources/LLM/`: source cards, paper summaries, report notes, links; no graph membership.
- `Experiments/`: date, hypothesis, setup, command/code, result, interpretation, next step.
- `Projects/`: capstone artifacts and multi-week deliverables.

## Writeback Rules

When writing a concept:

1. Search existing notes first.
2. Create/update one concept only.
3. Include definition, why it matters, mechanism, common confusion, connections, sources.
4. Add graph location:
   ```md
   ## Connections
   - Belongs to:
   - Related:
   - Used in:
   ```
5. Ensure at least one topic link and two related concept links when possible.
6. Update relevant topic map if concept is stable enough.
7. If public-blog ready, set `publish: true`; otherwise leave `publish: false`.

### Note Readability

- Begin each dense mechanism, transition, formula-heavy section, or recurring confusion with one plain-language orientation sentence. Skip this for Sources, Connections, and simple examples.
- Build beauty from information hierarchy: one top summary callout, zero or one useful Mermaid diagram, comparison tables only, warning callouts only for real confusion, short paragraphs, and consistent headings.
- Create diagrams directly as fenced `mermaid` blocks inside the note. Use Mermaid for small and large flows, architecture maps, training flows, and code/dataflow. Do not create Canvas or SVG artifacts unless the user explicitly requests that format. Read `references/canvas-diagrams.md` before adding or updating a diagram.

When writing source material:

1. Create/update source note under `Resources/LLM/`.
2. Update `Knowledge/LLM/Source Index.md`.
3. Track status: `raw`, `summarized`, `extracted`, `integrated`, `archived`.
4. Extract candidate concepts, but do not force them into topic maps until they become concept notes.

## Experiments

For every practical task, separate:

- project fact: what was built
- experiment log: what was tried and observed
- reusable concept: what generalizes

Experiment note must include:

```md
## Question
## Hypothesis
## Setup
## Command / Code
## Result
## Interpretation
## Next Step
## Concepts Updated
```

For LLM roadmap phases, prefer artifacts over passive study: tiny implementation, reproduction, benchmark, ablation, eval table, or blog-ready explanation.

## Lint Before Completion

Before claiming the wiki update is complete, check:

- Concept has clear home topic.
- Topic page can stand without `LLM Full Flow`.
- No source/report/project/log was inserted directly as a graph node.
- Source index status is updated when source material changed.
- No duplicate or near-duplicate concept page was created.
- Claims with weak support are marked `待验证`.
- Diagrams use fenced `mermaid` blocks unless the user explicitly requested another format.
- Dense topics have selective one-sentence orientation; simple sections do not repeat themselves.
- Every visual element serves explanation, comparison, navigation, or warning.
- Relevant verification ran or limitation is stated.

## References

- Use `references/workflow.md` for full routing and maintenance rules.
- Use `references/note-templates.md` for copy-ready note templates.
- Use `references/canvas-diagrams.md` for Mermaid layout rules.
