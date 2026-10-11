#!/usr/bin/env python3
import sys
import re

numbered_bullet = re.compile(r'^\d+\.\s')

def remove_line_breaks_from_stdin():
    """
    Reads from stdin, writes to stdout.
    Paragraphs are merged, except:
      - Lines starting with '#' (headers) are preserved
      - Lines starting with '>' (blockquotes) are preserved
      - Empty lines break paragraphs
    Lines ending with two spaces are treated as intentional line breaks and preserved.
    """

    paragraph = []  # buffer for the current paragraph
    def flush_paragraph():
        if not paragraph:
            return

        merged = []
        for line in paragraph:
            line = line.rstrip("\n")

            if line.endswith("  "):   # intentional line break
                merged.append(line)
                merged.append("\n")
            else:
                if merged and not merged[-1].endswith("\n"):
                    merged.append(" ")  # separate with space
                merged.append(line)

        sys.stdout.write("".join(merged))
        if not merged[-1].endswith("\n"):
            sys.stdout.write("\n")

        paragraph.clear()

    for raw_line in sys.stdin:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        is_boundary = (
            stripped == ""                          # Empty line → natural paragraph break
            or stripped.startswith("#")             # Header line (Markdown) → keep as-is
            or stripped.startswith(">")             # Blockquote → keep as-is
            or stripped.startswith("-")             # Unordered list item using '-' → boundary
            or stripped.startswith("+")             # Unordered list item using '+' → boundary
            or stripped.startswith("*")             # Unordered list item using '*' → boundary
            or numbered_bullet.match(stripped)      # Numbered list (e.g., 1., 23.) → boundary
        )

        if is_boundary:
            flush_paragraph()
            sys.stdout.write(line + "\n")  # output boundary line as-is
            # Optional logging:
            # sys.stderr.write(f"[INFO] boundary line preserved: {line}\n")
        else:
            paragraph.append(line)  # add to current paragraph

    # Flush any remaining paragraph at the end
    flush_paragraph()


if __name__ == "__main__":
    remove_line_breaks_from_stdin()
