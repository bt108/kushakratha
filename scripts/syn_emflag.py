#!/usr/bin/env python3
import sys

# ================= Configuration =================
MIN_SEMICOLONS = 2       # minimum number of ';' in a line to process
EMDASH_THRESHOLD = 1     # minimum number of '—' in a section to trigger

# ================= Logging helper =================
def log_section(line_no: int, section: str):
    """Log a single section with line number to stderr"""
    sys.stderr.write(f"{line_no}: {section}\n")

# ================= Main processing =================
for line_no, line in enumerate(sys.stdin, start=1):
    line_strip = line.rstrip("\n")

    # Only process lines with enough semicolons
    if line_strip.count(";") < MIN_SEMICOLONS:
        sys.stdout.write(line)
        continue

    # Split line into sections
    sections = line_strip.split(";")
    out_sections = []

    for section in sections:
        if section.count("—") > EMDASH_THRESHOLD:
            log_section(line_no, section)
            out_sections.append("<++>" + section)
        else:
            out_sections.append(section)

    # Rejoin sections with semicolons and add newline
    sys.stdout.write(";".join(out_sections) + "\n")
