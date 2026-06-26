# Data Availability

## Raw Data

Raw GEO datasets (~2.5 GB) are not included in this repository. All 19 datasets are publicly available from the NCBI Gene Expression Omnibus at https://www.ncbi.nlm.nih.gov/geo/.

## Download Instructions

```bash
mkdir -p datasets && cd datasets
```

### Bulk RNA-seq (4 datasets)
Download supplementary files from each GEO accession page:
- [GSE72509](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72509)
- [GSE112087](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112087)
- [GSE122459](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122459)
- [GSE228066](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228066)

### Single-Cell RNA-seq (6 datasets)
- [GSE135779](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135779)
- [GSE139358](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139358)
- [GSE162577](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162577)
- [GSE163121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163121)
- [GSE179633](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE179633)
- [GSE266852](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE266852)

### Tissue Transcriptomics (6 datasets)
- [GSE36700](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE36700)
- [GSE155405](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155405)
- [GSE174188](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174188)
- [GSE182825](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE182825)
- [GSE200306](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200306)
- [GSE294496](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294496)

### Senescence Reference (3 datasets)
- [GSE101766](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE101766)
- [GSE262856](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262856)
- [GSE297723](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE297723)

## Running the Pipeline

```bash
pip install -r requirements.txt
python scripts/pipeline_complete.py
python scripts/analyze_results.py
```

Pipeline processes all 19 datasets in ~3 minutes. Results are written to `data/external_validation/` (senescence scores) and `results/` (figures, tables, statistics).

## Processed Outputs

Pre-computed senescence scores and analysis results are included in the repository:
- `data/external_validation/` — per-dataset senescence scores (CSV)
- `results/figures/` — 8 publication figures (PNG)
- `results/tables/` — statistical tables (CSV)
- `results/VERIFIED_RESULTS.json` — machine-readable results summary

## Contact

For GEO access issues: geo@ncbi.nlm.nih.gov
For pipeline issues: see `docs/METHODS.md`
