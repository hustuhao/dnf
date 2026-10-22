#!/usr/bin/env python3
"""Map Frida ptr(0x...) literals into an ELF's PT_LOAD segments.

Static only. Segment membership is NOT function identity or ABI validation.
Works with ELF32/ELF64, little-/big-endian, with no third-party packages.
"""
import argparse
import csv
import re
import struct
import sys
from pathlib import Path

PTR_RE = re.compile(r"\bptr\s*\(\s*(0[xX][0-9a-fA-F]+)\s*\)")

def segments_from_elf(path: Path):
    with path.open("rb") as f:
        h = f.read(64)
        if len(h) < 52 or h[:4] != b"\x7fELF" or h[4] not in (1, 2):
            raise ValueError("Not a supported ELF32/ELF64 file")
        if h[5] not in (1, 2):
            raise ValueError("Unsupported byte order")
        endian = "<" if h[5] == 1 else ">"
        bits = 32 if h[4] == 1 else 64
        e_type = struct.unpack_from(endian + "H", h, 16)[0]
        if bits == 32:
            phoff = struct.unpack_from(endian + "I", h, 28)[0]
            phentsize, phnum = struct.unpack_from(endian + "HH", h, 42)
        else:
            phoff = struct.unpack_from(endian + "Q", h, 32)[0]
            phentsize, phnum = struct.unpack_from(endian + "HH", h, 54)
        if phnum == 0xffff:
            raise ValueError("Extended program-header counts are not supported")
        segments = []
        for i in range(phnum):
            f.seek(phoff + i * phentsize)
            raw = f.read(phentsize)
            fmt = endian + ("IIIIIIII" if bits == 32 else "IIQQQQQQ")
            if len(raw) < struct.calcsize(fmt):
                raise ValueError("Truncated program header")
            entry = struct.unpack_from(fmt, raw)
            if bits == 32:
                p_type, _, vaddr, _, _, memsz, flags, _ = entry
            else:
                p_type, flags, _, vaddr, _, _, memsz, _ = entry
            if p_type == 1:
                segments.append((vaddr, vaddr + memsz, flags))
    return bits, e_type, segments


def classify(address: int, segments):
    for begin, end, flags in segments:
        if begin <= address < end:
            return "executable-PT_LOAD" if flags & 1 else "nonexecutable-PT_LOAD"
    return "outside-PT_LOAD"


def inspect(elf: Path, frida: Path, writer):
    bits, e_type, segments = segments_from_elf(elf)
    counts = {}
    total = 0
    for lineno, line in enumerate(frida.read_text(encoding="utf-8").splitlines(), 1):
        for match in PTR_RE.finditer(line):
            address = int(match.group(1), 16)
            result = classify(address, segments)
            kind = ("NativeFunction" if "NativeFunction" in line else
                    "Interceptor" if "Interceptor." in line else "other-ptr")
            writer.writerow([lineno, hex(address), result, kind, line.strip()[:180]])
            counts[result] = counts.get(result, 0) + 1
            total += 1
    print(
        f"ELF{bits} e_type={e_type} PT_LOAD_segments={len(segments)} "
        f"Frida_ptr_occurrences={total} categories={counts}", file=sys.stderr
    )
    if e_type == 3:
        print(
            "WARNING: ET_DYN (PIE/shared object): absolute Frida addresses may "
            "need load-base relocation before matching.", file=sys.stderr
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--elf", type=Path, required=True)
    parser.add_argument("--frida", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="CSV destination (default stdout)")
    args = parser.parse_args()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["frida_line", "address", "segment_status", "kind", "source"])
            inspect(args.elf, args.frida, writer)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(["frida_line", "address", "segment_status", "kind", "source"])
        inspect(args.elf, args.frida, writer)


if __name__ == "__main__":
    main()
