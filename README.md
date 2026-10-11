# kushakratha

IAST Sanskrit/Bengali OCR cleanup toolkit + EPUB pipeline preserving
Kuśakratha Dāsa's Vaiṣṇava translations, with word-level changelog.

Kuśakratha Dāsa (ACBSP, 1949–2005), disciple of A. C. Bhaktivedanta Swami
Prabhupāda, translated 150+ Gauḍīya Vaiṣṇava works (Six Gosvāmīs,
Bhaktivinoda Ṭhākura, Bhaktisiddhānta Sarasvatī and others) into English
under the Krishna Institute / Krishna Library imprint. This repo takes
those printed editions through OCR, cleans them to IAST transliteration
standard with a script toolkit, and builds one EPUB per work with Pandoc.
It is for readers who want these translations as ebooks, and for editors
continuing the cleanup.

## Provenance and rights notice

The translations are by Kuśakratha Dāsa; biographical notes and
reminiscences live in `markdown/memory.md` (sourced from Chakra.org posts
and the Krishna Institute memorial). `config/metadata.yaml` claims
`Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 Unported`
for the EPUB output — **that is a claim in the config, unverified**.
Per his will (see `markdown/memory.md`), Kuśakratha Dāsa asked that his
books be given away for free, not sold. **Public release still needs the
owner's translation-rights confirmation** — this repo stays private until
that is obtained.

## 30-second example

Smallest work in the repo (`markdown/Bhaktivinoda_Thakura_Explanation_of_the_Mahamantra.md`):

```md
---
title: Explanation of the Mahā-mantra
author: Bhakti-vinoda Ṭhākura
---

O Haril Having captured my mind, please free me from material bondage.
```

```sh
make   # Markdown → EPUB in epub/ (one .epub per .md)
```

Single-file equivalent (exact rule from `makefile`, verified):

```sh
pandoc -t epub3 --css ./config/epub.css --template=./config/template.epub3 \
  -o /tmp/mahamantra-test.epub ./config/metadata.yaml \
  markdown/Bhaktivinoda_Thakura_Explanation_of_the_Mahamantra.md
```

Output lands in `epub/<Same_Base_Name>.epub` (gitignored build directory).

## Sample output

Real build artifacts from `make` (34 EPUBs, Pandoc 3.1.11.1):

```
epub/Bhaktisiddhanta_Sarasvati_Thakura_A_probe_into_lifes_relativities.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Duties_of_a_married_man.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Movement_of_unalloyed_devotion.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Putana.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Radical_Krishna_Consciousness.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Sri_Radha.epub
epub/Bhaktisiddhanta_Sarasvati_Thakura_Words.epub
epub/Bhaktivinoda_Thakura_Jaiva_Dharma.epub   # ~1.3 MB source, the main work
... (34 files total, `ls epub/` to see all)
```

## Contents

- `markdown/` — one `.md` per work: Bhaktivinoda Ṭhākura's *Jaiva-Dharma*
  (the main cleanup effort, ~10k lines), Sanātana Gosvāmī's
  *Bṛhad-Bhāgavatāmṛta*, Viśvanātha Cakravartī's *Mādhurya-Kādambinī*,
  Rūpa Gosvāmī's *Rādhā-Kṛṣṇa-Gaṇoddeśa-Dīpikā*, ~25 short works
  (aṣṭakas, stavās, essays), plus `memory.md` (remembrances, not a book).
- `scripts/` — OCR cleanup toolkit (see Pipeline below).
- `wordlist/` — IAST/Vaiṣṇava vocabulary lists used to check OCR output.
- `config/` — `metadata.yaml` (title/rights/language defaults),
  `template.epub3`, `epub.css`; `fonts/` — Charis SIL (IAST diacritics).
- `CHANGELOG.md` — word-level audit trail of every correction.
- `resources/` — photos of Kuśakratha Dāsa (used by `memory.md`).

## Prerequisites

- `pandoc` (builds EPUBs; tested with 3.1.11.1) — required for `make`.
- `make` — drives the build.
- `python3` — runs the `scripts/*.py` cleanup helpers (stdlib only).
- `tesseract` with an IAST-trained data file — only needed to OCR new
  scans (`parallel -j4 tesseract {} {.} -l IAST ::: *.tif`); **not**
  installed in this environment and **not** needed to build the EPUBs.

## Commands

```sh
make                # build every markdown/*.md → epub/*.epub (verified)
make clean          # remove built EPUBs
make debug          # print SRC/DST paths and list source files
```

Useful shell from the old notes (needs `tesseract` + scanned PDFs/TIFFs):

```sh
parallel -j4 pdftoppm -tiff {} {.}_page ::: *.pdf
parallel -j4 tesseract {} {.} -l IAST ::: *.tif
```

## Pipeline

OCR scan → page glue → auto-fix → artifact hunt → structure markup → EPUB:

- **Page glue** — `scripts/page_glue.sh` (`all_page_glue.sh` wrapper)
  combines OCR page files, joining with the `<++>` marker.
- **Auto-fix** — `scripts/autofix-*.py` (one pass each): double empty
  lines, trailing whitespace, orphaned glyphs, Unicode NFC normalisation.
- **Artifact hunt** — `scripts/find_artifacts.py` logs and marks likely
  mis-OCRed characters (`+ = * { [`, superscripts…); adjust its patterns
  per work. `scripts/strip_diacritics.py` optionally removes all
  diacritics.
- **Synonyms** — `scripts/syn_glue.py` joins wrapped synonym lines;
  `syn_emflag.py` flags sections with more than one em-dash;
  `syn_emconv.py` semi-automatically converts `-` to `—`.
- **Verses** — `scripts/verse_quote.py` detects verses, adds blockquote
  `>` markup and flags candidates; `verse_glue.py` joins wrapped verse
  lines (never across verse boundaries); `header_mark` (planned) logs
  headers once verses are marked.
- **Prose** — `scripts/prose_glue.py` collapses newlines in prose
  paragraphs (run only after headers and verses are marked).
- **Build** — `makefile`: `pandoc -t epub3` with `config/epub.css`,
  `config/template.epub3`, `config/metadata.yaml` → `epub/*.epub`.
  (`scripts/tokobo.sh` is a personal ereader-upload helper, not part of
  the build.)

## Editorial policy

- IAST transliteration standard for everything, as far as possible.
- Headers: `#` book/canto/division, `##` chapter, `###` verse number,
  `####` anything else (synonyms, translation, purport).
- File naming: `Author_Name-Title_Of_Work`, no diacritics in filenames.
- Silently corrected without a log entry: diacritics, obvious typos
  (e.g. `Krrsna`), capitalisation, punctuation, quote marks, and
  malformed verses/translations taken from the BBT.
- Every other correction is logged in [CHANGELOG.md](CHANGELOG.md) with
  type (typographical / grammatical / lexical), confidence
  (high / medium / low), original vs. revised text, and notes.
  Ambiguous cases are left unchanged and noted for review.

## Contributing

1. Pick a work in `markdown/` and run the pipeline scripts in order
   (page glue → auto-fix → artifacts → synonyms → verses → headers →
   prose).
2. Follow the header levels, IAST standard, and filename convention above.
3. Log every non-trivial correction in `CHANGELOG.md` (next sequential
   `## Change N`, with type, confidence, original/revised, notes).
4. Verify with `make` (full build must exit 0) before pushing.
5. Do not change visibility: this repo stays **private** until
   translation-rights confirmation (see Provenance notice).

## License and credits

No LICENSE file yet — rights status is unresolved (see Provenance and
rights notice). Translations: Kuśakratha Dāsa (Krishna Institute).
OCR cleanup and EPUB tooling: the repo maintainer (`bt108`).
Fonts: Charis SIL (OFL). Reminiscences in `memory.md` by their named
authors (Puskara Dāsa, Viśoka Dāsa, Mahā-saumya Dāsa and others).
