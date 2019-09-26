import datetime
import hashlib
import os
import pathlib
import re
import sys
import tempfile

import httpx

import psl

PACKAGE_PATH = pathlib.Path(__file__).parent / "psl" / "__init__.py"


def main() -> int:
    client = httpx.Client()
    resp = client.get(psl.PUBLIC_SUFFIX_URL)
    resp.raise_for_status()

    sha1 = hashlib.sha1()
    tmp = tempfile.mkstemp()[1]
    with open(tmp, "w") as f:
        for line in "".join(resp.text).split("\n"):
            line = line.strip()
            if not line or (line.startswith("//") and "===" not in line):
                continue
            sha1.update(line.encode("utf-8"))
            f.write(line + "\n")

    checksum = sha1.hexdigest()
    if psl.__checksum__ == checksum:
        print(f"Current package has latest Public Suffix list")
        return 1

    print("Updating psl.txt")
    os.rename(tmp, psl.PUBLIC_SUFFIX_PATH)

    print("Updating package metadata")
    lines = []
    version = datetime.date.today().strftime("%Y.%m.%d")

    with open(PACKAGE_PATH, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                line = re.sub(
                    r"__version__\s*=\s*['\"][\d.]+['\"]",
                    f'__version__ = "{version}"',
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
