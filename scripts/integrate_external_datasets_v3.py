#!/usr/bin/env python3
"""
Production-Grade Multi-Omics Integration Pipeline v3
Handles all file formats: Series Matrix, Excel, MTX sparse, RAW folders

Key improvements:
- Metadata header detection and skipping
- Robust Excel parsing with multiple fallbacks
- MTX file reading with proper gzip handling
- Comprehensive error logging
- Data validation before processing
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import glob
import gzip
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_v3.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_PATH = os.path.abspath('datasets')
OUTPUT_PATH = os.path.abspath('data/external_validation')

CONFIG = {
    'base_path': BASE_PATH,
    'output_path': OUTPUT_PATH,
    'senescence_genes': ['CDKN2A', 'CDKN1A', 'CDKN2B', 'TP53', 'RB1', 'E2F1',
                         'IL6', 'TNF', 'CXCL8', 'MMP3', 'MMP9', 'SERPINE1', 'IGFBP7'],
    'car_t_targets': ['CSPG4', 'CD44', 'ICAM1', 'VCAM1', 'CD38', 'EGFR'],
}

# Create output directories
for category in ['1_Bulk_Expansion', '2_scRNA_Expansion', '3_Tissue_Expansion', '4_Senescence_Validation']:
    os.makedirs(os.path.join(OUTPUT_PATH, category), exist_ok=True)


# ============================================================================
# ROBUST DATA LOADING FUNCTIONS
# ============================================================================

def detect_metadata_header_lines(filepath):
    """Detect how many lines of metadata to skip in GEO files"""
    try:
        with gzip.open(filepath, 'rt') as f:
            lines_to_skip = 0
            for line in f:
                if line.startswith('!'):
                    lines_to_skip += 1
                else:
                    break
        return lines_to_skip
    except:
        # Try regular file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines_to_skip = 0
                for line in f:
                    if line.startswith('!'):
                        lines_to_skip += 1
                    else:
                        break
            return lines_to_skip
        except:
            return 0


def load_series_matrix_robust(filepath):
    """Load GEO Series Matrix with metadata detection"""
    logger.info(f"Loading Series Matrix: {os.path.basename(filepath)}")

    try:
        # Detect metadata lines
        skip_rows = detect_metadata_header_lines(filepath)
        logger.info(f"  Skipping {skip_rows} metadata lines")

        # Load with proper separator
        if filepath.endswith('.gz'):
            df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows,
                           compression='gzip', encoding='utf-8', low_memory=False)
        else:
            df = pd.read_csv(filepath, sep='\t', skiprows=skip_rows,
                           encoding='utf-8', low_memory=False)

        # Set first column as index (gene names)
        if df.shape[0] > 0 and df.shape[1] > 0:
            df = df.set_index(df.columns[0])
            df.index.name = 'Gene'
            logger.info(f"  Loaded: {df.shape[0]} genes × {df.shape[1]} samples")
            return df
        else:
            logger.error(f"  Empty dataframe loaded")
            return None

    except Exception as e:
        logger.error(f"  Failed to load {os.path.basename(filepath)}: {str(e)}")
        return None


def load_excel_smart(filepath):
    """Load Excel file with intelligent header detection"""
    logger.info(f"Loading Excel: {os.path.basename(filepath)}")

    try:
        # Try to lock file
        xls = pd.ExcelFile(filepath)
        logger.info(f"  Available sheets: {xls.sheet_names}")

        # Load first sheet
        sheet_name = xls.sheet_names[0]
        df = pd.read_excel(filepath, sheet_name=sheet_name)

        # Skip metadata rows (rows with text descriptions)
        skip_rows = 0
        for idx, row in df.iterrows():
            first_val = str(row.iloc[0]).lower()
            if any(keyword in first_val for keyword in ['file', 'attribute', 'sample', 'description']):
                skip_rows = idx + 1
            else:
                break

        if skip_rows > 0:
            logger.info(f"  Skipping {skip_rows} metadata rows")
            df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=skip_rows)

        # Try to set gene column as index
        if df.shape[0] > 0:
            # Find numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                if df.columns[0] not in numeric_cols:
                    df = df.set_index(df.columns[0])
                logger.info(f"  Loaded: {df.shape[0]} rows × {len(numeric_cols)} numeric columns")
                return df

        logger.warning(f"  No numeric data found in {os.path.basename(filepath)}")
        return None

    except Exception as e:
        logger.error(f"  Failed to load {os.path.basename(filepath)}: {str(e)}")
        return None


def load_mtx_sparse(folder_path):
    """Load 10X Genomics MTX format"""
    logger.info(f"Loading MTX sparse from: {os.path.basename(folder_path)}")

    try:
        from scipy.io import mmread

        # Find MTX, barcodes, features files
        mtx_file = None
        barcodes_file = None
        features_file = None

        for f in os.listdir(folder_path):
            if 'matrix.mtx' in f.lower():
                mtx_file = os.path.join(folder_path, f)
            elif 'barcode' in f.lower():
                barcodes_file = os.path.join(folder_path, f)
            elif 'feature' in f.lower() or 'gene' in f.lower():
                features_file = os.path.join(folder_path, f)

        if not mtx_file:
            logger.warning(f"  No MTX file found in {folder_path}")
            return None

        # Read matrix with proper gzip handling
        try:
            if mtx_file.endswith('.gz'):
                with gzip.open(mtx_file, 'rb') as f:
                    matrix = mmread(f).T.tocsr()
            else:
                matrix = mmread(mtx_file).T.tocsr()
        except:
            logger.warning(f"  MTX read failed, trying alternative method")
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
                features = features.iloc[:, -1].values  # Take last column (gene name)
            except:
                features = [f"Gene_{i}" for i in range(matrix.shape[1])]
        else:
            features = [f"Gene_{i}" for i in range(matrix.shape[1])]

        logger.info(f"  Loaded MTX: {matrix.shape[0]} cells × {matrix.shape[1]} genes")

        # Convert to dense DataFrame for compatibility
        df = pd.DataFrame(matrix.toarray(), columns=features, index=barcodes)
        return df

    except Exception as e:
        logger.error(f"  Failed to load MTX: {str(e)}")
        return None


def load_txt_file(filepath):
    """Load generic TXT file (expression data)"""
    logger.info(f"Loading TXT: {os.path.basename(filepath)}")

    try:
        if filepath.endswith('.gz'):
            df = pd.read_csv(filepath, sep='\t', compression='gzip',
                           encoding='utf-8', low_memory=False)
        else:
            df = pd.read_csv(filepath, sep='\t', encoding='utf-8',
                           errors='ignore', low_memory=False)

        # Set first column as index
        if df.shape[0] > 0:
            df = df.set_index(df.columns[0])
            logger.info(f"  Loaded: {df.shape[0]} genes × {df.shape[1]} samples")
            return df

    except Exception as e:
        logger.error(f"  Failed to load {os.path.basename(filepath)}: {str(e)}")
        return None


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def normalize_expression(df):
    """Normalize expression data"""
    try:
        # Convert to numeric, replacing any non-numeric with NaN
        df_numeric = df.apply(pd.to_numeric, errors='coerce')

        # Remove rows with all NaN
        df_numeric = df_numeric.dropna(how='all')

        # Remove columns with all NaN
        df_numeric = df_numeric.dropna(axis=1, how='all')

        if df_numeric.shape[0] == 0 or df_numeric.shape[1] == 0:
            logger.warning(f"  No numeric data after conversion")
            return None

        # Log normalize: log2(CPM + 1)
        col_sums = df_numeric.sum(axis=0)
        col_sums = col_sums.replace(0, 1)  # Avoid division by zero

        df_cpm = df_numeric.div(col_sums, axis=1) * 1e6
        df_log = np.log2(df_cpm + 1)

        logger.info(f"  Normalized: {df_log.shape[0]} genes × {df_log.shape[1]} samples")
        return df_log

    except Exception as e:
        logger.error(f"  Normalization failed: {str(e)}")
        return None


def compute_senescence_score(expr_df, gene_list):
    """Compute senescence score"""
    try:
        # Find available genes
        available = [g for g in gene_list if g in expr_df.index]

        if len(available) < 3:  # Need at least 3 genes
            logger.warning(f"  Only {len(available)}/{len(gene_list)} senescence genes found")
            return None

        logger.info(f"  Computing senescence score ({len(available)} genes)")

        # Mean expression of available genes
        score = expr_df.loc[available, :].mean(axis=0)

        # Z-score normalize
        score_z = (score - score.mean()) / (score.std() + 1e-6)

        return score_z

    except Exception as e:
        logger.error(f"  Senescence scoring failed: {str(e)}")
        return None


# ============================================================================
# DATASET DISCOVERY & PROCESSING
# ============================================================================

def discover_and_process_dataset(dataset_name, filepath):
    """Intelligently load and process any dataset"""
    logger.info(f"\nProcessing: {dataset_name}")

    # Load based on file type
    data = None

    if os.path.isdir(filepath):
        # It's a folder - try MTX first, then TXT
        logger.info(f"  Folder detected, checking for data files...")

        files = os.listdir(filepath)
        mtx_files = [f for f in files if 'matrix.mtx' in f.lower()]
        txt_files = [f for f in files if f.endswith('.txt') or f.endswith('.txt.gz')]

        if mtx_files:
            data = load_mtx_sparse(filepath)
        elif txt_files:
            txt_path = os.path.join(filepath, txt_files[0])
            data = load_txt_file(txt_path)

    elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        data = load_excel_smart(filepath)

    elif filepath.endswith(('.txt', '.txt.gz', 'matrix.txt')):
        data = load_txt_file(filepath)

    elif 'series_matrix' in filepath:
        data = load_series_matrix_robust(filepath)

    else:
        # Try series matrix first, then generic TXT
        if os.path.exists(filepath):
            data = load_series_matrix_robust(filepath)
            if data is None:
                data = load_txt_file(filepath)

    if data is None:
        logger.warning(f"  FAILED TO LOAD: {dataset_name}")
        return None, 'LOAD_FAILED'

    # Normalize
    data_norm = normalize_expression(data)
    if data_norm is None:
        return None, 'NORMALIZE_FAILED'

    # Score senescence
    scores = compute_senescence_score(data_norm, CONFIG['senescence_genes'])
    if scores is None:
        return scores, 'SCORE_FAILED'

    return scores, 'SUCCESS'


def process_all_datasets():
    """Main processing loop"""
    logger.info("="*60)
    logger.info("ROBUST MULTI-OMICS INTEGRATION PIPELINE v3")
    logger.info("="*60)

    results = {}

    # Dataset categorization
    dataset_map = {
        # Bulk
        '1_Bulk_Expansion': {
            'GSE72509': 'datasets/GSE72509_SLE_RPKMs.txt',
            'GSE112087': 'datasets/GSE112087_counts-matrix-EnsembIDs-GRCh37.p10.txt',
            'GSE122459': 'datasets/GSE122459_normalized_genes_all_samples.xlsx',
            'GSE228066': 'datasets/GSE228066_gene.xlsx',
            'GSE181500': 'datasets/GSE181500_RAW',
        },
        # scRNA
        '2_scRNA_Expansion': {
            'GSE139358': 'datasets/GSE139358_RNA-Seq_gene_rpkm_33_samples.xlsx',
            'GSE162577': 'datasets/GSE162577_series_matrix.txt',
            'GSE163121': 'datasets/GSE163121_series_matrix.txt',
            'GSE179633': 'datasets/GSE179633_series_matrix.txt',
            'GSE142016': 'datasets/GSE142016_RAW',
        },
        # Tissue
        '3_Tissue_Expansion': {
            'GSE36700': 'datasets/GSE36700_series_matrix.txt',
            'GSE155405': 'datasets/GSE155405_GEN141016_F_Profiling_table.xlsx',
            'GSE174188': 'datasets/GSE174188_series_matrix.txt',
            'GSE182825': 'datasets/GSE182825_RAW',
            'GSE200306': 'datasets/GSE200306_Nanostring_RAW_1-21.xlsx',
        },
        # Senescence validation
        '4_Senescence_Validation': {
            'GSE101766': 'datasets/GSE101766_series_matrix.txt',
            'GSE226598': 'datasets/GSE226598_series_matrix.txt',
            'GSE262856': 'datasets/GSE262856_series_matrix.txt',
            'GSE297723': 'datasets/GSE297723_series_matrix.txt',
        },
    }

    # Process each dataset
    for category, datasets in dataset_map.items():
        logger.info(f"\n{'='*60}")
        logger.info(f"{category.upper()}")
        logger.info(f"{'='*60}")

        output_dir = os.path.join(OUTPUT_PATH, category)

        for dataset_name, filepath in datasets.items():
            # Try multiple path variations
            actual_path = None
            for variant in [filepath, filepath + '.gz', filepath.replace('\\', '/')]:
                if os.path.exists(variant):
                    actual_path = variant
                    break

            if actual_path is None:
                logger.warning(f"{dataset_name}: FILE NOT FOUND - {filepath}")
                results[f"Category_{category[0]}"].update({dataset_name: 'NOT_FOUND'})
                continue

            scores, status = discover_and_process_dataset(dataset_name, actual_path)

            if status == 'SUCCESS':
                # Save results
                dataset_dir = os.path.join(output_dir, dataset_name)
                os.makedirs(dataset_dir, exist_ok=True)

                scores_df = pd.DataFrame({'Senescence_Score': scores})
                scores_path = os.path.join(dataset_dir, f"{dataset_name}_senescence_scores.csv")
                scores_df.to_csv(scores_path)

                logger.info(f"✓ SUCCESS: Saved to {scores_path}")
            else:
                logger.warning(f"✗ {status}: {dataset_name}")

            category_key = f"Category_{category.split("_")[0]}"
            if category_key not in results:
                results[category_key] = {}
            results[category_key].update({dataset_name: status})

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("EXECUTION SUMMARY")
    logger.info(f"{'='*60}")

    total_success = 0
    total_datasets = 0

    for category, datasets in results.items():
        success = len([v for v in datasets.values() if v == 'SUCCESS'])
        total = len(datasets)
        total_success += success
        total_datasets += total

        logger.info(f"{category}: {success}/{total} successful")

    logger.info(f"\nOVERALL: {total_success}/{total_datasets} datasets processed")
    logger.info(f"Results saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    process_all_datasets()
