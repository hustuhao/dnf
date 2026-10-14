# Dungeon-sync research agent instructions

Scope: `research/dungeon-sync/`. Study the shipped DNF build, **not** generic MMO design.

1. Start with `cloud/README.md`, `README.md`, `evidence.md`, `open-questions.md`.
2. First run `bash research/dungeon-sync/cloud/verify-env.sh`, then the static-only `cloud/scan-static.sh`. Static ELF inspection is allowed; do not run game binaries, publish network ports, or connect to third-party game servers.
3. The first P0 question is whether the hardcoded addresses in `frida.js` map to executable `PT_LOAD` regions in **this exact** `df_game_r` and what actual functions/callers they resolve to.
4. For an identified entry, collect: path, Git blob SHA + SHA256, executable format and load base, VA, caller and callee evidence, inspected assembly, uncertainty. Never invent decoded opcodes, protocol IDs, host behavior, or experiments.
5. Prioritize `CParty::UseAncientDungeonItems`, `CDungeon_get_index`, `MapInfo::Add_Mob`, `CUser_Send`, `PacketBuf_get_*`, then packet dispatch and dungeon lifecycle.
6. Keep **normal dungeon mechanics** separate from Frida's special village-monster activity hooks. Never claim the server is authoritative for movement, AI, or damage unless proven.
7. Write evidence-backed Markdown changes to `evidence.md`, `architecture.md`, `combat-sync.md`, `network-protocol.md`, `open-questions.md` and add concise Mermaid diagrams when useful.
8. Raw outputs, ELF strings, packet captures, account identifiers, passwords and dumps remain in gitignored `artifacts-local/`; inspect/redact before any public commit.
9. Use only an authorized isolated environment for dynamic experiments; do not operate untrusted server binaries by default.
