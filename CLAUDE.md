@AGENTS.md

# Claude Code Operational Discipline (Anti-Loop & Anti-Bloat)

- Reply to the developer in concise, candid Russian (zero flattery). Keep all Luau code, comments, Blender Python scripts, Studio instance names, and NOTES.md strictly in English to avoid ~3x Cyrillic token overhead.
- **Anti-Loop Search Budget:** Max 8 read/search/inspect calls per turn before reporting or implementing. If `script_search` or `search_game_tree` misses twice, stop searching and ask for the exact path.
- **2-Strike Fix Limit:** If luau-lsp, lune, or a Studio playtest fails twice for the same root cause, STOP editing. Report the exact error trace, two competing hypotheses, and wait for direction.
- **Strict File Whitelist:** Never create helper docs, scratch scripts, or files outside `.claude/allowed_files.txt`. Delete temporary files before finishing your turn.
- **Minimal Diff:** Never refactor untouched modules, add unrequested abstractions, or swallow errors in silent pcall.
- **Session Hygiene:** One clean session = one phase. End every phase by appending a max 6-line status entry to NOTES.md (touched files, CLI/playtest outputs, open [VERIFY] items) and stopping cleanly.
