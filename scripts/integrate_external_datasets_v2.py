#!/usr/bin/env python3
"""
Flexible Data Integration Pipeline for SLE Senescence Study
Version 2 - Handles mixed file structures as downloaded

Auto-detects and processes:
- Series matrix TSV files (directly in datasets/)
- Excel files (.xlsx)
- Raw data folders (RAW/) with MTX or other formats
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BASE_PATH = os.path.abspath('datasets')
OUTPUT_PATH = os.path.abspath('data/external_validation')

CONFIG = {
    'base_path': BASE_PATH,
    'output_path': OUTPUT_PATH,
    'senescence_genes': {
        'canonical': ['CDKN2A', 'CDKN1A', 'CDKN2B', 'TP53', 'RB1', 'E2F1'],
        'sasp': ['IL6', 'TNF', 'CXCL8', 'MMP3', 'MMP9', 'SERPINE1', 'IGFBP7'],
    },
    'car_t_targets': ['CSPG4', 'CD44', 'ICAM1', 'VCAM1', 'CD38', 'EGFR'],
}

# Create output directories
for category in ['1_Bulk_Expansion', '2_scRNA_Expansion', '3_Tissue_Expansion', '4_Senescence_Validation']:
    os.makedirs(os.path.join(OUTPUT_PATH, category), exist_ok=True)


# ============================================================================
# AUTO-DETECTION FUNCTIONS
# ============================================================================

def find_available_datasets():
    """Auto-detect all available dataset files in datasets/ folder"""
    logger.info("AUTO-DETECTING AVAILABLE DATASETS...")

    datasets = {
        'series_matrix': {},
        'excel': {},
        'raw_folders': {},
    }

    # 1. Find series_matrix.txt files directly in datasets/
    for file in glob.glob(os.path.join(BASE_PATH, '*series_matrix.txt')):
        basename = os.path.basename(file)
        gse_id = basename.replace('_series_matrix.txt', '')
        datasets['series_matrix'][gse_id] = file
        logger.info(f"  Found: {gse_id} (series_matrix.txt)")

    # 2. Find Excel files
    for file in glob.glob(os.path.join(BASE_PATH, '*.xlsx')):
        basename = os.path.basename(file)
        datasets['excel'][basename] = file
        logger.info(f"  Found: {basename} (Excel)")

    # 3. Find RAW folders
    for folder in glob.glob(os.path.join(BASE_PATH, '*RAW')):
        basename = os.path.basename(folder)
        gse_id = basename.replace('_RAW', '')
        datasets['raw_folders'][gse_id] = folder
        logger.info(f"  Found: {gse_id} (RAW folder with {len(os.listdir(folder))} files)")

    return datasets


# ============================================================================
# LOADING FUNCTIONS FOR DIFFERENT FORMATS
# ============================================================================

def load_series_matrix(filepath):
    """Load GEO Series Matrix TSV file"""
    logger.info(f"Loading: {os.path.basename(filepath)}")
    try:
        df = pd.read_csv(filepath, sep='\t', encoding='utf-8', low_memory=False)
        logger.info(f"  Loaded: {df.shape[0]} genes × {df.shape[1]} samples")
        return df
    except Exception as e:
        logger.error(f"Failed to load {filepath}: {e}")
        return None


def load_excel_file(filepath):
    """Load Excel file (xlsx)"""
    logger.info(f"Loading: {os.path.basename(filepath)}")
    try:
        # Try to read first sheet
        df = pd.read_excel(filepath, sheet_name=0)
        logger.info(f"  Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        return df
    except Exception as e:
        logger.error(f"Failed to load {filepath}: {e}")
        return None


def load_raw_folder(folder_path, gse_id):
    """Load data from RAW folder (detect format: MTX, CEL, TXT, etc.)"""
    logger.info(f"Loading RAW folder: {gse_id}")

    files = os.listdir(folder_path)

    # Check for MTX format (scRNA-seq)
    mtx_files = [f for f in files if f.endswith('.mtx.gz') or f.endswith('.mtx')]
    if mtx_files:
        logger.info(f"  Detected: MTX sparse matrix format ({len(mtx_files)} file(s))")
        return load_mtx_from_raw(folder_path)

    # Check for CEL files (Affymetrix microarray)
    cel_files = [f for f in files if f.endswith('.CEL.gz') or f.endswith('.CEL')]
    if cel_files:
        logger.info(f"  Detected: Affymetrix CEL format ({len(cel_files)} files)")
        return None  # CEL files need special processing

    # Check for TXT files (expression data)
    txt_files = [f for f in files if f.endswith('.txt') or f.endswith('.txt.gz')]
    if txt_files:
        logger.info(f"  Detected: Text files ({len(txt_files)} file(s))")
        # Try loading first TXT file
        txt_file = txt_files[0]
        filepath = os.path.join(folder_path, txt_file)
        try:
            if txt_file.endswith('.gz'):
                df = pd.read_csv(filepath, sep='\t', compression='gzip', low_memory=False)
            else:
                df = pd.read_csv(filepath, sep='\t', low_memory=False)
            logger.info(f"  Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
            return df
        except Exception as e:
            logger.error(f"Failed to load {txt_file}: {e}")
            return None

    logger.warning(f"  RAW folder format not recognized")
    return None


def load_mtx_from_raw(folder_path):
    """Load 10X Genomics MTX format from RAW folder"""
    try:
        from scipy.io import mmread

        # Find MTX file
        mtx_files = [f for f in os.listdir(folder_path) if 'matrix.mtx' in f.lower()]
        if not mtx_files:
            return None

        mtx_file = os.path.join(folder_path, mtx_files[0])

        # Read matrix
        if mtx_file.endswith('.gz'):
            import gzip
            matrix = mmread(gzip.open(mtx_file, 'rb')).T.tocsr()
        else:
            matrix = mmread(mtx_file).T.tocsr()

        logger.info(f"  MTX loaded: {matrix.shape[0]} cells × {matrix.shape[1]} genes")
        return matrix
    except Exception as e:
        logger.error(f"Failed to load MTX: {e}")
        return None


# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def normalize_expression(df):
    """Normalize expression data to log2(CPM+1)"""
    try:
        # Assume first column is gene names
        if df.columns[0] in ['ID_REF', 'gene', 'Gene', 'GENE_ID']:
            genes = df.iloc[:, 0]
            expr = df.iloc[:, 1:].astype(float)
        else:
            genes = df.index
            expr = df.astype(float)

        # CPM normalization
        expr_cpm = expr.div(expr.sum(axis=0), axis=1) * 1e6
        expr_log = np.log2(expr_cpm + 1)
        expr_log.index = genes

        return expr_log
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        return None


def compute_senescence_score(expr_matrix, gene_list):
    """Compute senescence score for samples"""
    try:
        # Find available genes
        if isinstance(expr_matrix, pd.DataFrame):
            available_genes = [g for g in gene_list if g in expr_matrix.index]
            expr_subset = expr_matrix.loc[available_genes, :]
        else:
            # Sparse matrix or array
            available_genes = [g for g in gene_list if g in expr_matrix.var_names]
            expr_subset = expr_matrix[:, available_genes].X

        if len(available_genes) == 0:
            logger.warning(f"No senescence genes found")
            return None

        logger.info(f"Computing senescence score ({len(available_genes)}/{len(gene_list)} genes found)")

        # Calculate score
        if isinstance(expr_subset, pd.DataFrame):
            score = expr_subset.mean(axis=0)
        else:
            score = np.asarray(expr_subset.mean(axis=0)).flatten()

        # Z-score normalize
        score_zscore = (score - np.mean(score)) / (np.std(score) + 1e-6)

        return score_zscore
    except Exception as e:
        logger.error(f"Senescence scoring failed: {e}")
        return None


def extract_targets(expr_matrix, targets):
    """Extract target gene expression"""
    try:
        if isinstance(expr_matrix, pd.DataFrame):
            available = [t for t in targets if t in expr_matrix.index]
            return expr_matrix.loc[available, :]
        else:
            available = [t for t in targets if t in expr_matrix.var_names]
            return expr_matrix[:, available]
    except Exception as e:
        logger.error(f"Target extraction failed: {e}")
        return None


# ============================================================================
# CATEGORIZATION & PROCESSING
# ============================================================================

def categorize_datasets(datasets_dict):
    """Categorize datasets into CATEGORY 1-4 based on GSE ID patterns"""
    categories = {
        'category_1_bulk': {},
        'category_2_scrna': {},
        'category_3_tissue': {},
        'category_4_senescence': {},
    }

    # Dataset category mapping
    bulk_gse = ['GSE72509', 'GSE112087', 'GSE181500', 'GSE228066', 'GSE122459']
    scrna_gse = ['GSE135779', 'GSE139358', 'GSE162577', 'GSE163121', 'GSE179633', 'GSE266852']
    tissue_gse = ['GSE36700', 'GSE155405', 'GSE200306', 'GSE174188', 'GSE182825', 'GSE294496']
    senescence_gse = ['GSE101766', 'GSE226598', 'GSE262856', 'GSE297723', 'GSE157007']

    # Categorize series_matrix files
    for gse_id, filepath in datasets_dict['series_matrix'].items():
        if gse_id in bulk_gse:
            categories['category_1_bulk'][gse_id] = filepath
        elif gse_id in scrna_gse:
            categories['category_2_scrna'][gse_id] = filepath
        elif gse_id in tissue_gse:
            categories['category_3_tissue'][gse_id] = filepath
        elif gse_id in senescence_gse:
            categories['category_4_senescence'][gse_id] = filepath

    # Categorize Excel files by GSE ID
    for filename, filepath in datasets_dict['excel'].items():
        for gse in bulk_gse:
            if gse in filename:
                categories['category_1_bulk'][f"{gse}_excel"] = filepath
                break
        for gse in tissue_gse:
            if gse in filename:
                categories['category_3_tissue'][f"{gse}_excel"] = filepath
                break

    # Categorize RAW folders
    for gse_id, folder in datasets_dict['raw_folders'].items():
        if gse_id in scrna_gse:
            categories['category_2_scrna'][gse_id] = folder
        elif gse_id in tissue_gse:
            categories['category_3_tissue'][gse_id] = folder

    return categories


# ============================================================================
# BATCH PROCESSING
# ============================================================================

def process_category_1_bulk(datasets_dict):
    """Process Category 1: SLE Bulk RNA-seq"""
    logger.info("="*60)
    logger.info("CATEGORY 1: SLE BULK RNA-seq")
    logger.info("="*60)

    output_dir = os.path.join(CONFIG['output_path'], '1_Bulk_Expansion')
    results = {}

    for name, filepath in datasets_dict.items():
        # Load based on file type
        if isinstance(filepath, str):
            if filepath.endswith('.xlsx'):
                data = load_excel_file(filepath)
            else:
                data = load_series_matrix(filepath)

        if data is not None:
            # Normalize
            data_norm = normalize_expression(data)
            if data_norm is not None:
                # Compute senescence
                all_genes = CONFIG['senescence_genes']['canonical'] + CONFIG['senescence_genes']['sasp']
                scores = compute_senescence_score(data_norm, all_genes)

                if scores is not None:
                    # Save outputs
                    os.makedirs(os.path.join(output_dir, name), exist_ok=True)

                    # Save senescence scores
                    scores_df = pd.DataFrame({'Senescence_Score': scores})
                    scores_path = os.path.join(output_dir, name, f"{name}_senescence_scores.csv")
                    scores_df.to_csv(scores_path)
                    logger.info(f"Saved senescence scores: {scores_path}")

                    results[name] = 'SUCCESS'
                else:
                    results[name] = 'SCORE_FAILED'
            else:
                results[name] = 'NORMALIZE_FAILED'
        else:
            results[name] = 'LOAD_FAILED'

    return results


def process_category_2_scrna(datasets_dict):
    """Process Category 2: scRNA-seq"""
    logger.info("="*60)
    logger.info("CATEGORY 2: scRNA-seq")
    logger.info("="*60)

    output_dir = os.path.join(CONFIG['output_path'], '2_scRNA_Expansion')
    results = {}

    for name, filepath in datasets_dict.items():
        # Load based on file type
        if os.path.isdir(filepath):
            data = load_raw_folder(filepath, name)
        elif filepath.endswith('.xlsx'):
            data = load_excel_file(filepath)
        else:
            data = load_series_matrix(filepath)

        if data is not None:
            # For scRNA, would need more sophisticated processing
            # For now, just compute scores if it's expression data
            try:
                data_norm = normalize_expression(data)
                if data_norm is not None:
                    all_genes = CONFIG['senescence_genes']['canonical'] + CONFIG['senescence_genes']['sasp']
                    scores = compute_senescence_score(data_norm, all_genes)

                    if scores is not None:
                        os.makedirs(os.path.join(output_dir, name), exist_ok=True)
                        scores_df = pd.DataFrame({'Senescence_Score': scores})
                        scores_path = os.path.join(output_dir, name, f"{name}_senescence_scores.csv")
                        scores_df.to_csv(scores_path)
                        logger.info(f"Saved: {name}")
                        results[name] = 'SUCCESS'
            except Exception as e:
                logger.error(f"Processing {name} failed: {e}")
                results[name] = 'PROCESS_FAILED'
        else:
            results[name] = 'LOAD_FAILED'

    return results


def process_category_3_tissue(datasets_dict):
    """Process Category 3: Tissue"""
    logger.info("="*60)
    logger.info("CATEGORY 3: TISSUE")
    logger.info("="*60)

    output_dir = os.path.join(CONFIG['output_path'], '3_Tissue_Expansion')
    results = {}

    for name, filepath in datasets_dict.items():
        # Load based on file type
        if os.path.isdir(filepath):
            data = load_raw_folder(filepath, name)
        elif filepath.endswith('.xlsx'):
            data = load_excel_file(filepath)
        else:
            data = load_series_matrix(filepath)

        if data is not None:
            try:
                data_norm = normalize_expression(data)
                if data_norm is not None:
                    all_genes = CONFIG['senescence_genes']['canonical'] + CONFIG['senescence_genes']['sasp']
                    scores = compute_senescence_score(data_norm, all_genes)

                    if scores is not None:
                        os.makedirs(os.path.join(output_dir, name), exist_ok=True)
                        scores_df = pd.DataFrame({'Senescence_Score': scores})
                        scores_path = os.path.join(output_dir, name, f"{name}_senescence_scores.csv")
                        scores_df.to_csv(scores_path)
                        logger.info(f"Saved: {name}")
                        results[name] = 'SUCCESS'
            except Exception as e:
                logger.error(f"Processing {name} failed: {e}")
                results[name] = 'PROCESS_FAILED'
        else:
            results[name] = 'LOAD_FAILED'

    return results


def process_category_4_senescence(datasets_dict):
    """Process Category 4: Senescence Validation"""
    logger.info("="*60)
    logger.info("CATEGORY 4: SENESCENCE VALIDATION")
    logger.info("="*60)

    output_dir = os.path.join(CONFIG['output_path'], '4_Senescence_Validation')
    results = {}

    for name, filepath in datasets_dict.items():
        # Load based on file type
        if os.path.isdir(filepath):
            data = load_raw_folder(filepath, name)
        elif filepath.endswith('.xlsx'):
            data = load_excel_file(filepath)
        else:
            data = load_series_matrix(filepath)

        if data is not None:
            try:
                data_norm = normalize_expression(data)
                if data_norm is not None:
                    all_genes = CONFIG['senescence_genes']['canonical'] + CONFIG['senescence_genes']['sasp']
                    scores = compute_senescence_score(data_norm, all_genes)

                    if scores is not None:
                        os.makedirs(os.path.join(output_dir, name), exist_ok=True)
                        scores_df = pd.DataFrame({'Senescence_Score': scores})
                        scores_path = os.path.join(output_dir, name, f"{name}_senescence_scores.csv")
                        scores_df.to_csv(scores_path)
                        logger.info(f"Saved: {name}")
                        results[name] = 'SUCCESS'
            except Exception as e:
                logger.error(f"Processing {name} failed: {e}")
                results[name] = 'PROCESS_FAILED'
        else:
            results[name] = 'LOAD_FAILED'

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main execution pipeline"""
    logger.info("="*60)
    logger.info("FLEXIBLE MULTI-OMICS INTEGRATION PIPELINE v2")
    logger.info("="*60)
    logger.info(f"Base path: {CONFIG['base_path']}")
    logger.info(f"Output path: {CONFIG['output_path']}")
    logger.info("")

    # Auto-detect available datasets
    available_datasets = find_available_datasets()

    logger.info("")
    logger.info(f"SUMMARY: Found {len(available_datasets['series_matrix'])} series matrix files, "
                f"{len(available_datasets['excel'])} Excel files, "
                f"{len(available_datasets['raw_folders'])} RAW folders")
    logger.info("")

    # Categorize datasets
    categorized = categorize_datasets(available_datasets)

    # Process each category
    results = {
        'Category_1_Bulk': process_category_1_bulk(categorized['category_1_bulk']),
        'Category_2_scRNA': process_category_2_scrna(categorized['category_2_scrna']),
        'Category_3_Tissue': process_category_3_tissue(categorized['category_3_tissue']),
        'Category_4_Senescence': process_category_4_senescence(categorized['category_4_senescence']),
    }

    # Print summary
    logger.info("")
    logger.info("="*60)
    logger.info("PIPELINE SUMMARY")
    logger.info("="*60)
    for category, status_dict in results.items():
        success_count = len([v for v in status_dict.values() if v == 'SUCCESS'])
        total_count = len(status_dict)
        logger.info(f"{category}: {success_count}/{total_count} successful")
        if status_dict:
            for dataset, status in status_dict.items():
                if status != 'SUCCESS':
                    logger.warning(f"  {dataset}: {status}")

    logger.info("")
    logger.info(f"Results saved to: {CONFIG['output_path']}")
    logger.info("PIPELINE COMPLETE")


if __name__ == '__main__':
    main()
