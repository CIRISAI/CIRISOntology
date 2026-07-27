#!/usr/bin/env python3
"""Selective member fetch from the GlassBench zip on Zenodo, by HTTP range.

Zenodo serves HTTP/206 on this object (verified), and the zip carries a zip64
central directory. So the whole 6.04 GB archive never has to land on a disk that
is 98% full: parse the central directory once, then pull only the members a
stage actually needs.

Usage:
  python3 glass_zipfetch.py list
  python3 glass_zipfetch.py get <member-name> <outfile>
"""
import json
import os
import struct
import subprocess
import sys

# NOTE (2026-07-27): the /api/records/.../files/.../content endpoint answers small
# ranges but 504s on anything above a few MB.  The plain download URL serves the
# same object with working ranges at ~645 kB/s sustained.  Both were measured.
URL = "https://zenodo.org/records/10118191/files/GlassBench.zip?download=1"
ZIPSIZE = 6042260027
CHUNK = 32 << 20
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glass_zip_cd.json")


def _curl_range(start, end, out, tries=8):
    """One range, retried with backoff.  Zenodo intermittently 504s."""
    for attempt in range(tries):
        r = subprocess.run(
            ["curl", "-s", "-m", "900", "-r", f"{start}-{end}", URL,
             "-o", out, "-w", "%{http_code}"], capture_output=True, text=True)
        code = r.stdout.strip()
        got = os.path.getsize(out) if os.path.exists(out) else 0
        if code in ("206", "200") and got == end - start + 1:
            return out
        sys.stderr.write(f"  retry {attempt+1}: HTTP {code}, {got}/{end-start+1} B\n")
        sys.stderr.flush()
        subprocess.run(["sleep", str(5 * (attempt + 1))])
    raise RuntimeError(f"range {start}-{end} failed after {tries} tries")


def _curl_span(start, length, out):
    """Fetch [start, start+length) into `out`, resumable in CHUNK pieces.

    A partial `out` from an earlier run is kept and the fetch resumes at its
    length, so a 504 mid-transfer costs one chunk rather than the whole member.
    """
    done = os.path.getsize(out) if os.path.exists(out) else 0
    if done > length:
        raise RuntimeError(f"{out} is longer than the member; delete it")
    tmp = out + ".chunk"
    with open(out, "ab") as fo:
        while done < length:
            n = min(CHUNK, length - done)
            _curl_range(start + done, start + done + n - 1, tmp)
            fo.write(open(tmp, "rb").read())
            fo.flush()
            done += n
            sys.stderr.write(f"  {out}: {done}/{length} "
                             f"({100.0*done/length:.1f}%)\n")
            sys.stderr.flush()
    if os.path.exists(tmp):
        os.remove(tmp)
    return out


def central_directory():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    tail = "/tmp/_gb_tail.bin"
    _curl_range(ZIPSIZE - 100000, ZIPSIZE - 1, tail)
    d = open(tail, "rb").read()
    j = d.rfind(b"PK\x06\x06")
    if j < 0:
        raise RuntimeError("no zip64 EOCD")
    z = struct.unpack("<IQHHIIQQQQ", d[j:j + 56])
    nrec, cdsize, cdoff = z[7], z[8], z[9]
    cd = "/tmp/_gb_cd.bin"
    _curl_range(cdoff, cdoff + cdsize - 1, cd)
    d = open(cd, "rb").read()
    off, out = 0, []
    while off < len(d) - 4 and d[off:off + 4] == b"PK\x01\x02":
        (_sig, _vmb, _vne, _flg, meth, _mt, _md, crc, csz, usz,
         nlen, elen, clen, _dsk, _ia, _ea, lho) = struct.unpack(
            "<IHHHHHHIIIHHHHHII", d[off:off + 46])
        name = d[off + 46:off + 46 + nlen].decode("utf-8", "replace")
        extra = d[off + 46 + nlen:off + 46 + nlen + elen]
        if 0xFFFFFFFF in (usz, csz, lho):
            eo = 0
            while eo < len(extra) - 3:
                hid, hsz = struct.unpack("<HH", extra[eo:eo + 4])
                body = extra[eo + 4:eo + 4 + hsz]
                if hid == 1:
                    p = 0
                    if usz == 0xFFFFFFFF:
                        usz = struct.unpack("<Q", body[p:p + 8])[0]; p += 8
                    if csz == 0xFFFFFFFF:
                        csz = struct.unpack("<Q", body[p:p + 8])[0]; p += 8
                    if lho == 0xFFFFFFFF:
                        lho = struct.unpack("<Q", body[p:p + 8])[0]; p += 8
                eo += 4 + hsz
        out.append(dict(name=name, method=meth, csize=csz, usize=usz, lho=lho,
                        crc32=crc))
        off += 46 + nlen + elen + clen
    json.dump(out, open(CACHE, "w"), indent=1)
    return out


def fetch(name, outfile):
    ents = {e["name"]: e for e in central_directory()}
    if name not in ents:
        raise SystemExit(f"no such member: {name}")
    e = ents[name]
    # local file header: 30 fixed bytes + name + extra (its own lengths)
    hdr = "/tmp/_gb_lfh.bin"
    _curl_range(e["lho"], e["lho"] + 29, hdr)
    h = open(hdr, "rb").read()
    assert h[:4] == b"PK\x03\x04", h[:4]
    nlen, elen = struct.unpack("<HH", h[26:30])
    data0 = e["lho"] + 30 + nlen + elen
    raw = outfile + (".raw" if e["method"] != 0 else "")
    if e["csize"] <= CHUNK:
        _curl_range(data0, data0 + e["csize"] - 1, raw)
    else:
        _curl_span(data0, e["csize"], raw)
    if e["method"] == 0:
        return outfile
    if e["method"] == 8:
        import zlib
        dec = zlib.decompressobj(-15)
        crc, n = 0, 0
        with open(raw, "rb") as fi, open(outfile, "wb") as fo:
            while True:
                chunk = fi.read(1 << 20)
                if not chunk:
                    break
                b = dec.decompress(chunk)
                crc = zlib.crc32(b, crc)
                n += len(b)
                fo.write(b)
            b = dec.flush()
            crc = zlib.crc32(b, crc)
            n += len(b)
            fo.write(b)
        # integrity, end to end: a concurrent writer on the partial file is
        # exactly how this fetch was corrupted once (2026-07-27), so the zip's
        # own CRC32 is checked rather than trusted.
        if n != e["usize"] or crc != e["crc32"]:
            os.remove(outfile)
            raise RuntimeError(
                f"{name}: size {n}/{e['usize']} crc {crc:08x}/{e['crc32']:08x}")
        os.remove(raw)
        return outfile
    raise SystemExit(f"unsupported compression method {e['method']}")


if __name__ == "__main__":
    if sys.argv[1] == "list":
        for e in central_directory():
            print(f"{e['usize']:>13} {e['csize']:>13} m={e['method']} {e['name']}")
    elif sys.argv[1] == "get":
        print(fetch(sys.argv[2], sys.argv[3]))
