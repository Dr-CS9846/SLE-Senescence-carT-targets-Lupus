# Senescence Signatures and CAR-T Targets in Systemic Lupus Erythematosus

Exploratory multi-dataset analysis of cellular senescence burden across SLE cohorts, with hypothesis-generating identification of senescence-enriched surface antigens as candidate CAR-T targets.

## Overview

This project applies the 125-gene SenMayo senescence signature (Saul et al., MSigDB) to 19 public GEO datasets spanning bulk RNA-seq, single-cell RNA-seq, and tissue transcriptomics. The goal is to characterize senescence patterns across SLE immune cells and tissues, and to identify senescence-associated surface antigens that may warrant further investigation as CAR-T targets.

This is a computational discovery study. All findings are hypothesis-generating and require independent experimental validation.

## Data Sources

All datasets are publicly available from GEO (https://www.ncbi.nlm.nih.gov/geo/). Raw data files are not included in this repository due to size (~2.5 GB); see [docs/DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md) for download instructions.

### Bulk RNA-seq (4 datasets, 314 samples)
| Dataset | Samples | Description |
|---------|---------|-------------|
| GSE72509 | 122 | SLE + HC PBMC |
| GSE112087 | 120 | Whole blood transcriptomics |
| GSE122459 | 27 | PBMC gene expression |
| GSE228066 | 45 | Activity-stratified SLE |

### Single-Cell RNA-seq (6 datasets, 2,099 scored units)
| Dataset | Patients | Cells (post-QC) | Description |
|---------|----------|-----------------|-------------|
| GSE135779 | ~20 | 56 | CD4+ T cells |
| GSE139358 | 18 | 18 | Whole PBMC |
| GSE162577 | 3 | 3 | SLE vs HC paired |
| GSE163121 | 5 | 997 | SLE + HC PBMC (10X) |
| GSE179633 | ~30 | 30 | Cutaneous lupus |
| GSE266852 | — | 995 | SLE scRNA-seq (10X) |

### Tissue Transcriptomics (6 datasets, 182 samples)
| Dataset | Samples | Description |
|---------|---------|-------------|
| GSE36700 | 25 | Synovial biopsies (SLE, OA, RA) |
| GSE155405 | 13 | Kidney (lupus nephritis) |
| GSE174188 | 88 | Renal biopsies |
| GSE182825 | 41 | Skin spatial transcriptomics |
| GSE200306 | 13 | Kidney glomeruli |
| GSE294496 | 2 | Kidney scRNA |

### Senescence Reference (3 datasets, 324 samples)
| Dataset | Samples | Description |
|---------|---------|-------------|
| GSE101766 | 276 | IMR90 senescence induction |
| GSE262856 | 42 | MRC5 senescence transcriptomics |
| GSE297723 | 6 | Aging comparison |

## Installation

```bash
git clone https://github.com/Dr-CS9846/SLE-Senescence-carT-targets-Lupus.git
cd SLE-Senescence-carT-targets-Lupus
pip install -r requirements.txt
```

Requirements: Python 3.8+, pandas, numpy, scipy, openpyxl

## Usage

```bash
# Download datasets from GEO first (see docs/DATA_AVAILABILITY.md)
python scripts/pipeline_complete.py
```

This generates per-dataset senescence scores (Z-normalized) in `data/external_validation/`.

## Methods

### Senescence scoring
Senescence is scored using the **125-gene SenMayo panel** (loaded from `data/senmayo_125genes.csv`). For each sample, the pipeline computes mean expression of detected SenMayo genes (minimum 3 required), then Z-normalizes across the cohort. If fewer than 3 SenMayo genes are detected in a dataset, the pipeline falls back to the top 13 most variable genes as a proxy.

### Normalization
All expression data are normalized to log2(CPM + 1) before scoring.

### Pipeline
`scripts/pipeline_complete.py` is the sole analysis script. It auto-discovers datasets in the `datasets/` folder, handles multiple file formats (Series Matrix, Excel, CSV, 10X MTX sparse), and outputs standardized senescence scores.

### Current pipeline results
19/19 available datasets process successfully (see `pipeline_final.log`). Three target datasets (GSE181500, GSE226598, GSE157007) were not available for download.

Full methods: [docs/METHODS.md](docs/METHODS.md)

## Limitations

- **Computational discovery only.** No functional validation (flow cytometry, killing assays, animal models). All target nominations are hypothesis-generating.
- **Batch correction** uses Z-score global re-centering across datasets. Parametric methods (ComBat) were not applied as datasets lack shared samples.
- **scRNA-seq QC** includes mitochondrial filtering, min-genes, and min-cells thresholds. Doublet detection was not applied. MTX datasets are capped at 1,000 cells per sample.
- **Surface target plausibility** requires orthogonal validation. CD44 and ICAM1 are broadly expressed; CSPG4 is not a canonical immune marker.

## Repository Structure

```
scripts/pipeline_complete.py     # Senescence scoring pipeline (125-gene SenMayo)
scripts/analyze_results.py       # Downstream statistical analysis and figures
data/senmayo_125genes.csv        # 125-gene SenMayo panel
data/external_validation/        # Per-dataset senescence scores (CSV)
results/figures/                 # Publication figures (8 multi-panel)
results/tables/                  # Statistical tables (CSV)
docs/METHODS.md                  # Detailed methods
docs/RESULTS.md                  # Key findings
docs/DATA_AVAILABILITY.md        # Dataset download instructions
pipeline_final.log               # Pipeline execution log
```

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

Code: MIT License
Data: CC-BY-4.0 (publicly available GEO datasets)

## Contact

Zeshan Gondal
Email: 011april2025@gmail.com
