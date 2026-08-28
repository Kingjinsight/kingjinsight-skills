# Note Templates Reference

Use these when creating or updating King's LLM wiki notes. Keep templates flexible; content decides shape.

## Readability and Visual Budget

Use a one-sentence orientation immediately after a dense technical heading when it introduces a mechanism, transition, formula-heavy idea, or recurring confusion. State what the topic does or why it appears; do not restate the heading. Skip Sources, Connections, and simple examples.

Default concept-note budget:

- one summary callout near the top;
- zero or one embedded SVG concept map;
- tables only for comparisons;
- warnings only for genuine confusion or failure modes;
- formulas preceded by variable setup and followed by plain-language meaning;
- short paragraphs with consistent H2/H3 hierarchy.

Beauty comes from information hierarchy, spacing, and consistency. Decorative emoji, banners, repeated colored callouts, and duplicated summaries are outside the template.

## Concept Note

Path: `Knowledge/LLM/Concepts/<Concept>.md`

```md
---
type: knowledge
domain: llm
note_type: concept
status: seed # seed | developing | stable | publishable
roadmap_phase:
source:
publish: false
blog_status: draft # draft | ready | published
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Concept>

> [!note]
> One short paragraph: what it is, what problem it solves, why worth learning.

## Why It Matters

## Core Mechanism

<One-sentence orientation when this section is dense.>

## My Understanding

## Common Confusions
> [!warning]
> 

## Minimal Exercise

## Connections
- Belongs to: [[Knowledge/LLM/Topics/<Topic>]]
- Related: [[...]], [[...]]
- Used in:

## Sources
- 

## Open Questions
- [ ] 
```

Status meanings:

- `seed`: rough capture after first learning.
- `developing`: accurate enough to link from topic.
- `stable`: reviewed against source/experiment.
- `publishable`: ready for blog after cleanup.

## Topic Page

Path: `Knowledge/LLM/Topics/<Topic>.md`

```md
---
type: knowledge
domain: llm
note_type: topic
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Topic>

> [!note]
> What this topic covers and why it matters in the LLM lifecycle.

## Position

## Boundaries

| Belongs here | Goes elsewhere |
|---|---|
|  |  |

## Concept Map

| Concept | Role | Status |
|---|---|---|
| [[...]] |  | seed/developing/stable |

## Reading Order
1. 

## Key Sources
- 

## Experiments / Projects
- 

## Open Questions
- [ ] 
```

Topic candidates:

- `Architecture`
- `Pretraining`
- `Post-training`
- `PEFT`
- `Inference`
- `Systems`
- `Evaluation`
- `Data Engineering`
- `VLM and World Models`

## LLM Home

Path: `Knowledge/LLM/LLM Home.md`

```md
# LLM Home

## Current Sprint
- Phase:
- This week:
- Artifact:
- Blockers:

## Main Links
- [[LLM Full Flow]]
- [[Source Index]]

## Topics
- [[Topics/Architecture]]
- [[Topics/Pretraining]]
- [[Topics/Post-training]]
- [[Topics/PEFT]]
- [[Topics/Inference]]
- [[Topics/Systems]]
- [[Topics/Evaluation]]
- [[Topics/Data Engineering]]
- [[Topics/VLM and World Models]]

## Recent Concepts

## Experiments

## Publish Queue
```

## LLM Full Flow

Path: `Knowledge/LLM/LLM Full Flow.md`

Purpose: one page describing whole field.

````md
# LLM Full Flow

```text
data
-> tokenizer
-> architecture
-> pretraining
-> post-training
-> evaluation
-> inference
-> product / agents
```

## Lifecycle

| Stage | Question | Topic |
|---|---|---|
| Data | What does model eat? | [[Topics/Data Engineering]] |
| Tokenizer | How text becomes IDs? | [[Topics/Architecture]] |
| Architecture | How model computes? | [[Topics/Architecture]] |
| Pretraining | How base capability forms? | [[Topics/Pretraining]] |
| Post-training | How behavior is shaped? | [[Topics/Post-training]] |
| Evaluation | How know if good? | [[Topics/Evaluation]] |
| Inference | How serve cheaply/fast? | [[Topics/Inference]] |
| Systems | How run at scale? | [[Topics/Systems]] |
````

## Source Card

Path: `Resources/LLM/<YYYY-MM-DD>-<source-title>.md`

```md
---
type: source
domain: llm
source_type: paper # paper | report | code | course | article | chat-note
status: raw # raw | summarized | extracted | integrated | archived
url:
created: YYYY-MM-DD
---

# <Source Title>

## What This Is

## Why I Read It

## Summary

## Key Claims

## Candidate Concepts
- 

## Links Into Wiki
- 

## Source Notes
```

## Source Index

Path: `Knowledge/LLM/Source Index.md`

```md
# Source Index

| Source | Type | Status | Generated Notes | Candidate Concepts | Notes |
|---|---|---|---|---|---|
|  | paper/report/code/course | raw/summarized/extracted/integrated/archived |  |  |  |
```

## Experiment Log

Path: `Knowledge/LLM/Experiments/YYYY-MM-DD - <experiment>.md`

````md
---
type: experiment
domain: llm
status: running # planned | running | done | abandoned
roadmap_phase:
created: YYYY-MM-DD
---

# <Experiment>

## Question

## Hypothesis

## Setup
- Model:
- Dataset:
- Hardware:
- Environment:

## Command / Code

```bash

```

## Result

## Interpretation

## Failure / Debug Notes

## Next Step

## Concepts Updated
- 
````

## Project Note

Path: `Projects/LLM Phase <n> - <artifact>.md`

```md
---
type: project
status: active
domain: llm
roadmap_phase:
created: YYYY-MM-DD
deadline:
---

# LLM Phase <n> - <Artifact>

> [!note]
> What this artifact proves, current state, hardest open problem.

## Goal

## Success Criteria

## Plan

## Experiments
- 

## Related Concepts
- 

## Results

## Publishable Output
```

## Blog-Ready Metadata

Add to concept/project notes only when close to public:

```yaml
publish: true
blog_status: ready
blog_slug:
audience: technical
```

Never publish daily notes or raw source notes directly.
