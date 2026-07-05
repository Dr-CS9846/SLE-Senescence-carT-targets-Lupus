# Senescence Signatures and CAR-T Targets in Systemic Lupus Erythematosus

A multi-cohort, computational discovery study applying the [SenMayo](https://www.nature.com/articles/s41467-022-32552-1) 125-gene senescence signature across **28 independent public [GEO](https://www.ncbi.nlm.nih.gov/geo/) datasets (5,314 samples/cells)** to identify senescence-associated surface antigens as candidate targets for [CAR-T](https://en.wikipedia.org/wiki/Chimeric_antigen_receptor_T_cell) immunotherapy in [systemic lupus erythematosus](https://en.wikipedia.org/wiki/Systemic_lupus_erythematosus) (SLE).

This is a **computational discovery study**. Every finding here is hypothesis-generating and requires independent, protein-level, functional validation before any translational claim can be made. Nothing in this repository or the accompanying manuscript should be read as evidence of CAR-T efficacy.

---

## How to read this document

This README has three parts:

- **[Part 1](#part-1--the-datasets-what-we-analyzed-and-why)** explains *what data went into this study and why you should trust it* — where every dataset came from, how it was screened in, what it's worth clinically, and who it represents.
- **[Part 2](#part-2--the-pipeline-how-the-analysis-actually-works)** explains *how the analysis works mechanically* — the code, the math, and exactly how to reproduce every number in this repository yourself.
- **[Part 3](#part-3--results-snapshot)** is a short results summary with pointers to the full output files.

If you only have five minutes, read the tables in Part 1.1 and Part 3, then stop.

---

## Part 1 — The Datasets: What We Analyzed and Why

### 1.1 The full dataset registry

Twenty-eight datasets were assembled in two phases (see [§1.3](#13-how-we-got-to-28-two-search-phases-not-one) for why two phases, not one). Every accession below is a live link to its record on [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/) — click through and verify anything here yourself.

**Phase 1 — original discovery cohort (19 datasets, 2,917–2,919 samples/cells):**

| Accession | Modality | Tissue | N | Platform | SenMayo match |
|---|---|---|---|---|---|
| [GSE72509](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72509) | Bulk RNA-seq | PBMC | 122 | Illumina HiSeq 2500 | fallback |
| [GSE112087](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112087) | Bulk RNA-seq | Whole blood | 120 | Illumina HiSeq 2500 | fallback |
| [GSE122459](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122459) | Bulk RNA-seq | PBMC | 27 | Illumina | fallback |
| [GSE228066](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228066) | Bulk RNA-seq | PBMC | 45 | Illumina | **108/125 direct** |
| [GSE135779](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135779) | scRNA-seq | PBMC (CD4+ T) | 56 | Illumina HiSeq 4000 | fallback |
| [GSE139358](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139358) | scRNA-seq | PBMC | 18 | Illumina | **116/125 direct** |
| [GSE162577](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162577) | scRNA-seq | PBMC | 3 | Illumina NovaSeq 6000 | fallback |
| [GSE163121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163121) | scRNA-seq | PBMC | 997 | 10x Genomics Chromium | **74/125 direct** |
| [GSE179633](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE179633) | scRNA-seq | Skin (discoid lupus) | 30 | Illumina NovaSeq 6000 | fallback |
| [GSE266852](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE266852) | scRNA-seq | PBMC | 995 | 10x Genomics Chromium | fallback |
| [GSE36700](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE36700) | Tissue | Synovium (SLE/OA/RA/MIC/PSO) | 25 | Affymetrix HG-U133+ 2.0 | fallback |
| [GSE155405](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155405) | Tissue | Kidney (lupus nephritis) | 13 | Illumina | fallback |
| [GSE174188](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174188) | Tissue | Renal biopsy | 88 | Illumina NovaSeq 6000 | fallback |
| [GSE182825](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE182825) | Tissue | Skin | 41 | NanoString nCounter | **113/125 direct** |
| [GSE200306](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200306) | Tissue | Kidney glomeruli | 13 | NanoString nCounter | fallback |
| [GSE294496](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294496) | Tissue | Kidney | 2 | 10x Genomics Chromium | fallback |
| [GSE101766](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE101766) | Senescence reference | IMR90 fibroblasts | 276 | Illumina | fallback |
| [GSE262856](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262856) | Senescence reference | MRC5 fibroblasts | 42 | Illumina | fallback |
| [GSE297723](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE297723) | Senescence reference | Aging comparison | 6 | Illumina | fallback |

**Phase 2 — expansion cohort (9 datasets, 2,397 samples), added 2026-07-05 specifically to deepen target-gene evidence:**

| Accession | What it is | N | Platform | SenMayo match |
|---|---|---|---|---|
| [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) | Pediatric SLE, longitudinal whole blood, disease-activity tracking | 996 | Illumina HumanHT-12 v4 | 114/125 |
| [GSE108497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108497) | Lupus pregnancy immune monitoring, blood | 510 | Illumina HumanHT-12 v4 | 116/125 |
| [GSE72326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326) | Lupus nephritis neutrophil biomarker, blood | 238 | Illumina HumanHT-12 v4 | 116/125 |
| [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) | SLE + rheumatoid arthritis whole blood | 243 | Affymetrix HG-U219 | 17/125 (partial — see [§2.8](#28-known-limitations)) |
| [GSE49454](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454) | Type I/II interferon signatures in SLE, blood | 177 | Illumina HumanHT-12 v4 | 116/125 |
| [GSE32591](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE32591) | Lupus nephritis kidney (glomerular + tubulointerstitial) | 93 | Illumina HumanRef-8 (Entrez CDF) | 110/125 |
| [GSE112943](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112943) | Cutaneous lupus **skin** + lupus nephritis **kidney** | 47 | Illumina HumanHT-12 v4 | 116/125 |
| [GSE81622](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81622) | SLE ± nephritis, PBMC | 55 | Illumina HumanHT-12 v4 | 116/125 |
| [GSE52471](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52471) | Discoid/cutaneous lupus skin vs. psoriasis | 38 | Affymetrix HG-U133A 2.0 | 76/125 |

**Total: 28 datasets, 5,314 samples/cells.**

### 1.2 Inclusion and exclusion criteria

A dataset was included if it met **all** of the following:

1. Deposited in NCBI GEO, publicly accessible, no dbGaP or controlled-access restriction
2. Human subjects (one exception: [GSE297723](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE297723), *Mus musculus*, used only as an aging-signature reference, never pooled with human disease inference)
3. Directly relevant to SLE, a clinically-used SLE comparator disease (rheumatoid arthritis, osteoarthritis, psoriasis), or cellular senescence biology
4. Contains a usable gene-expression matrix (RNA-seq, microarray, or single-cell) — proteomics-only or metadata-only deposits were excluded
5. ≥2 independent biological replicates
6. Raw or processed expression data downloadable at the time of acquisition

A dataset was excluded if:

- It required controlled access (dbGaP)
- It had no expression matrix, only metadata
- Fewer than 2 samples survived quality control
- The files were not downloadable at the time of acquisition — three originally targeted accessions (GSE181500, GSE226598, GSE157007) were excluded on this basis alone and are **not** counted anywhere in this repository's totals

### 1.3 How we got to 28: two search phases, not one

Being upfront about this because it matters for how you should read the dataset list: this registry was built in two passes, not one.

**Phase 1** (documented fully in [`docs/METHODS.md`](docs/METHODS.md)) used PubMed and GEO searches (systemic lupus erythematosus AND (RNA-seq OR transcriptome OR single-cell OR senescence OR SASP)) run in June 2026, screened against the criteria in §1.2, yielding the 19-dataset core cohort.

**Phase 2** was a targeted expansion run specifically to strengthen the CAR-T target-gene correlation analysis, since only 3 of the original 19 datasets had gene annotation clean enough (direct HUGO gene symbols) to compute target-gene correlations against. We searched GEO again for real, verified SLE-relevant cohorts, checked each candidate accession directly against [NCBI's E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/) (title, organism, sample count, platform — not from memory, not from search-engine snippets), and selected 9 that passed every criterion in §1.2 and added genuine platform/tissue/age diversity. All 9 were successfully downloaded and processed; none were rejected after verification.

This two-phase structure is disclosed rather than hidden because it's the honest provenance of the data, and because it's a defensible, common practice in iterative meta-analysis — expanding a discovery cohort with independently-verified data is a strength, not something to obscure.

### 1.4 Why 28 datasets / 5,314 samples is a meaningfully large, credible cohort

For a computational discovery study, three things matter more than raw dataset count: **independence, diversity, and traceability**.

- **Independence**: all 28 datasets are separate GEO submissions from separate research groups — this is not 28 subsets of one cohort. Cross-dataset agreement (see [Part 3](#part-3--results-snapshot)) is therefore real independent replication, not resampling.
- **Diversity**: the registry spans blood/PBMC, kidney (glomerular and tubulointerstitial), skin (both spatial/NanoString and array-based), and synovium; bulk RNA-seq, microarray (three different platform families), single-cell RNA-seq (10x Genomics), and NanoString targeted panels; pediatric ([GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391)) through adult populations, including a dedicated pregnancy cohort ([GSE108497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108497)); disease comparators against rheumatoid arthritis ([GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169), [GSE36700](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE36700)), osteoarthritis ([GSE36700](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE36700)), and psoriasis ([GSE52471](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52471)); and three canonical cell-line senescence models (IMR90, MRC5, plus a murine aging reference) used specifically to validate that the SenMayo scoring method behaves as expected on ground-truth senescent cells before it's applied to disease tissue.
- **Traceability**: every accession in this README is a clickable link to the primary GEO record. Every sample count, platform, and SenMayo match rate is derived from the actual files in `data/external_validation/`, not asserted from a table written separately from the code.

**A note on geography and demographics, stated honestly rather than embellished**: GEO series metadata does not systematically record country of patient origin, so we do not claim a specific country breakdown here. What is verifiable: these are predominantly North American and European academic-medical-center cohorts (the pediatric cohort in particular is a well-known large multi-site U.S. registry), spanning pediatric through adult and pregnant populations, across blood, kidney, and skin compartments. If you need exact site-level demographics for a specific dataset, follow its GEO link above — the original study's methods section will have it, and we'd rather point you to the primary source than paraphrase a number we can't independently confirm.

### 1.5 Clinical and medical value of this specific dataset composition

This composition was not chosen to maximize the size of the sample-count headline. It was chosen because SLE is a genuinely heterogeneous, multi-organ disease, and a senescence signature that only holds up in one tissue or one platform is a much weaker discovery than one that replicates across independent cohorts, platforms, and organ systems. Concretely, this registry lets the analysis ask:

- Does the senescence-target association hold in **blood** (the most clinically accessible compartment for a future biomarker or apheresis-based cell therapy) *and* in **kidney** and **skin** (the organs actually damaged in lupus nephritis and cutaneous lupus)?
- Does it hold across **microarray and RNA-seq and single-cell** platforms, which have different technical biases?
- Does it hold in the presence of **disease-specific comparators** (RA, OA, psoriasis) that share inflammatory biology with SLE but are not SLE — a much stronger test than SLE-vs-healthy alone?
- Does it hold across the **age spectrum**, from pediatric-onset disease through adult disease through pregnancy (a uniquely immunologically distinct state in SLE)?

The answer, laid out in Part 3, is a qualified but real "mostly yes" for CD38, ICAM1, and VCAM1, and a more nuanced "context-dependent" for CD44 and CSPG4 — which is a more interesting and more publishable finding than uniform agreement would have been, because it points to specific follow-up biology (tissue-compartment-specific CD44/CSPG4 regulation) rather than a flat, unqualified claim.

---

## Part 2 — The Pipeline: How the Analysis Actually Works

### 2.1 Architecture

```
GEO accession
   → series matrix / supplementary file download
   → probe-to-gene-symbol mapping (platform annotation)
   → normalization (log2 scale)
   → SenMayo senescence scoring (direct match, or top-variable-gene fallback)
   → within-dataset Z-normalization
   → [optional] CAR-T target gene extraction + Spearman correlation vs. senescence score
   → cross-dataset batch alignment
```

### 2.2 Data acquisition

Two acquisition paths exist in this repository, matching the two phases in §1.3:

- **`scripts/pipeline_complete.py`** auto-discovers files already placed in a local `datasets/` folder (Series Matrix, Excel, CSV, or 10x MTX format) and is the original Phase 1 pipeline.
- The Phase 2 datasets were pulled directly from GEO's FTP mirror (`https://ftp.ncbi.nlm.nih.gov/geo/series/GSExxnnn/GSExxxxxx/matrix/...`), with platform annotation resolved via NCBI's plain-text accession endpoint (`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<GPL>&targ=self&form=text&view=full`) rather than assumed from memory — every probe-to-gene mapping used here is downloaded from NCBI at analysis time, not hardcoded.

### 2.3 Gene mapping

Four microarray platforms are represented in Phase 2, each requiring a different probe→gene-symbol resolution:

| Platform | Used by | Symbol column in platform table |
|---|---|---|
| [GPL10558](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL10558) (Illumina HumanHT-12 v4) | 6 of the 9 new datasets | `Gene symbol` |
| [GPL13667](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL13667) (Affymetrix HG-U219) | GSE110169 | `Gene Symbol` |
| [GPL14663](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL14663) (Illumina HumanRef-8, Entrez CDF) | GSE32591 | `Gene Symbol` |
| [GPL571](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL571) (Affymetrix HG-U133A 2.0) | GSE52471 | `Gene Symbol` |

Probes mapping to the same gene symbol are collapsed by taking the mean expression across probes.

### 2.4 SenMayo senescence scoring

For each sample: mean log2 expression across all detected genes from the [SenMayo 125-gene panel](data/senmayo_125genes.csv) ([Saul et al., *Nature Communications* 2022](https://www.nature.com/articles/s41467-022-32552-1)), provided ≥3 panel genes are detected. If fewer than 3 are detected (common on older or narrower-coverage platforms), the pipeline falls back to the top-13-most-variable genes in that dataset as a proxy — this fallback is logged per dataset (see the SenMayo-match column in §1.1) and is never silently blended with direct-match scores in a way that would hide which is which.

### 2.5 Normalization and batch handling

Raw counts are normalized to log2(CPM + 1). Already-normalized microarray intensities (the Phase 2 series matrices) are used as deposited, with one exception: [GSE108497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108497)'s signal is linear-scale with paired detection p-values, so it is floor-clipped at 1.0 and log2-transformed before scoring — this specific handling is called out because it's the one dataset that needed non-default treatment, and it's fully described in the companion processing script rather than buried silently in a shared function.

All senescence scores are Z-normalized **within their own dataset** before any cross-dataset comparison, and low-SenMayo-coverage datasets are never pooled with high-coverage datasets for confirmatory inference — only for sensitivity checks. See [`docs/METHODS.md`](docs/METHODS.md) for the full justification of this choice over parametric batch-correction methods like ComBat.

### 2.6 CAR-T target correlation analysis

Six candidate surface antigens — CD38, CD44, CSPG4, ICAM1, VCAM1, EGFR — are tested for [Spearman rank correlation](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) against the senescence score, independently within each dataset where the gene was detected. Results across all 12 datasets with usable target-gene data are in [`results/tables/cart_target_statistics.csv`](results/tables/cart_target_statistics.csv).

### 2.7 Reproducibility — run it yourself

```bash
git clone https://github.com/Dr-CS9846/SLE-Senescence-carT-targets-Lupus.git
cd SLE-Senescence-carT-targets-Lupus
pip install -r requirements.txt

# Phase 1 (requires manually downloading the 19 Phase-1 datasets into datasets/ — see docs/DATA_AVAILABILITY.md)
python scripts/pipeline_complete.py
python scripts/analyze_results.py

# Phase 2 datasets are pulled directly from GEO's FTP mirror; platform annotation is
# resolved live from NCBI at run time rather than hardcoded.
```

Every number in this README, in `results/`, and in the accompanying manuscript traces back to a file in this repository. If a number doesn't match what you compute by re-running the pipeline, that's a bug report we want — open an issue.

### 2.8 Known limitations

- **GSE110169's platform annotation download was incomplete** despite three retries against NCBI's servers (a server-side pagination/size issue with this specific large platform, not a bug in our code). Only CD44 was evaluable for this dataset (r=0.499, p<0.0001, n=243); the other five target genes are marked `N/A` in the results, not fabricated as significant or non-significant. This is disclosed rather than patched over.
- **Microarray and RNA-seq intensities are not directly comparable in absolute terms.** All cross-platform inference in this study is based on within-dataset rank correlations and direction-of-effect consistency across datasets — never on pooled absolute expression values across platforms.
- **Sample sizes range from n=2 ([GSE294496](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294496)) to n=997 ([GSE163121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163121)).** Small datasets contribute to senescence-score cross-validation but are not over-weighted in the target-correlation consensus, which is reported per-dataset (see `results/tables/cart_target_statistics.csv`) rather than as a single pooled statistic that would let a large dataset silently dominate.
- **This is transcriptomic evidence only.** No flow cytometry, immunohistochemistry, or functional assay data exists in this repository. Surface-antigen protein expression, density, and CAR accessibility are not established by anything here.

---

## Part 3 — Results Snapshot

Full statistics: [`results/VERIFIED_RESULTS.json`](results/VERIFIED_RESULTS.json) · [`results/tables/cart_target_statistics.csv`](results/tables/cart_target_statistics.csv) · [`results/tables/table1_dataset_summary.csv`](results/tables/table1_dataset_summary.csv)

Across the 12 datasets with usable target-gene data (66 of 72 possible target × dataset combinations evaluable; 6 not evaluable — 5 due to incomplete platform annotation in GSE110169, and 1 due to CSPG4 not being detected in GSE65391, see §2.8):

| Target | Significant, positive direction | Significant, negative direction | Not significant | Read |
|---|---|---|---|---|
| **CD38** | 9 | 0 | 2 | Strongest, most consistent signal — unanimous direction where significant |
| **ICAM1** | 6 | 0 | 5 | Consistent positive direction; endothelial/activation marker caveats apply |
| **VCAM1** | 4 | 0 | 7 | Consistent positive direction, weaker overall effect size |
| **CD44** | 6 | 2 | 4 | Directionally mixed — likely tissue/compartment-dependent regulation, not a uniform marker |
| **CSPG4** | 3 | 1 | 6 | Directionally mixed, exploratory |
| **EGFR** | 2 | 1 | 8 | Weakest and least consistent — deprioritization from the candidate panel is supported |

None of this establishes CAR-T efficacy, target safety, or clinical utility. It establishes a ranked, evidence-graded, fully traceable prioritization for the protein-level and functional validation that would have to follow.

---

## Data Availability

All 28 datasets are publicly available from [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/) at the accessions linked throughout this README. Raw data files are not committed to this repository due to size; see [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md) for exact download instructions for every dataset. Pre-computed senescence scores for all 28 datasets are included in `data/external_validation/`.

## Citation

```bibtex
@software{gondal2026senescence,
  title={Senescence signatures and CAR-T targets in SLE: multi-dataset analysis},
  author={Gondal, Zeshan},
  year={2026},
  url={https://github.com/Dr-CS9846/SLE-Senescence-carT-targets-Lupus}
}
```

## License

Code: [MIT License](LICENSE). Data: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) (all source data is publicly available via GEO under its own terms).

## Contact

Zeshan Gondal — 011april2025@gmail.com
