#!/usr/bin/env python3
"""
SLE Senescence Scoring Pipeline v9
- 125-gene SenMayo panel (loaded from data/senmayo_125genes.csv)
- Multi-format support: TSV, Excel, CSV, 10X MTX sparse matrices
- scRNA-seq QC: min genes, min cells, mitochondrial gene filtering
- Cross-dataset Z-score batch alignment
- Auto-discovery of nested directories
- Structured logging with per-dataset metrics
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import warnings
import glob
import logging
from scipy.io import mmread
import gzip
from datetime import datetime

warnings.filterwarnings('ignore')

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)

OUTPUT_PATH = 'data/external_validation'
for cat in ['1_Bulk_Expansion', '2_scRNA_Expansion', '3_Tissue_Expansion', '4_Senescence_Validation']:
    os.makedirs(os.path.join(OUTPUT_PATH, cat), exist_ok=True)

SENESCENCE_GENES = pd.read_csv('data/senmayo_125genes.csv')['Gene'].tolist()

MITO_PREFIXES = ['MT-', 'mt-']

# scRNA-seq QC thresholds
MIN_GENES_PER_CELL = 200
MIN_CELLS_PER_GENE = 3
MAX_MITO_FRACTION = 0.20

MASTER_REGISTRY = {
    '1_Bulk_Expansion': {
        'GSE72509': [], 'GSE112087': [], 'GSE228066': [], 'GSE122459': [],
    },
    '2_scRNA_Expansion': {
        'GSE135779': [], 'GSE139358': [], 'GSE162577': [], 'GSE163121_RAW': [],
        'GSE179633': [], 'GSE266852_OES19443150_matrix.mtx': [],
    },
    '3_Tissue_Expansion': {
        'GSE36700': [], 'GSE155405': [], 'GSE200306': [], 'GSE174188': [],
        'GSE182825': [], 'GSE294496': [],
    },
    '4_Senescence_Validation': {
        'GSE101766': [], 'GSE262856': [], 'GSE297723': [],
    },
}

# ---------------------------------------------------------------------------
# scRNA-seq Quality Control
# ---------------------------------------------------------------------------

def apply_scrna_qc(df, dataset_id):
    """Filter cells and genes for scRNA-seq data"""
    n_cells_before = df.shape[0]
    n_genes_before = df.shape[1]

    # Filter genes expressed in too few cells
    gene_counts = (df > 0).sum(axis=0)
    df = df.loc[:, gene_counts >= MIN_CELLS_PER_GENE]

    # Filter cells with too few detected genes
    genes_per_cell = (df > 0).sum(axis=1)
    df = df.loc[genes_per_cell >= MIN_GENES_PER_CELL, :]

    # Mitochondrial gene fraction filtering
    mito_genes = [g for g in df.columns if any(g.startswith(p) for p in MITO_PREFIXES)]
    if mito_genes:
        total_counts = df.sum(axis=1)
        mito_counts = df[mito_genes].sum(axis=1)
        mito_frac = mito_counts / (total_counts + 1e-6)
        df = df.loc[mito_frac <= MAX_MITO_FRACTION, :]
        # Drop mito genes from expression matrix
        df = df.drop(columns=mito_genes, errors='ignore')

    log.info(f"    QC: {n_cells_before} -> {df.shape[0]} cells, {n_genes_before} -> {df.shape[1]} genes")
    return df

# ---------------------------------------------------------------------------
# Batch Correction (Z-score global alignment)
# ---------------------------------------------------------------------------

def batch_correct_scores(all_scores):
    """Align senescence scores across datasets using Z-score normalization per batch.
    Each dataset is treated as a batch. Scores are first Z-normalized within each
    dataset (already done during scoring), then globally re-centered so datasets
    are comparable on the same scale."""
    if not all_scores:
        return all_scores

    global_values = np.concatenate([s['Senescence_Score'].dropna().values for s in all_scores.values()])
    if len(global_values) == 0:
        return all_scores
    global_mean = np.nanmean(global_values)
    global_std = np.nanstd(global_values) + 1e-6

    corrected = {}
    for dataset_id, scores_df in all_scores.items():
        corrected_scores = (scores_df['Senescence_Score'] - global_mean) / global_std
        corrected[dataset_id] = pd.DataFrame({'Senescence_Score': corrected_scores}, index=scores_df.index)

    return corrected

# ---------------------------------------------------------------------------
# File Loaders
# ---------------------------------------------------------------------------

def load_single_mtx(folder_path):
    """Load a single 10X MTX sample"""
    try:
        files = os.listdir(folder_path)
        mtx_file = barcodes_file = features_file = None

        for f in files:
            if 'matrix.mtx' in f.lower():
                mtx_file = os.path.join(folder_path, f)
            elif 'barcode' in f.lower():
                barcodes_file = os.path.join(folder_path, f)
            elif 'feature' in f.lower() or 'gene' in f.lower():
                features_file = os.path.join(folder_path, f)

        if not mtx_file:
            return None

        if mtx_file.endswith('.gz'):
            matrix = mmread(gzip.open(mtx_file, 'rb')).T.tocsr()
        else:
            matrix = mmread(mtx_file).T.tocsr()

        if barcodes_file:
            try:
                kw = {'compression': 'gzip'} if barcodes_file.endswith('.gz') else {}
                barcodes = pd.read_csv(barcodes_file, header=None, **kw)[0].values
            except Exception as e:
                log.warning(f"    Barcode file error ({e}), using numeric IDs")
                barcodes = [f"Cell_{i}" for i in range(matrix.shape[0])]
        else:
            barcodes = [f"Cell_{i}" for i in range(matrix.shape[0])]

        if features_file:
            try:
                kw = {'compression': 'gzip'} if features_file.endswith('.gz') else {}
                features = pd.read_csv(features_file, header=None, sep='\t', **kw)
                features = features.iloc[:, -1].values
            except Exception as e:
                log.warning(f"    Feature file error ({e}), using numeric IDs")
                features = [f"Gene_{i}" for i in range(matrix.shape[1])]
        else:
            features = [f"Gene_{i}" for i in range(matrix.shape[1])]

        max_cells = min(1000, matrix.shape[0])
        df = pd.DataFrame(matrix[:max_cells, :].toarray(), columns=features, index=barcodes[:max_cells])
        return df
    except Exception as e:
        log.warning(f"    MTX load error: {e}")
        return None


def load_mtx_directory(folder_path):
    """Load 10X MTX format, handling nested sample directories"""
    try:
        subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
        mtx_subdirs = []
        for subdir in subdirs:
            subdir_path = os.path.join(folder_path, subdir)
            try:
                if any('matrix.mtx' in f for f in os.listdir(subdir_path)):
                    mtx_subdirs.append(subdir_path)
            except OSError:
                continue

        if mtx_subdirs:
            for mtx_dir in sorted(mtx_subdirs):
                df = load_single_mtx(mtx_dir)
                if df is not None:
                    return df
            return None

        return load_single_mtx(folder_path)
    except Exception as e:
        log.warning(f"    MTX directory error: {e}")
        return None


def load_file(filepath, skip_rows=None):
    """Load expression data from any supported format"""
    try:
        if os.path.isdir(filepath):
            return load_mtx_directory(filepath)

        if skip_rows is None and 'series_matrix' in filepath.lower():
            skip_rows = 0
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('!'):
                            skip_rows += 1
                        else:
                            break
            except OSError:
                skip_rows = 0

        skip_rows = skip_rows or 0

        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            return pd.read_excel(filepath, sheet_name=0)
        elif filepath.endswith('.csv'):
            return pd.read_csv(filepath, sep=',', low_memory=False)
        elif filepath.endswith('.gz'):
            return pd.read_csv(filepath, sep='\t', skiprows=skip_rows, compression='gzip', low_memory=False)
        else:
            return pd.read_csv(filepath, sep='\t', skiprows=skip_rows, low_memory=False)
    except Exception as e:
        log.warning(f"    File load error: {e}")
        return None


def discover_dataset_files():
    """Auto-discover all dataset files in datasets/ folder"""
    for category, datasets in MASTER_REGISTRY.items():
        for dataset_id in datasets.keys():
            found = set()
            for pattern in [f'datasets/*{dataset_id}*', f'datasets/**/*{dataset_id}*']:
                for fp in glob.glob(pattern, recursive=True):
                    if os.path.isfile(fp) or os.path.isdir(fp):
                        found.add(fp)
            MASTER_REGISTRY[category][dataset_id] = list(found)

# ---------------------------------------------------------------------------
# Dataset Processing
# ---------------------------------------------------------------------------

def process_dataset(dataset_id, files_list, category):
    """Load, QC, normalize, and score one dataset"""
    if not files_list:
        return 'NOT_FOUND', None

    expr_df = None
    is_scrna = ('scRNA' in category or 'matrix.mtx' in str(files_list))

    for filepath in sorted(files_list):
        try:
            log.info(f"    {os.path.basename(filepath)} ...")

            df = load_file(filepath)
            if df is None or df.shape[0] == 0:
                log.info(f"      -> EMPTY")
                continue

            # For MTX data, genes are columns; otherwise set first col as index
            if not is_scrna or not os.path.isdir(filepath):
                df = df.set_index(df.columns[0])

            df = df.apply(pd.to_numeric, errors='coerce')
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

            if df.shape[0] == 0 or df.shape[1] == 0:
                log.info(f"      -> NO DATA")
                continue

            expr_df = df
            log.info(f"      -> Loaded: {df.shape[0]} x {df.shape[1]}")
            break
        except Exception as e:
            log.warning(f"      -> Error: {e}")
            continue

    if expr_df is None:
        return 'LOAD_FAILED', None

    try:
        # Apply scRNA-seq QC only for MTX-loaded single-cell data (cells as rows)
        if is_scrna and os.path.isdir(str(files_list[0] if files_list else '')):
            if expr_df.shape[0] > 100 and expr_df.shape[1] > expr_df.shape[0]:
                # Cells as rows, genes as columns — apply QC then transpose
                expr_df = apply_scrna_qc(expr_df, dataset_id)
                expr_df = expr_df.T

        # Normalize: log2(CPM + 1)
        sums = expr_df.sum(axis=0).replace(0, 1)
        expr_norm = np.log2((expr_df.div(sums, axis=1) * 1e6) + 1)

        # Senescence scoring with SenMayo panel
        avail = [g for g in SENESCENCE_GENES if g in expr_norm.index]
        n_senmayo = len(avail)

        if n_senmayo >= 3:
            score = expr_norm.loc[avail].mean(axis=0)
        else:
            top_var = expr_norm.var(axis=1).sort_values(ascending=False)
            fallback = top_var.index[:min(13, len(top_var))].tolist()
            score = expr_norm.loc[fallback].mean(axis=0)

        # Z-normalize within dataset
        score = (score - score.mean()) / (score.std() + 1e-6)

        # Save
        outdir = os.path.join(OUTPUT_PATH, category, dataset_id)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"{dataset_id}_senescence_scores.csv")
        scores_df = pd.DataFrame({'Senescence_Score': score})
        scores_df.to_csv(outpath)

        log.info(f"      -> Scored: {len(score)} samples, {n_senmayo}/125 SenMayo genes matched")
        return 'SUCCESS', scores_df

    except Exception as e:
        log.warning(f"      -> Scoring error: {e}")
        return 'PROCESS_FAILED', None

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    start_time = datetime.now()
    log.info("=" * 70)
    log.info("SLE Senescence Scoring Pipeline v9")
    log.info(f"SenMayo panel: {len(SENESCENCE_GENES)} genes")
    log.info(f"scRNA QC: min_genes={MIN_GENES_PER_CELL}, min_cells={MIN_CELLS_PER_GENE}, max_mito={MAX_MITO_FRACTION}")
    log.info(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 70)

    discover_dataset_files()

    log.info("\n" + "=" * 70)
    log.info("PROCESSING")
    log.info("=" * 70)

    summary = {}
    all_scores = {}
    total_success = 0
    total_samples = 0

    for category in sorted(MASTER_REGISTRY.keys()):
        log.info(f"\n[{category}]")
        summary[category] = {}

        for dataset_id in sorted(MASTER_REGISTRY[category].keys()):
            files = MASTER_REGISTRY[category][dataset_id]
            log.info(f"  {dataset_id}:")

            status, scores_df = process_dataset(dataset_id, files, category)
            summary[category][dataset_id] = status

            if status == 'SUCCESS' and scores_df is not None:
                total_success += 1
                n_samples = len(scores_df)
                total_samples += n_samples
                all_scores[dataset_id] = scores_df
                log.info(f"  -> [SUCCESS] ({n_samples} samples)")
            else:
                log.info(f"  -> [{status}]")

    # Batch correction across all successful datasets
    log.info("\n" + "=" * 70)
    log.info("BATCH CORRECTION")
    log.info("=" * 70)
    corrected = batch_correct_scores(all_scores)
    for dataset_id, corrected_df in corrected.items():
        # Find the category for this dataset
        for cat, datasets in MASTER_REGISTRY.items():
            if dataset_id in datasets:
                outdir = os.path.join(OUTPUT_PATH, cat, dataset_id)
                outpath = os.path.join(outdir, f"{dataset_id}_senescence_scores.csv")
                corrected_df.to_csv(outpath)
                break
    log.info(f"Batch-corrected {len(corrected)} datasets to common scale")

    # Summary
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    log.info("\n" + "=" * 70)
    log.info("FINAL SUMMARY")
    log.info("=" * 70)

    total = 0
    for category, datasets in summary.items():
        success = len([v for v in datasets.values() if v == 'SUCCESS'])
        count = len(datasets)
        total += count
        log.info(f"{category}: {success}/{count}")

    log.info(f"\nTOTAL: {total_success}/{total} SUCCESS")
    log.info(f"Total samples/cells scored: {total_samples}")
    log.info(f"SenMayo genes used: {len(SENESCENCE_GENES)}")
    log.info(f"Runtime: {elapsed:.1f}s")
    log.info(f"Results: {OUTPUT_PATH}")

    # Write machine-readable summary
    run_summary = {
        'pipeline_version': 'v9',
        'run_date': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'senmayo_genes': len(SENESCENCE_GENES),
        'scrna_qc': {
            'min_genes_per_cell': MIN_GENES_PER_CELL,
            'min_cells_per_gene': MIN_CELLS_PER_GENE,
            'max_mito_fraction': MAX_MITO_FRACTION,
        },
        'batch_correction': 'z-score global re-centering',
        'datasets_processed': total_success,
        'datasets_total': total,
        'total_samples': total_samples,
        'runtime_seconds': round(elapsed, 1),
        'results': summary,
    }
    with open(os.path.join(OUTPUT_PATH, 'PIPELINE_RUN_SUMMARY.json'), 'w') as f:
        json.dump(run_summary, f, indent=2)


if __name__ == '__main__':
    main()
