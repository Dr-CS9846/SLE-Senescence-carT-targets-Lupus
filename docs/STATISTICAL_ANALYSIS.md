# Statistical Analysis Plan and Annex — Revision of LUP-26-366

This document has four parts. **Part A is written and committed (tag `sap-v1`) before any
confirmatory result of this revision is produced.** Part B records what was actually run and
any deviation from Part A, with a reason. Part C maps every number quoted in the manuscript to
its source file and cell. Part D is a short, timed set of steps for an independent reviewer
(the study's statistician) to check this annex against the repository without re-running
anything, plus an optional full reproduction.

---

## Part A — Pre-specified statistical analysis plan

**Status at commit:** pre-specified, before confirmatory analysis. **Date:** 2026-11-25 (Day 1
of the revision timeline). **Author:** prepared on behalf of the corresponding author.

### A.1 Objective

To quantify, across as many independent public datasets as the Gene Expression Omnibus (GEO)
provides with usable annotation, the within-dataset association between a transcriptomic
senescence signature (SenMayo) and six literature-nominated candidate CAR-T surface targets
(CD38, CD44, CSPG4, ICAM1, VCAM1, EGFR) in systemic lupus erythematosus (SLE) and to test
whether a combined multi-target score associates with senescence more strongly than any single
target.

### A.2 Population and inclusion rules

- **DEC-01 (SenMayo coverage rule).** A dataset is scored directly from the SenMayo panel if at
  least 3 of the 125 panel genes are detected on its platform (the threshold already applied
  throughout Phase 1 and Phase 2 processing). Datasets below this threshold are scored with the
  top-13-variable-gene fallback and are labelled exploratory, not confirmatory.
- **DEC-02 (minimum unit count).** A dataset must have at least 15 scoring units (samples,
  donors, or de-duplicated single-cell donors) to enter any correlation or pooling analysis.
  Below 15, the dataset is sensitivity-only.
- **DEC-03.** GSE163121 (5 donors, 997 cells) is sensitivity-only: cells from the same donor are
  not independent statistical units.
- **DEC-04.** GSE110169 (17 of 125 SenMayo genes matched; CD44 only evaluable) is
  sensitivity-only (S1), not part of the confirmatory pooled estimate.
- **DEC-22 (publication window).** The inclusion criterion states a 2012–2024 GEO release
  window. Four datasets (GSE36700, 2012; GSE32591, 2012; GSE52471, 2013; GSE49454, 2014) were
  released before the originally stated 2015 cutoff. This is disclosed as a deviation, not
  silently corrected, and a sensitivity analysis (S9) excludes these four datasets.
- **Confirmatory set.** Three Phase 1 datasets with direct SenMayo matching and adequate size
  (GSE228066, GSE139358, GSE182825) plus the nine Phase 2 datasets, for 12 candidate datasets;
  of these, datasets meeting DEC-01 and DEC-02 for a given target enter that target's pooled
  estimate. The confirmatory raw files for GSE228066, GSE139358, and GSE182825 were confirmed
  present on disk on 2026-11-24 (see repository registry check log); the DEC-26 fallback
  (8-dataset confirmatory set) therefore does not apply.

### A.3 Candidate target selection

Six candidates (CD38, CD44, CSPG4, ICAM1, VCAM1, EGFR) were selected from the literature on
senescence biology and on CAR-T target precedent before any target-senescence correlation was
computed in this project. `[VERIFY: exact literature-review date range to be supplied by the
corresponding author if requested by a reviewer; not reconstructed here from memory.]`

### A.4 Primary endpoint

Within-dataset Spearman rank correlation (rho) between each target gene's expression value and
the dataset's senescence score (direct SenMayo mean or fallback proxy, per A.2), computed
independently in each dataset, with its two-sided p-value.

### A.5 Multiplicity

- **DEC-06.** Benjamini-Hochberg false-discovery-rate correction (q-value) is applied across all
  evaluable target-by-dataset tests. Holm correction is applied separately across the six
  pooled-target tests (one pooled test per target). Bonferroni is not used for either family.

### A.6 Random-effects pooling

- **DEC-07.** For each target, per-dataset Spearman rho is Fisher-z transformed; pooling uses
  the DerSimonian–Laird tau² estimator with a Hartung–Knapp–Sidik–Jonkman adjustment to the
  confidence interval. Cochran's Q, I², and tau² are reported alongside the pooled estimate.
  Holm correction (A.5) is applied across the six resulting pooled p-values.

### A.7 Combined score

- **DEC-08 [corrected 2026-11-24, see Part B].** The combined score is the row-mean, across
  CD38, CD44, and CSPG4, of each gene's log2(CPM+1) expression value (not z-scored). This is
  what the existing code (`scripts/analyze_results.py`, `fig8_target_combination`) actually
  computes; an earlier version of this line in Part A incorrectly described the combination as
  a mean of within-dataset z-scores, which does not reproduce the manuscript's r=0.576 (it gives
  r=0.456 on the same data). This was caught by independently recomputing both versions before
  reporting either, not assumed. The raw-mean definition is the one in the manuscript and is the
  one used by all downstream scripts in this revision. The combination's history is disclosed
  separately in Part B: earlier manuscript text named a different third marker (ICAM1) in
  places, while the committed code has always used CSPG4.

### A.8 Comparison of the combined score with single markers

- **DEC-09.** Because the combined score contains each single marker as a component, a Steiger
  test (which assumes independence between the two correlations being compared) is not valid
  here. Instead: a paired bootstrap of the difference in Spearman rho (combined score vs. each
  single marker), 2,000 resamples, seed 42, within the dataset where the combined score is
  evaluated; and a random-triplet null distribution (1,000 random three-target combinations
  drawn from the six candidates, with replacement across combinations but not within one
  combination) to give the percentile rank of the CD38+CD44+CSPG4 combination. A combination
  search across all twenty possible three-marker combinations of the six candidates is reported
  as exploratory (DEC-23), stating the rank of CD38+CD44+CSPG4 among them, not presented as a
  pre-registered confirmatory comparison.

### A.9 Composition adjustment (answers reviewer 2, point 2)

- **DEC-11.** A fixed, literature-standard marker panel approximates major leukocyte-class
  abundance, in the absence of a licensed deconvolution tool: T cells (CD3E); B cells (CD19,
  MS4A1); plasma cells (JCHAIN, MZB1); monocytes (CD14, LYZ); NK cells (NKG7); neutrophils
  (FCGR3B, CSF3R). Each class score is the mean of the within-dataset z-scores of its markers.
  The target-senescence correlation is then recomputed on the residuals of an ordinary
  least-squares regression of the target value and of the senescence score on all class scores
  jointly. This is labelled an approximation, not a validated deconvolution, in every place it is
  reported (sensitivity analysis S4).

### A.10 Canonical-gene subset (answers reviewer 2, point 1)

- **DEC-10.** Confirmed against `data/senmayo_125genes.csv` on 2026-11-24: the file's `Category`
  column contains exactly the six category labels named in this decision — Inflammation (4
  genes), NF-kB (2), Cytokine (3), SASP (7), Stat Pathway (5), TGF Pathway (4) — 25 of 125 genes
  in total. The canonical-gene subset excludes these 25 and rescales the SenMayo score (direct
  match or fallback, per A.2) to the remaining 100-gene panel, recomputing per-dataset coverage
  against this reduced panel. Target-senescence correlation on this canonical-only score is
  sensitivity analysis S3; correlation of the excluded 25-gene inflammation/SASP/cytokine subset
  score with the six targets is reported separately as S7.

### A.11 Synovium analysis

- **DEC-12.** GSE36700 (synovial tissue; SLE, OA, RA, MIC, and seronegative arthritis groups) is
  analysed as: an omnibus Kruskal–Wallis test across all groups; pairwise Mann–Whitney tests of
  SLE against each comparator group, with Holm correction across those pairwise tests; Cliff's
  delta effect size with a bootstrap confidence interval for each pairwise comparison; and an
  ROC curve (SLE vs. non-SLE) with a bootstrap confidence interval on the AUC. This whole
  analysis is labelled exploratory given the small SLE group (n = 4) and the absence of healthy
  controls in this dataset, and whatever result the code produces is reported as-is (no
  post-hoc selection of which comparisons to report).

### A.12 Sensitivity analyses

| ID | Analysis |
|---|---|
| S1 | Add GSE110169 (CD44 only, DEC-04) to the CD44 pooled estimate |
| S2 | All verified Phase-2-candidate accessions, including the three not processed (GSE61635, GSE99967, GSE175759) — P2, stated as a limitation if not run |
| S3 | Canonical-gene-subset score (A.10) vs. the full SenMayo score |
| S4 | Composition-adjusted correlation (A.9) |
| S5 | *(reserved — not separately defined beyond S1–S4 and S6–S9 in this plan; if used, defined in Part B before being reported)* |
| S6 | Fallback-scored (top-13-variable-gene) Phase 1 datasets, descriptive only — P2 |
| S7 | Correlation of the excluded inflammation/SASP/cytokine/NF-kB/STAT/TGF subset score with the six targets (A.10) |
| S8 | High- vs. low-senescence-quartile differential expression, bulk datasets only — P2 |
| S9 | Exclude the four pre-2015 datasets (A.2, DEC-22) and re-pool |

Items marked P2 are run only if time allows within the revision timeline; if not run, they are
stated as a limitation in the manuscript, not silently omitted.

### A.13 Phase 2 selection statement (DEC-20)

"Phase 2 comprised nine of thirteen verified candidates. Nine were selected on 5 July 2026 to
match the scope of the original manuscript and to limit processing time. The selection was not
based on target-correlation results. GSE142016 (three samples) was not selected for sample
size. GSE61635, GSE99967, and GSE175759 were not processed." This statement is reproduced
verbatim in the manuscript Methods and in the response to reviewers; it is not re-derived or
altered here.

### A.14 Software, seed, and significance level

Python environment pinned in `requirements.txt` (committed alongside this plan): pandas
2.3.3, numpy 2.4.0, scipy 1.16.3, scikit-learn 1.8.0, matplotlib 3.10.8, seaborn 0.13.2,
openpyxl 3.1.5, statsmodels 0.14.6. All randomised procedures (bootstrap, random-triplet null)
use seed 42. Significance level alpha = 0.05, two-sided, before any multiplicity correction in
A.5.

### A.15 Confirmatory vs. exploratory labelling

Confirmatory: A.4–A.8 (primary endpoint, pooling, combined score) on the dataset set defined in
A.2. Exploratory, and labelled as such wherever reported: the combination search (A.8, DEC-23),
the synovium analysis (A.11), the fallback-scored Phase 1 datasets (A.2, S6), and every
sensitivity analysis in A.12.

---

## Part B — Results and deviations

Written after running `scripts/statistical_analysis.py`, `scripts/sensitivity_analysis.py`, and
`scripts/composition_canonical_analysis.py` (2026-11-25). The committed, pre-existing analysis
outputs (`results/tables/cart_target_statistics.csv` and the per-dataset
`*_senescence_scores.csv` files) were **not** changed by any of this; each script only reads
from or adds new files alongside them.

**Confirmatory results (A.4–A.7).** Pooled rho (Fisher z, DerSimonian-Laird, Hartung-Knapp) for
the 11 confirmatory datasets: CD38 0.431 (95% CI 0.237–0.593, I²=91.4%, Holm p=0.0053 — the only
target surviving Holm correction), CD44 0.319 (ns after Holm), CSPG4 0.163 (ns), ICAM1 0.337
(Holm p=0.14), VCAM1 0.307 (Holm p=0.10), EGFR 0.069 (ns). These independently reproduce the
manuscript's existing pooled estimates to 2–3 decimal places. Tissue-level and leave-one-out
results likewise reproduce the manuscript's existing numbers closely (`stat_by_tissue.csv`,
`stat_loo.csv`).

**Deviation 1 — DEC-08 was mis-stated in the first version of this Part A, corrected in place.**
Originally described as a mean of within-dataset z-scores; the code that actually produced the
manuscript's r=0.576 uses a raw mean of log2(CPM+1) values (no z-scoring). Checked both ways
numerically before correcting the text. No manuscript number is affected; only this document's
wording was wrong, now fixed.

**Deviation 2 — a real bug in `analyze_results.py`'s `fig2_disease_comparison()`, fixed in the
new sensitivity script, not in the original file.** It matches synovium group labels by
searching for "PSO" in each sample ID; the dataset's actual 5th group is "SA" (seronegative
arthritis, samples SA1–SA4), which never matched and was silently excluded from every synovium
comparison. With all 5 groups correctly included: Kruskal-Wallis H=14.013, p=0.0073 (the
manuscript currently states H=12.69, p=0.005, which appears to be the 4-group result). The three
existing pairwise SLE-vs-comparator p-values (0.063/0.648/0.190) are unchanged; a fourth
comparison, SLE vs SA (p=0.343, Holm p=0.686), is new. Holm correction and Cliff's delta with
bootstrap CIs were added per A.11. **This changes a number currently in the manuscript** — see
the response-to-reviewers / manuscript-revision step for how to word the correction.

**Deviation 3 — the combined-score "outperformed any single marker" framing is only partly
supported by a formal test.** Paired bootstrap (A.8): the combined score (r=0.576) is
significantly higher than CD38 alone and CSPG4 alone (95% CI excludes 0), but not significantly
higher than CD44, ICAM1, or VCAM1 alone (CI includes 0). The combination search across all 20
three-marker combinations in GSE228066 ranks CD38+CD44+CSPG4 6th (r=0.576); CD38+ICAM1+VCAM1
ranks 1st (r=0.665). **This also affects manuscript wording**, not just this annex.

**S1/S9 (1.8.12, 1.8.11).** Adding GSE110169 to the CD44 pool: r=0.335 (vs. 0.319 without).
Excluding the pre-2015 datasets present in the confirmatory target table (GSE32591, GSE49454;
GSE52471 and GSE36700 are not both in this particular table — GSE36700 never was, as it only
enters the synovium analysis): results in `stat_S9.csv`. No material change to which targets are
significant.

**Deviation 4 — composition (S4) and canonical-gene/inflammation (S3, S7) sensitivity analyses
are scoped to 5 of the 12 confirmatory datasets, not all of them, and this is a real limitation,
not a simplification made for convenience.** Building these required full per-sample gene-level
matrices for genes beyond the six CAR-T targets. Attempting this for the remaining datasets
(GSE65391, GSE72326, GSE49454, GSE112943, GSE81622 — all GPL10558; GSE110169 — GPL13667) by
reusing this repository's own `process_phase2_datasets.py` surfaced that those platforms'
current live NCBI annotation files use a "Symbol" column header that the existing
`load_platform_map()` function does not match (it looks for "Gene Symbol"/"gene_symbol" only),
so it cannot resolve a gene symbol for those platforms as currently written. Broadening that
match was tried as a test, then **reverted**: re-running the full script with that change did
not reproduce the already-committed target correlations for 7 of the 8 affected datasets (only
GSE32591, a different platform, matched exactly) — meaning the committed results table was not
generated by this exact committed script as it stands today. This is a pre-existing
inconsistency between the committed pipeline code and the committed results, not something this
analysis introduced, and it was not something this revision set out to resolve. Per explicit
instruction, the already-established script and results are left exactly as committed, and the
composition/canonical sensitivity analysis is scoped down to the 5 datasets (GSE228066,
GSE139358, GSE182825, GSE32591, GSE52471) it can cover with loaders that do not depend on that
function. Results: `stat_S3.csv`, `stat_S4.csv`, `stat_S7.csv`. Composition adjustment (S4)
materially changes significance (both directions) for several target-dataset pairs in these 5
datasets (e.g. GSE139358 CD38 drops from r=0.711, p<0.001 unadjusted to r=-0.377, ns, adjusted),
underscoring that cell-type composition is a real confound worth stating plainly as a limitation
— consistent with what the manuscript's Limitations section already says about this being an
approximation, not a validated deconvolution.

**Deviation 5 — combined-score analysis extended from 1 to 5 datasets, answering the editor's and
Reviewer 1's explicit point that it was done in only one dataset (GSE228066).** Reusing the gene
matrices already loaded for Deviation 4's analysis, the same combined-score definition (DEC-08)
was computed in GSE139358, GSE182825, and GSE32591 in addition to GSE228066, plus GSE52471.
GSE228066 reproduced exactly (r=0.576), confirming correct calibration. Results:
`stat_combined_multidataset.csv`. The combined score exceeded every single marker in GSE228066,
GSE139358, GSE182825, and GSE32591 (r=0.576-0.975, all p<0.001) but was not significant and
weaker than CD38 alone in GSE52471 (r=0.259, p=0.117, vs. CD38 alone r=0.516, p<0.001) --
reported as-is, not selectively. Does not cover the other 7 confirmatory datasets, for the same
reason as Deviation 4.

**Not run in this revision:** full composition/canonical/combined-score coverage of the other 7
confirmatory datasets; the GPL10558/GPL13667 annotation-matching inconsistency itself (left as a
maintenance item, not fixed); S2, S6, S8 (already P2 in Part A).

## Part C — Traceability

Every number below is quoted as it appears in the manuscript (revision draft
`REVISED_MANUSCRIPT_v2_2026-11-25.md`), with its source file and, where the file is small enough
to name one, the row or cell.

| Manuscript location | Number quoted | Source file | Row / cell |
|---|---|---|---|
| Abstract, Results | CD38 pooled r = 0.43 (95% CI 0.24–0.59), significant in 9 of 11 datasets | `results/tables/stat_pooled_by_target.csv`; `stat_confirmatory_per_dataset.csv` | `Target == 'CD38'` row; count of `Significant == True & Spearman_r > 0` for CD38 |
| Abstract, Results | ICAM1 significant in 6 of 11 datasets | `stat_confirmatory_per_dataset.csv` | `Target == 'ICAM1'` rows |
| Abstract, Results | VCAM1 significant in 4 of 11 datasets | `stat_confirmatory_per_dataset.csv` | `Target == 'VCAM1'` rows |
| Abstract, Results | Synovium Kruskal-Wallis H = 14.013, p = 0.0073 | `results/tables/stat_synovium_omnibus.txt` | first line |
| Abstract, Results | Combined score r = 0.576, p < 0.0001 (GSE228066) | `results/tables/stat_combined_summary.txt` | sole line |
| Abstract | Single-marker range r = 0.23–0.40 | `results/tables/stat_combined_singles.csv` | CSPG4 (min) and CD38 (max) rows |
| Results, CAR-T Target Associations | Per-dataset r/p for CD38, ICAM1, VCAM1, CD44, CSPG4, EGFR (e.g. GSE228066, GSE108497, GSE32591, GSE139358, GSE52471) | `results/tables/cart_target_statistics.csv` | filter by `Target` and `Dataset` |
| Results, Pooled estimates paragraph | Pooled r, 95% CI, I² for all six targets | `stat_pooled_by_target.csv` | one row per target |
| Results, Pooled estimates paragraph | Blood (7 datasets) and skin (2 datasets) pooled r by target; kidney (GSE32591) per-target | `results/tables/stat_by_tissue.csv` | filter by `Tissue` |
| Results, Pooled estimates paragraph | Leave-one-dataset-out ranges | `results/tables/stat_loo.csv` | one row per target |
| Results, Pooled estimates paragraph | GSE110169 added to CD44 (r = 0.34 with vs 0.32 without — manuscript rounds to 2 d.p.; script output is 0.335 vs 0.319, see Deviation note) | `results/tables/stat_S1.csv` | `variant` column |
| Results, Pooled estimates paragraph | Excluding pre-2015 datasets: CD38 r = 0.37, ICAM1 r = 0.18 | `results/tables/stat_S9.csv` | `Target == 'CD38'` / `'ICAM1'` rows |
| Results, Table 2 | Dataset counts per target (tested / significant positive / negative / not significant) | `cart_target_statistics.csv` | aggregated manually by target; not produced by a dedicated script in this revision — a reviewer can recompute it directly from this file |
| Results, Disease-Specific Senescence Burden | Pairwise SLE-vs-comparator p (unadjusted and Holm), Cliff's delta, delta CI | `results/tables/stat_synovium.csv` | one row per comparison |
| Results, Disease-Specific Senescence Burden | ROC AUC = 0.679, bootstrap 95% CI | `stat_synovium_omnibus.txt` | second line |
| Results, Multi-Target Senescence Scoring | Combined vs. single-marker bootstrap CIs (which comparisons exclude 0) | `results/tables/stat_combined_bootstrap.csv` | `excludes_zero` column |
| Results, Multi-Target Senescence Scoring | Combination-search rank of CD38+CD44+CSPG4 (6th of 20); top combination CD38+ICAM1+VCAM1 (r = 0.665) | `results/tables/stat_combination_search.csv` | `rank` column |
| Abstract, Results, Discussion (Multi-Target Senescence Scoring) | Combined score across 5 datasets (r = 0.576–0.975 in 4; r = 0.259, ns, in GSE52471) | `results/tables/stat_combined_multidataset.csv` | one row per dataset |
| Results, Pooled estimates paragraph | Canonical-subset vs. full-SenMayo CD38 correlations; excluded-subset CD38 correlations | `results/tables/stat_S3.csv`, `stat_S7.csv` | `Target == 'CD38'` rows |
| Results, CAR-T Target Associations (CD38 paragraph) | CD38 weak-to-moderate in 9 of 11 datasets; r > 0.6 only in GSE32591 and GSE139358 | `results/tables/cart_target_statistics.csv` | `Target == 'CD38'` rows |
| Limitations / Pooled estimates paragraph | Composition adjustment flips significance (e.g. GSE139358 CD38 r=0.71 unadjusted to r=-0.38 adjusted) | `results/tables/stat_S4.csv` | `Dataset == 'GSE139358' & Target == 'CD38'` |
| Limitations | Composition/canonical sensitivity covers 5 of 12 confirmatory datasets | `results/tables/stat_S3.csv`, `stat_S4.csv`, `stat_S7.csv` | unique `Dataset` values in each file |
| Methods, dataset registry | GEO metadata (title, organism, n, platform, release date) for the 12 target-correlation datasets | `docs/dataset_registry.csv` | one row per accession |

## Part D — How to check

**Goal: an independent reviewer should be able to do this in about an hour, without running
anything, plus an optional faster re-run.**

1. **Confirm the plan preceded the results.** `git log --oneline` — commit `1b66bc0` ("Pre-specify
   statistical analysis plan...", tagged `sap-v1`) must appear before commit `c91acd2` ("Add
   confirmatory and sensitivity statistical analysis..."), which it does in this repository's
   history.
2. **Read Part A against Part B.** Three deviations are disclosed in Part B: (i) a wording error
   in the first version of DEC-08, corrected before any manuscript number was affected; (ii) a
   real labelling bug in `analyze_results.py`'s synovium figure code, which changes one pair of
   numbers now in the manuscript (H and p); (iii) composition/canonical sensitivity covering 5 of
   12 datasets instead of all 12, with the reason (a pre-existing mismatch between
   `process_phase2_datasets.py` and the already-committed results table for 7 other datasets,
   found, tested, and deliberately left unresolved rather than risked). No other deviation exists.
3. **Pick three numbers from the Abstract or Results and find them in Part C.** Each row names
   the exact source file and, for the smaller files, the exact row or column.
4. **Check the formulas against `scripts/statistical_analysis.py`'s `fisher_pool()` function**
   (also duplicated, identically, in `scripts/sensitivity_analysis.py`): Fisher z transform,
   DerSimonian-Laird tau², Hartung-Knapp-Sidik-Jonkman confidence interval, Benjamini-Hochberg
   (`statsmodels.stats.multitest`, method `fdr_bh`) and Holm (method `holm`) corrections, seed 42
   for every bootstrap and random-triplet procedure (`np.random.default_rng(42)` in
   `sensitivity_analysis.py`).
5. **Confirm every sensitivity analysis S1–S9 is reported somewhere**, even if only as a stated
   limitation: S1 (`stat_S1.csv`), S2 (not run — Part A, P2, stated as a limitation), S3/S7
   (`stat_S3.csv`, `stat_S7.csv`), S4 (`stat_S4.csv`), S6 (not run — P2), S8 (not run — P2), S9
   (`stat_S9.csv`).
6. **Optional, fastest check (about 2 minutes, no network, no raw data needed):**
   `pip install -r requirements.txt` then `python scripts/statistical_analysis.py` from the
   repository root. This script reads only the already-committed
   `results/tables/cart_target_statistics.csv` and reproduces `stat_confirmatory_per_dataset.csv`,
   `stat_pooled_by_target.csv`, `stat_loo.csv`, and `stat_by_tissue.csv` exactly.
7. **Optional, slower check (requires the raw GEO files locally, per `docs/DATA_AVAILABILITY.md`;
   not needed for the check above):** `scripts/sensitivity_analysis.py` and
   `scripts/composition_canonical_analysis.py` reproduce the synovium, combined-score,
   combination-search, and composition/canonical outputs, but need the raw per-dataset files
   (gitignored, not in this repository, downloadable from GEO) present locally first. This is the
   same raw-data arrangement the repository has always used (see README Part 2.7); it is not
   specific to this revision's new scripts.
8. **What this check does not re-verify:** whether `process_phase2_datasets.py`, if re-run fresh
   today for GSE65391, GSE72326, GSE49454, GSE112943, GSE81622, or GSE110169, would reproduce the
   already-committed `cart_target_statistics.csv` values for those six datasets. It was found,
   during this revision, that it currently would not (Part B, Deviation 4), and that script was
   deliberately left unmodified rather than changed mid-revision. This is stated here so the
   reviewer does not discover it independently and wonder why it wasn't mentioned.
