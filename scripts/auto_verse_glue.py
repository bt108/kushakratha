#!/usr/bin/env python3
import sys


# ---------- helpers ----------

def is_verse_line(line: str) -> bool:
    return line.startswith(">")


def is_empty(line: str) -> bool:
    return line.strip() == ""


# ---------- parsing ----------
def extract_blocks(lines):
    """
    Yields either:
      ("text", [lines])
      ("verse", start_line, [block_lines])
    """
    block = []
    block_start = None
    i = 0
    n_lines = len(lines)

    while i < n_lines:
        line = lines[i]

        # --------- Verse line ---------
        if is_verse_line(line):
            if not block:
                block_start = i + 1  # 1-based line number
            block.append(line)
            i += 1
            continue

        # --------- Empty line ---------
        if is_empty(line):
            if block:
                # Lookahead: is there a verse line after this empty line?
                j = i + 1
                while j < n_lines and is_empty(lines[j]):
                    j += 1
                if j < n_lines and is_verse_line(lines[j]):
                    # Empty line inside the block
                    block.append(line)
                else:
                    # End of block
                    yield ("verse", block_start, block)
                    block = []
                    block_start = None
                    # yield empty line as text
                    yield ("text", [line])
            else:
                # Not inside a block, yield empty line
                yield ("text", [line])
            i += 1
            continue

        # --------- Normal line ---------
        if block:
            yield ("verse", block_start, block)
            block = []
            block_start = None
        yield ("text", [line])
        i += 1

    # flush remaining block at EOF
    if block:
        yield ("verse", block_start, block)

# ---------- transformation ----------

def join_verse_block(block):
    """
    Removes empty lines and applies joining rules.
    joining rules:
    - multiples of 4 → join with empty line between each group of 4
    """

    verse_lines = [l for l in block if is_verse_line(l)]
    n = len(verse_lines)
    output = []

    if n % 4 == 0:
        for i in range(0, n, 4):
            output.extend(verse_lines[i:i+4])
            if i + 4 < n:
                output.append("\n")
        return output

    return verse_lines

# ---------- logging ----------

def log_verse_block(start_line, block):
    sys.stderr.write(f"=== VERBLOCK {start_line} ===\n")
    for line in block:
        sys.stderr.write(line)
    sys.stderr.write("\n")


# ---------- main ----------

def main():
    lines = sys.stdin.readlines()

    for item in extract_blocks(lines):
 
        if item[0] == "text":
            sys.stdout.writelines(item[1])
            continue
 
        _, start_line, original_block = item
 
        joined = join_verse_block(original_block)
        changed = joined != original_block
 
        if changed:
            log_verse_block(start_line, original_block)
 
        sys.stdout.writelines(joined)

if __name__ == "__main__":
    main()
