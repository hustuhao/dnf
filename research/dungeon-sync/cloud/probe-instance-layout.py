#!/usr/bin/env python3
"""Version-locked, static-only v0.6 ownership supplement. Never executes ELF."""
import hashlib, json, pathlib, re, struct, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
ELF = ROOT / "build/dnf_data/home/template/init/df_game_r"
OUT = ROOT / "research/dungeon-sync/artifacts-local/instance-layout-v06"
EXPECTED = "8859c99d8290dc5fb58151444138cf2697b2bfff12d47d6159596a03f20b5261"

# Independent byte anchors for the documented ownership / lifecycle claims.
ANCHORS = {
    0x082A55B1: "05 24 0b 00 00",
    0x082A55B9: "e8 40 ef ff ff",
    0x082A564A: "8d 90 24 0b 00 00",
    0x082A565A: "e8 5f ed ff ff",
    0x082A58E5: "05 24 0b 00 00",
    0x082A58ED: "e8 aa f0 ff ff",
    0x082A4557: "83 c0 78",
    0x082A455D: "e8 6e 66 00 00",
    0x0822CBC4: "6b c0 64",
    0x0822CC7E: "8d 48 78",
    0x082FF6D7: "89 90 88 01 00 00",
    0x0830ED31: "89 90 a0 01 00 00",
    0x0859ABE2: "e8 0f f6 d6 ff",
    0x0830A33A: "c7 80 88 01 00 00 00 00 00 00",
    0x0830A40E: "e8 db 78 00 00",
    0x085A0DAE: "e8 d3 e6 d5 ff",
    0x082FF943: "e8 8a 38 00 00",
    0x085A1747: "e8 58 79 d6 ff",
    0x085A175C: "e8 ed b9 ff ff",
    0x08590F39: "89 50 40",
    0x085912CB: "89 90 a8 00 00 00",
    0x0859135F: "89 90 b8 00 00 00",
    0x085913A9: "89 90 c0 00 00 00",
    0x08591746: "89 90 28 01 00 00",
    0x08594908: "8b 04 90",
    0x0830BD14: "e8 41 67 e4 ff",
    0x0830D1C4: "e8 7d 47 00 00",
    0x085AA876: "e8 6d 7f ff ff",
    0x086364BC: "e8 13 41 f7 ff",
    0x0859CDC8: "89 50 70",
    0x0859C915: "89 50 74",
    0x0859C91E: "e8 99 04 00 00",
    0x0859CDE5: "c7 44 24 08 1a 00 00 00",
    0x0859CEB5: "c7 44 24 08 0b 00 00 00",
}
TARGETS = [
    0x082A5516, 0x082A57FE, 0x082A44FE, 0x082A499C, 0x082A43BE,
    0x08294E10, 0x08294FC8, 0x082B11AA, 0x082A59CA,
    0x0859A974, 0x0859AD4C, 0x0830A1F6, 0x0822CBCC, 0x0822CC48,
    0x0822CBBE, 0x08300DA6, 0x0835F9F8, 0x081C7E10, 0x081C7F32,
    0x081C8102, 0x085A0954, 0x082FF486, 0x082FFB30, 0x083031D2,
    0x083090A4, 0x085B1FE0, 0x081EB0C4, 0x085A27E8, 0x0830BC78,
    0x085AA5D4, 0x0863647E, 0x0859CDBC, 0x0859CDD2, 0x0859CEA2,
    0x0859A48C, 0x0859C114, 0x0859C832, 0x0859C978, 0x081F088E,
    0x0859D14E, 0x08590A2E, 0x085948E2, 0x08594922, 0x08258956,
    0x081C335C, 0x081C47BA, 0x081FF7DE,
]
data = ELF.read_bytes()
assert hashlib.sha256(data).hexdigest() == EXPECTED, "ELF version mismatch"
assert data[:6] == b"\x7fELF\x01\x01" and struct.unpack_from("<H", data, 18)[0] == 3
phoff = struct.unpack_from("<I", data, 28)[0]
phsize, phnum = struct.unpack_from("<HH", data, 42)
segments = [struct.unpack_from("<8I", data, phoff+i*phsize) for i in range(phnum)]

def read_va(va, size):
    for typ, off, base, _, filesz, _, flags, _ in segments:
        if typ == 1 and flags & 1 and base <= va and va+size <= base+filesz:
            return data[off+va-base:off+va-base+size]
    raise ValueError(f"Not in executable PT_LOAD: {va:#x}")

VTABLE = {0x08BDBDC8: 0x08258956, 0x08BDBDDC: 0x081C7E10,
          0x08BDBDE0: 0x081C8102, 0x08BDBDE4: 0x081C8E9C}
for va, target in VTABLE.items():
    assert read_va(va, 4) == struct.pack("<I", target), f"Vtable mismatch: {va:#x}"
assert read_va(0x0859527C, 6) == bytes.fromhex("c7 00 c8 bd bd 08")

for va, expected in ANCHORS.items():
    expected = bytes.fromhex(expected)
    assert read_va(va, len(expected)) == expected, f"Byte anchor mismatch: {va:#x}"
OUT.mkdir(parents=True, exist_ok=True)
symbols = subprocess.check_output(["nm", "-S", "-n", "-C", "--defined-only", str(ELF)], text=True)
by_addr = {}
for line in symbols.splitlines():
    m = re.match(r"^([0-9a-f]+)\s+([0-9a-f]+)\s+[TWtw]\s+(.+)$", line)
    if m:
        by_addr[int(m[1],16)] = (int(m[2],16), m[3])
for va in TARGETS:
    size, name = by_addr[va]
    asm = subprocess.check_output(["objdump","-d","-C","-M","intel",
        f"--start-address={va}",f"--stop-address={va+size}",str(ELF)], text=True)
    (OUT/f"{va:08x}.asm").write_text(asm)

# Enumerate all direct callers, including the timeout death path; no xref truncation.
refs = {va: [] for va in TARGETS}
proc = subprocess.Popen(["objdump","-d","-C","-M","intel",str(ELF)],stdout=subprocess.PIPE,text=True)
parent = ""
for line in proc.stdout:
    m = re.match(r"^([0-9a-f]+) <([^\n]+)>:",line)
    if m:
        parent = m[2]
    c = re.search(r"\bcall\s+([0-9a-f]+)\b",line)
    if c and int(c[1],16) in refs:
        refs[int(c[1],16)].append({"caller":parent,"instruction":line.strip()})
assert proc.wait() == 0
report = {"sha256":EXPECTED, "anchors":len(ANCHORS), "functions":len(TARGETS),
          "select_dungeon_vtable": {f"{va:08x}": f"{target:08x}" for va,target in VTABLE.items()},
          "direct_xrefs":{f"{va:08x}":r for va,r in refs.items()}}
(OUT/"summary.json").write_text(json.dumps(report,indent=2))
print(f"PASS ELF32/x86 SHA256; {len(ANCHORS)} byte anchors; {len(TARGETS)} complete functions")
print("Raw output (gitignored):",OUT.relative_to(ROOT))
