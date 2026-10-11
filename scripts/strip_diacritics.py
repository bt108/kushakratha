#!/usr/bin/env python3
import sys
import unicodedata

# ================= Configuration =================
CONTEXT = 10  # optional: number of surrounding chars in log

# ================= Logging helper =================
def log_removed(line_no: int, index: int, char: str, line: str):
    start = max(0, index - CONTEXT)
    end = min(len(line), index + CONTEXT + 1)
    context = line[start:end]
    sys.stderr.write(f"{line_no}: {char} removed {context}\n")


# ================= Main processing =================
for line_no, line in enumerate(sys.stdin, start=1):
    out = []
    for i, ch in enumerate(line):
        # Normalize to decompose diacritics
        decomposed = unicodedata.normalize("NFD", ch)
        base_chars = []
        removed = False
        for c in decomposed:
            if unicodedata.category(c).startswith("M"):
                # It's a diacritic
                removed = True
            else:
                base_chars.append(c)
        if removed:
            log_removed(line_no, i, ch, line)
        out.append("".join(base_chars))
    sys.stdout.write("".join(out))
