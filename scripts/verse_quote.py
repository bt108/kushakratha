#!/usr/bin/env python3
import sys

# =====================
# CONFIGURATION
# =====================

MAX_VERSE_WORDS = 9
MIN_VERSE_LINES = 1
FORBIDDEN_STRING = ["\'s ", " his "," the "," where "," again "," is ",  " in ", " these ", " all ", " of ", " love ", " and ", "He ", "The ", "|", "!", "\"", "?", "#", "---", ":", "(", ")","{","}","[","]",";","—",".",">","0" ]

FORBIDDEN_SEQUENCE = [","]
LIMIT = 1

# =====================
# HELPERS
# =====================

def is_short_line(line: str) -> bool:
    stripped = line.strip()
    if stripped == "":
        return False
    return len(stripped.split()) <= MAX_VERSE_WORDS


def contains_forbidden_string(line: str) -> bool:
    return any(seq in line for seq in FORBIDDEN_STRING)

def contains_forbidden_sequence(line: str) -> bool:
    count = sum(1 for c in line if c in FORBIDDEN_SEQUENCE)
    return count > LIMIT

def format_verse_line(line: str) -> str:
    if not line.startswith("> "):
        line = "> " + line
    line = line.rstrip()
    if not line.endswith("  "):
        line += "  "
    return line


def flush_verse_buffer(buffer):
    """
    buffer: list of (line_number, line_text)
    """
    if len(buffer) >= MIN_VERSE_LINES:
        sys.stderr.write( f"[VERSE] ============" + "\n")
        for lineno, text in buffer:
            formatted = format_verse_line(text)
            sys.stdout.write(formatted + "\n")
            sys.stderr.write(
                f"[VERSE] line {lineno}: {formatted}\n"
            )
    else:
        for _, text in buffer:
            sys.stdout.write(text + "\n")

    buffer.clear()


# =====================
# MAIN
# =====================

def main():
    verse_buffer = []

    for lineno, raw_line in enumerate(sys.stdin, start=1):
        line = raw_line.rstrip("\n")

        is_candidate = (
            line != ""
            and not contains_forbidden_string(line)
            and not contains_forbidden_sequence(line)
            and is_short_line(line)
        )

        if is_candidate:
            verse_buffer.append((lineno, line))
        else:
            flush_verse_buffer(verse_buffer)
            sys.stdout.write(line + "\n")

    flush_verse_buffer(verse_buffer)


if __name__ == "__main__":
    main()
