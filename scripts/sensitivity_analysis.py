#!/usr/bin/env python3
"""
Remaining confirmatory and sensitivity items from the pre-specified plan
(docs/STATISTICAL_ANALYSIS.md Part A, tag sap-v1): 1.8.6 (combined score),
1.8.7 (combination search), 1.8.8 (synovium), 1.8.11 (S9, window
sensitivity), 1.8.12 (S1, GSE110169 added to CD44).

Data sources are the same already-committed files used by
scripts/analyze_results.py (figures 2 and 8) and
scripts/statistical_analysis.py -- no new download, no raw re-parsing beyond
what those scripts already do.

Not covered here: 1.8.9 (composition adjustment) and 1.8.10 (canonical-gene
and inflammation-subset sensitivity), which need full per-sample gene-level
expression matrices for marker genes outside the six CAR-T targets, across
all 12 confirmatory datasets. That is substantially more parsing work
(reusing the per-dataset loaders in pipeline_complete.py and
process_phase2_datasets.py) and is deliberately left for a separate pass --
see docs/STATISTICAL_ANALYSIS.md Part B.

Run from the repository root:
    python scripts/sensitivity_analysis.py
"""
import os
import itertools
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_curve, auc
from statsmodels.stats.multitest import multipletests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, 'results', 'tables')
SEED = 42
N_BOOT = 2000
N_NULL = 1000

TARGETS = ['CD38', 'CD44', 'CSPG4', 'ICAM1', 'VCAM1', 'EGFR']
PRE_2015_DATASETS = {'GSE36700', 'GSE32591', 'GSE52471', 'GSE49454'}


# ---------------------------------------------------------------------------
# Shared pooling function (same method as statistical_analysis.py; duplicated
# here in minimal form to keep this script runnable on its own -- identical
# formulas, not a different method).
# ---------------------------------------------------------------------------
def fisher_pool(r, n):
    r = np.asarray(r, dtype=float)
    n = np.asarray(n, dtype=float)
    k = len(r)
    if k == 0:
        return {'k': 0, 'pooled_r': np.nan, 'ci_lo': np.nan, 'ci_hi': np.nan, 'I2': np.nan, 'p_value': np.nan}
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    var = 1.0 / (n - 3)
    w = 1.0 / var
    if k == 1:
        se = np.sqrt(var[0])
        return {'k': 1, 'pooled_r': round(float(np.tanh(z[0])), 4),
                'ci_lo': round(float(np.tanh(z[0] - 1.96 * se)), 4),
                'ci_hi': round(float(np.tanh(z[0] + 1.96 * se)), 4), 'I2': np.nan,
                'p_value': round(float(2 * (1 - stats.norm.cdf(abs(z[0] / se)))), 6)}
    z_fe = np.sum(w * z) / np.sum(w)
    Q = np.sum(w * (z - z_fe) ** 2)
    df = k - 1
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - df) / c) if c > 0 else 0.0
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    w_star = 1.0 / (var + tau2)
    z_re = np.sum(w_star * z) / np.sum(w_star)
    q_star = np.sum(w_star * (z - z_re) ** 2) / df
    se_hk = np.sqrt(q_star / np.sum(w_star))
    tcrit = stats.t.ppf(0.975, df)
    lo, hi = z_re - tcrit * se_hk, z_re + tcrit * se_hk
    t_stat = z_re / se_hk if se_hk > 0 else np.nan
    p = 2 * (1 - stats.t.cdf(abs(t_stat), df)) if se_hk > 0 else np.nan
    return {'k': k, 'pooled_r': round(float(np.tanh(z_re)), 4), 'ci_lo': round(float(np.tanh(lo)), 4),
            'ci_hi': round(float(np.tanh(hi)), 4), 'I2': round(float(I2), 2),
            'p_value': round(float(p), 6) if not np.isnan(p) else np.nan}


def cliffs_delta(x, y):
    x = np.asarray(x); y = np.asarray(y)
    gt = sum(xi > yi for xi in x for yi in y)
    lt = sum(xi < yi for xi in x for yi in y)
    return (gt - lt) / (len(x) * len(y))


# ---------------------------------------------------------------------------
# 1.8.8 Synovium (GSE36700) -- corrects a labelling bug in the existing
# fig2_disease_comparison(): that function matches group labels by looking
# for 'PSO' in the sample ID, but the actual 5th group in this dataset's
# sample IDs is 'SA' (seronegative arthritis), not 'PSO'. Those 4 samples
# were therefore silently excluded from every comparison in that function.
# Fixed here: labels are read directly from the known prefix set.
# ---------------------------------------------------------------------------
def synovium_analysis():
    path = os.path.join(REPO_ROOT, 'data', 'external_validation', '3_Tissue_Expansion',
                         'GSE36700', 'GSE36700_senescence_scores.csv')
    df = pd.read_csv(path, index_col=0).dropna()

    prefix_to_group = {'SLE': 'SLE', 'OA': 'OA', 'RA': 'RA', 'MIC': 'MIC', 'SA': 'SA'}
    labels = []
    for idx in df.index:
        s = str(idx)
        matched = None
        for prefix in ['SLE', 'OA', 'RA', 'MIC', 'SA']:
            if s.startswith(prefix):
                matched = prefix
                break
        labels.append(prefix_to_group.get(matched, 'Other'))
    df['Group'] = labels
    print("Synovium group sizes:", df['Group'].value_counts().to_dict())

    order = ['SLE', 'OA', 'RA', 'MIC', 'SA']
    groups_present = [g for g in order if (df['Group'] == g).sum() >= 2]

    # Omnibus
    h, kw_p = stats.kruskal(*[df[df['Group'] == g]['Senescence_Score'].values for g in groups_present])

    rng = np.random.default_rng(SEED)
    sle = df[df['Group'] == 'SLE']['Senescence_Score'].values
    rows = []
    comparators = [g for g in groups_present if g != 'SLE']
    pvals = []
    for g in comparators:
        other = df[df['Group'] == g]['Senescence_Score'].values
        _, p = stats.mannwhitneyu(sle, other, alternative='two-sided')
        delta = cliffs_delta(sle, other)
        boot_deltas = np.empty(N_BOOT)
        for i in range(N_BOOT):
            bs = rng.choice(sle, size=len(sle), replace=True)
            bo = rng.choice(other, size=len(other), replace=True)
            boot_deltas[i] = cliffs_delta(bs, bo)
        ci_lo, ci_hi = np.percentile(boot_deltas, [2.5, 97.5])
        rows.append({'Comparison': f'SLE vs {g}', 'n_SLE': len(sle), 'n_other': len(other),
                     'cliffs_delta': round(float(delta), 4),
                     'delta_ci_lo': round(float(ci_lo), 4), 'delta_ci_hi': round(float(ci_hi), 4),
                     'p_unadjusted': round(float(p), 6)})
        pvals.append(p)
    _, p_holm, _, _ = multipletests(pvals, method='holm')
    for row, ph in zip(rows, p_holm):
        row['p_holm'] = round(float(ph), 6)

    # ROC: SLE vs non-SLE, with bootstrap CI on AUC
    y_true = (df['Group'] == 'SLE').astype(int).values
    y_score = df['Senescence_Score'].values
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    boot_aucs = []
    idx_all = np.arange(len(y_true))
    for i in range(N_BOOT):
        bi = rng.choice(idx_all, size=len(idx_all), replace=True)
        if len(set(y_true[bi])) < 2:
            continue
        f, t, _ = roc_curve(y_true[bi], y_score[bi])
        boot_aucs.append(auc(f, t))
    auc_ci = np.percentile(boot_aucs, [2.5, 97.5]) if boot_aucs else (np.nan, np.nan)

    summary = pd.DataFrame(rows)
    summary.to_csv(os.path.join(OUT_DIR, 'stat_synovium.csv'), index=False)

    with open(os.path.join(OUT_DIR, 'stat_synovium_omnibus.txt'), 'w') as f:
        f.write(f"Kruskal-Wallis H={h:.4f}, p={kw_p:.6f}, groups={groups_present}, "
                f"group sizes={df['Group'].value_counts().to_dict()}\n")
        f.write(f"ROC AUC (SLE vs non-SLE) = {roc_auc:.4f}, "
                f"bootstrap 95% CI = ({auc_ci[0]:.4f}, {auc_ci[1]:.4f}), n_boot={len(boot_aucs)}\n")

    print(f"1.8.8 -> stat_synovium.csv, stat_synovium_omnibus.txt")
    print(f"  KW H={h:.3f} p={kw_p:.4f}; groups used: {groups_present}")
    print(summary.to_string(index=False))
    print(f"  ROC AUC={roc_auc:.3f}, 95% CI ({auc_ci[0]:.3f}, {auc_ci[1]:.3f})")


# ---------------------------------------------------------------------------
# 1.8.6 + 1.8.7: combined score, comparison to single markers, combination
# search. GSE228066 only -- this is the one confirmatory dataset with a
# full per-sample target-expression matrix already loaded by the existing
# fig8_target_combination(); the manuscript already discloses the combined-
# score comparison as single-dataset, so this does not understate scope.
# ---------------------------------------------------------------------------
def load_gse228066():
    expr_path = os.path.join(REPO_ROOT, 'datasets', 'GSE228066_gene.xlsx')
    score_path = os.path.join(REPO_ROOT, 'data', 'external_validation', '1_Bulk_Expansion',
                               'GSE228066', 'GSE228066_senescence_scores.csv')
    df = pd.read_excel(expr_path)
    df = df.set_index(df.columns[0])
    df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all', axis=0).dropna(how='all', axis=1)
    sums = df.sum(axis=0).replace(0, 1)
    expr = np.log2((df.div(sums, axis=1) * 1e6) + 1)
    scores = pd.read_csv(score_path, index_col=0).dropna()
    common = expr.columns.intersection(scores.index)
    return expr[common], scores.loc[common, 'Senescence_Score']


def combined_score_analysis():
    expr, sen = load_gse228066()
    avail = [t for t in TARGETS if t in expr.index]
    print(f"Targets available in GSE228066: {avail}")

    # DEC-08 (corrected): raw mean of log2(CPM+1) values, NOT z-scored -- this
    # is what scripts/analyze_results.py's fig8_target_combination() actually
    # computes, and the only version that reproduces the manuscript's
    # r=0.576 (verified: a z-scored version gives r=0.456 on the same data).
    tgt_z = expr.loc[avail].T

    combo3 = ['CD38', 'CD44', 'CSPG4']
    combined = tgt_z[combo3].mean(axis=1)
    r_combined, p_combined = stats.spearmanr(combined, sen)

    single_rows = []
    for t in avail:
        r, p = stats.spearmanr(tgt_z[t], sen)
        single_rows.append({'Target': t, 'Spearman_r': round(float(r), 4), 'p_value': round(float(p), 6)})

    # DEC-09: paired bootstrap of difference (combined - each single marker)
    rng = np.random.default_rng(SEED)
    n = len(sen)
    diff_rows = []
    for t in avail:
        diffs = np.empty(N_BOOT)
        for i in range(N_BOOT):
            bi = rng.integers(0, n, n)
            r_c, _ = stats.spearmanr(combined.values[bi], sen.values[bi])
            r_s, _ = stats.spearmanr(tgt_z[t].values[bi], sen.values[bi])
            diffs[i] = r_c - r_s
        ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
        diff_rows.append({'Comparison': f'combined_vs_{t}',
                           'diff_mean_boot': round(float(diffs.mean()), 4),
                           'diff_ci_lo': round(float(ci_lo), 4), 'diff_ci_hi': round(float(ci_hi), 4),
                           'excludes_zero': bool(ci_lo > 0 or ci_hi < 0)})

    pd.DataFrame(single_rows).to_csv(os.path.join(OUT_DIR, 'stat_combined_singles.csv'), index=False)
    pd.DataFrame(diff_rows).to_csv(os.path.join(OUT_DIR, 'stat_combined_bootstrap.csv'), index=False)
    with open(os.path.join(OUT_DIR, 'stat_combined_summary.txt'), 'w') as f:
        f.write(f"Combined (CD38+CD44+CSPG4) score vs senescence, GSE228066 (n={n}): "
                f"r={r_combined:.4f}, p={p_combined:.6f}\n")

    # 1.8.7: combination search across all 20 three-marker combinations
    search_rows = []
    for combo in itertools.combinations(avail, 3):
        c = tgt_z[list(combo)].mean(axis=1)
        r, p = stats.spearmanr(c, sen)
        search_rows.append({'Combination': '+'.join(combo), 'Spearman_r': round(float(r), 4),
                             'p_value': round(float(p), 6)})
    search_df = pd.DataFrame(search_rows).sort_values('Spearman_r', ascending=False).reset_index(drop=True)
    search_df['rank'] = search_df.index + 1
    search_df.to_csv(os.path.join(OUT_DIR, 'stat_combination_search.csv'), index=False)

    cd38_44_cspg4_rank = search_df.loc[search_df['Combination'].apply(
        lambda c: set(c.split('+')) == {'CD38', 'CD44', 'CSPG4'}), 'rank']
    rank_val = int(cd38_44_cspg4_rank.iloc[0]) if len(cd38_44_cspg4_rank) else None

    # Random-triplet null (DEC-09): 1000 random 3-of-avail combinations WITH
    # replacement across draws (not restricted to the 20 unique ones), to
    # give a null distribution for the percentile of the actual combination.
    null_rs = np.empty(N_NULL)
    for i in range(N_NULL):
        combo = rng.choice(avail, size=3, replace=False)
        c = tgt_z[list(combo)].mean(axis=1)
        r, _ = stats.spearmanr(c, sen)
        null_rs[i] = r
    percentile = float((null_rs < r_combined).mean() * 100)
    pd.DataFrame({'null_r': null_rs}).to_csv(os.path.join(OUT_DIR, 'stat_combined_null.csv'), index=False)

    print(f"1.8.6 -> stat_combined_singles.csv, stat_combined_bootstrap.csv, stat_combined_summary.txt")
    print(f"  combined r={r_combined:.4f} p={p_combined:.6f}")
    print(f"1.8.7 -> stat_combination_search.csv (n={len(search_df)} combinations), "
          f"CD38+CD44+CSPG4 rank={rank_val} of {len(search_df)}")
    print(f"  random-triplet null (n={N_NULL}): actual combination percentile = {percentile:.1f}")


# ---------------------------------------------------------------------------
# 1.8.11 (S9) and 1.8.12 (S1): reuse the per-dataset table already produced
# by statistical_analysis.py.
# ---------------------------------------------------------------------------
def window_and_s1_sensitivity():
    per_ds = pd.read_csv(os.path.join(OUT_DIR, 'stat_confirmatory_per_dataset.csv'))
    evaluable = per_ds[~per_ds['not_evaluable']]

    # S9: exclude pre-2015 datasets from the confirmatory (non-sensitivity-only) pool
    conf = evaluable[~evaluable['Dataset'].isin({'GSE110169'})]
    s9_rows = []
    for t in TARGETS:
        sub = conf[(conf['Target'] == t) & (~conf['Dataset'].isin(PRE_2015_DATASETS))]
        res = fisher_pool(sub['Spearman_r'].values, sub['N'].values)
        s9_rows.append({'Target': t, **res})
    pd.DataFrame(s9_rows).to_csv(os.path.join(OUT_DIR, 'stat_S9.csv'), index=False)
    print("1.8.11 -> stat_S9.csv (excludes GSE36700, GSE32591, GSE52471, GSE49454 where present in the confirmatory CD38-EGFR set;"
          " note GSE36700 itself is not in this per-dataset table -- it only appears in the synovium analysis, so S9 here"
          " affects GSE32591, GSE52471, GSE49454 only)")

    # S1: add GSE110169 to the CD44 pool
    cd44_conf = evaluable[(evaluable['Target'] == 'CD44') & (~evaluable['Dataset'].isin({'GSE110169'}))]
    cd44_with_110169 = evaluable[evaluable['Target'] == 'CD44']
    res_without = fisher_pool(cd44_conf['Spearman_r'].values, cd44_conf['N'].values)
    res_with = fisher_pool(cd44_with_110169['Spearman_r'].values, cd44_with_110169['N'].values)
    pd.DataFrame([{'Target': 'CD44', 'variant': 'without_GSE110169', **res_without},
                  {'Target': 'CD44', 'variant': 'with_GSE110169', **res_with}]).to_csv(
        os.path.join(OUT_DIR, 'stat_S1.csv'), index=False)
    print(f"1.8.12 -> stat_S1.csv: CD44 pooled r without GSE110169={res_without['pooled_r']}, "
          f"with GSE110169={res_with['pooled_r']}")


if __name__ == '__main__':
    synovium_analysis()
    print()
    combined_score_analysis()
    print()
    window_and_s1_sensitivity()
    print("\nDone. 1.8.9 (composition) and 1.8.10 (canonical/inflammation) remain -- see Part B.")
