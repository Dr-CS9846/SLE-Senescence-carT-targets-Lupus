# Data Manifest

Raw GEO datasets are stored locally (~2.5 GB), not committed to this repository. See `docs/DATA_AVAILABILITY.md` for download instructions.

**Pipeline Status**: 19/19 datasets successfully processed (2,919 samples/cells)  
**Last Updated**: June 26, 2026  
**Pipeline Version**: v9 (`scripts/pipeline_complete.py`)

---

## Dataset Inventory

### Category 1: SLE Bulk RNA-seq (4 datasets, 314 samples)

| Dataset | Samples | Format | Platform | Status |
|---------|---------|--------|----------|--------|
| GSE72509 | 122 | TSV (RPKM) | Illumina HiSeq 2500 | ✅ Processed |
| GSE112087 | 120 | TSV (Ensembl counts) | Illumina HiSeq 2500 | ✅ Processed |
| GSE122459 | 27 | Excel (normalized) | Illumina | ✅ Processed |
| GSE228066 | 45 | Excel (gene counts) | Illumina | ✅ Processed (108/125 SenMayo matched) |

### Category 2: Single-Cell RNA-seq (6 datasets, 1,099 samples/cells)

| Dataset | Samples | Format | Platform | Status |
|---------|---------|--------|----------|--------|
| GSE135779 | 56 | Series Matrix | Illumina HiSeq 4000 | ✅ Processed |
| GSE139358 | 18 | Excel (RPKM) | Illumina | ✅ Processed (116/125 SenMayo matched) |
| GSE162577 | 3 | Series Matrix | Illumina NovaSeq 6000 | ✅ Processed |
| GSE163121 | 997 | 10X MTX sparse | 10x Genomics Chromium | ✅ Processed (74/125 SenMayo matched, QC applied) |
| GSE179633 | 30 | Series Matrix | Illumina NovaSeq 6000 | ✅ Processed |
| GSE266852 | 995 | MTX sparse | 10x Genomics Chromium | ✅ Processed |

### Category 3: Tissue Transcriptomics (6 datasets, 182 samples)

| Dataset | Samples | Format | Tissue | Status |
|---------|---------|--------|--------|--------|
| GSE36700 | 25 | Series Matrix | Synovium (SLE/OA/RA) | ✅ Processed |
| GSE155405 | 13 | TSV (DESeq counts) | Kidney (lupus nephritis) | ✅ Processed |
| GSE174188 | 88 | Series Matrix | Renal biopsy | ✅ Processed |
| GSE182825 | 41 | TSV (NanoString) | Skin | ✅ Processed (113/125 SenMayo matched) |
| GSE200306 | 13 | Excel (NanoString) | Kidney glomeruli | ✅ Processed |
| GSE294496 | 2 | Series Matrix | Kidney scRNA | ✅ Processed |

### Category 4: Senescence Reference (3 datasets, 324 samples)

| Dataset | Samples | Format | Model | Status |
|---------|---------|--------|-------|--------|
| GSE101766 | 276 | Excel (read counts) | IMR90 fibroblast senescence | ✅ Processed |
| GSE262856 | 42 | TSV | MRC5 senescence transcriptomics | ✅ Processed |
| GSE297723 | 6 | CSV (raw counts) | Aging comparison | ✅ Processed |

---

## Pipeline Output

All senescence scores are generated in `data/external_validation/` with the following structure:

```
data/external_validation/
├── 1_Bulk_Expansion/
│   ├── GSE72509/GSE72509_senescence_scores.csv
│   ├── GSE112087/GSE112087_senescence_scores.csv
│   ├── GSE122459/GSE122459_senescence_scores.csv
│   └── GSE228066/GSE228066_senescence_scores.csv
├── 2_scRNA_Expansion/
│   ├── GSE135779/GSE135779_senescence_scores.csv
│   ├── GSE139358/GSE139358_senescence_scores.csv
│   ├── GSE162577/GSE162577_senescence_scores.csv
│   ├── GSE163121_RAW/GSE163121_RAW_senescence_scores.csv
│   ├── GSE179633/GSE179633_senescence_scores.csv
│   └── GSE266852_.../GSE266852_..._senescence_scores.csv
├── 3_Tissue_Expansion/
│   ├── GSE36700/GSE36700_senescence_scores.csv
│   ├── GSE155405/GSE155405_senescence_scores.csv
│   ├── GSE174188/GSE174188_senescence_scores.csv
│   ├── GSE182825/GSE182825_senescence_scores.csv
│   ├── GSE200306/GSE200306_senescence_scores.csv
│   └── GSE294496/GSE294496_senescence_scores.csv
├── 4_Senescence_Validation/
│   ├── GSE101766/GSE101766_senescence_scores.csv
│   ├── GSE262856/GSE262856_senescence_scores.csv
│   └── GSE297723/GSE297723_senescence_scores.csv
└── PIPELINE_RUN_SUMMARY.json
```

---

## Verification

- [x] All 19 datasets present in datasets/ folder
- [x] Pipeline processes all 19 datasets successfully
- [x] Senescence scores generated for all 19 datasets
- [x] Batch correction applied across datasets
- [x] scRNA-seq QC applied to MTX-loaded datasets
