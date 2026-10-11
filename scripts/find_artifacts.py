#!/usr/bin/env python3
import sys
import unicodedata
import re

# ---- Easily extendable configuration ----

SUSPICIOUS_CHARS = {
    # Replacement / invisible / formatting
    "\uFFFD", "\u200B", "\u200C", "\u200D", "\u2060", "\uFEFF",

    # Ligatures
    "\ufb00", "\ufb01", "\ufb02", "\ufb03", "\ufb04", "\ufb05", "\ufb06",

    # Uncommon punctuation / math / technical symbols
    "§", "¶", "•", "†", "‡", "※", "‽", "‰", "‱",
    "…", "‥", "‧", "′", "″", "‴",
    "‾", "‗",

    # Arrows
    "→","←","↑","↓","↔","↕","⇄","⇌","⇥","⇤","⇐","⇒","⇑","⇓","⇔","⇕","⟶","⟵","⟷","⤴","⤵",

    # Currency symbols
    "$","¥","€","£","₤","₣","₨","₩","₪","₫","₭","₮","₲","₱","₳","₴","₺","₼",

    # Include user-requested symbols
    "[", "]", "{", "}", "&", "@", "`", "~", "=", "^", "%", "\\",  "/", 
    ### ">", "<", "|", "©", "*",

    # Math / operator symbols
    ### "+",
    "−","×","÷","=","≠","≈","≡","≃","≤","≥","±","∓","∑","∏","∐","∫","∬","∭","∮", 
    "∇","∂","∞","∝","∠","∟","∡","∣","∤","∥","∦","∩","∪","∈","∉","∋","∌","⊂","⊃",
    "⊆","⊇","⊕","⊗","⊥","⊤","⊢","⊣","∀","∃","∄","∧","∨","¬","∗","∶","∷","∴","∵","∼"

    "©",  # Copyright
    "®",  # Registered Trademark
    "™",  # Trademark
    "µ",   # Micro sign
    "§",   # Section sign
    "¶",   # Pilcrow (paragraph symbol)
    "∆",   # Increment (delta)
    "∑",   # Summation
    "√",   # Square root
    "≈",   # Approximately equal
    "∞",   # Infinity
    "∫",   # Integral
    "∂",   # Partial derivative
    "∧",   # Logical AND
    "∨",   # Logical OR
    "⊕",   # Circled plus (exclusive OR)
    "⊗",   # Circled times (tensor product)
    "∉",   # Not an element of
    "∈",   # Element of
    "∀",   # For all
    "∃",   # There exists
    "⇔",   # Equivalent (if and only if)
    "≠",   # Not equal
    "⊥",   # Perpendicular
    "∇",   # Nabla (del operator)
    "∅",   # Empty set
    "⊆",   # Subset
    "⊇",   # Superset
    "⟶",   # Right arrow
    "⟵",   # Left arrow
    "⨁",   # Circled addition
    "⨂",   # Circled multiplication
    "◊",   # Lozenge
    "ℵ",   # Aleph (cardinality)
    "∫∫", # Double integral
    "⥀",   # Rightwards arrow with curved tail
    "◈",   # Diamond

    # Diacritics
    # "r̥",
    # "ǒ",
    # "ç",    # c with a cedilla
    # "ł",    # l with a stroke
    # "ś",    # s with an acute accent
    # "ń",    # n with an acute accent
    # "ů",    # u with a ring above
    # "č",    # c with a caron
    # "ř",    # r with a caron
    # "ť",    # t with a caron
    # "ž",    # z with a caron
    # "ğ",    # g with a breve
    # "ş",    # s with a cedilla
    # "ő",    # o with double acute
    # "˙",    # dot above (not used in IAST, could be mistaken for regular letters)
    # "ő",    # o with double acute
    # "ǵ",    # g with an acute accent
    # "ș",    # s with a comma below
    # "ț",    # t with a comma below
    # "ğ",    # g with a breve
    # "ž",    # z with a caron
    # "ř",    # r with a caron
    # "č",    # c with a caron
    # "ḱ",    # k with an acute accent
}

# Compile into regex
SUSPICIOUS_RE = re.compile(
    "[" + re.escape("".join(SUSPICIOUS_CHARS)) + "]"
)

SUPERSUB_RANGES = (
    {0x00B2, 0x00B3, 0x00B9} |          # ¹ ² ³
    set(range(0x2070, 0x209F)) |        # Superscripts and Subscripts
    set(range(0x1D2C, 0x1D6B)) |        # Phonetic Extensions (superscripts)
    set(range(0xA700, 0xA71F))           # Modifier Tone Letters (raised)
)

# Common doubled letters in English (DISABLED, commented)
COMMON_DOUBLES = {
    # Sanskrit (IAST)
    'ēē',
 
    # English
    'll', 'ee', 'ss', 'tt', 'nn', 'mm', 'aa', 'oo', 'cc'
}

CONTEXT = 18


# ---- Helper functions ----

def is_supersub(char: str) -> bool:
    return ord(ch) in SUPERSUB_RANGES


def is_suspicious_char(char: str) -> bool:
    if ch == "\n":
        return False

    if SUSPICIOUS_RE.search(char):
        return True

    if is_supersub(char):
        return True

    cat = unicodedata.category(char)

    # Diacritics are expected
    if cat.startswith("M"):
        return False

    # Control, surrogate, private-use, or unassigned
    if cat in {"Cc", "Cs", "Co", "Cn"}:
        return True

    return False


def is_uncommon_double(a: str, b: str) -> bool:
    if not (a.isalpha() and b.isalpha()):
        return False
    if a.lower() != b.lower():
        return False
    return (a.lower() * 2) not in COMMON_DOUBLES

def log_issue(line_no: int, line: str, index: int):
    start = max(0, index - CONTEXT)
    end = min(len(line), index + CONTEXT + 1)

    before = line[start:index]
    ch = line[index]
    after = line[index + 1:end]

    sys.stderr.write(
        f"{line_no}: {ch} {before}{ch}{after}\n"
    )


# ---- Stream processing (line by line, no buffering) ----

for line_no, line in enumerate(sys.stdin, start=1):
    out = []
    length = len(line)
    i = 0

    while i < length:
        ch = line[i]
        flagged = is_suspicious_char(ch)

        # Double-character check (flag first character)
        # if i + 1 < length and is_uncommon_double(ch, line[i + 1]):
        #     flagged = True

        if flagged:
            log_issue(line_no, line, i)
            out.append(ch + "<++>")
        else:
            out.append(ch)

        i += 1

    sys.stdout.write("".join(out))
