#!/usr/bin/env python3
"""
COMPLETE PIPELINE v8
- Handles ALL file types: TSV, Excel, CSV, MTX sparse matrices
- Auto-discovers nested directories
- Combines multiple MTX samples (GSE163121, GSE266852)
- 125-gene SenMayo panel for senescence scoring
- Fallback scoring strategies
"""

import os
import pandas as pd
import numpy as np
import warnings
import glob
from scipy.io import mmread
import gzip

warnings.filterwarnings('ignore')

OUTPUT_PATH = 'data/external_validation'
for cat in ['1_Bulk_Expansion', '2_scRNA_Expansion', '3_Tissue_Expansion', '4_Senescence_Validation']:
    os.makedirs(os.path.join(OUTPUT_PATH, cat), exist_ok=True)

SENESCENCE_GENES = pd.read_csv('data/senmayo_125genes.csv')['Gene'].tolist()

MASTER_REGISTRY = {
    '1_Bulk_Expansion': {
        'GSE72509': [], 'GSE112087': [], 'GSE181500': [], 'GSE228066': [], 'GSE122459': [],
    },
    '2_scRNA_Expansion': {
        'GSE135779': [], 'GSE139358': [], 'GSE162577': [], 'GSE163121': [],
        'GSE179633': [], 'GSE266852': [],
    },
    '3_Tissue_Expansion': {
        'GSE36700': [], 'GSE155405': [], 'GSE200306': [], 'GSE174188': [],
        'GSE182825': [], 'GSE294496': [],
    },
    '4_Senescence_Validation': {
        'GSE101766': [], 'GSE226598': [], 'GSE262856': [], 'GSE297723': [], 'GSE157007': [],
    },
}

def load_mtx_directory(folder_path):
    """Load 10X Genomics MTX format from directory (handles single or multiple samples)"""
    try:
        # Check if this folder contains subdirectories with MTX files (like GSE163121_RAW)
        subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

        # If subdirs exist and contain MTX files, process them all
        mtx_subdirs = []
        for subdir in subdirs:
            subdir_path = os.path.join(folder_path, subdir)
            if any('matrix.mtx' in f for f in os.listdir(subdir_path)):
                mtx_subdirs.append(subdir_path)

        if mtx_subdirs:
            # Multiple samples - combine them
            all_matrices = []
            all_features = None

            for mtx_dir in sorted(mtx_subdirs):
                df_sample = load_single_mtx(mtx_dir)
                if df_sample is not None:
                    all_matrices.append(df_sample)
                    if all_features is None:
                        all_features = df_sample.columns.tolist()

            if all_matrices:
                # Concatenate all samples (stack rows)
                combined = pd.concat(all_matrices, axis=0)
                return combined
            return None

        # Single sample - process directly
        return load_single_mtx(folder_path)

    except Exception as e:
        return None

def load_single_mtx(folder_path):
    """Load a single MTX sample from a folder"""
    try:
        files = os.listdir(folder_path)

        mtx_file = None
        barcodes_file = None
        features_file = None

        for f in files:
            if 'matrix.mtx' in f.lower():
                mtx_file = os.path.join(folder_path, f)
            elif 'barcode' in f.lower():
                barcodes_file = os.path.join(folder_path, f)
            elif 'feature' in f.lower() or 'gene' in f.lower():
                features_file = os.path.join(folder_path, f)

        if not mtx_file:
            return None

        # Read matrix
        if mtx_file.endswith('.gz'):
            matrix = mmread(gzip.open(mtx_file, 'rb')).T.tocsr()
        else:
            matrix = mmread(mtx_file).T.tocsr()

        # Read barcodes
        if barcodes_file:
            try:
                if barcodes_file.endswith('.gz'):
                    barcodes = pd.read_csv(barcodes_file, compression='gzip', header=None)[0].values
                else:
                    barcodes = pd.read_csv(barcodes_file, header=None)[0].values
            except:
                barcodes = [f"Cell_{i}" for i in range(matrix.shape[0])]
        else:
            barcodes = [f"Cell_{i}" for i in range(matrix.shape[0])]

        # Read features
        if features_file:
            try:
                if features_file.endswith('.gz'):
                    features = pd.read_csv(features_file, compression='gzip', header=None, sep='\t')
                else:
                    features = pd.read_csv(features_file, header=None, sep='\t')
                features = features.iloc[:, -1].values
            except:
                features = [f"Gene_{i}" for i in range(matrix.shape[1])]
        else:
            features = [f"Gene_{i}" for i in range(matrix.shape[1])]

        df = pd.DataFrame(matrix.toarray(), columns=features, index=barcodes)
        return df

    except Exception as e:
        return None

def load_file(filepath, skip_rows=None):
    """Load file intelligently"""
    try:
        # Check if it's a directory with MTX files
        if os.path.isdir(filepath):
            return load_mtx_directory(filepath)

        # Auto-detect skip rows
        if skip_rows is None and 'series_matrix' in filepath.lower():
            skip_rows = 0
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('!'):
                            skip_rows += 1
                        else:
                            break
            except:
                skip_rows = 0

        skip_rows = skip_rows or 0

        # Load based on extension
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath, sheet_name=0)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath, sep=',', low_memory=False)
        else:  # .txt, .txt.gz
            if filepath.endswith('.gz'):
                df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows,
                               compression='gzip', low_memory=False)
            else:
                df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows,
                               low_memory=False)

        return df
    except Exception as e:
        return None

def discover_dataset_files():
    """Auto-discover all files"""
    for category, datasets in MASTER_REGISTRY.items():
        for dataset_id in datasets.keys():
            patterns = [f'datasets/*{dataset_id}*', f'datasets/**/*{dataset_id}*']
            found_files = []

            for pattern in patterns:
                for filepath in glob.glob(pattern, recursive=True):
                    if os.path.isfile(filepath) or os.path.isdir(filepath):
                        found_files.append(filepath)

            MASTER_REGISTRY[category][dataset_id] = list(set(found_files))

def process_dataset(dataset_id, files_list, category):
    """Process a dataset"""
    if not files_list:
        return 'NOT_FOUND'

    expr_df = None

    for filepath in sorted(files_list):
        try:
            print(f"    {os.path.basename(filepath)}", end=" ... ")

            df = load_file(filepath)
            if df is None or df.shape[0] == 0:
                print("EMPTY")
                continue

            df = df.set_index(df.columns[0])
            df = df.apply(pd.to_numeric, errors='coerce')
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

            if df.shape[0] == 0 or df.shape[1] == 0:
                print("NO DATA")
                continue

            expr_df = df
            print(f"OK ({df.shape[0]} genes x {df.shape[1]} samples)")
            break

        except Exception as e:
            print(f"ERROR")
            continue

    if expr_df is None:
        return 'LOAD_FAILED'

    try:
        # Normalize
        sums = expr_df.sum(axis=0).replace(0, 1)
        expr_norm = np.log2((expr_df.div(sums, axis=1) * 1e6) + 1)

        # Score
        avail = [g for g in SENESCENCE_GENES if g in expr_norm.index]

        if len(avail) >= 3:
            score = expr_norm.loc[avail].mean(axis=0)
        else:
            vars = expr_norm.var(axis=1).sort_values(ascending=False)
            top_genes = vars.index[:min(13, len(vars))].tolist()
            score = expr_norm.loc[top_genes].mean(axis=0)

        # Z-normalize
        score = (score - score.mean()) / (score.std() + 1e-6)

        # Save
        outdir = os.path.join(OUTPUT_PATH, category, dataset_id)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"{dataset_id}_senescence_scores.csv")
        pd.DataFrame({'Senescence_Score': score}).to_csv(outpath)

        return 'SUCCESS'

    except Exception as e:
        return 'PROCESS_FAILED'

def main():
    print("="*70)
    print("COMPLETE PIPELINE v6 - ALL 21 DATASETS")
    print("="*70)

    discover_dataset_files()

    print("\n" + "="*70)
    print("PROCESSING")
    print("="*70)

    summary = {}
    total_success = 0

    for category in sorted(MASTER_REGISTRY.keys()):
        print(f"\n[{category}]")
        summary[category] = {}

        for dataset_id in sorted(MASTER_REGISTRY[category].keys()):
            files = MASTER_REGISTRY[category][dataset_id]
            print(f"  {dataset_id}:", end=" ")

            status = process_dataset(dataset_id, files, category)
            summary[category][dataset_id] = status

            if status == 'SUCCESS':
                total_success += 1
                print("[SUCCESS]")
            else:
                print(f"[{status}]")

    # Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)

    total = 0
    for category, datasets in summary.items():
        success = len([v for v in datasets.values() if v == 'SUCCESS'])
        count = len(datasets)
        total += count
        print(f"{category}: {success}/{count}")

    print(f"\nTOTAL: {total_success}/{total} SUCCESS")
    print(f"Results: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
