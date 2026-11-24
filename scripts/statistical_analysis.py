#!/usr/bin/env python3
"""
Confirmatory and sensitivity statistical analysis (plan step 1.8 of the
LUP-26-366 revision), per the pre-specified plan in docs/STATISTICAL_ANALYSIS.md
Part A (committed at tag sap-v1, before this script existed).

This script implements plan items 1.8.1-1.8.5 (per-dataset correlation table
with BH q-values; random-effects pooling by target with Holm correction;
leave-one-dataset-out; tissue-stratified pooling). It reads only the
already-committed, already-verified per-dataset correlation table
(results/tables/cart_target_statistics.csv) -- no raw expression data is
re-parsed here, and no number in that source table is changed.

Items 1.8.6-1.8.12 (combined score, combination search, synovium, composition
and canonical-gene sensitivity, window sensitivity, GSE110169 addition) need
either full per-sample gene-expression matrices (composition/canonical) or a
separate re-run of the existing combined-score/synovium code paths in
analyze_results.py, and are deliberately NOT included in this script. See
docs/STATISTICAL_ANALYSIS.md Part B for what is and is not yet covered.

Run from the repository root:
    python scripts/statistical_analysis.py
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_PATH = os.path.join(REPO_ROOT, 'results', 'tables', 'cart_target_statistics.csv')
OUT_DIR = os.path.join(REPO_ROOT, 'results', 'tables')

TARGETS = ['CD38', 'CD44', 'CSPG4', 'ICAM1', 'VCAM1', 'EGFR']

# DEC-02: minimum 15 units. DEC-04: GSE110169 is sensitivity-only (added back
# in S1), not part of the main confirmatory pooled estimate even though it
# clears the unit threshold, because it is evaluable for CD44 only.
SENSITIVITY_ONLY_DATASETS = {'GSE110169'}

# Tissue assignment, from the manuscript/README dataset descriptions (not
# re-derived here). GSE112943 mixes skin and kidney samples in one series
# with no per-sample tissue label in the committed senescence-score file, so
# it is excluded from tissue-stratified pooling rather than assigned to
# either tissue.
TISSUE = {
    'GSE228066': 'blood', 'GSE139358': 'blood', 'GSE65391': 'blood',
    'GSE108497': 'blood', 'GSE72326': 'blood', 'GSE49454': 'blood',
    'GSE81622': 'blood', 'GSE110169': 'blood',  # sensitivity-only; excluded from main tissue pooling below
    'GSE182825': 'skin', 'GSE52471': 'skin',
    'GSE32591': 'kidney',
    'GSE112943': 'mixed_skin_kidney_excluded',
}

# Four datasets released before 2015 (DEC-22); used later for S9, not in this script.
PRE_2015_DATASETS = {'GSE36700', 'GSE32591', 'GSE52471', 'GSE49454'}


def fisher_pool(r, n, label=''):
    """Random-effects pooling of Spearman rho via Fisher z, DerSimonian-Laird
    tau^2, Hartung-Knapp-Sidik-Jonkman CI. r, n are same-length arrays/lists
    for the studies entering this pool (already filtered by caller)."""
    r = np.asarray(r, dtype=float)
    n = np.asarray(n, dtype=float)
    k = len(r)
    out = {'k': k}
    if k == 0:
        return {**out, 'pooled_r': np.nan, 'ci_lo': np.nan, 'ci_hi': np.nan,
                'Q': np.nan, 'I2': np.nan, 'tau2': np.nan, 'p_value': np.nan}
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    var = 1.0 / (n - 3)
    w = 1.0 / var

    if k == 1:
        z_pooled = z[0]
        se = np.sqrt(var[0])
        tcrit = stats.t.ppf(0.975, max(k - 1, 1))
        lo, hi = z_pooled - 1.96 * se, z_pooled + 1.96 * se  # single study: normal approx, no HK df
        pooled_r = np.tanh(z_pooled)
        p = 2 * (1 - stats.norm.cdf(abs(z_pooled / se)))
        return {**out, 'pooled_r': round(float(pooled_r), 4),
                'ci_lo': round(float(np.tanh(lo)), 4), 'ci_hi': round(float(np.tanh(hi)), 4),
                'Q': np.nan, 'I2': np.nan, 'tau2': 0.0, 'p_value': round(float(p), 6)}

    z_fe = np.sum(w * z) / np.sum(w)
    Q = np.sum(w * (z - z_fe) ** 2)
    df = k - 1
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - df) / c) if c > 0 else 0.0
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0

    w_star = 1.0 / (var + tau2)
    z_re = np.sum(w_star * z) / np.sum(w_star)

    # Hartung-Knapp-Sidik-Jonkman variance and CI
    q_star = np.sum(w_star * (z - z_re) ** 2) / df
    var_hk = q_star / np.sum(w_star)
    se_hk = np.sqrt(var_hk)
    tcrit = stats.t.ppf(0.975, df)
    lo, hi = z_re - tcrit * se_hk, z_re + tcrit * se_hk
    t_stat = z_re / se_hk if se_hk > 0 else np.nan
    p = 2 * (1 - stats.t.cdf(abs(t_stat), df)) if se_hk > 0 else np.nan

    return {**out, 'pooled_r': round(float(np.tanh(z_re)), 4),
            'ci_lo': round(float(np.tanh(lo)), 4), 'ci_hi': round(float(np.tanh(hi)), 4),
            'Q': round(float(Q), 4), 'I2': round(float(I2), 2), 'tau2': round(float(tau2), 5),
            'p_value': round(float(p), 6) if not np.isnan(p) else np.nan}


def main():
    df = pd.read_csv(IN_PATH)

    # ---- 1.8.1 + 1.8.2: per-dataset table with not-evaluable flag and BH q ----
    df['not_evaluable'] = df['Spearman_r'].isna()
    df['q_BH'] = np.nan
    evaluable_mask = ~df['not_evaluable']
    _, q, _, _ = multipletests(df.loc[evaluable_mask, 'p_value'].values, method='fdr_bh')
    df.loc[evaluable_mask, 'q_BH'] = q
    df.to_csv(os.path.join(OUT_DIR, 'stat_confirmatory_per_dataset.csv'), index=False)
    print(f"1.8.1/1.8.2 -> stat_confirmatory_per_dataset.csv ({evaluable_mask.sum()} evaluable of {len(df)} rows)")

    # ---- 1.8.3: random-effects pooled rho per target, confirmatory set only ----
    # Confirmatory set excludes sensitivity-only datasets (DEC-04: GSE110169).
    conf = df[evaluable_mask & ~df['Dataset'].isin(SENSITIVITY_ONLY_DATASETS)]
    pooled_rows = []
    for t in TARGETS:
        sub = conf[conf['Target'] == t]
        res = fisher_pool(sub['Spearman_r'].values, sub['N'].values)
        pooled_rows.append({'Target': t, **res})
    pooled = pd.DataFrame(pooled_rows)
    _, p_holm, _, _ = multipletests(pooled['p_value'].values, method='holm')
    pooled['p_holm'] = p_holm
    pooled.to_csv(os.path.join(OUT_DIR, 'stat_pooled_by_target.csv'), index=False)
    print("1.8.3 -> stat_pooled_by_target.csv")
    print(pooled[['Target', 'k', 'pooled_r', 'ci_lo', 'ci_hi', 'I2', 'p_value', 'p_holm']].to_string(index=False))

    # ---- 1.8.4: leave-one-dataset-out range per target ----
    loo_rows = []
    for t in TARGETS:
        sub = conf[conf['Target'] == t]
        if len(sub) < 2:
            continue
        pooled_vals = []
        for ds in sub['Dataset']:
            rest = sub[sub['Dataset'] != ds]
            r = fisher_pool(rest['Spearman_r'].values, rest['N'].values)['pooled_r']
            pooled_vals.append(r)
        loo_rows.append({'Target': t, 'loo_min': round(float(np.nanmin(pooled_vals)), 4),
                          'loo_max': round(float(np.nanmax(pooled_vals)), 4), 'n_loo_runs': len(pooled_vals)})
    pd.DataFrame(loo_rows).to_csv(os.path.join(OUT_DIR, 'stat_loo.csv'), index=False)
    print("1.8.4 -> stat_loo.csv")

    # ---- 1.8.5: tissue-stratified pooling (blood, skin: >=2 datasets; kidney: single dataset reported per-dataset) ----
    conf_t = conf.copy()
    conf_t['tissue'] = conf_t['Dataset'].map(TISSUE)
    tissue_rows = []
    for tissue_name in ['blood', 'skin']:
        for t in TARGETS:
            sub = conf_t[(conf_t['tissue'] == tissue_name) & (conf_t['Target'] == t)]
            if len(sub) < 2:
                continue
            res = fisher_pool(sub['Spearman_r'].values, sub['N'].values)
            tissue_rows.append({'Tissue': tissue_name, 'Target': t, **res})
    # Kidney: single dataset (GSE32591) -- report per-dataset values directly, not pooled.
    kidney = conf_t[conf_t['tissue'] == 'kidney']
    for _, row in kidney.iterrows():
        tissue_rows.append({'Tissue': 'kidney', 'Target': row['Target'], 'k': 1,
                             'pooled_r': row['Spearman_r'], 'ci_lo': np.nan, 'ci_hi': np.nan,
                             'Q': np.nan, 'I2': np.nan, 'tau2': np.nan, 'p_value': row['p_value'],
                             'note': 'single dataset (GSE32591); not pooled'})
    pd.DataFrame(tissue_rows).to_csv(os.path.join(OUT_DIR, 'stat_by_tissue.csv'), index=False)
    print("1.8.5 -> stat_by_tissue.csv (GSE112943 excluded: mixed skin+kidney, no per-sample tissue label available)")

    print("\nDone. Items 1.8.6-1.8.12 (combined score, combination search, synovium,")
    print("composition/canonical/window sensitivity, GSE110169 addition) are not")
    print("produced by this script -- see docs/STATISTICAL_ANALYSIS.md Part B.")


if __name__ == '__main__':
    main()
