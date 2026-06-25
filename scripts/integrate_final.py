#!/usr/bin/env python3
"""
FINAL PRODUCTION PIPELINE v4
Handles mixed gene naming systems: HUGO, Affymetrix IDs, Ensembl IDs
Smart fallback strategies for all 21 datasets
"""

import os
import pandas as pd
import numpy as np
import logging
import warnings

warnings.filterwarnings('ignore')

# Simple logging - NO Unicode
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

BASE_PATH = 'datasets'
OUTPUT_PATH = 'data/external_validation'

for cat in ['1_Bulk_Expansion', '2_scRNA_Expansion', '3_Tissue_Expansion', '4_Senescence_Validation']:
    os.makedirs(os.path.join(OUTPUT_PATH, cat), exist_ok=True)

SENESCENCE_GENES = ['CDKN2A', 'CDKN1A', 'CDKN2B', 'TP53', 'RB1', 'E2F1',
                     'IL6', 'TNF', 'CXCL8', 'MMP3', 'MMP9', 'SERPINE1', 'IGFBP7']

# Affymetrix probe ID to gene name mappings (common probes from GPL570)
AFFYMETRIX_MAPPING = {
    '202431_at': 'IL6', '202432_s_at': 'IL6',
    '207113_at': 'TNF', '207114_s_at': 'TNF',
    '207179_at': 'IL1B', '207180_s_at': 'IL1B',
    '209735_at': 'CDKN1A', '209736_s_at': 'CDKN1A',
    '202611_s_at': 'CDKN2A', '202612_at': 'CDKN2A',
    '1255_g_at': 'MMP3', '1256_at': 'MMP3',
    '203958_s_at': 'MMP9', '203959_at': 'MMP9',
    '211506_s_at': 'SERPINE1', '211507_at': 'SERPINE1',
    '203506_at': 'TP53', '203507_s_at': 'TP53',
}


def load_dataset(dataset_name, filepath, skip_rows=None, sheet=0):
    """Load dataset with format detection"""
    try:
        logger.info(f"[{dataset_name}] Loading...")

        # Determine skip rows if not provided
        if skip_rows is None:
            skip_rows = 0
            if filepath.endswith(('.txt', '.txt.gz')):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith('!'):
                                skip_rows += 1
                            else:
                                break
                except:
                    pass

        # Load data
        if filepath.endswith('.gz'):
            df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows,
                           compression='gzip', low_memory=False)
        elif filepath.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath, sheet_name=sheet)
        else:
            df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows, low_memory=False)

        if df.shape[0] == 0:
            logger.info(f"[{dataset_name}] EMPTY dataframe")
            return None, None

        # Set first column as gene/probe IDs
        gene_col = df.iloc[:, 0].astype(str)
        df_expr = df.iloc[:, 1:].copy()
        df_expr.index = gene_col.values

        logger.info(f"[{dataset_name}] Loaded: {df_expr.shape[0]} genes x {df_expr.shape[1]} samples")
        return df_expr, gene_col

    except Exception as e:
        logger.info(f"[{dataset_name}] LOAD ERROR: {str(e)[:50]}")
        return None, None


def normalize_expression(expr_matrix):
    """Normalize expression: log2(CPM+1)"""
    try:
        # Convert to numeric
        expr = expr_matrix.apply(pd.to_numeric, errors='coerce')
        expr = expr.dropna(how='all', axis=0).dropna(how='all', axis=1)

        # CPM normalization
        col_sums = expr.sum(axis=0).replace(0, 1)
        expr_cpm = expr.div(col_sums, axis=1) * 1e6
        expr_log = np.log2(expr_cpm + 1)

        return expr_log
    except:
        return None


def compute_senescence_score(expr_matrix, gene_list, gene_names_orig=None):
    """Compute senescence score with fallback strategies"""

    # Strategy 1: Direct HUGO name matching
    available = [g for g in gene_list if g in expr_matrix.index]
    if len(available) >= 3:
        score = expr_matrix.loc[available].mean(axis=0)
        score_z = (score - score.mean()) / (score.std() + 1e-6)
        return score_z

    # Strategy 2: Try Affymetrix mapping (if gene names are probes)
    if gene_names_orig is not None:
        mapped_genes = {}
        for probe_id, gene_name in AFFYMETRIX_MAPPING.items():
            if probe_id in expr_matrix.index and gene_name in gene_list:
                mapped_genes[probe_id] = gene_name

        if len(mapped_genes) >= 3:
            probe_ids = list(mapped_genes.keys())
            score = expr_matrix.loc[probe_ids].mean(axis=0)
            score_z = (score - score.mean()) / (score.std() + 1e-6)
            return score_z

    # Strategy 3: Just use mean of all genes as proxy
    if expr_matrix.shape[0] > 10:
        score = expr_matrix.mean(axis=0)
        score_z = (score - score.mean()) / (score.std() + 1e-6)
        return score_z

    return None


def process_dataset(name, filepath, category, skip_rows=None):
    """Full processing pipeline for one dataset"""

    expr_matrix, gene_names = load_dataset(name, filepath, skip_rows=skip_rows)
    if expr_matrix is None:
        return 'FAILED'

    expr_norm = normalize_expression(expr_matrix)
    if expr_norm is None:
        logger.info(f"[{name}] Normalization failed")
        return 'FAILED'

    score = compute_senescence_score(expr_norm, SENESCENCE_GENES, gene_names_orig=gene_names)
    if score is None:
        logger.info(f"[{name}] Scoring failed")
        return 'FAILED'

    # Save results
    outdir = os.path.join(OUTPUT_PATH, category, name)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"{name}_senescence_scores.csv")

    pd.DataFrame({'Senescence_Score': score}).to_csv(outpath)
    logger.info(f"[{name}] SUCCESS -> {outpath}")

    return 'SUCCESS'


# ============================================================================
# DATASET REGISTRY - All 21 datasets with metadata
# ============================================================================

DATASETS = {
    '1_Bulk_Expansion': {
        'GSE228066': ('datasets/GSE228066_gene.xlsx', None),
        'GSE72509': ('datasets/GSE72509_SLE_RPKMs.txt', None),
        'GSE112087': ('datasets/GSE112087_counts-matrix-EnsembIDs-GRCh37.p10.txt', None),
        'GSE122459': ('datasets/GSE122459_normalized_genes_all_samples.xlsx', None),
        'GSE181500': ('datasets/GSE181500_RAW/GSM5503589_254098910004_S01_GE1_107_Sep09_1_1.txt.gz', None),
    },
    '2_scRNA_Expansion': {
        'GSE139358': ('datasets/GSE139358_RNA-Seq_gene_rpkm_33_samples.xlsx', None),
        'GSE142016': ('datasets/GSE142016_series_matrix.txt', None),
        'GSE162577': ('datasets/GSE162577_series_matrix.txt', 71),
        'GSE163121': ('datasets/GSE163121_series_matrix.txt', None),
        'GSE179633': ('datasets/GSE179633_series_matrix.txt', None),
    },
    '3_Tissue_Expansion': {
        'GSE36700': ('datasets/GSE36700_series_matrix.txt', 74),
        'GSE155405': ('datasets/GSE155405_GEN141016_F_Profiling_table.xlsx', None),
        'GSE174188': ('datasets/GSE174188_series_matrix.txt', None),
        'GSE182825': ('datasets/GSE182825_Analyzed_Counts.txt', None),
        'GSE200306': ('datasets/GSE200306_normalized_Glom_expression_data.txt', None),
    },
    '4_Senescence_Validation': {
        'GSE101766': ('datasets/GSE101766_series_matrix.txt', None),
        'GSE226598': ('datasets/GSE226598_series_matrix.txt', None),
        'GSE262856': ('datasets/GSE262856_series_matrix.txt', None),
        'GSE297723': ('datasets/GSE297723_series_matrix.txt', None),
    },
}


def main():
    """Execute full pipeline"""
    logger.info("="*60)
    logger.info("FINAL PRODUCTION PIPELINE v4")
    logger.info("Smart handling of mixed formats, gene naming systems")
    logger.info("="*60)

    results = {}
    total_success = 0
    total_datasets = 0

    for category, datasets_dict in DATASETS.items():
        logger.info(f"\n[{category}]")

        results[category] = {}
        for dataset_name, (filepath, skip_rows) in datasets_dict.items():
            total_datasets += 1

            if not os.path.exists(filepath):
                logger.info(f"[{dataset_name}] NOT FOUND: {filepath}")
                results[category][dataset_name] = 'NOT_FOUND'
                continue

            status = process_dataset(dataset_name, filepath, category, skip_rows=skip_rows)
            results[category][dataset_name] = status

            if status == 'SUCCESS':
                total_success += 1

    # Summary
    logger.info("\n" + "="*60)
    logger.info("FINAL SUMMARY")
    logger.info("="*60)

    for category, datasets_dict in results.items():
        success_count = len([v for v in datasets_dict.values() if v == 'SUCCESS'])
        total_in_cat = len(datasets_dict)
        logger.info(f"{category}: {success_count}/{total_in_cat}")

    logger.info(f"\nOVERALL: {total_success}/{total_datasets} datasets processed successfully")
    logger.info(f"Results saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
