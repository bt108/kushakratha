#!/usr/bin/env python3
import sys
import unicodedata

def log(line_no: int, original: str, new: str) -> None:
    sys.stderr.write(
        f"{line_no}: removed orphaned combining mark | {original} -> {new}\n"
    )

def fix_line(line: str) -> str:
    result = []
    has_base = False
    for ch in line:
        if unicodedata.combining(ch):
            if has_base:
                result.append(ch)
        else:
            result.append(ch)
            has_base = not ch.isspace()
    return "".join(result)

def main() -> None:
    lines = sys.stdin.read().splitlines(keepends=True)

    for i, line in enumerate(lines):
        new = fix_line(line)
        if new != line:
            log(i + 1, line.rstrip("\n"), new.rstrip("\n"))
        lines[i] = new

    sys.stdout.write("".join(lines))

if __name__ == "__main__":
    main()
