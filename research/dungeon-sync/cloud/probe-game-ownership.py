#!/usr/bin/env python3
"""Bounded, static-only Game ELF symbol and control-flow probe.

Reads ELF symbols and disassembly, never runs df_game_r. Output is a shortlist
of function addresses / direct machine-code calls, NOT an inferred wire protocol.
"""
import collections
import re
import subprocess
import sys

elf = sys.argv[1] if len(sys.argv) > 1 else "build/dnf_data/home/template/init/df_game_r"
proc = subprocess.run(["nm", "-C", "-S", "-n", "--defined-only", elf],
                      capture_output=True, text=True, errors="replace", check=True)
sym = []
for line in proc.stdout.splitlines():
    match = re.match(r"^([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([A-Za-z])\s+(.+)$", line)
    if match:
        addr, size, kind, name = match.groups()
        if kind.lower() in ("t", "w"):
            sym.append((int(addr, 16), int(size, 16), name))

groups = [
    ("GameManager / party registry", lambda n: "CGameManager::" in n, 110),
    ("Party lifecycle / map / dungeon / user / network", lambda n:
        "CParty::" in n and re.search(
            r"Dungeon|Map|User|user|Game|Room|Host|Monster|Party|Field|Sync|Battle|"
            r"Join|Create|Destroy|Clear|State|Send|Result|Reward|Enter|Exit|Fight|"
            r"Member|Start|Finish|Dead|Drop|GetParty|Init|Remove|Leave", n), 210),
    ("Battle_Field map / monster / room", lambda n:
        "CBattle_Field::" in n and re.search(
            r"Map|Monster|Room|Dungeon|Game|Field|Enter|Exit|Create|Destroy|"
            r"Clear|Add|Find|Get|Process|Update|Sync|Move", n), 110),
    ("Dungeon / MapInfo", lambda n:
        ("CDungeon::" in n or "MapInfo::" in n) and re.search(
            r"get_|Get|Set|Map|Dungeon|Monster|Mob|Drop|Init|Create|Clear|"
            r"Index|index|Add|Del|Destroy", n), 95),
    ("Dungeon / gameplay packet dispatchers", lambda n:
        ("DisPatcher_" in n or "Dispatcher_" in n or "DISPATCHER" in n)
        and re.search(r"Dungeon|Map|Stage|Fight|Monster|Host|Move|Drop|"
                      r"Damage|DieCharac|Skill|StartGame|EndGame|FinishGame|"
                      r"Packet|P2P|Room|Battle", n, re.I), 130),
]
print("SYMBOL_INDEX_V1 ELF=" + elf + " defined_functions=" + str(len(sym)))
for title, test, limit in groups:
    candidates = [(addr, size, name) for addr, size, name in sym if test(name)]
    print(f"\n=== {title}: {len(candidates)} matched; showing {min(limit, len(candidates))} ===")
    for addr, size, name in candidates[:limit]:
        print(f"0x{addr:08X} size=0x{size:X} {name[:190]}")

prefixes = [
    "CGameManager::GetParty(int)",
    "CGameManager::GetPartyIdx(CParty*)",
    "CUser::GetParty()",
    "CParty::get_user(int)",
    "CParty::checkInoutConditionDungeon(",
    "CParty::UseAncientDungeonItems(",
]
print("\n=== TARGETED MACHINE-CODE DISASSEMBLY (ELF symbol boundaries) ===")
for prefix in prefixes:
    found = [(a, s, n) for a, s, n in sym if n.startswith(prefix)]
    if not found:
        print("NOT_FOUND " + prefix)
        continue
    addr, size, name = found[0]
    stop = addr + min(size if size else 256, 640)
    print(f"\nFUNCTION 0x{addr:08X} size=0x{size:X} {name}")
    cmd = ["objdump", "-d", "-M", "intel", f"--start-address={addr}",
           f"--stop-address={stop}", elf]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    lines = [line for line in r.stdout.splitlines()
             if re.match(r"^\s+[0-9a-f]+:", line)]
    for line in lines[:60]:
        print(line[:210])
    if len(lines) > 60:
        print(f"... truncated after 60 of {len(lines)} instructions")
