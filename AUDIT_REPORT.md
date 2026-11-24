# AUDIT_REPORT.md — SHADEWARD 4.0, Phase 0 (Greenfield)

Date: 2026-11-24. Source of truth: "SHADEWARD 4.0 — AI-Native TDD, Agent Rules, & Step-by-Step Build Prompts" (45 pp).

## 1. Exact Inventory & Legacy Debt
- **There is no legacy place.** The developer confirmed the project starts from zero: no Roblox place, no repository, no 6-scene OpenAI prototype, no `.blend` files.
- The Phase 0 audit targets in the TDD (client-authoritative remotes, `Lighting.Technology`, `FilterDescendantsInstances`, `UnionOperation` walls, stray `Highlight`, floating `BillboardGui` hints, legacy `Sound`, untimed `WaitForChild`) therefore have **nothing to inspect**. Legacy debt = 0.
- No Studio MCP calls were made in Phase 0.
- Repository scaffold created (non-Luau, so it does not count toward the 29-file budget):
  - Rule pack: `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/agent_guard.py` (transcribed from TDD Part II).
  - `.claude/allowed_files.txt` set to the Phase 1 whitelist.
  - Toolchain: `rokit.toml`, `default.project.json`, `stylua.toml`, `selene.toml`, `.luaurc`, `.gitignore`, `.github/workflows/ci.yml`.
  - `src/shared`, `src/server`, `src/client` (empty, `.gitkeep` only). Luau files: 0 / 29.
  - `SPEC_4_0.md`: the TDD formulas that exist only as images in the PDF (Glicko-2, latency score).

## 2. Repurpose / Quarantine Matrix
- Nothing to repurpose or quarantine. The fixed symmetric arena (Sectors 1-4: BoardingWing 110 st, FloodedCollector 170 st, ShadowGreenhouse 230 st, EclipseHall 300 st) and the AmberHearth Hub are built from scratch in Phase 1.
- Phase 1 Step 1 ("quarantine legacy OpenAI clutter via `execute_luau`") becomes a no-op on a fresh place.

## 3. Spec Issues Found While Scaffolding (Candor Over Compliance)
1. **Script-to-script calls are impossible as written.** Rojo maps `*.server.luau` to `Script`, and a `Script` cannot be `require()`d. Yet Phase 3 has `MatchOrchestrator` call `WorldBootstrap.preStreamAndRelocate`, and Phase 5/7 services need `LagCompensation`, `DataService` profiles, and `AcousticBus` from other scripts. Options: (a) rename shared services to ModuleScripts (`WorldBootstrap.luau`) with one boot Script, or (b) keep Scripts and expose APIs via `BindableFunction`/`BindableEvent`. Option (a) keeps the file count at 29 but changes whitelisted file names. **Decision needed before Phase 1** (it fixes the name of `WorldBootstrap`).
2. **Lune tests vs. the 29-file cap and whitelists.** Phases 2, 3, 5, 7 require `lune` tests (codec, Glicko-2 fixtures, raid/owl/gadget, receipts), but no phase whitelists a test file and every test file is Luau. Either test files are exempt from the 29-file cap and get added to the whitelists (proposed: `tests/<Module>.spec.luau`), or the gate cannot be met.
3. **Pure modules required from lune.** `SnapshotCodec`, `Glicko2`, scoring math must not touch Roblox globals at require time so lune can load them; `ScoringAndRaidService.server.luau` is a Script, so its raid math is not testable by lune unless split into a module (affects Phase 5 acceptance test).
4. **Search budget mismatch.** `CLAUDE.md` says max 8 read/search calls per turn; `agent_guard.py` blocks only after 10 searches and does not count `Read` or Studio `inspect_instance`. Kept as written in the TDD.
5. **Guard bypass.** `agent_guard.py` checks only `Write`/`Edit`; file writes via `Bash` or `NotebookEdit` skip the whitelist. Kept as written; low risk if agents follow `CLAUDE.md`.
6. **MCP server name.** `.claude/settings.json` uses `Roblox_Studio`; the real name on the developer's machine must be read from `/mcp`. [VERIFY]
7. **Tool pins.** TDD pins `rojo@7.7.1` and `luau-lsp@1.70.1`; publicly confirmed releases are `rojo 7.7.0` and `luau-lsp 1.70.0`. [VERIFY] before `rokit install`.
8. **Late-2026 API typings.** `Player:GetCameraState()`, `RaycastParams.ExcludeInstances/IncludeInstances`, `Enum.AuthorityMode`, `RunService:BindToSimulation()`, `MarketplaceService:BindReceiptHandler()` must exist in the luau-lsp definitions file, or `luau-lsp analyze` fails the gate. [VERIFY] in Phase 1/2.
9. Glicko-2 fixtures were spot-checked by hand: Duos even #1 +25.3 (RD 77.8) and #2 +8.4 reproduce with the SPEC_4_0.md formulas (w = 0.5, volatility held at 0.06). Full check is the Phase 3 gate.

## 4. What Requires Roblox Studio on the Developer's Machine
- Create the new place (Baseplate removed or kept as Hub placeholder) and save `.rbxl` backup.
- Manually set `Workspace.AuthorityMode = Server` (protected property, cannot be scripted). This also turns on StreamingEnabled, Deferred signals, fixed simulation, IAS for PlayerScripts.
- Install the Rojo Studio plugin matching the Rojo version and connect `rojo serve`.
- Connect Studio MCP to Claude Code and confirm the server name.
- Place-only settings (`ModelStreamingBehavior = Improved`, Lighting) are done via Studio MCP in Phase 1, not via Rojo.

## 5. Blocking Questions (max 3)
1. Issue 3.1: ModuleScript services or Bindable-based Scripts? Recommendation: **Bindables** (e.g. `WorldBootstrap.server.luau` exposes a server-only `BindableFunction` `PreStreamAndRelocate`). It keeps every whitelisted file name and the 29-file cap; ModuleScripts would need extra boot Scripts to run in Phase 1.
2. Issue 3.2: may lune tests live in `tests/` outside the 29-file Luau budget?
3. Has the place been created and `Workspace.AuthorityMode` set to `Server` in Studio, and what is the Studio MCP server name in `/mcp`?
