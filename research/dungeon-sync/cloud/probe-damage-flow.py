#!/usr/bin/env python3
"""Tiny, read-only disassembly window for PvE SDC server-side damage checks.

This script cannot determine network packet IDs or whether client/host is combat authority.
"""
import re
import subprocess
from collections import Counter

GAME="build/dnf_data/home/template/init/df_game_r"
raw=subprocess.run(["nm","-n","-S","-C","--defined-only",GAME],capture_output=True,text=True,check=True).stdout
names={}
for line in raw.splitlines():
    match=re.match(r"^([0-9A-Fa-f]+)\s+([0-9A-Fa-f]+)\s+[tTwW]\s+(.+)$",line)
    if match:
        a,s,n=match.groups()
        names[int(a,16)]=(int(s,16),n)
targets={
    0x08095C32:"computeHpDamageSDC",
    0x08308FF8:"CBattle_Field::SetDamageValue",
    0x08308F4E:"CBattle_Field::SetDamagedPacketCnt",
    0x081E9E84:"Dispatcher_SDC_Damage_Check::dispatch_sig",
    0x081EA16E:"Dispatcher_SDC_ActiveStatus_Damage_Check::dispatch_sig",
}
for addr,label in targets.items():
    entry=names.get(addr)
    if not entry:
        print("NOT_FOUND", hex(addr),label);continue
    size,actual=entry
    print("====="+label+" VA="+hex(addr)+" size="+hex(size)+" ELF_SYMBOL="+actual+"=====")
    end=addr+min(size,0x1600)
    output=subprocess.run(["objdump","-d","-M","intel",f"--start-address={addr}",f"--stop-address={end}",GAME],
                          capture_output=True,text=True,check=True).stdout
    instructions=[ln.strip() for ln in output.splitlines() if re.match(r"^\s+[0-9a-f]+:\s+",ln)]
    print("instruction_count",len(instructions))
    if label.startswith("Dispatcher"):
        for ln in instructions:
            m=re.match(r"([0-9a-f]+):",ln)
            if m and (int(m.group(1),16) in range(0x081E9FF0,0x081EA162) or
                      int(m.group(1),16) in range(0x081EA400,0x081EA610)):
                print(" ",ln[:230])
    else:
        for ln in instructions[:340]:
            print(" ",ln[:230])
        if len(instructions)>340:print("TRUNCATED",len(instructions)-340)
