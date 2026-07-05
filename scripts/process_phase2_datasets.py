#!/usr/bin/env python3
"""
Phase 2 dataset acquisition and senescence scoring.

Downloads 9 independently-verified real GEO SLE datasets directly from NCBI
(series matrix or, where the series matrix table is empty, the relevant
supplementary file), resolves probe-to-gene-symbol mapping live from NCBI's
platform annotation endpoint, and applies the same SenMayo scoring methodology
used in scripts/pipeline_complete.py:
  - SenMayo mean-expression scoring (>=3 genes required, else top-13-variable-gene fallback)
  - Z-normalization within dataset
  - Spearman correlation of 6 CAR-T target genes against the senescence score

Every accession was verified against NCBI's E-utilities API before being added
here (title, organism, sample count, platform) — see README.md Section 1.3.

Run from the repository root:
    python scripts/process_phase2_datasets.py
"""
import pandas as pd
import numpy as np
from scipy import stats
import json, os, gzip, urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO_ROOT, 'datasets', 'phase2_cache')
PLATFORM_DIR = os.path.join(REPO_ROOT, 'data', 'platform_annotations')
SENMAYO_PATH = os.path.join(REPO_ROOT, 'data', 'senmayo_125genes.csv')
OUT_DIR = os.path.join(REPO_ROOT, 'data', 'external_validation', '5_New_SLE_Cohorts')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PLATFORM_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

SENMAYO_GENES = pd.read_csv(SENMAYO_PATH)['Gene'].tolist()
TARGETS = ['CD38', 'CD44', 'CSPG4', 'ICAM1', 'VCAM1', 'EGFR']

# accession -> (platform, series-matrix URL, optional override supplementary-file URL)
DATASETS = {
    'GSE108497': ('GPL10558',
                  'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE108nnn/GSE108497/matrix/GSE108497_series_matrix.txt.gz',
                  'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE108nnn/GSE108497/suppl/GSE108497_normalized_data.txt.gz'),
    'GSE110169': ('GPL13667', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE110nnn/GSE110169/matrix/GSE110169_series_matrix.txt.gz', None),
    'GSE112943': ('GPL10558', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE112nnn/GSE112943/matrix/GSE112943_series_matrix.txt.gz', None),
    'GSE32591':  ('GPL14663', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE32nnn/GSE32591/matrix/GSE32591_series_matrix.txt.gz', None),
    'GSE49454':  ('GPL10558', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE49nnn/GSE49454/matrix/GSE49454_series_matrix.txt.gz', None),
    'GSE52471':  ('GPL571',   'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE52nnn/GSE52471/matrix/GSE52471_series_matrix.txt.gz', None),
    'GSE65391':  ('GPL10558', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE65nnn/GSE65391/matrix/GSE65391_series_matrix.txt.gz', None),
    'GSE72326':  ('GPL10558', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE72nnn/GSE72326/matrix/GSE72326_series_matrix.txt.gz', None),
    'GSE81622':  ('GPL10558', 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE81nnn/GSE81622/matrix/GSE81622_series_matrix.txt.gz', None),
}

PLATFORM_URL = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gpl}&targ=self&form=text&view=full"


def download(url, dest):
    if os.path.exists(dest):
        return dest
    print(f"  downloading {url} ...")
    urllib.request.urlretrieve(url, dest)
    return dest


def load_platform_map(gpl):
    dest = os.path.join(PLATFORM_DIR, f"{gpl}.txt")
    if not os.path.exists(dest):
        download(PLATFORM_URL.format(gpl=gpl), dest)

    with open(dest, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    start = next(i for i, l in enumerate(lines) if l.startswith('!platform_table_begin')) + 1
    header = lines[start].rstrip('\n').split('\t')
    sym_col = next((i for i, h in enumerate(header) if h.strip().lower() in ('gene symbol', 'gene_symbol')), None)
    mapping = {}
    for l in lines[start + 1:]:
        if l.startswith('!platform_table_end'):
            break
        parts = l.rstrip('\n').split('\t')
        if len(parts) <= sym_col:
            continue
        sym = parts[sym_col].strip()
        if sym and sym != '---':
            mapping[parts[0].strip()] = sym.split(' /// ')[0].strip()
    return mapping


def parse_series_matrix(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    start = end = None
    for i, l in enumerate(lines):
        if l.startswith('!series_matrix_table_begin'):
            start = i + 1
        elif l.startswith('!series_matrix_table_end'):
            end = i
            break
    header = lines[start].rstrip('\n').replace('"', '').split('\t')
    sample_ids = header[1:]
    ids, rows = [], []
    for l in lines[start + 1:end]:
        parts = l.rstrip('\n').replace('"', '').split('\t')
        if len(parts) < 2:
            continue
        ids.append(parts[0])
        vals = []
        for v in parts[1:]:
            try:
                vals.append(float(v))
            except ValueError:
                vals.append(np.nan)
        rows.append(vals)
    return pd.DataFrame(rows, index=ids, columns=sample_ids)


def score_and_correlate(gene_expr, acc):
    avail = [g for g in SENMAYO_GENES if g in gene_expr.index]
    if len(avail) >= 3:
        score = gene_expr.loc[avail].mean(axis=0)
        method = f"SenMayo direct ({len(avail)}/125)"
    else:
        top_var = gene_expr.var(axis=1).sort_values(ascending=False)
        score = gene_expr.loc[top_var.index[:13]].mean(axis=0)
        method = f"Fallback top-variable (SenMayo matched={len(avail)}/125)"
    score_z = (score - score.mean()) / (score.std() + 1e-6)

    results = []
    for t in TARGETS:
        if t not in gene_expr.index:
            results.append({'Target': t, 'Dataset': acc, 'N': len(score_z), 'Spearman_r': None, 'p_value': None,
                             'Note': 'gene not detected on this platform/dataset'})
            continue
        tv = gene_expr.loc[t]
        common = tv.index.intersection(score_z.index)
        r, p = stats.spearmanr(tv[common], score_z[common])
        results.append({'Target': t, 'Dataset': acc, 'N': len(common),
                         'Mean_Expr': round(float(tv[common].mean()), 4),
                         'Spearman_r': round(float(r), 4), 'p_value': round(float(p), 6),
                         'Significant': bool(p < 0.05)})
    return score_z, method, len(avail), results


def process_standard(acc, gpl, url):
    dest = os.path.join(CACHE_DIR, f"{acc}_series_matrix.txt.gz")
    download(url, dest)
    txt_path = dest[:-3]
    if not os.path.exists(txt_path):
        with gzip.open(dest, 'rt', encoding='utf-8', errors='ignore') as f_in, open(txt_path, 'w', encoding='utf-8') as f_out:
            f_out.write(f_in.read())
    expr = parse_series_matrix(txt_path)
    probe_map = load_platform_map(gpl)
    expr['gene'] = expr.index.map(lambda p: probe_map.get(p))
    gene_expr = expr.dropna(subset=['gene']).groupby('gene').mean(numeric_only=True)
    return gene_expr


def process_gse108497():
    """GSE108497's series matrix table is empty; real data is in its suppl normalized-data file
    as interleaved signal/detection-p-value columns, linear scale, needing log2 transform."""
    _, _, suppl_url = DATASETS['GSE108497']
    dest = os.path.join(CACHE_DIR, "GSE108497_normalized_data.txt.gz")
    download(suppl_url, dest)
    df = pd.read_csv(dest, sep='\t', compression='gzip', index_col=0)
    sig_cols = [c for c in df.columns if not c.startswith('Detection Pval')]
    expr = df[sig_cols].apply(pd.to_numeric, errors='coerce').clip(lower=1.0)
    expr_log = np.log2(expr)
    probe_map = load_platform_map('GPL10558')
    expr_log['gene'] = expr_log.index.map(lambda p: probe_map.get(p))
    return expr_log.dropna(subset=['gene']).groupby('gene').mean(numeric_only=True)


def main():
    all_results = {}
    for acc, (gpl, url, suppl) in DATASETS.items():
        print(f"\n=== {acc} ({gpl}) ===")
        try:
            if acc == 'GSE108497':
                gene_expr = process_gse108497()
            else:
                gene_expr = process_standard(acc, gpl, url)
            score_z, method, n_matched, target_results = score_and_correlate(gene_expr, acc)

            outdir = os.path.join(OUT_DIR, acc)
            os.makedirs(outdir, exist_ok=True)
            score_z.to_frame('Senescence_Score').to_csv(os.path.join(outdir, f"{acc}_senescence_scores.csv"))

            all_results[acc] = {'platform': gpl, 'n_samples': len(score_z),
                                 'senmayo_genes_matched': n_matched, 'scoring_method': method,
                                 'target_results': target_results}
            print(f"  n={len(score_z)}, SenMayo matched={n_matched}/125, method={method}")
        except Exception as e:
            print(f"  !! FAILED: {e}")
            all_results[acc] = {'error': str(e)}

    with open(os.path.join(OUT_DIR, 'PHASE2_RESULTS.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nDone. Results written to {OUT_DIR}")


if __name__ == '__main__':
    main()
