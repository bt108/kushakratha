#!/usr/bin/env python3
import sys

def log(line_no: int, original: str, new: str) -> None:
    sys.stderr.write(
        f"{line_no}: removed trailing whitespace | {original.rstrip()} -> {new.rstrip()}\n"
    )

def main() -> None:
    lines = sys.stdin.read().splitlines(keepends=True)

    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")
        new = stripped.rstrip() + ("\n" if line.endswith("\n") else "")
        if new != line:
            log(i + 1, stripped, new.rstrip("\n"))
        lines[i] = new

    sys.stdout.write("".join(lines))

if __name__ == "__main__":
    main()
