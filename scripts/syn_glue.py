#!/usr/bin/env python3
import sys

def dash_before_semicolon_backward(s):
    """
    Scan backward: return True if '—' is found before ';'
    """
    for ch in reversed(s):
        if ch == ";":
            return False
        if ch == "—":
            return True
    return False

def dash_before_semicolon_forward(s):
    """
    Scan forward: return True if '—' is found before ';'
    """
    for ch in s:
        if ch == ";":
            return False
        if ch == "—":
            return True
    return False

def merge_lines(line1, line2):
    """
    Merge two lines and return:
    (merged_line, merge_index)
    """
    ends_with_dash = line1.endswith("—") or line1.endswith("-")

    # Default merge
    if ends_with_dash:
        merged = line1 + line2
        merge_index = len(line1)
    else:
        merged = line1 + " " + line2
        merge_index = len(line1) + 1

        if (
            dash_before_semicolon_backward(line1)
            and dash_before_semicolon_forward(line2)
        ):
            merged = line1.rstrip() + "; " + line2.lstrip()
            merge_index = len(line1.rstrip()) + 2

    return merged, merge_index

def log_change(line_number, merged_line, merge_index):
    start = max(0, merge_index - 28)
    end = min(len(merged_line), merge_index + 28)
    snippet = merged_line[start:end]
    sys.stderr.write(f"Line {line_number}: {snippet}\n")

def main():
    lines = [line.rstrip("\n") for line in sys.stdin]
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.count(";") >= 2:
            merged_line = line
            line_number = i + 1
            j = i + 1

            # Skip empty or whitespace-only lines
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            if j < len(lines) and lines[j].count(";") >= 2:
                merged_line, merge_index = merge_lines(line, lines[j])
                log_change(line_number, merged_line, merge_index)
                i = j

            output.append(merged_line)
        else:
            output.append(line)

        i += 1

    for line in output:
        print(line)

if __name__ == "__main__":
    main()
