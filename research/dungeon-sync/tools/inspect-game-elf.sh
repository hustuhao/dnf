#!/usr/bin/env bash
# Read-only static inspection: run from the authorized repository checkout root (Linux).
set -euo pipefail
BIN="build/dnf_data/home/template/init/df_game_r"
OUT="research/dungeon-sync/artifacts-local"
if [[ $# -ge 1 ]]; then BIN="$1"; fi
if [[ $# -ge 2 ]]; then OUT="$2"; fi
[[ -f "$BIN" ]] || { echo "Missing ELF: $BIN" >&2; exit 2; }
for cmd in file sha256sum readelf objdump strings; do
  command -v "$cmd" >/dev/null || { echo "Missing tool: $cmd" >&2; exit 3; }
done
mkdir -p "$OUT"
file "$BIN" > "$OUT/file.txt"
sha256sum "$BIN" > "$OUT/sha256.txt"
readelf -hW "$BIN" > "$OUT/header.txt"
readelf -lW "$BIN" > "$OUT/program-headers.txt"
readelf -SW "$BIN" > "$OUT/sections.txt"
readelf -Ws "$BIN" > "$OUT/symbols.txt"
readelf -nW "$BIN" > "$OUT/notes.txt" 2>&1 || true
(strings -a -t x "$BIN" | grep -Ei 'CParty|CDungeon|MapInfo|Monster|Damage|Skill|Packet|Drop|Reward|Relay|P2P') > "$OUT/strings.txt" || true
: > "$OUT/frida-addresses.txt"
: > "$OUT/disassembly-unverified.txt"
# These addresses come from frida.js annotations, and MUST be version-checked.
for pair in \
  '0x080FDCF0 CDungeon_get_index' \
  '0x0865514C CUser_GetParty' \
  '0x08145764 CParty_get_user' \
  '0x0859EAC2 CParty_UseAncientDungeonItems' \
  '0x08151612 MapInfo_Add_Mob' \
  '0x086B330A SendVillageMonsterFightResult' \
  '0x086485BA CUser_Send' \
  '0x0858D27E PacketBuf_get_int' \
  '0x08632A18 TimerDispatcher_dispatch'; do
  read -r address label <<< "$pair"
  printf '%s %s\n' "$address" "$label" >> "$OUT/frida-addresses.txt"
  printf '\n=== %s %s : UNVERIFIED ADDRESS ===\n' "$address" "$label" >> "$OUT/disassembly-unverified.txt"
  lo=$((address))
  hi=$((lo + 128))
  objdump -d -M intel --start-address="$lo" --stop-address="$hi" "$BIN" >> "$OUT/disassembly-unverified.txt" 2>&1 || true
done
echo "Static ELF report written to: $OUT"
echo "Verify ELF matching and executable PT_LOAD mapping before attaching function names to addresses."
echo "The script never executes the target ELF."
