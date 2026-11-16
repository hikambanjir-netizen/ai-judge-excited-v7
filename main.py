#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory, verifying its hash.

The entry image is a single still frame: a colossal humpback whale leaping
clean over a lighthouse on a towering curling wave at golden sunset, a tiny
red sailboat below, seabirds scattering in the spray.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "26b04a38f3b125a8b947e3ace9bd14df8ecd8367706f3335f48b9421efe2758c"
SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)

    shutil.copyfile(source, target)

    copied_hash = sha256_of(target)
    size = os.path.getsize(target)
    print(f"wrote {target} ({size} bytes, sha256 {copied_hash})")
    if copied_hash != EXPECTED_SHA256:
        print(
            f"ERROR: sha256 mismatch: expected {EXPECTED_SHA256}, "
            f"got {copied_hash}",
            file=sys.stderr,
        )
        return 1
    print("sha256 verified: entry.png is byte-identical to the source image")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
