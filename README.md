# kushakratha

IAST Sanskrit/Bengali OCR cleanup toolkit + EPUB pipeline preserving
Kuśakratha Dāsa's Vaiṣṇava translations, with word-level changelog.

Kuśakratha Dāsa (ACBSP, 1949–2005), disciple of A. C. Bhaktivedanta Swami
Prabhupāda, translated 150+ Gauḍīya Vaiṣṇava works (Six Gosvāmīs,
Bhaktivinoda Ṭhākura, Bhaktisiddhānta Sarasvatī and others) into English
under the Krishna Institute / Krishna Library imprint. This repo OCRs those
editions, cleans them to IAST standard, and builds one EPUB per work with
Pandoc — for readers, and editors continuing the cleanup.

## Provenance and rights notice

The translations are by Kuśakratha Dāsa; biography and reminiscences in
`markdown/memory.md` (Chakra.org posts, Krishna Institute memorial).
`config/metadata.yaml` claims `Creative Commons
Attribution-NonCommercial-NoDerivatives 3.0 Unported` for the EPUBs —
**that is a claim in the config, unverified**. Per his will, his books are
given away for free, not sold. **Public release still needs the owner's
translation-rights confirmation** — this repo stays private until that is
obtained.

## 30-second example

Smallest work (`markdown/Bhaktivinoda_Thakura_Explanation_of_the_Mahamantra.md`):

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

Single-file equivalent (same rule as `makefile`):

```sh
pandoc -t epub3 --css ./config/epub.css --template=./config/template.epub3 \
  -o /tmp/mahamantra-test.epub ./config/metadata.yaml \
  markdown/Bhaktivinoda_Thakura_Explanation_of_the_Mahamantra.md
```

Output lands in `epub/<Same_Base_Name>.epub` (gitignored build directory).

## Sample output

`make` builds 34 EPUBs (Pandoc 3.1.11.1), e.g.:

```
epub/Bhaktivinoda_Thakura_Jaiva_Dharma.epub   # ~1.3 MB source, the main work
epub/Bhaktisiddhanta_Sarasvati_Thakura_Sri_Radha.epub
... (34 total, `ls epub/` to see all)
```

## Contents

- `markdown/` — one `.md` per work: Bhaktivinoda Ṭhākura's *Jaiva-Dharma*
  (~10k lines, the main effort), Sanātana Gosvāmī's
  *Bṛhad-Bhāgavatāmṛta*, Viśvanātha Cakravartī's *Mādhurya-Kādambinī*,
  Rūpa Gosvāmī's *Rādhā-Kṛṣṇa-Gaṇoddeśa-Dīpikā*, ~25 short works,
  plus `memory.md` (remembrances, not a book).
- `scripts/` — OCR cleanup toolkit (see Pipeline below).
- `wordlist/` — IAST/Vaiṣṇava vocab lists for checking OCR output.
- `config/` — `metadata.yaml`, `template.epub3`, `epub.css`; `fonts/` —
  Charis SIL (IAST diacritics).
- `CHANGELOG.md` — word-level audit trail of every correction.
- `resources/` — photos of Kuśakratha Dāsa (used by `memory.md`).

## Prerequisites

- `pandoc` (tested 3.1.11.1) + `make` — build the EPUBs.
- `python3` (stdlib only) — runs the `scripts/*.py` helpers.
- `tesseract` with an IAST-trained data file — only needed to OCR new
  scans (`parallel -j4 tesseract {} {.} -l IAST ::: *.tif`); not
  needed to build the EPUBs.

## Commands

```sh
make                # build every markdown/*.md → epub/*.epub (verified)
make clean          # remove built EPUBs
make debug          # print SRC/DST paths and list source files
```

To OCR new scans (needs `tesseract` + scanned PDFs/TIFFs):

```sh
parallel -j4 pdftoppm -tiff {} {.}_page ::: *.pdf
parallel -j4 tesseract {} {.} -l IAST ::: *.tif
```

## Pipeline

OCR scan → page glue → auto-fix → artifact hunt → structure markup → EPUB:

- **Page glue** — `scripts/page_glue.sh` (`all_page_glue.sh` wrapper)
  joins OCR page files with the `<++>` marker.
- **Auto-fix** — `scripts/autofix-*.py` (one pass each): double blank
  lines, trailing whitespace, orphaned glyphs, Unicode NFC normalisation.
- **Artifact hunt** — `scripts/find_artifacts.py` flags likely mis-OCRs
  (`+ = * { [`, superscripts…; patterns per work).
  `scripts/strip_diacritics.py` optionally strips all diacritics.
- **Synonyms** — `scripts/syn_glue.py` joins wrapped synonym lines;
  `syn_emflag.py` flags multi-em-dash sections; `syn_emconv.py` converts
  `-` to `—`.
- **Verses** — `scripts/verse_quote.py` detects verses (blockquote `>` +
  flags); `verse_glue.py` joins wrapped verse lines (never across
  boundaries).
- **Prose** — `scripts/prose_glue.py` collapses prose newlines (after
  headers and verses are marked).
- **Build** — `makefile`: `pandoc -t epub3` with `config/epub.css`,
  `config/template.epub3`, `config/metadata.yaml` → `epub/*.epub`.

## Editorial policy

- IAST throughout, as far as possible.
- Headers: `#` book/canto/division, `##` chapter, `###` verse number,
  `####` anything else (synonyms, translation, purport).
- File naming: `Author_Name-Title_Of_Work`, no diacritics in filenames.
- Silent fixes (no log entry): diacritics, obvious typos (e.g. `Krrsna`),
  capitalisation, punctuation, quotes, malformed BBT verses/translations.
- All other corrections logged in [CHANGELOG.md](CHANGELOG.md) (type,
  confidence, original/revised, notes); ambiguous cases left unchanged
  for review.

## Contributing

1. Run the pipeline in order on a work in `markdown/` (glue → auto-fix →
   artifacts → synonyms → verses → headers → prose).
2. Follow the header levels, IAST standard, and filename convention above.
3. Log non-trivial corrections in `CHANGELOG.md` (next `## Change N`:
   type, confidence, original/revised, notes).
4. Verify with `make` (full build must exit 0) before pushing.
5. Do not change visibility: this repo stays **private** until
   translation-rights confirmation (see Provenance notice).

## License and credits

No LICENSE yet — rights unresolved (see Provenance notice). Translations:
Kuśakratha Dāsa (Krishna Institute). Tooling: `bt108`. Fonts: Charis SIL
(OFL). Reminiscences by their named authors (Puskara, Viśoka,
Mahā-saumya Dāsas and others).
