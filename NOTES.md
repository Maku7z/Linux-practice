# NOTES.md — SHADEWARD 4.0 phase log

## Phase 0 — Greenfield scaffold (2026-11-24)
- Greenfield: no legacy place/repo exists; audit targets empty. See AUDIT_REPORT.md.
- Touched: AGENTS.md, CLAUDE.md, .claude/{settings.json,hooks/agent_guard.py,allowed_files.txt}, rokit.toml, default.project.json, stylua.toml, selene.toml, .luaurc, .gitignore, .github/workflows/ci.yml, SPEC_4_0.md, AUDIT_REPORT.md, NOTES.md. Luau files: 0/29.
- Checks: agent_guard.py tested (whitelisted write exit 0, other write exit 2, 11th search exit 2, --reset ok); JSON/TOML/YAML parse ok. rojo/stylua/selene/luau-lsp NOT run yet (not installed here).
- Open [VERIFY]: rojo 7.7.1 / luau-lsp 1.70.1 pins; stylua/selene/lune/pesde versions; setup-rokit action; luau-lsp definitions URL; Studio MCP server name; late-2026 API typings.
- Open decisions: Script-vs-ModuleScript cross-calls (AUDIT 3.1); lune tests vs 29-file cap (AUDIT 3.2).
- Next: create place in Studio, set Workspace.AuthorityMode = Server, `rokit install`, commit, then Phase 1 in a fresh Opus 5.5 session.
