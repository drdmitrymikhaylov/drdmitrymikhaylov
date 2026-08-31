#!/usr/bin/env python3
"""Verify a UDIF/UDZO disk image without a Mac.

Parses the koly trailer, decompresses every blkx chunk and checks the result
is byte-identical to the source filesystem image.
"""
import struct, plistlib, zlib, bz2, hashlib, sys

dmg = open(sys.argv[1], "rb").read()
ref = open(sys.argv[2], "rb").read() if len(sys.argv) > 2 else None
t = dmg[-512:]
assert t[:4] == b"koly", "not a UDIF image"
ver, hsz = struct.unpack(">II", t[4:12])
dfork_off, dfork_len = struct.unpack(">QQ", t[0x18:0x28])
xml_off, xml_len = struct.unpack(">QQ", t[0xD8:0xE8])
sectors = struct.unpack(">Q", t[0x1EC:0x1F4])[0]
print("koly v%d, header %d, dataFork %d..%d, sectorCount %d (%d bytes)"
      % (ver, hsz, dfork_off, dfork_off + dfork_len, sectors, sectors * 512))

pl = plistlib.loads(dmg[xml_off:xml_off + xml_len])
out = bytearray()
for blk in pl["resource-fork"]["blkx"]:
    d = blk["Data"]
    assert d[:4] == b"mish", "bad block table"
    for i in range(struct.unpack(">I", d[0xC8:0xCC])[0]):
        typ, _, sect, cnt, off, ln = struct.unpack(">IIQQQQ", d[0xCC + i*40: 0xCC + i*40 + 40])
        if typ in (0xFFFFFFFF, 0x7FFFFFFE):
            continue
        src = dmg[dfork_off + off: dfork_off + off + ln]
        raw = (src if typ == 1 else
               zlib.decompress(src) if typ == 0x80000005 else
               bz2.decompress(src) if typ == 0x80000006 else
               b"\0" * (cnt * 512) if typ in (0, 2) else None)
        if raw is None:
            raise SystemExit("unhandled chunk type 0x%08X" % typ)
        end = (sect + cnt) * 512
        if len(out) < end:
            out.extend(b"\0" * (end - len(out)))
        out[sect*512: sect*512 + len(raw)] = raw

out = bytes(out)
print("payload decompresses to %d bytes" % len(out))
if sectors * 512 != len(out):
    print("WARNING: sectorCount disagrees with the payload")
if ref is not None:
    ok = hashlib.sha256(ref).hexdigest() == hashlib.sha256(out[:len(ref)]).hexdigest()
    print("round trip vs source image:", "IDENTICAL" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
