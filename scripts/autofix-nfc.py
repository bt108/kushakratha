#!/usr/bin/env python3
import sys
import unicodedata

NORMALIZATION_FORM = "NFC"

def log(line_no: int, original: str, new: str) -> None:
    sys.stderr.write(
        f"{line_no}: unicode normalized | {original} -> {new}\n"
    )

def main() -> None:
    lines = sys.stdin.read().splitlines(keepends=True)

    for i, line in enumerate(lines):
        new = unicodedata.normalize(NORMALIZATION_FORM, line)
        if new != line:
            log(i + 1, line.rstrip("\n"), new.rstrip("\n"))
        lines[i] = new

    sys.stdout.write("".join(lines))

if __name__ == "__main__":
    main()
