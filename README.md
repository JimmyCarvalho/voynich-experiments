# Eighty experiments on the Voynich manuscript

**Site (EN):** https://jimmycarvalho.github.io/voynich-experiments/ · **Site (PT):** https://jimmycarvalho.github.io/voynich-experiments/pt/

Eighty statistical experiments on the text of the Voynich manuscript (Beinecke MS 408), every one of them run first on natural-language controls (Latin, Portuguese, German, Hebrew, Greek, Turkish, Arabic, Finnish, Hungarian, Basque, Nahuatl) and on controls enciphered with the method under test, then on the manuscript.

**Result in one sentence:** the text is statistically indistinguishable from a process with three rules, a two-glyph habit (each glyph depends on the two before it), 4% copying of a nearby word, and a page-by-page bias in preferences; it has no lexicon above that habit, no page has vocabulary of its own, and the only words that behave like names are the labels attached to the drawings. A Naibbe-class verbose homophonic cipher (Greshko, 2025) reproduces the entropy and the absence of repeated phrases but not the copying or the boundary link; our solvers could not break Greshko's own control, so that hypothesis remains open.

The full argument, figures and numbers are on the site. This repository holds what is needed to check them.

## Layout

```
experiments/   one script per experiment (exp49.py ... exp80e.py) plus the earlier attack/entropy code
results/       the numbers each script produced, as JSON
figures/       charts and annotated scans used on the site
docs/          the bilingual site (GitHub Pages serves this folder)
scripts/       fetch_data.sh downloads the transliterations, corpora, the Naibbe code and the scans
paper/         the earlier long-form article for X (v1, 36 experiments; superseded by the site)
data/          empty until you run scripts/fetch_data.sh (nothing is redistributed here)
```

## Reproduce

```bash
git clone https://github.com/JimmyCarvalho/voynich-experiments
cd voynich-experiments
pip install -r requirements.txt
bash scripts/fetch_data.sh          # transliterations, corpora, Naibbe code, scans
cd experiments
python3 exp65.py                    # memory length of the process (~1 min)
python3 exp66.py                    # order-k glyph chain against the battery
python3 exp71.py                    # word level vs 3-glyph habit, per corpus
```

The scripts expect to run from the `experiments/` directory with the data files beside them; `fetch_data.sh` puts them there. Most experiments finish in seconds to a couple of minutes. The solvers in `exp80*.py` take 5 to 15 minutes each; run them in the background.

Experiments 1 to 48 (substitution attacks in seven languages, polyalphabetic, abjad, abbreviation, Cardan grille, null glyphs, verbose cipher, syllabic table, anagram, nomenclator, self-citation simulator, scribes, zodiac labels, adjacency communities, drift, agglutinative languages, litany controls, sorted list, numeric table, Friedman taxonomy, transposition, reversal, glyph merging, repeated n-grams, word-as-letter, fake spaces, word-length distribution) were run in an earlier session; their aggregate numbers are in `results/numbers.json` and `results/boost.json` and their charts in `figures/`. `experiments/EXPERIMENTS.md` maps every experiment number to its script and result file.

## Data and credits

- Transliterations: Zandbergen-Landini EVA (`ZL3b-n.txt`) and Glen Claston v101 (`GC2a-n.txt`), from René Zandbergen's [voynich.nu](http://voynich.nu/). Used with attribution; not redistributed here.
- Comparison corpora: [christos-c/bible-corpus](https://github.com/christos-c/bible-corpus) (public-domain translations) and Project Gutenberg.
- Naibbe cipher: Michael A. Greshko, *Cryptologia* 2025, [doi:10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408); code at [greshko/naibbe-cipher](https://github.com/greshko/naibbe-cipher), used under its licence, which requires citing the paper.
- Scans: [Internet Archive](https://archive.org/details/TheVoynichManuscript), public domain.
- Scribes and multispectral imaging: Lisa Fagin Davis (2020, 2024).

## Licence

Code: MIT (see `LICENSE`). Text and figures in `docs/` and `figures/`: CC BY 4.0. Written by Jimmy with Claude (Anthropic) as copilot.

## Cite

If you use this, cite the repository (a Zenodo DOI will be attached to the first release) and the sources above, in particular Zandbergen for the transliteration and Greshko for the Naibbe cipher.
