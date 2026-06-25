# Data Availability and Download Instructions

## Important: Raw GEO Data Not Included in Repository

This repository contains **analysis scripts and processed results** but **NOT the raw GEO datasets** (~180 GB). Raw RNA-seq files cannot be committed to GitHub due to storage constraints. Instead, they must be downloaded independently from the Gene Expression Omnibus (GEO) database before running the pipeline.

---

## Getting Started: Download Required Datasets

### Step 1: Create datasets folder
```bash
mkdir -p datasets
cd datasets
```

### Step 2: Download datasets from GEO

The following 19 datasets were targeted for integration. Currently, 3/19 (16%) successfully process through the pipeline:

#### Category 1: SLE Bulk RNA-seq (5 datasets)
```bash
# Primary bulk validation cohorts
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE72509 -O GSE72509.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE112087 -O GSE112087.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE122459 -O GSE122459.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE228066 -O GSE228066.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE181500 -O GSE181500.tar
```

#### Category 2: Single-Cell RNA-seq (6 datasets)
```bash
# scRNA-seq cohorts for cell-type resolution
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE135779 -O GSE135779.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE139358 -O GSE139358.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162577 -O GSE162577.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE163121 -O GSE163121.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE179633 -O GSE179633.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE266852 -O GSE266852.tar
```

#### Category 3: Tissue Transcriptomics (6 datasets)
```bash
# Kidney, skin, synovial tissue samples
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE36700 -O GSE36700.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE155405 -O GSE155405.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE174188 -O GSE174188.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE182825 -O GSE182825.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE200306 -O GSE200306.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE294496 -O GSE294496.tar
```

#### Category 4: Senescence Reference (5 datasets)
```bash
# Ground-truth senescence models and validation cohorts
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE101766 -O GSE101766.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE226598 -O GSE226598.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE262856 -O GSE262856.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE297723 -O GSE297723.tar
wget -q https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE157007 -O GSE157007.tar
```

### Step 3: Extract and organize
```bash
for tar in *.tar; do
  tar -xf "$tar"
  rm "$tar"
done
```

---

## Alternative: GEO Query (R/Python)

### Using R
```R
library(GEOquery)
gse <- getGEO("GSE72509", AnnotGpl=TRUE)
```

### Using Python
```python
from GEOparse import get_GEO
gse = get_GEO("GSE72509")
```

---

## File Structure After Download

After successful download and extraction, the `datasets/` folder should contain:

```
datasets/
├── GSE36700_series_matrix.txt
├── GSE72509_SLE_RPKMs.txt
├── GSE101766_Set2_Readcounts.xlsx
├── GSE112087_counts-matrix-EnsembIDs-GRCh37.p10.txt
├── GSE122459_normalized_genes_all_samples.xlsx
├── GSE135779_series_matrix.txt
├── GSE139358_RNA-Seq_gene_rpkm_18_samples.xlsx
├── GSE155405_deseq_out_counts.tab
├── GSE162577_series_matrix.txt
├── GSE174188_series_matrix.txt
├── GSE179633_series_matrix.txt
├── GSE181500_RAW/ (directory)
├── GSE182825_Analyzed_Counts.txt
├── GSE200306_Nanostring_RAW_1-21.xlsx
├── GSE228066_gene.xlsx
├── GSE262856_MRC5_Senescence_Transcriptomics.txt
├── GSE266852_OES19443150_matrix.mtx
├── GSE294496_series_matrix.txt
├── GSE297723_raw_counts.csv
├── GSE163121_RAW/ (directory)
└── GSE226598/ (if available)
```

---

## Running the Pipeline

Once all datasets are downloaded:

```bash
python scripts/pipeline_complete.py
```

This will:
1. Auto-discover all dataset files in `datasets/`
2. Attempt to process all 19 datasets
3. Generate senescence scores in `data/external_validation/` for successfully loaded datasets

Expected runtime: ~5 minutes. Note: Due to file access and format compatibility issues, only 3/19 datasets (16%) currently process successfully.

---

## Successfully Integrated Datasets (3/19 total)

Only 3/19 datasets currently process successfully through the pipeline and generate senescence scores in `data/external_validation/`

**Integration status by category:**
- Bulk RNA-seq: 1/5 successfully processed (GSE228066)
- scRNA-seq: 1/5 successfully processed (GSE139358)
- Tissue: 1/5 successfully processed (GSE36700)
- Senescence Reference: 0/4 successfully processed

---

## Pipeline Failures (16/19 datasets not processed)

### Permission Denied (Windows File Locks)
The following datasets fail with permission errors due to file locks (likely antivirus or file explorer):
- GSE72509, GSE112087, GSE122459, GSE174188, GSE182825, GSE200306

### File Not Found / Format Issues
These datasets either were not downloaded or have format compatibility issues:
- GSE101766, GSE226598, GSE262856, GSE297723 (Senescence reference - not found)
- GSE163121, GSE266852 (scRNA - MTX format or nested structure issues)
- GSE179633 (scRNA - file format issues)

### Reason for Low Success Rate
The high failure rate (16/19) is primarily due to:
1. **Windows file locking** - Files locked by antivirus/file explorer prevent reading
2. **Missing files** - Some datasets incomplete download or unavailable on GEO
3. **Format complexity** - MTX sparse matrices with nested directory structures
4. **Alternative approach needed** - Consider Git LFS or external data storage for large files

---

## Data Citation

All datasets are publicly available and freely accessible from:

**Gene Expression Omnibus (GEO)**  
https://www.ncbi.nlm.nih.gov/geo/

Please cite GEO and individual dataset authors when publishing results using this data.

---

## Reproducibility

The integration pipeline is fully reproducible once datasets are downloaded:

1. **Requirements**: Python 3.8+, pandas, numpy, scipy
2. **Time**: ~5 minutes to run on standard laptop
3. **Output**: Senescence scores (CSV files) in `data/external_validation/`
4. **All processing is deterministic** — same input datasets → same output scores

---

## Questions or Issues?

For GEO dataset access issues:
- GEO Help: https://www.ncbi.nlm.nih.gov/grc/submit/tools/eutils/
- Contact GEO: geo@ncbi.nlm.nih.gov

For pipeline issues:
- Check `DATA_MANIFEST.md` for dataset specifics
- See `METHODS.md` for methodology details
- Review `scripts/pipeline_complete.py` for implementation

