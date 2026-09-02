# Experiment map

Numbers 1 to 48 were run in an earlier session (aggregate results in `../results/numbers.json`, `../results/boost.json`; attack and entropy code in `final_numbers.py`, `boost.py`, charts in `charts.py`). The rest map as follows.

| # | question | script | results |
|---|---|---|---|
| 49 | memory of the line above (Timm prediction) | exp49.py, exp49b.py (bootstrap), exp49c.py (within paragraph), exp49d.py (by section) | exp49_50.json |
| 50 | words adjacent to drawings | exp50.py | exp49_50.json |
| 51 | alternative glyph segmentations | exp51.py | exp51_52.json |
| 52 | best possible segmentation (greedy merges) | exp52.py, exp52b.py | exp51_52.json |
| 53 | do the five scribes share one system | exp53.py, exp53b.py, exp53c.py | exp53_55.json |
| 54 | do labels behave like names | exp54.py | exp53_55.json |
| 55 | Naibbe cipher against the battery | exp55.py, exp55b.py | exp53_55.json |
| 56 | word-boundary link and space predictability | exp56.py, exp56b.py | exp56_60.json |
| 57 | Naibbe + copied filler | exp57.py | exp56_60.json |
| 58 | hand changes vs text jumps; within-word vs cross-boundary MI | exp58.py, exp58_mi_within.py | exp56_60.json |
| 59 | Naibbe with a last-glyph table schedule | naibbe_sched_variant.py, exp59.py, exp59b.py | exp56_60.json |
| 60 | does the boundary link cross line breaks | exp60.py, exp60b.py | exp56_60.json |
| 61 | gap widths measured on the scans | gaps.py, gaps2.py | f20r_fixed.gaps.json, rec196.gaps.json, exp61_62.json |
| 62 | uncertain spaces and re-segmentation at soft joints | exp62b.py | exp61_62.json |
| 63 | unit discovery by junction, repeats without spaces | exp63.py, exp63b.py | exp63_67.json |
| 64 | branching-entropy unit discovery | exp64.py | exp63_67.json |
| 65 | memory length of the process | exp65.py | exp63_67.json |
| 66 | order-k glyph chain null model | exp66.py | exp63_67.json |
| 67 | chain + local copying | exp67.py | exp63_67.json |
| 68 | zodiac labels: position, sign marker, prefixes | exp68.py | exp68_70.json |
| 69 | out-of-sample validation of the model; burstiness within blocks | exp69.py, exp69b.py | exp68_70.json |
| 70 | size of the recipe | exp70.py | exp68_70.json |
| 71 | does the word level carry information beyond 3-glyph habits | exp71.py | exp71_yale.json |
| 72 | word predictability; long-range correlations (DFA) | exp72.py, exp72b.py | exp72_75.json |
| 73 | page-wide copying | exp73.py | exp72_75.json |
| 74 | per-page habit bias | exp74.py | exp72_75.json |
| 75 | page-exclusive words | exp75.py | exp72_75.json |
| 76 | drift along the book, rule violations, habit vs table | exp76.py | exp76.json |
| 77 | periodicity (rotating device) | exp77.py | (printed) |
| 78 | the f57v ring vs the text alphabet | (inline, see results) | exp78_80.json |
| 79 | crib attack on labels | exp79.py | exp78_80.json |
| 80 | Naibbe-class solver with control | exp80.py, exp80b.py (segmentation), exp80c.py (affix annealing), exp80d.py (context clustering), exp80e.py (HMM/EM) | exp78_80.json, exp80*.json |
