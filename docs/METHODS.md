# Methods

## Study Design

Computational discovery study applying the 125-gene SenMayo senescence signature to 19 public GEO datasets in SLE. This study identifies candidate senescence-associated surface antigens for further investigation; it does not constitute preclinical validation of CAR-T targets.

---

## Dataset Selection

### Inclusion Criteria

Datasets were included if they met ALL of the following:

1. Deposited in NCBI GEO (public, no access restrictions)
2. Human subjects (Homo sapiens), except GSE297723 (Mus musculus, aging reference)
3. Relevant to SLE, autoimmune disease, or cellular senescence
4. Contains gene expression data (RNA-seq, microarray, or targeted RNA)
5. ≥2 biological replicates
6. Published between 2012–2026
7. Raw or processed expression matrix downloadable

### Exclusion Criteria

1. Datasets requiring dbGaP controlled access
2. Proteomics-only datasets (no transcriptomic data)
3. Datasets with <2 samples after quality control
4. Datasets not downloadable at the time of acquisition (June 2026)
5. Datasets lacking expression matrices (metadata-only deposits)

Three initially targeted datasets were excluded post-selection because files were unavailable for download: GSE181500, GSE226598, GSE157007.

### Search Strategy

PubMed and GEO searches (June 1–24, 2026) using terms: "systemic lupus erythematosus" AND ("RNA-seq" OR "transcriptome" OR "single-cell" OR "senescence" OR "SASP"). Cross-referenced with recent SLE CAR-T literature (Mackensen et al. 2022, Müller et al. 2024) for relevant cohorts.

---

## Master Dataset Table

| # | GEO ID | Category | Platform | Tissue | Patients | Samples | Cells | SenMayo Genes Matched | Year |
|---|--------|----------|----------|--------|----------|---------|-------|-----------------------|------|
| 1 | GSE72509 | Bulk RNA-seq | Illumina HiSeq 2500 | PBMC | ~100 SLE + 18 HC | 122 | — | 0/125 (fallback) | 2016 |
| 2 | GSE112087 | Bulk RNA-seq | Illumina HiSeq 2500 | Whole blood | ~120 | 120 | — | 0/125 (fallback) | 2018 |
| 3 | GSE122459 | Bulk RNA-seq | Illumina | PBMC | ~27 | 27 | — | 0/125 (fallback) | 2019 |
| 4 | GSE228066 | Bulk RNA-seq | Illumina | PBMC | ~45 | 45 | — | 108/125 | 2024 |
| 5 | GSE135779 | scRNA-seq | Illumina HiSeq 4000 | PBMC (CD4+ T) | ~20 | 56 | — | 0/125 (fallback) | 2019 |
| 6 | GSE139358 | scRNA-seq | Illumina | PBMC | 18 | 18 | — | 116/125 | 2020 |
| 7 | GSE162577 | scRNA-seq | Illumina NovaSeq 6000 | PBMC | 3 (2 SLE + 1 HC) | 3 | — | 0/125 (fallback) | 2021 |
| 8 | GSE163121 | scRNA-seq | 10x Genomics Chromium | PBMC | 5 (3 SLE + 2 HC) | — | 997 (post-QC) | 74/125 | 2021 |
| 9 | GSE179633 | scRNA-seq | Illumina NovaSeq 6000 | Skin (DLE) | ~30 | 30 | — | 0/125 (fallback) | 2022 |
| 10 | GSE266852 | scRNA-seq | 10x Genomics Chromium | PBMC | Unknown | — | 995 (post-QC) | 0/125 (fallback) | 2024 |
| 11 | GSE36700 | Tissue | Affymetrix HG-U133+ 2.0 | Synovium | 25 (4 SLE, 5 OA, 7 RA, 5 MIC, 4 PSO) | 25 | — | 0/125 (fallback) | 2012 |
| 12 | GSE155405 | Tissue | Illumina | Kidney (LN) | ~13 | 13 | — | 0/125 (fallback) | 2021 |
| 13 | GSE174188 | Tissue | Illumina NovaSeq 6000 | Renal biopsy | ~88 | 88 | — | 0/125 (fallback) | 2022 |
| 14 | GSE182825 | Tissue | NanoString nCounter | Skin | ~20 | 41 | — | 113/125 | 2022 |
| 15 | GSE200306 | Tissue | NanoString nCounter | Kidney glomeruli | ~13 | 13 | — | 0/125 (fallback) | 2022 |
| 16 | GSE294496 | Tissue | 10x Genomics Chromium | Kidney | 2 | 2 | — | 0/125 (fallback) | 2024 |
| 17 | GSE101766 | Senescence Ref | Illumina | IMR90 fibroblasts | — | 276 | — | 0/125 (fallback) | 2017 |
| 18 | GSE262856 | Senescence Ref | Illumina | MRC5 fibroblasts | — | 42 | — | 0/125 (fallback) | 2024 |
| 19 | GSE297723 | Senescence Ref | Illumina | Mouse lung | — | 6 | — | 0/125 (fallback) | 2025 |

### Count Summary

| Metric | Bulk RNA-seq | scRNA-seq | Tissue | Senescence Ref | Total |
|--------|-------------|-----------|--------|----------------|-------|
| Datasets | 4 | 6 | 6 | 3 | **19** |
| Patients (estimated) | ~310 | ~76 | ~161 | N/A (cell lines) | ~547 |
| Samples (bulk/tissue) | 314 | 107 | 182 | 324 | **927** |
| Cells (scRNA, post-QC) | — | 1,992 | — | — | **1,992** |
| Total scored units | 314 | 2,099 | 182 | 324 | **2,919** |

**Important distinction**: "Samples" refers to biological specimens (one per patient in bulk RNA-seq). "Cells" refers to individual cells in scRNA-seq datasets (many cells per patient). The 2,919 total includes both samples and cells. Patient-level analyses (disease comparisons, correlations) use sample-level data. Cell-level analyses (QC, heterogeneity) use single-cell data.

---

## Senescence Scoring

### Gene Panel

The **SenMayo 125-gene senescence signature** (Saul et al., Nature Aging 2022; MSigDB ID: M39564) was used for all scoring. The panel was loaded from `data/senmayo_125genes.csv` and spans 7 functional categories:

- Canonical cell-cycle arrest (CDKN2A, CDKN1A, TP53, RB1, etc.)
- SASP (IL6, CXCL8, MMP3, MMP9, TNF, SERPINE1, IGFBP7, etc.)
- DNA damage response
- Apoptosis regulators
- DNA repair
- Tumor suppressors
- Heat shock proteins

### Scoring Algorithm

For each sample or cell *i* in dataset *d*:

1. **Gene detection**: Identify which SenMayo genes are present in the expression matrix (exact HUGO symbol match, case-sensitive)
2. **Threshold**: If ≥3 SenMayo genes detected, use those genes. If <3, fall back to the 13 most variable genes in the dataset
3. **Raw score**: S_raw(i) = mean expression across detected genes
4. **Within-dataset normalization**: S_z(i) = (S_raw(i) - μ_d) / (σ_d + ε), where μ_d and σ_d are the mean and standard deviation of raw scores within dataset *d*, and ε = 10⁻⁶

### SenMayo Gene Matching

| Match Level | Datasets | Genes Matched | Implication |
|-------------|----------|---------------|-------------|
| High (≥100/125) | GSE228066, GSE139358, GSE182825 | 108–116 | True SenMayo-based scoring |
| Moderate (50–99) | GSE163121 | 74 | Partial SenMayo scoring |
| Fallback (<3) | 15 datasets | 0 | Top-variable-gene proxy (Ensembl/probe IDs) |

**Limitation**: 15 of 19 datasets use Ensembl IDs or Affymetrix probe IDs that do not map to HUGO gene symbols. These datasets use a variable-gene fallback that captures transcriptomic variance but is NOT a direct senescence measurement. Findings from these 15 datasets should be interpreted as exploratory. The 4 datasets with direct SenMayo matching (GSE228066, GSE139358, GSE182825, GSE163121) provide the strongest senescence evidence.

---

## Preprocessing

### Step 1: Format Loading

| Format | Datasets | Method |
|--------|----------|--------|
| Series Matrix TSV | GSE72509, GSE112087, GSE135779, GSE162577, GSE174188, GSE179633, GSE294496, GSE36700 | Auto-skip GEO header lines (lines starting with "!"), then pd.read_csv(sep='\t') |
| Excel (.xlsx) | GSE122459, GSE228066, GSE139358, GSE101766, GSE200306 | pd.read_excel(), first sheet, first column as index |
| CSV | GSE297723 | pd.read_csv() |
| TSV (plain) | GSE112087, GSE155405, GSE182825, GSE262856 | pd.read_csv(sep='\t') |
| 10X MTX sparse | GSE163121, GSE266852 | scipy.io.mmread() + barcode/feature files, transposed to cells × genes |

### Step 2: scRNA-seq Quality Control

Applied only to 10X MTX-loaded datasets (GSE163121, GSE266852):

| Filter | Threshold | Rationale |
|--------|-----------|-----------|
| Min genes per cell | 200 | Remove empty droplets and debris |
| Min cells per gene | 3 | Remove noise genes |
| Max mitochondrial fraction | 0.20 (20%) | Remove dying/damaged cells |
| Cell cap per sample | 1,000 | Memory constraint; representative subsample |

Mitochondrial genes identified by prefix "MT-" (human) or "mt-" (mouse).

### Step 3: Normalization

All datasets normalized identically:

```
expr_normalized = log2( (raw_counts / library_size) × 10^6 + 1 )
```

Where library_size = sum of all gene counts per sample. This is the standard log2(CPM+1) transformation used in bulk and single-cell transcriptomics for cross-sample comparability.

### Step 4: Batch Correction

Two-stage Z-score alignment:

1. **Within-dataset**: Each dataset's senescence scores are Z-normalized (mean=0, sd=1)
2. **Global re-centering**: All Z-normalized scores are concatenated, and a global mean and standard deviation are computed. Each dataset's scores are re-scaled:

```
S_corrected(i) = (S_z(i) - μ_global) / σ_global
```

This approach assumes senescence score distributions are approximately normal within each dataset. It removes dataset-level shifts (platform effects, library preparation differences) while preserving within-dataset biological variation.

**Limitation**: This is a simplified batch correction. Parametric methods (ComBat) or mutual nearest neighbors (MNN) were not applied because the datasets lack shared samples or matched conditions required for those methods. The Z-score approach is conservative and may underestimate true cross-dataset differences.

---

## Statistical Analysis

### Disease Group Comparisons (GSE36700)

- Kruskal-Wallis test: non-parametric comparison across SLE (n=4), OA (n=5), RA (n=7), MIC (n=5), PSO (n=4)
- Pairwise Mann-Whitney U tests (SLE vs each group)
- ROC curve: SLE vs non-SLE classification by senescence score

### CAR-T Candidate Surface Antigen Analysis

Six surface antigens were selected from literature as potential CAR-T targets: CSPG4, CD44, ICAM1, VCAM1, CD38, EGFR. For each target:

- Expression extracted from raw data (3 datasets with HUGO gene names: GSE228066, GSE139358, GSE182825)
- Spearman rank correlation computed between target expression and senescence score
- A target was considered "consistently associated" if significant (p < 0.05) in ≥2 of 3 datasets

**Cautious interpretation**: These correlations identify co-expression patterns between surface antigens and senescence burden. They do NOT demonstrate that these antigens are selectively expressed on senescent cells, that CAR-T cells targeting them would selectively kill senescent cells, or that such an approach would be safe or effective in vivo. Functional validation (flow cytometry, co-culture killing assays, animal models) is required before any translational claims.

### Multiple Testing

Bonferroni correction applied within each target × dataset comparison (6 targets × 3 datasets = 18 tests). FDR (Benjamini-Hochberg) applied for genome-wide differential expression.

---

## External Validation Plan

The following steps are proposed to validate computational findings before any translational claims:

### Tier 1: Computational (immediate)
- [ ] Apply scoring to additional independent SLE cohorts as they become available on GEO
- [ ] Cross-reference target candidates with Human Protein Atlas surface expression data
- [ ] Validate SenMayo scores against established senescence scoring methods (GSVA, ssGSEA)

### Tier 2: In Vitro (required before translational claims)
- [ ] Flow cytometry: Confirm CD38, CD44, CSPG4 surface expression on senescent vs. non-senescent PBMCs from SLE patients
- [ ] Co-culture: Test whether CAR-T cells targeting these antigens selectively kill senescent cells
- [ ] Cytokine profiling: Measure SASP reduction after senescent cell clearance

### Tier 3: In Vivo (required before clinical translation)
- [ ] Lupus mouse models (MRL/lpr or NZB/W F1): senescence burden quantification
- [ ] CAR-T efficacy and safety in murine lupus
- [ ] Off-target toxicity assessment (CD44 and ICAM1 are broadly expressed)

---

## Computational Environment

- **Language**: Python 3.8+
- **Dependencies**: pandas, numpy, scipy, openpyxl, scikit-learn, matplotlib, seaborn (see `requirements.txt`)
- **Pipeline**: `scripts/pipeline_complete.py` (senescence scoring)
- **Analysis**: `scripts/analyze_results.py` (statistics and figures)
- **Container**: `Dockerfile` for reproducible execution
- **Runtime**: ~3 minutes (19 datasets)
- **Memory**: <2 GB

---

## Data Availability

Raw GEO datasets (~2.5 GB) are not included in this repository. Download instructions: `docs/DATA_AVAILABILITY.md`. All processed senescence scores: `data/external_validation/`. Verified results: `results/VERIFIED_RESULTS.json`.

---

## Ethical Considerations

All data from publicly available repositories with prior IRB approval and participant consent. No new human subjects data collected. Analysis conducted in accordance with GEO data use policies.
