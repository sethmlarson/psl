import datetime
import hashlib
import os
import pathlib
import re
import sys
import tempfile

import idna
import urllib3

import psl

PACKAGE_PATH = pathlib.Path(__file__).parent / "psl" / "__init__.py"


def main() -> int:
    http = urllib3.PoolManager()
    resp = http.request("GET", psl.PUBLIC_SUFFIX_URL, preload_content=True)

    sha1 = hashlib.sha1()
    tmp = tempfile.mkstemp()[1]
    with open(tmp, "w") as f:
        for line in "".join(resp.data.decode("utf-8")).split("\n"):
            line = line.strip()
            if not line or (line.startswith("//") and "===" not in line):
                continue
            if any(ord(c) > 0x7F for c in line):
                line = idna.encode(line, strict=True, std3_rules=True).decode()
            sha1.update(line.encode("utf-8"))
            f.write(line + "\n")

    checksum = sha1.hexdigest()
    if psl.__checksum__ == checksum:
        print(f"Current package has latest Public Suffix list")
        return 1

    print("Updating psl.txt")
    os.rename(tmp, psl._PUBLIC_SUFFIX_PATH)

    print("Updating package metadata")
    lines = []
    today = datetime.date.today()

    with open(PACKAGE_PATH, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                line = re.sub(
                    r"__version__\s*=\s*['\"][\d.]+['\"]",
                    f'__version__ = "{today.year}.{today.month}.{today.day}"',
                    line,
                )
            elif line.startswith("__checksum__"):
                line = re.sub(
                    r"__checksum__\s*=\s*['\"][a-f0-9]+['\"]",
                    f'__checksum__ = "{checksum}"',
                    line,
                )
            lines.append(line)

    with open(PACKAGE_PATH, "w") as f:
        f.truncate()
        f.write("".join(lines))

    print("Successfully updated psl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
