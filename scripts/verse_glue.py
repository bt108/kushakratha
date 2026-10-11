#!/usr/bin/env python3
import sys

def main():
    lines = [line.rstrip("\n") for line in sys.stdin]
    n = len(lines)
    i = 0

    while i < n:
        if lines[i].startswith(">"):
            # Start of a > block
            block_start = i
            block = [lines[i]]
            i += 1
            while i < n and lines[i].startswith(">"):
                block.append(lines[i])
                i += 1

            block_len = len(block)
            # Check new rule: divisible by 4 or (length-1) divisible by 4
            if block_len == 1 or block_len == 3:
                # Log the block with line numbers
                start_line = block_start + 1
                end_line = block_start + block_len
                sys.stderr.write(f"BLOCK (lines {start_line}-{end_line}):\n")
                for idx, line in enumerate(block, start=block_start + 1):
                    sys.stderr.write(f"{idx}: {line}\n")
        else:
            i += 1

    # Print input unchanged
    for line in lines:
        print(line)

if __name__ == "__main__":
    main()
