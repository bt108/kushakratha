#!/usr/bin/env python3
import sys

def log(line_no: int, msg: str) -> None:
    sys.stderr.write(f"{line_no}: {msg}\n")

def main() -> None:
    lines = sys.stdin.read().splitlines(keepends=True)

    out = []
    last_empty = False

    for i, line in enumerate(lines):
        is_empty = line.strip() == ""
        if is_empty and last_empty:
            log(i + 1, "removed repeated empty line")
            continue
        out.append(line)
        last_empty = is_empty

    sys.stdout.write("".join(out))

if __name__ == "__main__":
    main()
