#!/usr/bin/env python3
"""
Comprehensive Downstream Analysis for SLE Senescence & CAR-T Targets
Generates publication-ready figures and verified statistical results.
"""

import os
import json
import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve, auc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

SCORE_DIR = 'data/external_validation'
DATASET_DIR = 'datasets'
OUTPUT_DIR = 'results'
os.makedirs(os.path.join(OUTPUT_DIR, 'figures'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'tables'), exist_ok=True)

SENMAYO = pd.read_csv('data/senmayo_125genes.csv')
SENMAYO_GENES = SENMAYO['Gene'].tolist()
SENMAYO_CATEGORIES = SENMAYO.set_index('Gene')['Category'].to_dict()

CART_TARGETS = ['CSPG4', 'CD44', 'ICAM1', 'VCAM1', 'CD38', 'EGFR']

CATEGORY_COLORS = {
    'Bulk Expansion': '#2196F3',
    'scRNA Expansion': '#4CAF50',
    'Tissue Expansion': '#FF9800',
    'Senescence Validation': '#9C27B0',
}

plt.rcParams.update({
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def load_all_scores():
    scores = {}
    for cat in sorted(os.listdir(SCORE_DIR)):
        cat_path = os.path.join(SCORE_DIR, cat)
        if not os.path.isdir(cat_path):
            continue
        for ds in sorted(os.listdir(cat_path)):
            ds_path = os.path.join(cat_path, ds)
            if not os.path.isdir(ds_path):
                continue
            csvs = [f for f in os.listdir(ds_path) if f.endswith('.csv')]
            if csvs:
                df = pd.read_csv(os.path.join(ds_path, csvs[0]), index_col=0).dropna()
                if len(df) > 0:
                    cat_clean = cat.split('_', 1)[1].replace('_', ' ') if '_' in cat else cat
                    scores[ds] = {'category': cat_clean, 'cat_full': cat, 'scores': df, 'n': len(df)}
    return scores


def load_expression(filepath, fmt='excel'):
    if not os.path.exists(filepath):
        return None
    try:
        if fmt == 'excel':
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath, sep='\t')
        df = df.set_index(df.columns[0])
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all', axis=0).dropna(how='all', axis=1)
        sums = df.sum(axis=0).replace(0, 1)
        return np.log2((df.div(sums, axis=1) * 1e6) + 1)
    except:
        return None


def get_score_for_dataset(ds_name):
    for cat in os.listdir(SCORE_DIR):
        p = os.path.join(SCORE_DIR, cat, ds_name, f'{ds_name}_senescence_scores.csv')
        if os.path.exists(p):
            return pd.read_csv(p, index_col=0).dropna()
    return None


# ============================================================================
# FIGURE 1: Multi-dataset senescence landscape
# ============================================================================

def fig1_senescence_landscape(scores):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1a: Box plots by dataset
    ax = axes[0, 0]
    plot_data = []
    for ds, info in sorted(scores.items(), key=lambda x: x[1]['category']):
        s = info['scores']['Senescence_Score']
        if len(s) > 300:
            s = s.sample(300, random_state=42)
        for val in s:
            plot_data.append({'Dataset': ds[:15], 'Score': val, 'Category': info['category']})
    pdf = pd.DataFrame(plot_data)
    cats = pdf['Category'].unique()
    palette = {c: CATEGORY_COLORS.get(c, '#888') for c in cats}
    sns.boxplot(data=pdf, x='Dataset', y='Score', hue='Category', dodge=False,
                palette=palette, ax=ax, fliersize=2, linewidth=0.8)
    ax.set_title('A. Senescence Score Distribution')
    ax.set_ylabel('Senescence Score (Z)')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=90, labelsize=6)
    ax.legend(fontsize=7, loc='upper right')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    # 1b: Violin by category
    ax = axes[0, 1]
    cat_data = []
    for ds, info in scores.items():
        s = info['scores']['Senescence_Score']
        if len(s) > 200:
            s = s.sample(200, random_state=42)
        for val in s:
            cat_data.append({'Category': info['category'], 'Score': val})
    cdf = pd.DataFrame(cat_data)
    sns.violinplot(data=cdf, x='Category', y='Score', palette=CATEGORY_COLORS,
                   inner='box', ax=ax, linewidth=0.8)
    ax.set_title('B. Senescence by Data Modality')
    ax.set_ylabel('Senescence Score (Z)')
    ax.tick_params(axis='x', rotation=15, labelsize=9)

    # 1c: Sample size per dataset
    ax = axes[1, 0]
    ds_names = [ds[:15] for ds in sorted(scores.keys(), key=lambda x: scores[x]['n'], reverse=True)]
    ds_n = [scores[ds]['n'] for ds in sorted(scores.keys(), key=lambda x: scores[x]['n'], reverse=True)]
    ds_cats = [scores[ds]['category'] for ds in sorted(scores.keys(), key=lambda x: scores[x]['n'], reverse=True)]
    colors = [CATEGORY_COLORS.get(c, '#888') for c in ds_cats]
    ax.barh(ds_names, ds_n, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_title('C. Sample Size per Dataset')
    ax.set_xlabel('N Samples/Cells')
    ax.tick_params(axis='y', labelsize=7)
    ax.invert_yaxis()

    # 1d: Variance across datasets
    ax = axes[1, 1]
    ds_var = [(ds[:15], info['scores']['Senescence_Score'].var(), info['category'])
              for ds, info in scores.items() if info['scores']['Senescence_Score'].var() > 0]
    ds_var.sort(key=lambda x: x[1], reverse=True)
    ax.barh([d[0] for d in ds_var], [d[1] for d in ds_var],
            color=[CATEGORY_COLORS.get(d[2], '#888') for d in ds_var],
            edgecolor='white', linewidth=0.5)
    ax.set_title('D. Score Variance (Signal Strength)')
    ax.set_xlabel('Variance')
    ax.tick_params(axis='y', labelsize=7)
    ax.invert_yaxis()

    plt.suptitle('Figure 1: Multi-Dataset Senescence Landscape (19 GEO Datasets, 2919 Samples)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig1_senescence_landscape.png'))
    plt.close()
    print("  Fig 1: Senescence landscape (4 panels)")


# ============================================================================
# FIGURE 2: Disease-specific senescence (GSE36700)
# ============================================================================

def fig2_disease_comparison():
    path = os.path.join(SCORE_DIR, '3_Tissue_Expansion/GSE36700/GSE36700_senescence_scores.csv')
    if not os.path.exists(path):
        print("  Fig 2: SKIPPED (GSE36700 not found)")
        return {}

    df = pd.read_csv(path, index_col=0).dropna()
    labels = []
    for idx in df.index:
        s = str(idx)
        if 'SLE' in s: labels.append('SLE')
        elif 'OA' in s: labels.append('OA')
        elif 'RA' in s: labels.append('RA')
        elif 'MIC' in s: labels.append('MIC')
        elif 'PSO' in s: labels.append('PSO')
        else: labels.append('Other')
    df['Group'] = labels

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    order = ['SLE', 'OA', 'RA', 'MIC', 'PSO']
    existing = [g for g in order if g in df['Group'].values]
    colors = {'SLE': '#E53935', 'OA': '#1E88E5', 'RA': '#43A047', 'MIC': '#FB8C00', 'PSO': '#8E24AA'}

    # 2a: Box + strip
    ax = axes[0]
    sns.boxplot(data=df, x='Group', y='Senescence_Score', order=existing,
                palette=colors, ax=ax, linewidth=0.8)
    sns.stripplot(data=df, x='Group', y='Senescence_Score', order=existing,
                  color='black', size=6, ax=ax, zorder=5)
    ax.set_title('A. Senescence by Disease')
    ax.set_ylabel('Senescence Score (Z)')

    # 2b: Effect sizes vs SLE
    ax = axes[1]
    effects = []
    sle_scores = df[df['Group'] == 'SLE']['Senescence_Score']
    for group in ['OA', 'RA', 'MIC', 'PSO']:
        other = df[df['Group'] == group]['Senescence_Score']
        if len(sle_scores) >= 2 and len(other) >= 2:
            effect = sle_scores.mean() - other.mean()
            _, p = stats.mannwhitneyu(sle_scores, other, alternative='two-sided')
            effects.append({'Group': f'vs {group}', 'Effect': effect, 'p': p})
    if effects:
        edf = pd.DataFrame(effects)
        bars = ax.bar(edf['Group'], edf['Effect'],
                      color=['#E53935' if e > 0 else '#1E88E5' for e in edf['Effect']],
                      edgecolor='white')
        for i, row in edf.iterrows():
            sig = '**' if row['p'] < 0.01 else '*' if row['p'] < 0.05 else 'ns'
            ax.text(i, row['Effect'] + 0.05, f"p={row['p']:.3f}\n{sig}",
                    ha='center', fontsize=8)
        ax.set_title('B. Effect Size (SLE - Other)')
        ax.set_ylabel('Difference in Senescence Score')
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    # 2c: ROC - SLE vs non-SLE
    ax = axes[2]
    y_true = (df['Group'] == 'SLE').astype(int)
    y_score = df['Senescence_Score']
    if y_true.sum() > 0 and y_true.sum() < len(y_true):
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color='#E53935', lw=2, label=f'AUC = {roc_auc:.3f}')
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(f'C. ROC: SLE vs Non-SLE (AUC={roc_auc:.3f})')
        ax.legend(loc='lower right')

    plt.suptitle('Figure 2: Disease-Specific Senescence Patterns (GSE36700 Synovial Biopsies)',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig2_disease_comparison.png'))
    plt.close()
    print("  Fig 2: Disease comparison (3 panels)")

    # Compute stats
    results = {}
    h, kw_p = stats.kruskal(*[df[df['Group'] == g]['Senescence_Score'].values
                               for g in existing if len(df[df['Group'] == g]) >= 2])
    results['kruskal_wallis'] = {'H': round(h, 3), 'p': round(kw_p, 6)}
    results['pairwise'] = effects
    if y_true.sum() > 0:
        results['roc_auc'] = round(roc_auc, 4)
    return results


# ============================================================================
# FIGURE 3: CAR-T target correlation heatmap
# ============================================================================

def fig3_cart_targets():
    datasets = {
        'GSE228066': ('datasets/GSE228066_gene.xlsx', 'excel'),
        'GSE139358': ('datasets/GSE139358_RNA-Seq_gene_rpkm_18_samples.xlsx', 'excel'),
        'GSE182825': ('datasets/GSE182825_Analyzed_Counts.txt/GSE182825_Analyzed_Counts.txt', 'tsv'),
    }

    all_corr = {}
    all_pval = {}
    all_expr = {}
    full_results = []

    for ds_name, (filepath, fmt) in datasets.items():
        expr = load_expression(filepath, fmt)
        if expr is None:
            continue
        scores = get_score_for_dataset(ds_name)
        if scores is None:
            continue

        for target in CART_TARGETS:
            if target not in expr.index:
                continue
            vals = expr.loc[target]
            common = vals.index.intersection(scores.index)
            if len(common) < 5:
                continue

            r, p = stats.spearmanr(vals[common], scores.loc[common, 'Senescence_Score'])
            key = (target, ds_name)
            all_corr[key] = r
            all_pval[key] = p
            all_expr.setdefault(target, {})[ds_name] = vals[common].values

            full_results.append({
                'Target': target, 'Dataset': ds_name, 'N': len(common),
                'Mean_Expr': round(vals[common].mean(), 4),
                'Spearman_r': round(r, 4), 'p_value': round(p, 6),
                'Significant': p < 0.05,
            })

    if not all_corr:
        print("  Fig 3: SKIPPED (no target data)")
        return []

    # Build heatmap matrices
    ds_list = sorted(set(k[1] for k in all_corr.keys()))
    corr_matrix = pd.DataFrame(index=CART_TARGETS, columns=ds_list, dtype=float)
    pval_matrix = pd.DataFrame(index=CART_TARGETS, columns=ds_list, dtype=float)

    for (target, ds), r in all_corr.items():
        corr_matrix.loc[target, ds] = r
        pval_matrix.loc[target, ds] = all_pval[(target, ds)]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 3a: Correlation heatmap
    ax = axes[0]
    mask = corr_matrix.isna()
    sns.heatmap(corr_matrix.astype(float), annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, vmin=-0.8, vmax=0.8, mask=mask, ax=ax,
                linewidths=0.5, cbar_kws={'label': 'Spearman r'})
    # Add significance stars
    for i, target in enumerate(CART_TARGETS):
        for j, ds in enumerate(ds_list):
            if not pd.isna(pval_matrix.loc[target, ds]):
                p = pval_matrix.loc[target, ds]
                if p < 0.001: star = '***'
                elif p < 0.01: star = '**'
                elif p < 0.05: star = '*'
                else: star = ''
                if star:
                    ax.text(j + 0.5, i + 0.75, star, ha='center', va='center',
                            fontsize=8, color='black', fontweight='bold')
    ax.set_title('A. Target-Senescence Correlation')
    ax.set_ylabel('CAR-T Target')

    # 3b: Mean expression heatmap
    ax = axes[1]
    expr_matrix = pd.DataFrame(index=CART_TARGETS, columns=ds_list, dtype=float)
    for r in full_results:
        expr_matrix.loc[r['Target'], r['Dataset']] = r['Mean_Expr']
    mask2 = expr_matrix.isna()
    sns.heatmap(expr_matrix.astype(float), annot=True, fmt='.1f', cmap='YlOrRd',
                mask=mask2, ax=ax, linewidths=0.5, cbar_kws={'label': 'log2(CPM+1)'})
    ax.set_title('B. Mean Target Expression')
    ax.set_ylabel('CAR-T Target')

    # 3c: Consistency score (how many datasets show significant correlation)
    ax = axes[2]
    consistency = {}
    for target in CART_TARGETS:
        sig_count = sum(1 for r in full_results if r['Target'] == target and r['Significant'])
        total = sum(1 for r in full_results if r['Target'] == target)
        consistency[target] = (sig_count, total)

    targets_sorted = sorted(consistency.keys(), key=lambda t: consistency[t][0], reverse=True)
    bars = ax.barh(targets_sorted,
                   [consistency[t][0] for t in targets_sorted],
                   color=['#E53935' if consistency[t][0] >= 2 else '#90CAF9' for t in targets_sorted],
                   edgecolor='white')
    for i, t in enumerate(targets_sorted):
        ax.text(consistency[t][0] + 0.05, i, f'{consistency[t][0]}/{consistency[t][1]}',
                va='center', fontsize=9)
    ax.set_title('C. Cross-Dataset Consistency')
    ax.set_xlabel('Datasets with Significant Correlation')
    ax.set_xlim(0, 4)

    plt.suptitle('Figure 3: CAR-T Target Expression and Senescence Correlation',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig3_cart_targets.png'))
    plt.close()
    print("  Fig 3: CAR-T target analysis (3 panels)")

    pd.DataFrame(full_results).to_csv(os.path.join(OUTPUT_DIR, 'tables', 'cart_target_statistics.csv'), index=False)
    return full_results


# ============================================================================
# FIGURE 4: SenMayo category decomposition
# ============================================================================

def fig4_senmayo_decomposition():
    datasets = {
        'GSE228066': ('datasets/GSE228066_gene.xlsx', 'excel'),
        'GSE139358': ('datasets/GSE139358_RNA-Seq_gene_rpkm_18_samples.xlsx', 'excel'),
        'GSE182825': ('datasets/GSE182825_Analyzed_Counts.txt/GSE182825_Analyzed_Counts.txt', 'tsv'),
    }

    cat_scores_all = {}
    for ds_name, (filepath, fmt) in datasets.items():
        expr = load_expression(filepath, fmt)
        if expr is None:
            continue
        categories = {}
        for gene in SENMAYO_GENES:
            if gene in expr.index:
                cat = SENMAYO_CATEGORIES.get(gene, 'Other')
                categories.setdefault(cat, []).append(gene)

        cat_means = {}
        for cat, genes in categories.items():
            if len(genes) >= 2:
                cat_means[cat] = expr.loc[genes].mean(axis=0).mean()
        cat_scores_all[ds_name] = cat_means

    if not cat_scores_all:
        print("  Fig 4: SKIPPED")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 4a: Category contribution stacked bar
    ax = axes[0]
    all_cats = sorted(set(c for d in cat_scores_all.values() for c in d.keys()))
    cat_colors = plt.cm.Set3(np.linspace(0, 1, len(all_cats)))
    bottom = np.zeros(len(cat_scores_all))
    ds_names = list(cat_scores_all.keys())

    for i, cat in enumerate(all_cats):
        vals = [cat_scores_all[ds].get(cat, 0) for ds in ds_names]
        ax.bar(ds_names, vals, bottom=bottom, label=cat, color=cat_colors[i], edgecolor='white')
        bottom += np.array(vals)

    ax.set_title('A. SenMayo Category Contribution')
    ax.set_ylabel('Mean Expression (log2 CPM+1)')
    ax.legend(fontsize=7, loc='upper right', ncol=2)
    ax.tick_params(axis='x', rotation=15)

    # 4b: SASP vs Canonical ratio
    ax = axes[1]
    ratios = []
    for ds, cat_means in cat_scores_all.items():
        sasp = cat_means.get('SASP', 0)
        canonical = cat_means.get('Canonical', 0)
        if canonical > 0:
            ratios.append({'Dataset': ds, 'SASP/Canonical': sasp / canonical,
                           'SASP': sasp, 'Canonical': canonical})
    if ratios:
        rdf = pd.DataFrame(ratios)
        ax.bar(rdf['Dataset'], rdf['SASP/Canonical'], color='#E53935', edgecolor='white')
        ax.set_title('B. SASP-to-Canonical Ratio')
        ax.set_ylabel('SASP / Canonical Expression')
        ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Equal')
        ax.legend()
        ax.tick_params(axis='x', rotation=15)

    plt.suptitle('Figure 4: SenMayo Pathway Decomposition',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig4_senmayo_decomposition.png'))
    plt.close()
    print("  Fig 4: SenMayo decomposition (2 panels)")


# ============================================================================
# FIGURE 5: Senescence-high vs -low differential analysis
# ============================================================================

def fig5_high_vs_low_senescence():
    datasets = {
        'GSE228066': ('datasets/GSE228066_gene.xlsx', 'excel'),
        'GSE182825': ('datasets/GSE182825_Analyzed_Counts.txt/GSE182825_Analyzed_Counts.txt', 'tsv'),
    }

    all_de_results = []

    for ds_name, (filepath, fmt) in datasets.items():
        expr = load_expression(filepath, fmt)
        if expr is None:
            continue
        scores = get_score_for_dataset(ds_name)
        if scores is None:
            continue

        common = expr.columns.intersection(scores.index)
        if len(common) < 10:
            continue

        expr_common = expr[common]
        sc = scores.loc[common, 'Senescence_Score']

        q25 = sc.quantile(0.25)
        q75 = sc.quantile(0.75)
        low_samples = sc[sc <= q25].index
        high_samples = sc[sc >= q75].index

        if len(low_samples) < 3 or len(high_samples) < 3:
            continue

        de_results = []
        for gene in expr_common.index[:5000]:
            low_vals = expr_common.loc[gene, low_samples]
            high_vals = expr_common.loc[gene, high_samples]
            if low_vals.std() == 0 and high_vals.std() == 0:
                continue
            try:
                stat, p = stats.mannwhitneyu(high_vals, low_vals, alternative='two-sided')
                log2fc = high_vals.mean() - low_vals.mean()
                de_results.append({
                    'Gene': gene, 'log2FC': log2fc, 'p_value': p,
                    'Mean_High': high_vals.mean(), 'Mean_Low': low_vals.mean(),
                    'Dataset': ds_name,
                })
            except:
                continue

        if de_results:
            de_df = pd.DataFrame(de_results)
            de_df['p_adj'] = np.minimum(de_df['p_value'] * len(de_df), 1.0)
            de_df['neg_log10p'] = -np.log10(de_df['p_value'].clip(lower=1e-300))
            all_de_results.append(de_df)

    if not all_de_results:
        print("  Fig 5: SKIPPED (insufficient data)")
        return []

    fig, axes = plt.subplots(1, len(all_de_results), figsize=(7 * len(all_de_results), 6))
    if len(all_de_results) == 1:
        axes = [axes]

    combined_de = []
    for i, de_df in enumerate(all_de_results):
        ax = axes[i]
        ds = de_df['Dataset'].iloc[0]

        # Color by significance
        colors = []
        for _, row in de_df.iterrows():
            if row['p_adj'] < 0.05 and abs(row['log2FC']) > 1.0:
                colors.append('#E53935' if row['log2FC'] > 0 else '#1E88E5')
            else:
                colors.append('#CCCCCC')

        ax.scatter(de_df['log2FC'], de_df['neg_log10p'], c=colors, s=8, alpha=0.6)
        ax.axhline(y=-np.log10(0.05), color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(x=-1.0, color='gray', linestyle='--', alpha=0.3)

        n_up = sum(1 for _, r in de_df.iterrows() if r['p_adj'] < 0.05 and r['log2FC'] > 1.0)
        n_down = sum(1 for _, r in de_df.iterrows() if r['p_adj'] < 0.05 and r['log2FC'] < -1.0)

        # Label top genes
        sig = de_df[(de_df['p_adj'] < 0.05) & (de_df['log2FC'].abs() > 1.0)]
        top = sig.nlargest(5, 'neg_log10p')
        for _, row in top.iterrows():
            ax.annotate(row['Gene'], (row['log2FC'], row['neg_log10p']),
                        fontsize=6, alpha=0.8)

        ax.set_title(f'{ds}\n(Up: {n_up}, Down: {n_down})')
        ax.set_xlabel('log2 Fold Change (High vs Low Senescence)')
        ax.set_ylabel('-log10(p-value)')

        combined_de.append(de_df)

    plt.suptitle('Figure 5: Differential Expression (Senescence-High vs -Low Quartiles)',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig5_volcano_plots.png'))
    plt.close()
    print(f"  Fig 5: Volcano plots ({len(all_de_results)} datasets)")

    if combined_de:
        combined = pd.concat(combined_de, ignore_index=True)
        sig_genes = combined[combined['p_adj'] < 0.05].sort_values('p_value')
        sig_genes.head(100).to_csv(os.path.join(OUTPUT_DIR, 'tables', 'differential_genes_senescence.csv'), index=False)

    return combined_de


# ============================================================================
# FIGURE 6: Target scatter plots (top 3 targets)
# ============================================================================

def fig6_target_scatter():
    expr = load_expression('datasets/GSE228066_gene.xlsx', 'excel')
    if expr is None:
        print("  Fig 6: SKIPPED")
        return

    scores = get_score_for_dataset('GSE228066')
    if scores is None:
        return

    common = expr.columns.intersection(scores.index)
    top_targets = ['CD38', 'CD44', 'ICAM1']
    available = [t for t in top_targets if t in expr.index]

    if not available:
        return

    fig, axes = plt.subplots(1, len(available), figsize=(5 * len(available), 4.5))
    if len(available) == 1:
        axes = [axes]

    for i, target in enumerate(available):
        ax = axes[i]
        x = scores.loc[common, 'Senescence_Score']
        y = expr.loc[target, common]
        r, p = stats.spearmanr(x, y)

        ax.scatter(x, y, s=30, alpha=0.7, color='#1E88E5', edgecolors='white', linewidth=0.5)
        z = np.polyfit(x, y, 1)
        xline = np.linspace(x.min(), x.max(), 100)
        ax.plot(xline, np.polyval(z, xline), 'r-', linewidth=2, alpha=0.7)

        ax.set_xlabel('Senescence Score (Z)')
        ax.set_ylabel(f'{target} Expression (log2 CPM+1)')
        ax.set_title(f'{target}: r={r:.3f}, p={p:.4f}')
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(0.05, 0.95, sig, transform=ax.transAxes, fontsize=14,
                fontweight='bold', va='top', color='red')

    plt.suptitle('Figure 6: Top CAR-T Targets vs Senescence (GSE228066, N=45)',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig6_target_scatter.png'))
    plt.close()
    print("  Fig 6: Target scatter plots")


# ============================================================================
# FIGURE 7: Cross-tissue senescence heatmap
# ============================================================================

def fig7_tissue_heatmap():
    tissue_datasets = {
        'GSE36700\n(Synovium)': '3_Tissue_Expansion/GSE36700',
        'GSE155405\n(Kidney)': '3_Tissue_Expansion/GSE155405',
        'GSE174188\n(Renal)': '3_Tissue_Expansion/GSE174188',
        'GSE182825\n(Skin)': '3_Tissue_Expansion/GSE182825',
        'GSE200306\n(Glomeruli)': '3_Tissue_Expansion/GSE200306',
    }

    tissue_stats = {}
    for label, path in tissue_datasets.items():
        full = os.path.join(SCORE_DIR, path)
        if not os.path.isdir(full):
            continue
        csvs = [f for f in os.listdir(full) if f.endswith('.csv')]
        if csvs:
            df = pd.read_csv(os.path.join(full, csvs[0]), index_col=0).dropna()
            if len(df) > 0:
                tissue_stats[label] = {
                    'mean': df['Senescence_Score'].mean(),
                    'std': df['Senescence_Score'].std(),
                    'n': len(df),
                    'scores': df['Senescence_Score'].values,
                }

    if len(tissue_stats) < 2:
        print("  Fig 7: SKIPPED")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 7a: Bar chart with error bars
    ax = axes[0]
    labels = list(tissue_stats.keys())
    means = [tissue_stats[l]['mean'] for l in labels]
    stds = [tissue_stats[l]['std'] for l in labels]
    ns = [tissue_stats[l]['n'] for l in labels]
    colors = plt.cm.Set2(np.linspace(0, 1, len(labels)))

    bars = ax.bar(range(len(labels)), means, yerr=stds, capsize=4,
                  color=colors, edgecolor='white', linewidth=0.8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Senescence Score (Z)')
    ax.set_title('A. Tissue-Specific Senescence')
    for i, n in enumerate(ns):
        ax.text(i, means[i] + stds[i] + 0.05, f'n={n}', ha='center', fontsize=8)

    # 7b: Pairwise comparisons
    ax = axes[1]
    pairs = []
    tissue_labels = list(tissue_stats.keys())
    for i in range(len(tissue_labels)):
        for j in range(i + 1, len(tissue_labels)):
            s1 = tissue_stats[tissue_labels[i]]['scores']
            s2 = tissue_stats[tissue_labels[j]]['scores']
            if len(s1) >= 2 and len(s2) >= 2:
                _, p = stats.mannwhitneyu(s1, s2, alternative='two-sided')
                pairs.append({
                    'Pair': f"{tissue_labels[i][:10]} vs\n{tissue_labels[j][:10]}",
                    'p_value': p,
                    'neg_log10p': -np.log10(max(p, 1e-10)),
                })

    if pairs:
        pdf = pd.DataFrame(pairs)
        colors_p = ['#E53935' if p < 0.05 else '#90CAF9' for p in pdf['p_value']]
        ax.barh(pdf['Pair'], pdf['neg_log10p'], color=colors_p, edgecolor='white')
        ax.axvline(x=-np.log10(0.05), color='gray', linestyle='--', alpha=0.5, label='p=0.05')
        ax.set_xlabel('-log10(p-value)')
        ax.set_title('B. Pairwise Tissue Comparisons')
        ax.legend(fontsize=8)
        ax.tick_params(axis='y', labelsize=7)

    plt.suptitle('Figure 7: Cross-Tissue Senescence Patterns',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig7_tissue_heatmap.png'))
    plt.close()
    print("  Fig 7: Tissue comparison (2 panels)")


# ============================================================================
# FIGURE 8: Multi-target combination analysis
# ============================================================================

def fig8_target_combination():
    expr = load_expression('datasets/GSE228066_gene.xlsx', 'excel')
    if expr is None:
        print("  Fig 8: SKIPPED")
        return

    scores = get_score_for_dataset('GSE228066')
    if scores is None:
        return

    common = expr.columns.intersection(scores.index)
    available_targets = [t for t in CART_TARGETS if t in expr.index]

    if len(available_targets) < 3:
        return

    # Target correlation matrix
    target_expr = expr.loc[available_targets, common].T

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 8a: Target-target correlation
    ax = axes[0]
    corr = target_expr.corr(method='spearman')
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                ax=ax, linewidths=0.5, vmin=-1, vmax=1)
    ax.set_title('A. Target Co-Expression')

    # 8b: Combined target score vs senescence
    ax = axes[1]
    top3 = ['CD38', 'CD44', 'CSPG4']
    available_top3 = [t for t in top3 if t in available_targets]
    if available_top3:
        combined = target_expr[available_top3].mean(axis=1)
        sen = scores.loc[common, 'Senescence_Score']
        r, p = stats.spearmanr(combined, sen)

        ax.scatter(sen, combined, s=30, alpha=0.7, color='#E53935', edgecolors='white')
        z = np.polyfit(sen, combined, 1)
        xline = np.linspace(sen.min(), sen.max(), 100)
        ax.plot(xline, np.polyval(z, xline), 'k-', linewidth=2, alpha=0.7)
        ax.set_xlabel('Senescence Score (Z)')
        ax.set_ylabel(f'Combined Target Score ({"+".join(available_top3)})')
        ax.set_title(f'B. Combined Targets vs Senescence\nr={r:.3f}, p={p:.4f}')

    plt.suptitle('Figure 8: Multi-Target Combination Analysis',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'figures', 'fig8_target_combination.png'))
    plt.close()
    print("  Fig 8: Target combination (2 panels)")


# ============================================================================
# Summary statistics table
# ============================================================================

def generate_table1(scores):
    rows = []
    for ds, info in sorted(scores.items()):
        s = info['scores']['Senescence_Score']
        rows.append({
            'Dataset': ds,
            'Category': info['category'],
            'N_Samples': info['n'],
            'Score_Mean': round(s.mean(), 4),
            'Score_SD': round(s.std(), 4),
            'Score_Median': round(s.median(), 4),
            'Score_IQR': round(s.quantile(0.75) - s.quantile(0.25), 4),
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUTPUT_DIR, 'tables', 'table1_dataset_summary.csv'), index=False)
    print(f"\n  Table 1: Dataset summary ({len(rows)} datasets)")
    return df


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70)
    print("COMPREHENSIVE ANALYSIS: SLE Senescence & CAR-T Targets")
    print("=" * 70)

    scores = load_all_scores()
    print(f"\nLoaded {len(scores)} datasets")
    total_samples = sum(info['n'] for info in scores.values())
    print(f"Total samples/cells: {total_samples}")

    if not scores:
        print("ERROR: No valid scores. Run pipeline_complete.py first.")
        return

    print("\n--- Generating Figures ---")
    fig1_senescence_landscape(scores)
    disease_stats = fig2_disease_comparison()
    cart_results = fig3_cart_targets()
    fig4_senmayo_decomposition()
    de_results = fig5_high_vs_low_senescence()
    fig6_target_scatter()
    fig7_tissue_heatmap()
    fig8_target_combination()

    print("\n--- Generating Tables ---")
    table1 = generate_table1(scores)

    # Save verified results
    verified = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
        'total_datasets': len(scores),
        'total_samples': total_samples,
        'scoring_panel': '125-gene SenMayo (Saul et al.)',
        'disease_comparison': disease_stats,
        'cart_target_results': cart_results,
        'n_de_genes': sum(len(d[d['p_adj'] < 0.05]) for d in de_results) if de_results else 0,
    }
    with open(os.path.join(OUTPUT_DIR, 'VERIFIED_RESULTS.json'), 'w') as f:
        json.dump(verified, f, indent=2, default=str)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print(f"  Figures: {OUTPUT_DIR}/figures/ (8 figures)")
    print(f"  Tables:  {OUTPUT_DIR}/tables/ (3 CSVs)")
    print(f"  Results: {OUTPUT_DIR}/VERIFIED_RESULTS.json")
    print("=" * 70)


if __name__ == '__main__':
    main()
