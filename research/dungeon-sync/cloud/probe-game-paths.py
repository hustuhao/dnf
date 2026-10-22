#!/usr/bin/env python3
"""ELF-only ownership / packet-dispatch cross-reference report.

Read-only: runs nm and objdump on the checked-out Game ELF; no game processes.
Machine code is evidence of static calls/stores, not evidence of runtime authority.
"""
import collections
import re
import subprocess
import sys

elf=sys.argv[1] if len(sys.argv)>1 else "build/dnf_data/home/template/init/df_game_r"
raw=subprocess.run(["nm","-S","-n","-C","--defined-only",elf],capture_output=True,text=True,check=True).stdout
symbols=[]
seen=set()
for l in raw.splitlines():
    m=re.match(r"^([0-9A-Fa-f]+)\s+([0-9A-Fa-f]+)\s+([A-Za-z])\s+(.+)$",l)
    if not m: continue
    a,size,typ,name=m.groups()
    if typ.lower() not in ("t","w"): continue
    rec=(int(a,16),int(size,16),name)
    if rec not in seen: symbols.append(rec);seen.add(rec)

chosen=[
 "CGameManager::GetParty()",
 "CGameManager::PutParty(",
 "CParty::create_party(",
 "CParty::join_user(",
 "CParty::send_to_party(",
 "CParty::set_host()",
 "CParty::send_host_info(",
 "CParty::send_party_ipinfo(",
 "CParty::dungeon_start(",
 "CParty::move_map(",
 "CParty::kill_monster(",
 "CParty::get_item(",
 "CParty::drop_item(",
 "CParty::dungeon_clear()",
 "CParty::clear_reward(",
 "CBattle_Field::SetParty(",
 "CBattle_Field::GetDungeon()",
 "CBattle_Field::GetCurrentMapInfo()",
 "CBattle_Field::GetMapInfo()",
 "CParty::SetPlayResult(",
]
match={}
for prefix in chosen:
    c=[(a,s,n) for a,s,n in symbols if n.startswith(prefix)]
    if c: match[prefix]=c[0]

print("=== GAMEPLAY OWNERSHIP SYMBOL ADDRESS TABLE ===")
for key in chosen:
    c=match.get(key)
    print(f"{key:44} 0x{c[0]:08X} size=0x{c[1]:X} {c[2]}" if c else "NOT FOUND "+key)

print("\n=== RELEVANT PARTY / BATTLE FIELD ACCESSORS ===")
for a,s,n in symbols:
    if n.startswith("CParty::") and re.search("Battle|Field|MapInfo|Map|Room|host|realtime|P2P|state|index",n,re.I):
        print(f"0x{a:08X} size=0x{s:X} {n[:150]}")
    elif n.startswith("CBattle_Field::") and re.search(r"^(?:CBattle_Field::)(?:[A-Za-z_]*(?:Get|Set|Map|Dungeon|Monster|Party|create|init|start|clear|kill))",n):
        if "std::" not in n and "CBattle_Field::CBattle" not in n:
            print(f"0x{a:08X} size=0x{s:X} {n[:150]}")

print("\n=== SELECTED METHOD MACHINE CODE: ENTRY + RELEVANT DIRECT CALLS ===")
for prefix in chosen:
    if prefix not in match: continue
    a,size,n=match[prefix]
    stop=a+min(size,16000) if size else a+128
    result=subprocess.run(["objdump","-d","-M","intel",f"--start-address={a}",f"--stop-address={stop}",elf],
                          capture_output=True,text=True)
    ins=[l for l in result.stdout.splitlines() if re.match(r"^\s+[0-9a-f]+:",l)]
    calls=[l for l in ins if re.search(r"\bcall\s+\S+",l)]
    rel=[l for l in calls if re.search(
        r"CParty|CBattle_Field|MapInfo|CDungeon|CGameManager|CUser|"
        r"PacketBuf|PacketGuard|CInventory|CMap|GameResult|Drop|Monster|"
        r"send_|ConnectP2P|CUserCharacInfo|StaticPool|hash_map",l,re.I)]
    print(f"\nFUNCTION 0x{a:08X} size=0x{size:X} {n} instructions={len(ins)} direct_call_instructions={len(calls)}")
    print("ENTRY:")
    for l in ins[:min(22,len(ins))]: print("  "+l[:215])
    print("RELEVANT CALLS:")
    for l in rel[:50]: print("  "+l[:215])
    if len(rel)>50: print("  ... truncated relevant calls "+str(len(rel)))

print("\n=== DIRECT CALLERS FOR LIFECYCLE / TRANSPORT METHODS ===")
target_to_name={v[0]:key for key,v in match.items()}
refs=collections.defaultdict(list)
p=subprocess.Popen(["objdump","-d","-M","intel",elf],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,errors="replace")
parent="unknown"
for line in p.stdout:
    label=re.match(r"^([0-9a-f]+) <([^>]+)>:",line)
    if label:parent=label.group(2)[:140]
    m=re.search(r"\bcall\s+([0-9a-f]+)\b",line)
    if m:
        dest=int(m.group(1),16)
        if dest in target_to_name:
            refs[dest].append((parent,line.strip()[:190]))
p.stdout.close();p.wait()
for addr, name in target_to_name.items():
    arr=refs.get(addr,[])
    print(f"{name} 0x{addr:08X} direct_callers={len(arr)}")
    for parent,line in arr[:18]:print("  "+parent+": "+line)
print("objdump_status="+str(p.returncode))
