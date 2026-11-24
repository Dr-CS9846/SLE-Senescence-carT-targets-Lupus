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

- **DEC-08.** The combined score is the mean of the within-dataset z-scores of CD38, CD44, and
  CSPG4. This matches what the existing code (`scripts/analyze_results.py`) already computes;
  it is written down here, before any new confirmatory run, as the pre-specified definition. The
  combination's history is disclosed in Part B: earlier manuscript text named a different third
  marker (ICAM1) in places, while the committed code has always used CSPG4. Both facts are
  stated plainly, not reconciled by changing either without saying so.

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

*Not yet completed. To be filled in after the confirmatory analysis (plan step 1.8) is run,
with every deviation from Part A listed by ID and reason, or "none" if there is none.*

## Part C — Traceability

*Not yet completed. To be filled in after step 1.8, mapping every Abstract and Results number
to its source file and cell.*

## Part D — How to check

*Not yet completed. To be filled in at step 4 (statistician hand-off), after Parts B and C
exist.*
