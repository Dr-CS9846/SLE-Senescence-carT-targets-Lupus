# Data Availability

## Raw Data

Raw GEO datasets are not included in this repository. All 28 datasets (19 Phase 1 + 9 Phase 2, see README §1.3) are publicly available from the NCBI Gene Expression Omnibus at https://www.ncbi.nlm.nih.gov/geo/.

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

### Phase 2 — Expansion Cohort (9 datasets, added 2026-07-05)

Downloaded directly from GEO's FTP series-matrix mirror (`https://ftp.ncbi.nlm.nih.gov/geo/series/GSExxnnn/GSExxxxxx/matrix/`), with the exception of GSE108497 whose usable expression data is in its `suppl/` normalized-data file rather than its series matrix (its series matrix table is empty; see repository note in `data/external_validation/5_New_SLE_Cohorts/`).

- [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) — pediatric SLE longitudinal whole blood
- [GSE108497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108497) — lupus pregnancy immune monitoring
- [GSE72326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326) — lupus nephritis neutrophil biomarker
- [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) — SLE + RA whole blood
- [GSE49454](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454) — SLE interferon signatures
- [GSE32591](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE32591) — lupus nephritis kidney
- [GSE112943](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112943) — cutaneous lupus skin + lupus nephritis kidney
- [GSE81622](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81622) — SLE ± nephritis PBMC
- [GSE52471](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52471) — discoid lupus vs. psoriasis skin

Platform annotation (probe → gene symbol) for these 9 datasets was resolved live from NCBI (`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<GPL>&targ=self&form=text&view=full`) for GPL10558, GPL14663, and GPL571. GPL13667's annotation download was incomplete after repeated attempts (see README §2.8); GSE110169's CD44 result is unaffected, the other five target genes are marked not evaluable for that dataset only.

## Running the Pipeline

```bash
pip install -r requirements.txt
python scripts/pipeline_complete.py
python scripts/analyze_results.py
```

Phase 1 processes 19 datasets in ~3 minutes. Phase 2's 9 datasets were processed via a separate script that downloads directly from GEO and resolves platform annotation live; see README §2.7 for the exact commands. Results are written to `data/external_validation/` (senescence scores) and `results/` (figures, tables, statistics).

## Processed Outputs

Pre-computed senescence scores and analysis results are included in the repository:
- `data/external_validation/` — per-dataset senescence scores (CSV)
- `results/figures/` — 8 publication figures (PNG)
- `results/tables/` — statistical tables (CSV)
- `results/VERIFIED_RESULTS.json` — machine-readable results summary

## Contact

For GEO access issues: geo@ncbi.nlm.nih.gov
For pipeline issues: see `docs/METHODS.md`
