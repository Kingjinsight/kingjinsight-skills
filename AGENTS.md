# Codex — Global Instructions

## Communication
- Be short, direct, low-fluff.
- Criticize weak ideas when useful; do not over-affirm.
- Ask only when ambiguity changes outcome, safety, or scope.
- When asking, give numbered options and accept compact replies like `1Y 2N`.
- Use numbered lists for options/steps; keep nesting shallow.

## Code Rules
- Minimal diffs. Scope changes to request.
- No change-note comments (`legacy`, `hotfix`, `cleanup`, `removed X`).
- Comment only non-obvious logic, max 2 lines.
- Remove dead code, unused imports, debug prints, and extra blank lines.
- No temporary scaffolding or leftover migration paths.
- Do not add helpers, abstractions, or error handling beyond current need.
- Never skip hooks (`--no-verify`); fix root cause.

## Workflow
- Read existing code/config before editing.
- Use `rg` / `rg --files` for search.
- Use `apply_patch` for manual edits when possible.
- Use `multi_tool_use.parallel` for independent reads/searches.
- Before saying done, run relevant verification or state why not run.
- After 3 failed attempts, summarize failure cause and switch approach.

## Skills
- Use `caveman:caveman` / `/caveman` to save tokens unless clarity or safety would suffer.
- Use `ian-xiaohei-illustrations` / xiaohei for Chinese article summaries, diagrams, workflow visuals, method summaries, or 小黑/Ian-style hand-drawn explanatory images.
- New feature/component → `superpowers:brainstorming` first.
- Bug/test failure → `superpowers:systematic-debugging` first.
- Multi-step implementation plan → `superpowers:writing-plans` before touching code.
- Executing written plan → `superpowers:executing-plans`.
- Parallel independent tasks → `superpowers:subagent-driven-development`.
- Before claiming complete → `superpowers:verification-before-completion`.
- Finishing branch → `superpowers:finishing-a-development-branch`.
- Before merge / major self-review → `superpowers:requesting-code-review`.

## Tool Use
- Use `tool_search` before assuming a plugin/MCP tool is unavailable.
- Use `context7` for external library/framework/API docs.
- Use `playwright` or browser tools for UI verification.
- Use `github` tools or `gh` for PRs, issues, reviews, checks.
- For UI work, verify with browser screenshot when feasible.

## Commits & PRs
- `/commit` → use `caveman-commit` when available; otherwise concise Conventional Commit.
- `/commit-push-pr` → use `github:yeet` when available.
- Do not force-push `main`/`master`.
- Confirm before destructive commands or irreversible git actions.
