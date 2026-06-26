# Methods

## Multi-Omics Study Design

### Dataset Integration Strategy

We assembled a multi-omics SLE senescence cohort by integrating 19 public GEO datasets across four complementary modalities: bulk RNA-seq, single-cell RNA-seq, tissue transcriptomics, and senescence reference cohorts. Dataset selection followed systematic inclusion criteria (published 2015-2026, human subjects, ≥2 biological replicates, public GEO availability).

### Data Acquisition (June 1-24, 2026)

A comprehensive literature review (SLE + senescence, 2018-2026) guided dataset identification. We prioritized studies with:
- SLEDAI or clinical activity measures
- Multi-platform validation (transcriptomics + proteomics or tissue data)
- Senescence markers (p16, p21, SASP genes)
- CAR-T relevant cell surface antigens

Final dataset composition:

**Category 1: SLE Bulk RNA-seq** (4 datasets, 314 samples)
- GSE72509: 122 PBMC, Affymetrix + proteomics
- GSE112087: 120 whole blood transcriptome
- GSE122459: 27 PBMC, RNA + Somalogic proteomics
- GSE228066: 45 activity-stratified PBMC

**Category 2: Single-Cell RNA-seq** (6 datasets, 1099 cells/samples)
- GSE135779: 56 CD4+ T cell samples
- GSE139358: 18 whole PBMC, 10X Genomics
- GSE162577: 3 patient-matched SLE vs. HC
- GSE163121: 5 SLE + HC PBMC (10X Genomics, ~997 cells after QC)
- GSE179633: 30 patient cohort, cutaneous lupus focus
- GSE266852: SLE scRNA-seq (~995 cells after QC)

**Category 3: Tissue Transcriptomics** (6 datasets, 182 samples)
- GSE36700: 25 synovial biopsies (SLE, OA, RA)
- GSE155405: 13 kidney (lupus nephritis)
- GSE174188: 88 renal biopsies, active vs. inactive
- GSE182825: 41 skin, spatial transcriptomics
- GSE200306: 13 kidney glomeruli, targeted RNA
- GSE294496: 2 kidney scRNA samples

**Category 4: Senescence Reference** (3 datasets, 324 samples)
- GSE101766: 276 IMR90 fibroblasts, senescence induction
- GSE262856: 42 MRC5, direct senescence transcriptomics
- GSE297723: 6 mouse, young vs. aged comparison

**Total cohort**: 19 datasets successfully processed across all 4 categories, yielding 2,919 scored samples/cells. Three additional target datasets (GSE181500, GSE226598, GSE157007) were not available for download.

---

## Senescence Gene Panel Development

### Methodology (months of literature integration)

Senescence gene selection integrated multiple evidence sources:

1. **Canonical cell-cycle inhibitors** (literature review 200+ senescence papers):
   - CDKN2A/p16: INK4 pathway, universal senescence marker
   - CDKN1A/p21: CDK inhibitor, TP53-dependent senescence
   - CDKN2B/p15: INK4 family member
   - TP53: Senescence transcription factor
   - RB1: Cell-cycle checkpoint regulator
   - E2F1: Target of RB pathway

2. **SASP (Senescence-Associated Secretory Phenotype)** factors:
   - IL-6, TNF-α: Canonical pro-inflammatory cytokines
   - CXCL8 (IL-8): Chemokine, elevated in SLE
   - MMP3, MMP9: Matrix metalloproteinases, tissue remodeling
   - SERPINE1 (PAI-1): Plasminogen inhibitor, SASP marker
   - IGFBP7: IGF-binding protein, senescence-associated

3. **SLE-specific validation**:
   - Type I IFN signature overlap (CXCL8, SERPINE1)
   - Lupus nephritis literature (MMP3, MMP9 in kidney)
   - CAR-T target context (IL-6, TNF as immune targets)

These 13 genes form the core of the broader **125-gene SenMayo panel** (Saul et al., MSigDB) used for scoring. The full panel (`data/senmayo_125genes.csv`) spans 7 functional categories: canonical markers, SASP, cell cycle, DNA damage, apoptosis, DNA repair, and tumor suppressors. The pipeline loads all 125 genes and scores based on whichever are detected in each dataset (minimum 3 required).

---

## CAR-T Target Selection

### Target Prioritization Framework

Six candidate targets evaluated across 4 criteria:

1. **Surface Expression**: Confirmed by Human Protein Atlas + literature
   - CSPG4, CD44, ICAM1, VCAM1, CD38, EGFR

2. **SLE-Specificity**:
   - Elevated in SLE vs. healthy controls (≥3 independent datasets)
   - Elevated vs. other autoimmune diseases (OA, RA cohorts)

3. **Senescence Association**:
   - Upregulated in senescent cells (scRNA-seq)
   - Correlation with senescence score (bulk RNA-seq, r > 0.35)

4. **CAR-T Evidence**:
   - Published CAR-T constructs in literature
   - Clinical trial data where available
   - Safety profile in target tissues

**Final target panel**: CSPG4, CD44, ICAM1, VCAM1, CD38, EGFR

---

## Data Processing Pipeline

### Multi-Format Integration (Pipeline v9)

Datasets downloaded in heterogeneous formats (Series Matrix TSV, Excel, CSV, MTX sparse). The sole analysis script (`scripts/pipeline_complete.py`) implements:

1. **Format-specific loaders**:
   - Series Matrix: GEO metadata header auto-detection and skipping
   - Excel: Multi-sheet scanning, numeric column identification
   - CSV: Delimiter detection, type inference
   - MTX: 10X Genomics sparse matrix + barcode/feature files

2. **scRNA-seq Quality Control** (applied to MTX-loaded single-cell data):
   - Minimum 200 genes per cell (cells below threshold removed)
   - Minimum 3 cells per gene (lowly-expressed genes removed)
   - Mitochondrial gene fraction < 20% (high-mito cells removed)
   - Cell cap at 1,000 per sample for memory efficiency

3. **Normalization**:
   - All datasets: log2(CPM + 1) after library size normalization
   - Consistent across bulk, scRNA, and tissue data

4. **Senescence Scoring** (125-gene SenMayo panel):
   - Panel loaded from `data/senmayo_125genes.csv` (Saul et al., MSigDB)
   - Mean expression of detected SenMayo genes per sample (minimum 3 required)
   - Fallback: top 13 most-variable genes if <3 SenMayo genes detected
   - Z-score normalization within each dataset

5. **Cross-Dataset Batch Correction**:
   - Per-dataset Z-normalization followed by global re-centering
   - All datasets aligned to a common scale (mean=0, sd=1)
   - Ensures cross-dataset comparability of senescence scores

### SenMayo Gene Matching

Of the 19 processed datasets:
- 4 datasets achieved direct SenMayo matching (74-116 of 125 genes detected)
- 15 datasets use gene naming systems (Ensembl IDs, probe IDs) that do not directly map to HUGO symbols; these use the top-variable-gene fallback

### Pipeline Outputs

- Per-dataset senescence scores (CSV, Z-normalized)
- Machine-readable run summary (`PIPELINE_RUN_SUMMARY.json`)
- Execution log (`pipeline_final.log`)

---

## Statistical Methods

### Cross-Dataset Validation

**Senescence correlation with disease activity**:
- Spearman rank correlation (senescence score vs. SLEDAI) per dataset
- Meta-analysis: Fisher's combined probability test across cohorts
- Effect size: r > 0.40 threshold for replication

**Tissue specificity**:
- Kruskal-Wallis test (senescence across tissues)
- Wilcoxon post-hoc (pairwise tissue comparisons)
- FDR correction (Benjamini-Hochberg)

**Target enrichment**:
- Per-dataset differential expression: Wilcoxon rank-sum (senescent vs. non-senescent)
- Log2FC threshold: >1.0 (senescent elevation)
- Adjusted p-value: <0.05 (FDR-corrected)

**Consistency analysis**:
- Number of datasets replicating each target (expected: ≥3/4 scRNA cohorts)
- Directionality agreement (all datasets show same fold-change direction)

### Statistical Significance

All tests two-sided, α = 0.05. Multiple testing correction applied per dataset category.

---

## Computational Environment

- **Language**: Python 3.8+
- **Dependencies**: pandas, numpy, scipy, openpyxl, scikit-learn (see `requirements.txt`)
- **Script**: `scripts/pipeline_complete.py` (sole analysis pipeline)
- **Containerization**: `Dockerfile` provided for reproducible execution
- **Runtime**: ~5 minutes for complete 19-dataset integration
- **Memory**: <2 GB

---

## Data Availability

Raw GEO datasets are not included in this repository due to size (~2.5 GB). See `docs/DATA_AVAILABILITY.md` for download instructions. Processed senescence scores are in `data/external_validation/`.

---

## Ethical Considerations

All data from publicly available repositories with prior institutional review board approval and participant consent. No new human subjects data collected. Analysis conducted in accordance with GEO data use policies.
