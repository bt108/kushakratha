#!/usr/bin/env python3
import sys
import re

def process_lines():
    total_sections = 0
    emdash_before = 0
    emdash_after = 0

    # Patterns, add or remove as needed
    generic_pattern = re.compile(r"-[a-zA-Z]+ [a-zA-Z]") # -krsna is the supreem
    uvaca_pattern = re.compile(r"uvāca-")

    for line_num, line in enumerate(sys.stdin, 1):
        semicolon_count = line.count(";")

        # only process lines with 3+ semicolons
        if semicolon_count >= 3:
            sections = [s.strip() for s in line.strip().split(";") if s.strip()]
            new_sections = []

            for section in sections:
                total_sections += 1
                # if section contains an em-dash, skip modifications
                if "—" in section:
                    emdash_before += 1
                    new_sections.append(section)
                    emdash_after += 1  # already has em-dash
                    continue

                section_dash_count = section.count("-")
                if section_dash_count == 1:
                    section = section.replace("-", "—", 1)
                elif section_dash_count == 2:
                    # split into parts at hyphens, maximum 3 parts
                    parts = section.split("-", 2)  # ['before first', 'between', 'after second']
                    section = f"{parts[0]}-{parts[1]}—{parts[2]}"  # keep first hyphen, replace second
                elif section_dash_count >= 3:
                    # apply regex for 3+ dashes
                    match = (
                        generic_pattern.search(section)
                        or uvaca_pattern.search(section)
                    )

                    if match:
                        matched_text = match.group()
                        replaced_text = matched_text.replace("-", "—", 1)
                        section = section.replace(matched_text, replaced_text, 1)
                    else:
                        section = "<++>" + section
                        print(
                            f"MARKED {line_num}: {section}",
                            file=sys.stderr,
                        )
                else:
                    # section without -
                    section = "<++>" + section
                    print(
                        f"no dash {line_num}: {section}",
                        file=sys.stderr,
                    )

                # after modifications, check if section now contains an em-dash
                if "—" in section:
                    emdash_after += 1

                new_sections.append(section)

            print("; ".join(new_sections))
        else:
            # write unmodified line
            print(line, end='')

    # print statistics to stderr
    before_pct = (emdash_before / total_sections * 100) if total_sections else 0
    after_pct = (emdash_after / total_sections * 100) if total_sections else 0

    print(f"total sections: {total_sections}", file=sys.stderr)
    print(f"sections with em-dash before: {emdash_before} ({before_pct:.2f}%)", file=sys.stderr)
    print(f"sections with em-dash after: {emdash_after} ({after_pct:.2f}%)", file=sys.stderr)

if __name__ == "__main__":
    process_lines()

