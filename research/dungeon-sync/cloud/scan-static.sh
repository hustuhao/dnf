#!/usr/bin/env bash
# Analyze ELF files without executing the game server or opening network ports.
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
cd "$root"

bash research/dungeon-sync/cloud/verify-env.sh

if [[ $# -gt 0 ]]; then
  out="$1"
else
  out="research/dungeon-sync/artifacts-local/cloud-scan/$(date -u +%Y%m%dT%H%M%SZ)"
fi
mkdir -p "$out"
out="$(cd "$out" && pwd -P)"
printf 'Git commit: %s\nUTC run: %s\n' "$(git rev-parse HEAD)" "$(date -u +%FT%TZ)" > "$out/provenance.txt"

game="build/dnf_data/home/template/init/df_game_r"
relay="build/dnf_data/home/template/neople/relay/df_relay_r"
stun="build/dnf_data/home/template/neople/stun/df_stun_r"
frida="build/dnf_data/home/template/init/frida.js"

for name in game relay stun; do
  case "$name" in
    game) elf="$game" ;;
    relay) elf="$relay" ;;
    stun) elf="$stun" ;;
  esac
  dest="$out/$name"
  mkdir -p "$dest"
  printf '%s\n' "$elf" > "$dest/source-path.txt"
  git hash-object "$elf" > "$dest/git-blob-sha.txt"
  sha256sum "$elf" > "$dest/sha256.txt"
  file "$elf" > "$dest/file.txt"
  readelf -hW "$elf" > "$dest/elf-header.txt"
  readelf -lW "$elf" > "$dest/program-headers.txt"
  readelf -SW "$elf" > "$dest/sections.txt"
  readelf -Ws "$elf" > "$dest/symbols.txt"
  (readelf -nW "$elf" > "$dest/notes.txt" 2>&1) || true
  (grep -Ei 'CParty|CDungeon|MapInfo|Dungeon|Monster|Damage|Skill|Packet|Drop|Reward|Relay|STUN|P2P' "$dest/symbols.txt" > "$dest/relevant-symbols.txt") || true
  # Local-only strings: never upload raw logs/reports containing embedded data.
  (strings -a -n 8 -t x "$elf" | grep -Ei 'CParty|CDungeon|MapInfo|Dungeon|Monster|Damage|Skill|Packet|Drop|Reward|P2P') > "$dest/relevant-strings.txt" || true
done

python3 research/dungeon-sync/cloud/check-frida-addresses.py \
  --elf "$game" --frida "$frida" \
  --output "$out/game/frida-address-map.csv" \
  2> "$out/game/frida-address-summary.txt"

bash research/dungeon-sync/tools/inspect-game-elf.sh \
  "$game" "$out/game/frida-disassembly"

cat <<MSG
Completed read-only scan: $out
Next: inspect game/frida-address-map.csv and game/frida-disassembly/.
The report is local and gitignored; review/redact before publishing evidence.
No ELF program was executed and no game ports were opened.
MSG
