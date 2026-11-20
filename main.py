"""Salin entry.png hasil pre-render ke direktori output grader.

Hanya memakai standard library: periksa signature PNG, salin file,
lalu verifikasi hasil salinan byte per byte sebelum melaporkan sukses.
"""

import hashlib
import os
import shutil

PNG_SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])


def die(message):
    os.write(2, ("error: " + message + "\n").encode("utf-8"))
    raise SystemExit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        die("cannot read entry.png: %s" % exc)
    if data[:8] != PNG_SIGNATURE:
        die("entry.png is not a PNG file (bad signature)")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(outdir, "entry.png")
    try:
        os.makedirs(outdir, exist_ok=True)
        shutil.copyfile(source, dest)
        with open(dest, "rb") as handle:
            copied = handle.read()
    except OSError as exc:
        die("copy failed: %s" % exc)
    if copied != data:
        die("copied entry.png differs from source (bytes)")
    if len(copied) != len(data):
        die("copied entry.png differs from source (size)")
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        die("copied entry.png differs from source (sha256)")
    print("entry.png: %d bytes sha256=%s"
          % (len(copied), hashlib.sha256(copied).hexdigest()))


if __name__ == "__main__":
    main()
