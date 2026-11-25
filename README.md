# kingjinsight-skills

My own agent skills. Each one is a folder with a `SKILL.md` in the [Agent Skills](https://agentskills.io) format, so it works in Claude Code, Codex and other agents that read skills.

| Skill | What it does |
|---|---|
| [distill](skills/distill) | Turns a conversation or an article into a note in my Obsidian vault when I say "沉淀一下". |
| [editorial-collage](skills/editorial-collage) | Makes archival-collage covers and banners for posts, in the style of Anthropic's site illustrations. |
| [king-handdrawn-illustrations](skills/king-handdrawn-illustrations) | Plans and draws 16:9 hand-drawn illustrations for Chinese articles, starring my character. |
| [llm-wiki-learning](skills/llm-wiki-learning) | Writes and organizes LLM notes in my Obsidian vault. |
| [storage-analyzer](storage-analyzer) | Finds what fills the disk on Arch Linux and builds a cleanup report with move-to-trash buttons. Linux only. |

distill and llm-wiki-learning follow my vault's layout. Before using distill, replace the `<...>` placeholders with your own vault path and repo.

## Install

Ask your agent "Install this skill for me: <link to the skill folder>", or copy the folder into your agent's skills directory (`~/.claude/skills/` for Claude Code, `~/.codex/skills/` for Codex). Start a new session afterwards.

## License

[MIT](LICENSE)
