#!/usr/bin/env python3
"""
Regenerate Figure S3 (target-senescence correlation across 12 datasets) and
Figure S1 (senescence score distribution across all 28 datasets), using the
real, already-computed data in results/tables/. No new statistics computed
here -- purely visualization of existing verified numbers.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams.update({'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
                      'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})

# ---------------------------------------------------------------------------
# FIGURE S3 (fig3_cart_targets.png): target x dataset correlation heatmap,
# now across all 12 datasets with usable target-gene annotation (was 3)
# ---------------------------------------------------------------------------
corr = pd.read_csv(f"{REPO}/results/tables/cart_target_statistics.csv")
targets = ['CD38', 'CD44', 'CSPG4', 'ICAM1', 'VCAM1', 'EGFR']
datasets_order = ['GSE228066', 'GSE139358', 'GSE182825', 'GSE65391', 'GSE108497',
                   'GSE72326', 'GSE110169', 'GSE49454', 'GSE32591', 'GSE112943',
                   'GSE81622', 'GSE52471']

r_mat = pd.DataFrame(index=targets, columns=datasets_order, dtype=float)
sig_mat = pd.DataFrame(index=targets, columns=datasets_order, dtype=object)
for _, row in corr.iterrows():
    t, d = row['Target'], row['Dataset']
    if t in targets and d in datasets_order:
        r_mat.loc[t, d] = row['Spearman_r'] if pd.notna(row['Spearman_r']) and row['Spearman_r'] != '' else np.nan
        sig_mat.loc[t, d] = row['Significant']

r_mat = r_mat.astype(float)

fig, axes = plt.subplots(1, 2, figsize=(16, 5.5), gridspec_kw={'width_ratios': [2.1, 1]})

ax = axes[0]
mask = r_mat.isna()
sns.heatmap(r_mat, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            mask=mask, cbar_kws={'label': "Spearman r"}, linewidths=0.5, linecolor='white',
            ax=ax, annot_kws={'size': 8})
ax.set_title('A. Target-Senescence Correlation Across 12 Independent Datasets\n(3 Phase 1 anchor + 9 Phase 2 datasets; grey = not evaluable)', fontsize=11)
ax.set_xlabel('')
ax.set_ylabel('')
for tick in ax.get_xticklabels():
    tick.set_rotation(45)
    tick.set_ha('right')
for i in range(len(r_mat.index)):
    for j in range(len(r_mat.columns)):
        if mask.iloc[i, j]:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color='#D9D9D9'))

ax2 = axes[1]
consensus_rows = []
for t in targets:
    sub = corr[corr['Target'] == t]
    sig = sub['Significant'].astype(str)
    n_pos = ((sig == 'True') & (sub['Spearman_r'].astype(float) > 0)).sum()
    n_neg = ((sig == 'True') & (sub['Spearman_r'].astype(float) < 0)).sum()
    n_ns = (sig == 'False').sum()
    consensus_rows.append({'Target': t, 'Sig. positive': n_pos, 'Sig. negative': n_neg, 'Not significant': n_ns})
cons_df = pd.DataFrame(consensus_rows).set_index('Target')
cons_df[['Sig. positive', 'Sig. negative', 'Not significant']].plot(
    kind='barh', stacked=True, ax=ax2, color=['#2E7D32', '#C62828', '#BDBDBD'])
ax2.set_title('B. Cross-Dataset Consensus\n(datasets meeting p<0.05, by direction)', fontsize=11)
ax2.set_xlabel('Number of datasets')
ax2.legend(loc='lower right', fontsize=8)
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(f"{REPO}/results/figures/fig3_cart_targets.png")
plt.close()
print("Saved fig3_cart_targets.png (Figure S3)")

# ---------------------------------------------------------------------------
# FIGURE S1 (fig1_senescence_landscape.png): senescence score distribution
# across all 28 datasets, by modality and by phase
# ---------------------------------------------------------------------------
t1 = pd.read_csv(f"{REPO}/results/tables/table1_dataset_summary.csv")

modality_map = {
    'Bulk Expansion': 'Bulk RNA-seq', 'scRNA Expansion': 'scRNA-seq',
    'Tissue Expansion': 'Bulk RNA-seq / NanoString', 'Senescence Validation': 'Bulk RNA-seq (reference)',
}
new_modality_map = {
    'New SLE Cohort (Blood)': 'Microarray', 'New SLE Cohort (Kidney)': 'Microarray',
    'New SLE Cohort (Skin+Kidney)': 'Microarray', 'New SLE Cohort (Skin)': 'Microarray',
}
t1['Modality'] = t1['Category'].map(lambda c: modality_map.get(c, new_modality_map.get(c, c)))
t1['Phase'] = t1['Category'].apply(lambda c: 'Phase 2 (new)' if str(c).startswith('New SLE') else 'Phase 1')

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

ax = axes[0, 0]
order = t1.sort_values('Score_Median')['Dataset']
sns.barplot(data=t1, y='Dataset', x='Score_Median', hue='Phase', order=order, dodge=False,
            palette={'Phase 1': '#90A4AE', 'Phase 2 (new)': '#1E88E5'}, ax=ax)
ax.axvline(0, color='k', lw=0.8)
ax.set_title('A. Median Senescence Score (Z) by Dataset, All 28 Datasets', fontsize=11)
ax.set_xlabel('Score_Median (mean is ~0 by construction under Z-normalization)')
ax.set_ylabel('')
ax.tick_params(axis='y', labelsize=6)

ax = axes[0, 1]
sns.violinplot(data=t1, x='Modality', y='Score_Median', hue='Modality', ax=ax, palette='Set2', cut=0, legend=False)
ax.axhline(0, color='k', lw=0.8, alpha=0.5)
ax.set_title('B. Score Median Distribution by Modality', fontsize=11)
ax.tick_params(axis='x', rotation=30)

ax = axes[1, 0]
sns.histplot(data=t1, x='N_Samples', hue='Phase', bins=15, ax=ax,
             palette={'Phase 1': '#90A4AE', 'Phase 2 (new)': '#1E88E5'}, multiple='stack')
ax.set_title('C. Sample Size Distribution', fontsize=11)
ax.set_xlabel('N samples/cells per dataset')

ax = axes[1, 1]
sns.scatterplot(data=t1, x='N_Samples', y='Score_SD', hue='Phase', s=60,
                 palette={'Phase 1': '#90A4AE', 'Phase 2 (new)': '#1E88E5'}, ax=ax)
ax.set_xscale('log')
ax.set_title('D. Signal Strength (Score SD) vs. Dataset Size', fontsize=11)
ax.set_xlabel('N samples/cells (log scale)')
ax.set_ylabel('Senescence score SD')

plt.suptitle('Senescence Score Distribution Across All 28 Datasets (Phase 1 + Phase 2)', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig(f"{REPO}/results/figures/fig1_senescence_landscape.png")
plt.close()
print("Saved fig1_senescence_landscape.png (Figure S1)")

print("\nDone. Both figures regenerated from real, already-verified data in results/tables/.")
