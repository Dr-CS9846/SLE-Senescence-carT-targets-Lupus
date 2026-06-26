#!/usr/bin/env python3
"""
Downstream Statistical Analysis
Computes real statistics from senescence scores and raw expression data.
Generates figures and a verified results summary.
"""

import os
import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

SCORE_DIR = 'data/external_validation'
DATASET_DIR = 'datasets'
OUTPUT_DIR = 'results'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'figures'), exist_ok=True)

SENMAYO = pd.read_csv('data/senmayo_125genes.csv')['Gene'].tolist()
CART_TARGETS = ['CSPG4', 'CD44', 'ICAM1', 'VCAM1', 'CD38', 'EGFR']

# ---------------------------------------------------------------------------
# 1. Load all senescence scores
# ---------------------------------------------------------------------------

def load_all_scores():
    scores = {}
    for cat in os.listdir(SCORE_DIR):
        cat_path = os.path.join(SCORE_DIR, cat)
        if not os.path.isdir(cat_path):
            continue
        for ds in os.listdir(cat_path):
            ds_path = os.path.join(cat_path, ds)
            csv_files = [f for f in os.listdir(ds_path) if f.endswith('_senescence_scores.csv')]
            if csv_files:
                df = pd.read_csv(os.path.join(ds_path, csv_files[0]), index_col=0)
                df = df.dropna()
                if len(df) > 0:
                    scores[ds] = {'category': cat, 'scores': df, 'n': len(df)}
    return scores

# ---------------------------------------------------------------------------
# 2. Cross-dataset senescence distribution
# ---------------------------------------------------------------------------

def analyze_distributions(scores):
    print("\n=== CROSS-DATASET SENESCENCE DISTRIBUTION ===")
    summary = []
    for ds, info in sorted(scores.items()):
        s = info['scores']['Senescence_Score']
        summary.append({
            'Dataset': ds,
            'Category': info['category'],
            'N': len(s),
            'Mean': round(s.mean(), 4),
            'SD': round(s.std(), 4),
            'Min': round(s.min(), 4),
            'Max': round(s.max(), 4),
        })
        print(f"  {ds:45s}  N={len(s):6d}  mean={s.mean():+.3f}  sd={s.std():.3f}")

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(os.path.join(OUTPUT_DIR, 'senescence_score_summary.csv'), index=False)
    return summary_df

# ---------------------------------------------------------------------------
# 3. Disease group comparisons (where sample IDs encode condition)
# ---------------------------------------------------------------------------

def extract_disease_groups():
    """Extract SLE vs HC vs other groups from sample IDs where possible"""
    groups = {}

    # GSE36700: OA1-5, RA1-7, SLE1-4, MIC1-5, PSO1-4
    path = os.path.join(SCORE_DIR, '3_Tissue_Expansion/GSE36700/GSE36700_senescence_scores.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0).dropna()
        labels = []
        for idx in df.index:
            idx_str = str(idx)
            if 'SLE' in idx_str: labels.append('SLE')
            elif 'OA' in idx_str: labels.append('OA')
            elif 'RA' in idx_str: labels.append('RA')
            elif 'MIC' in idx_str: labels.append('MIC')
            elif 'PSO' in idx_str: labels.append('PSO')
            else: labels.append('Unknown')
        df['Group'] = labels
        groups['GSE36700'] = df

    # GSE163121: folder names contain HC1, HC2, SLE1, SLE2, SLE3
    path = os.path.join(SCORE_DIR, '2_scRNA_Expansion/GSE163121_RAW/GSE163121_RAW_senescence_scores.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0).dropna()
        # Cells from HC vs SLE folders — we can't distinguish after merging
        # but we know the dataset had 2 HC + 3 SLE patients
        groups['GSE163121_info'] = '2 HC + 3 SLE patients (cell-level labels not preserved after loading)'

    # GSE294496: Control_D7 vs aCSF1R_D7
    path = os.path.join(SCORE_DIR, '3_Tissue_Expansion/GSE294496/GSE294496_senescence_scores.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0).dropna()
        if len(df) >= 2:
            groups['GSE294496'] = df

    return groups

def analyze_disease_comparisons(groups):
    print("\n=== DISEASE GROUP COMPARISONS ===")
    results = []

    if 'GSE36700' in groups:
        df = groups['GSE36700']
        print("\n  GSE36700 (Synovial Biopsies):")

        for group in ['OA', 'RA', 'MIC', 'PSO']:
            sle = df[df['Group'] == 'SLE']['Senescence_Score']
            other = df[df['Group'] == group]['Senescence_Score']
            if len(sle) >= 2 and len(other) >= 2:
                stat, p = stats.mannwhitneyu(sle, other, alternative='two-sided')
                effect = sle.mean() - other.mean()
                result = {
                    'Comparison': f'SLE vs {group}',
                    'Dataset': 'GSE36700',
                    'N_SLE': len(sle),
                    'N_Other': len(other),
                    'Mean_SLE': round(sle.mean(), 4),
                    'Mean_Other': round(other.mean(), 4),
                    'Effect_Size': round(effect, 4),
                    'U_statistic': stat,
                    'p_value': round(p, 6),
                    'Significant': p < 0.05,
                }
                results.append(result)
                sig = '*' if p < 0.05 else 'ns'
                print(f"    SLE (n={len(sle)}) vs {group} (n={len(other)}): "
                      f"effect={effect:+.3f}, U={stat:.0f}, p={p:.4f} {sig}")

        # Kruskal-Wallis across all groups
        group_data = [df[df['Group'] == g]['Senescence_Score'].values
                      for g in ['SLE', 'OA', 'RA', 'MIC', 'PSO']
                      if len(df[df['Group'] == g]) >= 2]
        if len(group_data) >= 3:
            h_stat, kw_p = stats.kruskal(*group_data)
            print(f"    Kruskal-Wallis (all groups): H={h_stat:.2f}, p={kw_p:.4f}")
            results.append({
                'Comparison': 'Kruskal-Wallis (all groups)',
                'Dataset': 'GSE36700',
                'U_statistic': h_stat,
                'p_value': round(kw_p, 6),
                'Significant': kw_p < 0.05,
            })

    if results:
        pd.DataFrame(results).to_csv(os.path.join(OUTPUT_DIR, 'disease_comparisons.csv'), index=False)
    return results

# ---------------------------------------------------------------------------
# 4. CAR-T target expression analysis
# ---------------------------------------------------------------------------

def analyze_cart_targets():
    print("\n=== CAR-T TARGET GENE EXPRESSION ===")
    results = []

    # Load datasets where we have HUGO gene names
    target_datasets = [
        ('GSE228066', 'datasets/GSE228066_gene.xlsx', 'excel'),
        ('GSE139358', 'datasets/GSE139358_RNA-Seq_gene_rpkm_18_samples.xlsx', 'excel'),
        ('GSE182825', 'datasets/GSE182825_Analyzed_Counts.txt/GSE182825_Analyzed_Counts.txt', 'tsv'),
    ]

    for ds_name, filepath, fmt in target_datasets:
        if not os.path.exists(filepath):
            continue
        try:
            if fmt == 'excel':
                df = pd.read_excel(filepath)
            else:
                df = pd.read_csv(filepath, sep='\t')
            df = df.set_index(df.columns[0])
            df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all', axis=0)

            # Normalize
            sums = df.sum(axis=0).replace(0, 1)
            expr = np.log2((df.div(sums, axis=1) * 1e6) + 1)

            # Check each target
            for target in CART_TARGETS:
                if target in expr.index:
                    vals = expr.loc[target]
                    mean_expr = vals.mean()
                    std_expr = vals.std()

                    # Correlation with senescence score
                    score_path = None
                    for cat in os.listdir(SCORE_DIR):
                        p = os.path.join(SCORE_DIR, cat, ds_name, f'{ds_name}_senescence_scores.csv')
                        if os.path.exists(p):
                            score_path = p
                            break

                    corr_r = corr_p = None
                    if score_path:
                        scores = pd.read_csv(score_path, index_col=0).dropna()
                        common = vals.index.intersection(scores.index)
                        if len(common) >= 5:
                            r, p = stats.spearmanr(vals[common], scores.loc[common, 'Senescence_Score'])
                            corr_r = round(r, 4)
                            corr_p = round(p, 6)

                    result = {
                        'Target': target,
                        'Dataset': ds_name,
                        'Mean_Expression': round(mean_expr, 4),
                        'SD_Expression': round(std_expr, 4),
                        'Senescence_Correlation_r': corr_r,
                        'Senescence_Correlation_p': corr_p,
                        'N_Samples': len(vals),
                    }
                    results.append(result)
                    corr_str = f"r={corr_r:.3f}, p={corr_p:.4f}" if corr_r else "N/A"
                    print(f"  {target:8s} in {ds_name}: mean={mean_expr:.3f}, sd={std_expr:.3f}, "
                          f"corr_with_senescence: {corr_str}")

        except Exception as e:
            print(f"  Error loading {ds_name}: {e}")

    if results:
        pd.DataFrame(results).to_csv(os.path.join(OUTPUT_DIR, 'cart_target_expression.csv'), index=False)
    return results

# ---------------------------------------------------------------------------
# 5. Cross-dataset consistency (are senescence patterns reproducible?)
# ---------------------------------------------------------------------------

def analyze_consistency(scores):
    print("\n=== CROSS-DATASET CONSISTENCY ===")

    # Compare variance of senescence scores across categories
    cat_scores = {}
    for ds, info in scores.items():
        cat = info['category'].split('_', 1)[1] if '_' in info['category'] else info['category']
        if cat not in cat_scores:
            cat_scores[cat] = []
        cat_scores[cat].append({
            'dataset': ds,
            'mean': info['scores']['Senescence_Score'].mean(),
            'var': info['scores']['Senescence_Score'].var(),
            'n': info['n'],
        })

    for cat, datasets in cat_scores.items():
        print(f"\n  {cat}:")
        for d in datasets:
            print(f"    {d['dataset']:40s}  n={d['n']:5d}  mean={d['mean']:+.4f}  var={d['var']:.4f}")

    return cat_scores

# ---------------------------------------------------------------------------
# 6. Generate figures
# ---------------------------------------------------------------------------

def generate_figures(scores, groups):
    fig_dir = os.path.join(OUTPUT_DIR, 'figures')

    # Figure 1: Senescence score distribution across all datasets
    fig, ax = plt.subplots(figsize=(14, 6))
    plot_data = []
    for ds, info in sorted(scores.items()):
        s = info['scores']['Senescence_Score']
        if len(s) > 500:
            s = s.sample(500, random_state=42)
        for val in s:
            plot_data.append({'Dataset': ds.replace('_', '\n')[:20], 'Score': val,
                              'Category': info['category'].split('_', 1)[1][:15]})
    plot_df = pd.DataFrame(plot_data)
    if len(plot_df) > 0:
        sns.boxplot(data=plot_df, x='Dataset', y='Score', hue='Category', dodge=False, ax=ax)
        ax.set_title('Senescence Score Distribution Across Datasets')
        ax.set_ylabel('Senescence Score (Z-normalized)')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=90, labelsize=7)
        ax.legend(fontsize=8, loc='upper right')
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, 'fig1_senescence_distributions.png'), dpi=150)
        plt.close()
        print(f"\n  Saved: fig1_senescence_distributions.png")

    # Figure 2: GSE36700 disease comparison
    if 'GSE36700' in groups:
        fig, ax = plt.subplots(figsize=(8, 5))
        df = groups['GSE36700']
        order = ['SLE', 'OA', 'RA', 'MIC', 'PSO']
        existing = [g for g in order if g in df['Group'].values]
        sns.boxplot(data=df, x='Group', y='Senescence_Score', order=existing, ax=ax)
        sns.stripplot(data=df, x='Group', y='Senescence_Score', order=existing,
                      color='black', size=5, ax=ax)
        ax.set_title('Senescence Scores: SLE vs Other Arthropathies (GSE36700)')
        ax.set_ylabel('Senescence Score (Z-normalized)')
        ax.set_xlabel('Disease Group')
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, 'fig2_disease_comparison_GSE36700.png'), dpi=150)
        plt.close()
        print(f"  Saved: fig2_disease_comparison_GSE36700.png")

    # Figure 3: Category-level summary
    fig, ax = plt.subplots(figsize=(8, 5))
    cat_data = []
    for ds, info in scores.items():
        cat = info['category'].split('_', 1)[1].replace('_', ' ')
        s = info['scores']['Senescence_Score']
        if len(s) > 200:
            s = s.sample(200, random_state=42)
        for val in s:
            cat_data.append({'Category': cat, 'Score': val})
    cat_df = pd.DataFrame(cat_data)
    if len(cat_df) > 0:
        sns.violinplot(data=cat_df, x='Category', y='Score', ax=ax, inner='box')
        ax.set_title('Senescence Scores by Data Category')
        ax.set_ylabel('Senescence Score (Z-normalized)')
        ax.tick_params(axis='x', rotation=15)
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, 'fig3_category_comparison.png'), dpi=150)
        plt.close()
        print(f"  Saved: fig3_category_comparison.png")

# ---------------------------------------------------------------------------
# 7. Generate verified results JSON
# ---------------------------------------------------------------------------

def save_verified_results(summary_df, disease_results, cart_results, cat_scores):
    verified = {
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
        'datasets_analyzed': len(summary_df),
        'total_samples': int(summary_df['N'].sum()),
        'senescence_panel': '125-gene SenMayo (Saul et al.)',
        'score_summary': summary_df.to_dict(orient='records'),
        'disease_comparisons': disease_results if disease_results else 'No labeled groups available',
        'cart_target_analysis': cart_results if cart_results else 'No target data available',
        'category_summary': {cat: len(ds) for cat, ds in cat_scores.items()},
    }
    with open(os.path.join(OUTPUT_DIR, 'VERIFIED_RESULTS.json'), 'w') as f:
        json.dump(verified, f, indent=2, default=str)
    print(f"\n  Saved: VERIFIED_RESULTS.json")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("DOWNSTREAM ANALYSIS: Real Statistics from Senescence Scores")
    print("=" * 70)

    scores = load_all_scores()
    print(f"\nLoaded {len(scores)} datasets with valid scores")

    if not scores:
        print("ERROR: No valid senescence scores found. Run pipeline_complete.py first.")
        return

    summary_df = analyze_distributions(scores)
    groups = extract_disease_groups()
    disease_results = analyze_disease_comparisons(groups)
    cart_results = analyze_cart_targets()
    cat_scores = analyze_consistency(scores)
    generate_figures(scores, groups)
    save_verified_results(summary_df, disease_results, cart_results, cat_scores)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print(f"Results saved to: {OUTPUT_DIR}/")
    print(f"Figures saved to: {OUTPUT_DIR}/figures/")
    print("=" * 70)

if __name__ == '__main__':
    main()
