#!/usr/bin/env bash
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

for tool in bash git python3 file readelf objdump nm strings sha256sum; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "MISSING: $tool" >&2
    exit 2
  fi
done

printf 'Research checkout: %s\nGit HEAD: ' "$root"
git rev-parse HEAD
printf 'Tools: '
readelf --version | head -n 1

for rel in \
  build/dnf_data/home/template/init/df_game_r \
  build/dnf_data/home/template/neople/relay/df_relay_r \
  build/dnf_data/home/template/neople/stun/df_stun_r; do
  if [[ ! -s "$rel" ]]; then
    echo "MISSING ELF: $rel (check clone / LFS / checkout)" >&2
    exit 3
  fi
  if ! readelf -h "$rel" >/dev/null 2>&1; then
    echo "INVALID ELF: $rel" >&2
    exit 4
  fi
  sha="$(git hash-object "$rel")"
  printf '%s | %s | git-blob=%s\n' "$rel" "$(file -b "$rel")" "$sha"
  case "$rel" in
    */init/df_game_r) expected="f7a65ba7bc723e96fadeae07e87b72e05560d989" ;;
    */relay/df_relay_r) expected="c39c47eeb19127a105a0c3309e9b663de81e239a" ;;
    */stun/df_stun_r) expected="9e8e459f5bc1144617213d3141e2c5a740e2bc2c" ;;
    *) expected="" ;;
  esac
  if [[ -n "$expected" && "$sha" != "$expected" ]]; then
    echo "WARNING: binary does not match original v0.4 evidence baseline: $rel" >&2
    echo "Old Frida function names/addresses MUST be revalidated." >&2
  fi
done

echo "OK: Static ELF research prerequisites present."
echo "Run: bash research/dungeon-sync/cloud/scan-static.sh"
