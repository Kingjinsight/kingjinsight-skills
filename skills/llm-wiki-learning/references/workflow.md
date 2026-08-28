# Workflow Reference

Use this when organizing, ingesting, writing back, or linting King's LLM wiki.

## Principle

Do not turn every note into wiki. A good learning wiki has layers:

```text
raw source / daily trace
-> source index
-> concept notes
-> topic maps
-> project or experiment artifacts
-> public blog when polished
```

## Layers In King's Vault

| Layer | Path | Role |
|---|---|---|
| Daily capture | `Daily Notes/YYYY-MM/` | Raw daily learning trace, not permanent concept storage |
| Source layer | `Resources/LLM/` | Papers, reports, links, source cards, chat extracts |
| Wiki layer | `Knowledge/LLM/Topics/`, `Knowledge/LLM/Concepts/` | Topic routers and reusable concepts |
| Process layer | `Knowledge/LLM/Experiments/` | Experiment results, debug logs, ablations |
| Project layer | `Projects/` | Multi-week artifacts and capstones |
| Blog layer | notes with `publish: true` | Only polished public output |

## Request Routing

| Input | Output |
|---|---|
| "I learned X today" | daily learning block; maybe concept seed |
| "Explain X" | learning session; offer concept note |
| "We discussed X, write it down" | update/create concept note |
| Paper/report/link | source note + source index + candidate concepts |
| Code experiment | experiment log + concept/project updates |
| Multi-week artifact | project note + experiment logs |
| "Make this clearer visually" | Mermaid or Canvas depending complexity |

## Source Status

Use these exact statuses in `Knowledge/LLM/Source Index.md`:

| Status | Meaning |
|---|---|
| `raw` | saved but not processed |
| `summarized` | summary exists |
| `extracted` | concept candidates extracted |
| `integrated` | concepts/topic maps updated |
| `archived` | kept for reference, no active processing |

## Ingest Flow

1. Identify source type: `paper`, `report`, `code`, `experiment-log`, `chat-note`, `raw-note`.
2. Preserve original source. Do not overwrite PDF/source/raw extract.
3. Create/update source card under `Resources/LLM/`.
4. Update `Knowledge/LLM/Source Index.md`.
5. Extract candidate concepts.
6. Search existing concepts; update before creating.
7. Create concept note only when it explains one reusable technical idea.
8. Update relevant topic map only for stable concepts.
9. If linked to project or experiment, update that note too.

## Concept Writeback Flow

1. Read relevant topic map and existing concepts.
2. Decide note type:
   - one technical idea -> concept
   - one report/paper -> source/analysis
   - one run/debug/result -> experiment
   - multi-week artifact -> project
3. Write in King's understanding, not generic source summary.
4. Use callouts for key summary and pitfalls.
5. Add graph location: `Belongs to`, `Related`, `Used in`.
6. Add sources or mark `source: conversation` when from chat only.
7. Update topic map if note reaches `developing` or stronger.

## Topic Map Rules

Topic pages are routers. They should contain:

- topic positioning
- boundaries: belongs here / belongs elsewhere
- concept map table
- recommended reading order
- key sources
- project/artifact links
- open questions

Avoid:

- dumping raw papers into topic map
- linking every concept from `LLM Full Flow`
- making topic pages too granular before content exists

Split a topic only when it has 5-8 stable concept notes.

## Graph Rules

Only these are graph nodes:

- `LLM Full Flow`
- topic pages
- concept pages

These are not graph nodes:

- daily notes
- source notes
- paper/report summaries
- experiment logs
- project logs
- templates/rules

They may link to graph nodes, but should not be treated as durable concept nodes.

## Study Session Pattern

Use this when user is learning a concept:

1. Ask: "What is your current guess?"
2. Explain mechanism.
3. Give one minimal exercise.
4. Ask user for 3-sentence summary.
5. Identify next source/paper/code.
6. Offer writeback target.

If user wants speed or already knows topic, reduce Socratic friction and move to artifact.

## Daily Learning Block

Suggest adding this to daily note:

```md
## LLM Learning
- Roadmap phase:
- Source:
- Solo attempt:
- 3-sentence summary:
- What clicked:
- What confused me:
- Code/exercise:
- Link to concept:
- Blog potential: no / maybe / yes
```

## Lint Flow

Run after 5 new LLM notes, a topic rewrite, source batch, or before publishing:

- orphan concept notes?
- duplicate/synonym concept notes?
- concept missing topic?
- concept missing two related links?
- topic not updated?
- source status stale?
- experiment/project results worth abstracting?
- `待验证` claims still unresolved?
- blog notes have proper source/support?

Report first; edit only if user asked.
