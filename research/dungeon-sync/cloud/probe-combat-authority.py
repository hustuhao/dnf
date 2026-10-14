#!/usr/bin/env python3
"""Bounded, static-only battle authority probe against df_game_r.
Print symbol metadata, selected disassembly and exact direct callers.
Does not run DNF server or perform any network activity.
"""
import collections
import re
import subprocess
import sys

ELF = sys.argv[1] if len(sys.argv) > 1 else "build/dnf_data/home/template/init/df_game_r"

def execute(argv):
    return subprocess.run(argv, capture_output=True, text=True, errors="replace", check=True).stdout

def symbol_entries():
    found = []
    for line in execute(["nm", "-n", "-S", "-C", "--defined-only", ELF]).splitlines():
        m = re.match(r"^([a-fA-F0-9]+)\s+([a-fA-F0-9]+)\s+([A-Za-z])\s+(.+)$", line)
        if not m: continue
        a, s, kind, name = m.groups()
        if kind.lower() not in ("t", "w"): continue
        found.append((int(a, 16), int(s, 16), name))
    return found

symbols = symbol_entries()
targets = [
    "CBattle_Field::SetDamageValue(",
    "CBattle_Field::SetDamagedPacketCnt(",
    "CBattle_Field::kill_monster(",
    "CBattle_Field::GetFieldMob(",
    "CParty::use_skill(",
    "CParty::OnKilledMonster(",
    "CParty::MemberRegisterKillMonster(",
    "CParty::CheckHackAverageHitCount(",
    "CParty::ClearMapHitCount(",
    "CParty::kill_monster(",
    "CParty::ConnectP2P(",
    "CParty::send_host_info(",
    "CParty::send_to_party(",
    "DisPatcher_DieMob::dispatch_sig(",
    "DisPatcher_ResPeer::dispatch_sig(",
]
print("BATTLE_PROBE_V1: STATIC ONLY", ELF)
print("=== DAMAGE/HIT/SKILL/PEER RELATED SYMBOL SHORTLIST ===")
shortlist = [
    (a, size, name) for a, size, name in symbols
    if (
        ("CBattle_Field::" in name or "CParty::" in name or "DisPatcher" in name
         or "Dispatcher" in name or "Packet" in name or "Monster" in name)
        and re.search(r"Damage|Damaged|Hurt|Hit|Hitted|Attack|Skill|Hack|P2P|"
                      r"Peer|Host|DieMob|KillMonster|Combat|Bullet|HP|AI|Fight",
                      name, flags=re.I)
        and not re.search(r"std::|_M_|allocator|vector|map<|less<|basic_string",
                          name)
    )
]
print("related_function_count", len(shortlist))
for a, size, name in shortlist[:180]:
    print(f"SYMBOL 0x{a:08X} size=0x{size:X} {name[:180]}")
if len(shortlist) > 180:
    print("TRUNCATED symbols", len(shortlist) - 180)

selected = {}
for key in targets:
    candidate = [entry for entry in symbols if entry[2].startswith(key)]
    if candidate:
        selected[key] = candidate[0]

print("\n=== TARGETED ENTRY INSTRUCTIONS AND NAMED CALL SITES ===")
for key in targets:
    sym = selected.get(key)
    if not sym:
        print("NOT_FOUND", key)
        continue
    addr, length, name = sym
    upper = addr + min(length if length else 160, 16384)
    disasm = execute(["objdump", "-d", "-M", "intel",
                      f"--start-address={addr}", f"--stop-address={upper}", ELF])
    rows = [s.strip() for s in disasm.splitlines()
            if re.match(r"^\s+[0-9a-fA-F]+:\s+", s)]
    calls = [s for s in rows if re.search(r"\bcall\s+", s)]
    relevant = [s for s in calls
                if re.search(r"CParty|CBattle|Damage|Hit|Monster|Skill|"
                             r"Kill|Dungeon|Item|Host|P2P|Packet|Field|"
                             r"GameWorld|CUser|DisPatcher|Anti|Check|"
                             r"get_|send_|Update", s, re.I)]
    print(f"\nTARGET {name} VA=0x{addr:08X} size=0x{length:X} "
          f"instr_count={len(rows)} total_calls={len(calls)}")
    print("ENTRY first 42:")
    for s in rows[:42]: print(" ", s[:235])
    print("RELEVANT DIRECT CALLS first 60:")
    for s in relevant[:60]: print(" ", s[:235])
    if len(relevant) > 60: print("  TRUNCATED_RELEVANT_CALLS", len(relevant) - 60)

print("\n=== DIRECT CALLER XREFS / SELECTED TARGET FUNCTIONS ===")
address_map = {sym[0]: name for name, sym in selected.items()}
xref = collections.defaultdict(list)
p = subprocess.Popen(["objdump", "-d", "-M", "intel", ELF],
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                     text=True, errors="replace")
owner = "unknown"
for line in p.stdout:
    m = re.match(r"^[0-9a-fA-F]+ <([^>]+)>:", line)
    if m: owner = m.group(1)[:190]
    c = re.search(r"\bcall\s+([0-9a-fA-F]+)\b", line)
    if c:
        destination = int(c.group(1), 16)
        if destination in address_map:
            xref[destination].append((owner, line.strip()[:235]))
p.stdout.close()
p.wait()
print("objdump_exit_status", p.returncode)
for addr, name in address_map.items():
    callers = xref.get(addr, [])
    print(f"CALLERS {name} 0x{addr:08X} n={len(callers)}")
    for owner, instruction in callers[:32]:
        print("  ", owner, ":", instruction)
    if len(callers) > 32: print("  TRUNCATED_CALLERS", len(callers) - 32)
