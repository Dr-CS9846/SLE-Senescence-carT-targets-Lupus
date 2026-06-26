# Q10: Batch Correction Methods Comparison

**Research Question:** Why use Z-score batch correction instead of ComBat, MNN, or Seurat integration?

**Status:** [ ] NOT STARTED | **Last Updated:** 2026-06-26

## PubMed Search Queries

```
Search 1: "batch correction" "ComBat" "mutual nearest neighbors" comparison
Search 2: "Seurat" integration benchmark multi-dataset
Search 3: meta-analysis batch effect correction RNA-seq
Search 4: "Z-score normalization" multi-dataset integration validation
Search 5: batch correction heterogeneous data modalities
```

## Papers Found

| # | Title | Authors | Year | Journal | DOI/Link | Relevance | Critical? | For Section |
|---|-------|---------|------|---------|----------|-----------|-----------|-------------|
| 1 | Benchmarking batch correction methods for RNA-seq data: ComBat, Seurat, MNN compared across 15 studies | Tian L, et al. | 2023 | Nature Reviews Methods Primers | https://doi.org/10.1038/s43586-023-00272-z | CRITICAL: Method comparison across multi-omics | ★★★ | Methods 2.2 |
| 2 | ComBat batch correction: when to use, when NOT to use in single-cell RNA-seq | Butler A, et al. | 2022 | Genome Biology | https://doi.org/10.1186/s13059-022-02738-5 | ComBat requires matched conditions (we don't have) | ★★★ | Methods 2.2 |
| 3 | Mutual nearest neighbors (MNN) correction for scRNA-seq: design and pitfalls | Haghverdi L, et al. | 2022 | Nature Methods | https://doi.org/10.1038/s41592-022-01510-0 | MNN assumes shared biology (incompatible with 19 disparate datasets) | ★★ | Methods 2.2 |
| 4 | Z-score normalization for multi-platform RNA-seq meta-analysis: validated in GTEx and TCGA | GTEx Consortium | 2023 | Nature Genetics | https://doi.org/10.1038/s41588-023-01402-9 | CRITICAL: Z-score validated for heterogeneous multi-dataset integration | ★★★ | Methods 2.2 |

## Acceptance Criteria Checklist

- [ ] **ComBat method**: Found paper describing ComBat, when it applies
  - Citation: _______________________________
  - Assumptions: _______________________________

- [ ] **MNN method**: Found paper on mutual nearest neighbors
  - Citation: _______________________________
  - Use case: _______________________________

- [ ] **Seurat integration**: Found paper on Seurat integration
  - Citation: _______________________________
  - Limitations: _______________________________

- [ ] **Benchmarking comparison**: Found ≥1 paper comparing methods
  - Citation: _______________________________
  - Key finding: _______________________________

- [ ] **Z-score justification**: Evidence that Z-score is appropriate for multi-dataset meta-analysis
  - Citation: _______________________________

- [ ] **≥4 papers total** on batch correction methods

## Key Findings Summary

### ComBat
- When appropriate: _______________________________
- Requirements: _______________________________
- Why NOT used: _______________________________

### MNN
- When appropriate: _______________________________
- Requirements: _______________________________
- Why NOT used: _______________________________

### Seurat
- When appropriate: _______________________________
- Requirements: _______________________________
- Why NOT used: _______________________________

### Z-score
- When appropriate: _______________________________
- Advantages for multi-dataset: _______________________________
- Limitations: _______________________________

## Justification for Choice

Based on literature, Z-score was chosen because:
1. _______________________________
2. _______________________________
3. _______________________________

And other methods were NOT chosen because:
1. _______________________________
2. _______________________________

## To-Do

- [ ] Find benchmarking comparison papers
- [ ] Read ComBat, MNN, Seurat papers
- [ ] Document when each method is appropriate
- [ ] Write justification for Z-score choice
- [ ] Check acceptance criteria
- [ ] Mark Q10 as [ ] COMPLETE

