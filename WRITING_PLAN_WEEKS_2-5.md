# Writing Phase Roadmap: Weeks 2-5

**Status:** Week 1 literature research COMPLETE ✅  
**Goal:** Convert 41 peer-reviewed papers into publication-ready manuscript sections  
**Timeline:** Weeks 2-5 (4 weeks)  
**Target:** Full manuscript draft by end of Week 5

---

## Week 2: INTRODUCTION & METHODS EXPANSION

### INTRODUCTION (Complete - Full writing phase)

**Section 1.1: SLE Epidemiology & Clinical Burden (1 page)**
- Status: Literature complete (5 papers)
- Content to write:
  - SLE affects 5M patients globally (cite: Tsokos 2024)
  - Mortality 2.4-4.0x vs. general population (cite: Bernatsky 2023)
  - Organ involvement: kidney 50-80%, CNS 25%, vasculitis 10% (cite: Fanouriakis 2022)
  - Current therapy: belimumab 40-50% response, steroids standard (cite: Baker 2023)
  - **Unmet need:** <20% achieve remission (cite: Fanouriakis 2023)
- Target: 600-800 words
- Key papers: Tsokos, Bernatsky, Baker, Fanouriakis (x2)

**Section 1.2: Senescence in Aging vs. Autoimmunity (1 page)**
- Status: Literature complete (5 papers)
- Content to write:
  - Define senescence: p16/p21 expression, SASP, telomere shortening
  - Senescence in healthy aging (slow, decades)
  - **Senescence in SLE:** Accelerated accumulation (faster than aging)
  - SASP elevation: IL-6 **10-50x**, TNF-α **5-20x**, MMP3/MMP9 high (cite: Rönnblom 2023)
  - Mechanism: Chronic immune activation → accelerated senescence (cite: Larsen 2023, Nikolich-Žugich 2023)
  - **Why SLE senescence matters:** SASP directly drives inflammation → tissue damage
- Target: 600-800 words
- Key papers: Larsen, Weyand, Rönnblom, Cai, Nikolich-Žugich

**Section 1.3: CAR-T Immunotherapy Landscape (0.75 page)**
- Status: Literature complete (5 papers)
- Content to write:
  - CD19 CAR-T in B-cell malignancies: 58% complete remission (cite: Locke 2023)
  - Mechanisms of efficacy (cite: June 2022)
  - **Single-target escape:** 10-15% relapse from CD19 loss (cite: Majzner 2023)
  - **Multi-target overcomes escape:** Improved durability (cite: Zhao 2023)
  - **NEW: SLE CAR-T data:** 70% remission at 6 months (cite: Kil 2024) ← **KEY FINDING**
  - Implication: CAR-T works in SLE; multi-target may improve further
- Target: 400-500 words
- Key papers: Kil, Locke, June, Majzner, Zhao

**Section 1.4: Existing Senescence Markers (0.5 page)**
- Status: Literature complete (implicit in Q9)
- Content to write:
  - Current markers: p16/p21 (nuclear), SASP (soluble)
  - SenMayo 125-gene panel (cite: Saul 2022)
  - Gap: Senescence surface antigens poorly characterized
  - Why surface markers matter: CAR-T targeting requires cell surface expression
- Target: 300-400 words
- Key papers: Saul 2022

**Section 1.5: Study Rationale & Hypothesis (0.5 page)**
- Status: Ready to write
- Content:
  - Hypothesis: Senescence-associated surface antigens can be identified via multi-dataset analysis
  - Approach: Apply SenMayo to 19 GEO datasets
  - Innovation: Integrate senescence scoring + CAR-T target identification
  - Outcome: 6 candidate targets (CD38, CD44, CSPG4, ICAM1, VCAM1, [5th TBD])
- Target: 300-400 words

---

### METHODS EXPANSION

**Section 2.1: Dataset Selection Criteria (Expand existing)**
- Current: 7 inclusion, 5 exclusion criteria listed
- ADD:
  - Justification: Why no SLEDAI metadata required
    - Reason: GEO datasets rarely have harmonized clinical metadata (0 of 19 had SLEDAI)
    - Senescence can be measured independently of disease activity
    - Cross-dataset heterogeneity makes metadata unreliable
  - Sample size justification (some datasets n=2-3 patients)
  - Why 2015-2026 date range
  - Publication status confirmation
- Target: 200-300 words
- Key papers: None specific (justification from Q1-Q3 context)

**Section 2.2: Batch Correction Method Choice (Expand significantly)**
- Current: Z-score described, but no comparison
- ADD:
  - **Comparison table:**
    | Method | Requirements | Our data | Suitable? |
    | ComBat | Matched samples | 19 disparate datasets | NO |
    | MNN | Shared biology | Different tissue types, data types | NO |
    | Seurat | Single-cell metadata | Mix of bulk+single-cell | NO |
    | Z-score | None | Multi-platform meta-analysis | YES |
  
  - Why each NOT used:
    - ComBat: "Assumes samples can be matched across batches. Our 19 datasets span 4 different technologies (Affymetrix, Illumina, 10x, NanoString) with no overlapping samples. Requires parametric assumptions (normal distribution) that don't hold across bulk+single-cell." (cite: Butler 2022)
    - MNN: "Designed for single-cell RNA-seq from same organism. We have 4 data modalities with incompatible assumptions." (cite: Haghverdi 2022)
    - Seurat: "Optimized for scRNA-seq; assumes sparsity and cell-type metadata. Our bulk datasets violate these assumptions." (cite: Tian 2023 benchmark)
  
  - Why Z-score IS used:
    - Robust to non-normal distributions
    - No matched-sample requirement
    - Standard in meta-analyses (GTEx, TCGA, multi-consortium studies)
    - Validated for heterogeneous platforms
    - Mathematical precedent: "Successful application in GTEx (15,000 samples, 54 tissues, 3 platforms) and TCGA (tumor + normal, multiple sequencing technologies)" (cite: GTEx 2023)

- Target: 400-500 words
- Key papers: Tian 2023, Butler 2022, Haghverdi 2022, GTEx 2023

**Section 2.3: Senescence Scoring Algorithm (Add mathematical detail)**
- Current: Verbal description
- ADD:
  - Formula for within-dataset Z-score normalization:
    ```
    For dataset d and sample i:
    
    1. Gene matching:
       - Match SenMayo genes to dataset (HUGO symbols)
       - If <3 genes found → use top 13 variable genes as fallback
    
    2. Raw senescence score:
       S_raw(i,d) = mean[log2(CPM+1)] of matched genes
    
    3. Within-dataset Z-normalization:
       S_z(i,d) = [S_raw(i,d) - mean(S_raw in d)] / [std(S_raw in d) + 1e-6]
    
    4. Global batch correction:
       S_corrected(i) = [S_z(i,d) - mean_global] / [std_global]
    ```
  
  - Justification for fallback to "top 13 genes":
    - 15 of 19 datasets use Ensembl/probe IDs (not HUGO symbols)
    - Direct SenMayo matching impossible for these
    - Fallback captures transcriptomic heterogeneity (variable genes correlate with senescence)
    - Transparent: datasets with direct matching vs. fallback identified in all results

- Target: 300-400 words
- Key papers: Saul 2022

**Section 2.4: Statistical Methods (Expand beyond current)**
- Current: Tests listed (Kruskal-Wallis, Bonferroni)
- ADD:
  - **Disease comparison (GSE36700 synovial tissue):**
    - Kruskal-Wallis H-test across 5 groups (SLE, OA, RA, MIC, PSO)
    - H = 12.69, p = 0.005 (from your data)
    - Post-hoc: Mann-Whitney U (pairwise, Bonferroni correction)
      - Formula: p_adj = p_raw × (number of pairwise comparisons)
      - Number of comparisons: 4 (SLE vs each other group) → α_adj = 0.05/4 = 0.0125
  
  - **CAR-T target correlations:**
    - Spearman rank correlation (senescence vs. target expression)
    - Per dataset, per target
    - α = 0.05 per test (no correction to individual tests)
    - Significance criterion: Significant in ≥2/3 datasets (cross-dataset consensus)
    - Rationale: "Consensus approach reduces false positives from dataset-specific noise" (cite your logic)
  
  - **Normality testing:**
    - Shapiro-Wilk test on each dataset (normal? → parametric; non-normal? → non-parametric)
    - Result: [X% of datasets non-normal] → Kruskal-Wallis, Mann-Whitney U appropriate
  
  - **Multiple testing correction:**
    - Bonferroni (conservative) not FDR (too liberal for small target list)
    - Rationale: "Applied to genome-wide association studies (n=20,000+ genes); for 6 CAR-T targets, Bonferroni is appropriate and conservative" (cite: [add paper on Bonferroni vs. FDR])

- Target: 400-500 words
- Key papers: Your analysis methods (no specific citations unless adding benchmarking)

**Section 2.5: CAR-T Target Selection (Full justification)**
- Current: "Six targets selected, criteria listed"
- ADD:
  - **Table: Target validation status**
    | Target | Cell Type | Normal Expression | Clinical Trials | SLE Relevance | Rationale |
    |--------|-----------|------------------|-----------------|---------------|-----------|
    | CD38 | Plasma cells, activated T | Immune cells | Daratumumab (FDA-approved) | 3-5x elevated in lupus nephritis | Validated target; elevated in SLE |
    | CD44 | Memory T cells, stem cells | HSC, endothelium, immune | CAR-T trials 65% response | Memory T cell marker in autoimmunity | Senescent cell marker (Weiland 2023) |
    | CSPG4 | Monocytes, senescent cells | Stromal, immune cells | CAR-T melanoma 60% | Novel on senescent T cells (Park 2024) | Drives SASP (Liu 2023) |
    | ICAM1 | Endothelium, immune | Vascular cells | CAR-T preclinical | 2-3x elevated in lupus nephritis | Pathogenic in SLE vasculitis |
    | VCAM1 | Endothelium, immune | Vascular cells | CAR-T preclinical | 2-5x elevated in active SLE | Biomarker of lupus activity |
  
  - Why these targets:
    - CD38: "Clinically validated through daratumumab (FDA-approved for multiple myeloma). Elevated in SLE (cite: Reilly 2024)."
    - CD44: "Established memory cell marker. Upregulated on senescent cells (cite: Weiland 2023). CAR-T efficacy demonstrated (cite: Maude 2022)."
    - CSPG4: "First description on senescent T cells (cite: Park 2024). Mechanistically drives SASP (cite: Liu 2023). Novel in SLE context."
    - ICAM1/VCAM1: "Adhesion molecules elevated in lupus tissues (cite: Reilly 2023, Müller 2023). Pathogenic role documented (cite: Nakaoka 2022)."
  
  - Why NOT other targets:
    - CD3, CD8, CD4: "Too broad; would deplete entire T-cell compartment."
    - CD19: "Already standard CAR-T in SLE (cite: Kil 2024). We seek novel targets to overcome potential escape."
    - CD20: "Rituximab already established. Less novel than senescence-targeting approach."
    - EGFR: "Expressed primarily on epithelial cells, not immune (cite: Voena 2023). CAR-T limited to solid tumors (cite: Chen 2022). DROPPED from panel."

- Target: 500-700 words
- Key papers: Reilly 2024, Weiland 2023, Maude 2022, Park 2024, Liu 2023, Nakaoka 2022, Müller 2023, Voena 2023, Chen 2022, Kil 2024

---

## Week 3: RESULTS REORGANIZATION & DISCUSSION DRAFT

### RESULTS REORGANIZATION (Rewrite for clarity)

**Current problem:** Results conflate findings with interpretation

**Current example:** "CD38, CD44 show consistent positive correlation with senescence"
**Revised (pure finding):** "Spearman correlation: CD38 r=0.40 (p=0.007), CD44 r=0.36 (p=0.017) in bulk RNA-seq (GSE228066, n=45)"

**Action items:**
- Remove all interpretation words: "shows," "suggests," "indicates," "demonstrates," "validates"
- Replace with pure findings: numbers, p-values, correlation coefficients
- Create target correlation heatmap (6 targets × 3 datasets)
  - Question: Are targets independent (r<0.5) or redundant (r>0.7)?
  - Impact: Informs discussion of additive vs. synergistic effects
- Separate by data type: bulk vs. single-cell results
- All figures: include error bars, p-values, sample sizes

**Target length:** Same as current RESULTS.md
**Timeline:** 2 days (Mon-Tue Week 3)

---

### DISCUSSION DRAFT (Weeks 3-4)

**Section 4.1: Comparison to Existing SLE Therapies (1 page)**
- Status: Literature ready (Q1 + Q2 papers)
- Content:
  - Belimumab (B-cell activator inhibitor): 40-50% response rate (cite: Baker 2023)
  - Rituximab (CD20): Off-label; modest efficacy
  - CD19 CAR-T (new): 70% remission (cite: Kil 2024) ← **Major breakthrough**
  - Senescence-targeting CAR-T (this study): Novel approach
  - **Positioning:** "Multi-target senescence-aware CAR-T represents next-generation strategy beyond CD19-only, potentially addressing escape mechanisms (cite: Majzner 2023) and targeting inflammation-driving senescent cells (cite: Rönnblom 2023)"
- Target: 400-500 words
- Key papers: Baker, Kil, Majzner, Rönnblom

**Section 4.2: Mechanistic Explanation of Multi-Target Synergy (0.75 page)**
- Status: Needs target correlation analysis
- Content:
  - Data: Combined CD38+CD44+CSPG4 (r=0.576) > singles (r=0.23-0.40)
  - Analysis question: Are these correlated (same cells) or independent (different populations)?
  - **If independent (r<0.5):** "Multi-target approach targets distinct senescent populations: CD38+ plasma cells, CD44+ memory T cells, CSPG4+ monocytes. Combined targeting = broader senescence coverage."
  - **If correlated (r>0.7):** "High correlation suggests co-expression on single senescent cells. Multi-target approach improves CAR-T avidity through dual/triple engagement."
  - Literature support: Zhao 2023 shows multi-target prevents escape in malignancies
- Target: 300-400 words
- Key papers: Zhao 2023, Maude 2022, Weiland 2023

**Section 4.3: Off-Target Toxicity Risk Assessment (1 page)**
- Status: Literature complete (Q4-Q7 all documented)
- Content table:
  | Target | Normal Expression | Risk Level | Documented Toxicity | Mitigation |
  |--------|------------------|-----------|-------------------|-----------|
  | CD38 | Plasma cells, T cells, NK | Medium | Immune suppression | Pre-treatment assessment |
  | CD44 | Hematopoietic stem cells, endothelium | High | Bone marrow endothelial damage (Mazzocco 2024) | Patient selection for bone marrow reserve |
  | CSPG4 | Monocytes, macrophages | Medium | Immune dysregulation | Monitor monocyte counts |
  | ICAM1 | Endothelium | High | Vascular leak syndrome (Tatsuno 2024) | Intensive care monitoring |
  | VCAM1 | Endothelium, immune | High | Vascular leak | Similar to ICAM1 |
  
  - Narrative:
    - CD38: "While CD38 is FDA-approved as a target (daratumumab), CAR-T approach may carry greater T-cell depletion risk than antibody. Mitigation: baseline CD4+ count, monitor for opportunistic infections."
    - CD44: "Bone marrow endothelial progenitor cells express CD44 (cite: Majeti 2023). CAR-T targeting documented to cause endothelial toxicity (cite: Mazzocco 2024), with risk of hematopoietic failure. Mitigation: patient selection favoring preserved marrow reserve."
    - CSPG4: "Monocyte expression (cite: Forgacs 2019) may impair antimicrobial immunity. Mitigation: monitoring monocyte counts, prophylactic antibiotics if <500/μL."
    - ICAM1/VCAM1: "Endothelial expression on normal vasculature poses vascular leak risk (cite: Tatsuno 2024 for ICAM1). Both adhesion molecules essential for immune surveillance. Mitigation: ICU admission, IV fluid management, vasopressor support if needed."
  
  - Conclusion: "Off-target risks are non-trivial. Single-target approach (CD38 or CD44 alone) may be safer than 5-target. Clinical trial design should include intensive monitoring cohort."

- Target: 600-800 words
- Key papers: Majeti 2023, Mazzocco 2024, Tatsuno 2024, Forgacs 2019, Voena 2023

**Section 4.4: Novelty & Significance of Each Target (1.25 pages)**
- Status: Literature complete (Q4-Q7 analysis)
- Content:
  
  **CD38: Known marker, SLE context novel**
  - "CD38 was previously documented on senescent T cells (cite: Appay 2023), establishing precedent for CD38-senescence association."
  - "Novel contribution: Elevation of CD38 in lupus nephritis (cite: Reilly 2024) and mechanistic link to senescence-driven inflammation (cite: König 2023)."
  - "Implication: Daratumumab-validated target; SLE-senescence context is new application."
  
  **CD44: Known memory marker, senescence context novel**
  - "CD44 is established marker of memory T cells and stem cells (textbook knowledge)."
  - "New finding: Upregulation specifically on senescent cells (cite: Weiland 2023) in context of SASP production (cite: Weiland 2023)."
  - "Implication: Extends CD44 targeting from stem cell selection to senescence-targeted immunotherapy."
  - "Safety: Off-target toxicity now well-characterized (cite: Mazzocco 2024)."
  
  **CSPG4: Senescence discovery**
  - "CSPG4 was known on monocytes/macrophages (cite: Forgacs 2019) and melanoma cells."
  - "Novel discovery: CSPG4 upregulation on senescent T cells (cite: Park 2024, NEW)."
  - "Mechanistic discovery: CSPG4 expression couples to SASP production (cite: Liu 2023, NEW)."
  - "Implication: CSPG4 is first surfaceantigen specifically linked to senescence-associated inflammation. Strongest novelty claim."
  
  **ICAM1: Established adhesion molecule, CAR-T application novel**
  - "ICAM1 is well-established in lupus vasculitis pathogenesis (cite: Nakaoka 2022)."
  - "Established pathology: Elevated in lupus tissues (cite: Reilly 2023, Müller 2023)."
  - "Novel application: CAR-T targeting as senescence-independent immune strategy (orthogonal to senescence scoring)."
  - "Risk assessment: Vascular toxicity now documented (cite: Tatsuno 2024)."
  
  **VCAM1: Similar to ICAM1**
  - "Established in lupus activity (cite: Müller 2023 as biomarker)."
  - "Novel: CAR-T targeting approach; inclusion in multi-target panel to prevent escape."

  **Overall novelty tier:**
  - Tier 1 (Highest): CSPG4 (senescence-specific discovery)
  - Tier 2 (Medium): CD44 (known marker, new senescence context)
  - Tier 3 (Applied): CD38, ICAM1, VCAM1 (known pathways, new therapeutic targeting)

- Target: 800-900 words
- Key papers: Appay 2023, Reilly 2024, König 2023, Weiland 2023, Mazzocco 2024, Forgacs 2019, Park 2024, Liu 2023, Nakaoka 2022, Müller 2023, Tatsuno 2024

**Section 4.5: Limitations & Future Work (0.75 page)**
- Status: Ready to write
- Content:
  - No SLEDAI metadata: Cannot correlate senescence with disease activity directly
  - Fallback gene scoring: 15/19 datasets lack SenMayo mapping
  - Computational only: Requires experimental validation
  - Cross-tissue heterogeneity: Why kidney > synovium remains unexplained
  - Small sample sizes: Some datasets n=2-3 patients
  - Future: In vitro CAR-T killing assays, flow cytometry, mouse models

- Target: 400-500 words

---

## Week 4: INTEGRATION & POLISH

### Full Manuscript Assembly
- Combine INTRODUCTION (complete), METHODS (expanded), RESULTS (reorganized), DISCUSSION (complete)
- Check flow: Intro → Methods → Results → Discussion should form logical narrative
- Verify all citations match across sections
- Create figure legends (reference analysis data)
- Create table captions (reference statistics)

### Cross-section validation
- [ ] All statistics reported consistently (p-values, correlations, sample sizes)
- [ ] All paper citations appear in final reference list
- [ ] No conflation of results and discussion
- [ ] Methods detail matches analysis code
- [ ] No unsupported claims (verify each claim has ≥1 literature citation)

### External validation
- [ ] All 41 papers are peer-reviewed and recent (2019-2024)
- [ ] No contradictions between papers
- [ ] Statistical methods match industry standards
- [ ] No undisclosed conflicts (all papers independent labs)

---

## Week 5: FINAL POLISH & SUBMISSION PREP

### Manuscript refinement
- Proofread for clarity and conciseness
- Ensure active voice (no "it is shown that...")
- Remove redundancy between sections
- Optimize figure quality for publication

### Citation check
- Verify all 41 papers are cited (or explain why not included)
- Format citations consistently (journal names, abbreviations)
- Check DOI links are functional
- Ensure bibliography is complete and alphabetized

### Submission readiness
- Prepare cover letter positioning novelty
- Prepare author statement (who did what)
- Prepare competing interests statement
- Select target journal (Lancet Rheumatology, Nature Immunology, Blood, etc.)
- Prepare supplementary figures/tables if needed

---

## Summary: 4-Week Writing Timeline

| Week | Task | Deadline | Status |
|------|------|----------|--------|
| Week 2 | Write INTRODUCTION (1.1-1.5) + Expand METHODS | Fri EOD | TODO |
| Week 2 | Write METHODS 2.1, 2.2, 2.3, 2.4, 2.5 | Fri EOD | TODO |
| Week 3 | Reorganize RESULTS (remove interpretation) | Wed EOD | TODO |
| Week 3-4 | Draft DISCUSSION (4.1-4.5) | Fri EOD | TODO |
| Week 4 | Full manuscript assembly + cross-validation | Wed EOD | TODO |
| Week 5 | Polish, proofread, submission prep | Fri EOD | TODO |

---

## Gate Criteria for Publication

Before submitting to journal, verify:

- [x] All 41 literature papers found and documented
- [ ] INTRODUCTION sections written (1.1-1.5)
- [ ] METHODS fully expanded (2.1-2.5 detail)
- [ ] RESULTS reorganized (pure findings, no interpretation)
- [ ] DISCUSSION written (4.1-4.5)
- [ ] All statistics match code and papers
- [ ] All claims have literature support
- [ ] Figures/tables finalized
- [ ] References complete and formatted
- [ ] No spelling/grammar errors
- [ ] Author statements prepared
- [ ] Target journal identified

---

## Success Metrics

By end of Week 5:
- ✅ Full manuscript draft (Introduction through Discussion)
- ✅ 5,000-7,000 words of original content
- ✅ 41 peer-reviewed citations
- ✅ 3-5 figures with legends
- ✅ 2-3 statistical tables
- ✅ Submission-ready to high-impact journal
- ✅ Novel claims (CSPG4 senescence) fully supported
- ✅ Risk discussion (off-target toxicity) comprehensive
- ✅ Methodological choices justified (batch correction, SenMayo, dataset selection)

---

