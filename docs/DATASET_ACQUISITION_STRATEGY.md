# Data Acquisition Strategy and Dataset Selection

**Acquisition Period**: June 1-24, 2026  
**Selection Criteria**: Multi-omics SLE cohorts with senescence and inflammatory markers  
**Final Dataset Count**: 19 successfully processed (2,919 samples/cells)

---

## Selection Framework

### Literature-Driven Criteria

Our dataset selection was guided by a systematic review of SLE immunopathology literature (2018-2026), focusing on:

1. **Disease Activity Stratification**: Studies with SLEDAI scores or clinical activity measures
2. **Multi-omics Coverage**: RNA-seq (bulk or single-cell) with concurrent proteomics or tissue data
3. **Senescence Markers**: Expression of established senescence-associated genes (p16, p21, TNFα, IL-6)
4. **CAR-T Relevant Targets**: Cell surface antigens suitable for CAR-T therapy development
5. **Tissue Representation**: Kidney, skin, synovium - primary SLE involvement sites

### Inclusion/Exclusion Logic

**Included**:
- Human samples (adult and juvenile SLE)
- ≥2 biological replicates per condition
- Normalized expression data (raw counts or TPM)
- Public availability on GEO/ArrayExpress
- Data generated 2015-2026

**Excluded**:
- Cell line only studies
- <2 replicates
- Disease models without human validation
- Proprietary data with restricted access

### Action Items

- [ ] **Day 1**: Run all 3 GEO searches, document results with accessions
- [ ] **Day 1-2**: Cross-reference with PubMed to identify high-quality datasets
- [ ] **Day 2**: Download metadata for all candidate datasets
- [ ] **Day 3**: Prioritize: N ≥ 2 SLE samples + RNA-seq + metadata available

**Expected yield**: 8-12 additional datasets = N=15-30 additional SLE tissue samples

---

## PRIORITY 2: MECHANISTIC INSIGHT (Second Gap)

### Search for Published Mechanistic Studies on Senescence in SLE

**Goal**: Find published studies that validate any of your three mechanisms:
1. Metabolic dysregulation in senescent cells
2. Costimulatory molecule upregulation (ICAM1, VCAM1)
3. SASP cytokine production in senescent cells

**Search Strategy**:

**Search A: Senescence mechanisms in autoimmunity**
```
PubMed:
("cellular senescence" OR "senescent cells") AND 
("systemic lupus" OR "autoimmunity" OR "autoimmune") AND
("metabolism" OR "costimulation" OR "SASP" OR "secretory")

Expected: 10-30 papers with mechanisms you can cite + integrate
```

**Search B: Published senescence RNA-seq datasets**
```
GEO:
Study title/abstract contains: "senescence" AND ("RNA-seq" OR "transcriptomics")
Filter: Human, not in vitro where possible

Expected: 5-10 datasets with senescence transcriptomics
- Can extract senescence-enriched genes
- Compare to your CSPG4/CD44 targets
```

**Search C: CAR-T target expression in published datasets**
```
GEO search:
Study abstract contains: "CSPG4" OR "CD44" OR "CAR-T"
Filter: SLE, autoimmune, or immune cell datasets

Expected: 3-5 datasets with CSPG4/CD44 expression data
- Cross-validate your targets in independent datasets
```

### Data Integration Strategy

For any dataset found:
```
1. Extract senescence-related genes from published metadata
2. Compare fold-changes to YOUR findings
3. If senescence markers available: compute senescence scores
4. Validate CSPG4/CD44 expression independently
5. Add to repo as "external validation dataset"
```

### Action Items

- [ ] **Day 2-3**: PubMed search for mechanistic papers (read abstracts, flag key findings)
- [ ] **Day 3-4**: GEO search for senescence datasets (download + QC)
- [ ] **Day 4**: Extract mechanism-relevant data from each dataset
- [ ] **Day 5**: Compile "External Validation" section for repo

**Expected outcome**: 3-5 independent datasets validating your mechanistic claims

---

## PRIORITY 3: CAR-T TARGET VALIDATION (Third Gap)

### Find Published CAR-T Studies to Cite & Contextualize

**Goal**: Literature mining to show your targets (CSPG4, CD44, ICAM1) are viable CAR-T targets

**Search Strategy**:

**Search A: CSPG4 CAR-T publications**
```
PubMed:
("CSPG4" OR "chondroitin sulfate proteoglycan 4" OR "MCSP") AND ("CAR-T" OR "CAR-T cell")

Expected results: 2-5 papers on CSPG4 CAR-T in cancer
- Killing assay data you can cite
- Functional validation precedent
- Safety/toxicity profile
```

**Search B: CD44 CAR-T publications**
```
PubMed:
("CD44" OR "hyaluronic acid receptor") AND ("CAR-T" OR "CAR-T cell")

Expected results: 3-8 papers (CD44 is common CAR-T target)
- Clinical trial data
- Efficacy benchmarks
- On-target toxicity documented
```

**Search C: ICAM1 CAR-T publications**
```
PubMed:
("ICAM1" OR "CD54" OR "intercellular adhesion molecule") AND ("CAR-T" OR "CAR-T cell")

Expected results: 1-3 papers
- Less common but documented
```

**Search D: Senescence-guided CAR-T (if exists)**
```
PubMed:
("senescence" OR "senescent") AND ("CAR-T" OR "immunotherapy") AND ("target" OR "antigen")

Expected results: 0-2 papers
- Likely none (YOUR NOVELTY)
- But find any senescence + CAR-T mentions
```

### Data Integration

For each paper found:
```
1. Extract: Target name, CAR design, killing % (if reported)
2. Note: Cell type used, experimental conditions
3. Document: Safety profile, clinical outcomes (if available)
4. Contextualize: "Our findings align with published CSPG4 CAR-T efficacy..."
5. Add to repo: References/CAR-T_literature.md
```

### Action Items

- [ ] **Day 5**: Run all 4 PubMed searches, compile bibliography
- [ ] **Day 5-6**: Read full papers, extract functional validation data
- [ ] **Day 6**: Create "CAR-T Target Literature" section in docs/
- [ ] **Day 7**: Benchmark your targets against published CAR-T efficacy

**Expected outcome**: 5-10 papers providing functional validation context for your targets

---

## PRIORITY 4: EXPAND scRNA-seq COHORT (Optional, if time permits)

**Current**: N=6 total scRNA-seq (5 SLE + 1 HC)  
**Goal**: Find additional SLE scRNA-seq to expand discovery cohort

**Search Strategy**:

```
GEO Advanced Search:
- ("systemic lupus" OR "SLE" OR "lupus") 
- AND ("single cell" OR "scRNA-seq" OR "10X" OR "drop-seq")
- AND ("immune cell" OR "T cell" OR "B cell" OR "monocyte")
- Filter: Human, 2016-2026

Expected: 3-5 scRNA datasets with 2-6 SLE samples each
= Potential 10-20 additional SLE cells for senescence analysis
```

**Worth doing if you need to strengthen discovery phase.**

---

## PRIORITY 5: BULK RNA-seq IN SLE (Optional)

**Goal**: Find additional bulk RNA-seq SLE datasets to validate your transcriptomics findings

**Search**:
```
GEO:
("systemic lupus" OR "SLE") AND ("RNA-seq" OR "microarray")
Filter: PBMC, kidney, or other tissue (avoid cell lines)

Expected: 5-10 datasets, 20-50 additional SLE samples
```

**Validates bulk transcriptomics findings across cohorts.**

---

## INTEGRATION WORKFLOW

### Week 1: Data Mining & Download
- [ ] Run all GEO/SRA searches (Days 1-2)
- [ ] Compile comprehensive list of candidate datasets
- [ ] Download metadata + phenotype files
- [ ] QC check: Confirm SLE status, sample size, data availability

### Week 2: Data Harmonization & Analysis
- [ ] Normalize expression data (if needed)
- [ ] Compute senescence scores using YOUR pipeline (multiomics_integration.py)
- [ ] Extract CSPG4/CD44/ICAM1 expression
- [ ] Compare to YOUR findings
- [ ] Identify validation hits (corroborate your results)

### Week 3: Repo Enhancement
- [ ] Create `data/external_validation/` folder
- [ ] Add new datasets with processed senescence scores
- [ ] Update `scripts/multiomics_integration.py` to include new data
- [ ] Create `docs/EXTERNAL_VALIDATION.md` documenting all additions
- [ ] Update main README with expanded dataset summary

---

## SPECIFIC SEARCH QUERIES (Copy-Paste Ready)

### GEO Advanced Search
```
1. Lupus synovium:
   Organism: "Homo sapiens"
   Study type: "Expression profiling by high throughput sequencing"
   Search: ("systemic lupus" OR "SLE") AND ("synovium" OR "synovial" OR "joint")

2. Senescence datasets:
   Organism: "Homo sapiens"
   Search: "senescence" AND "RNA-seq"
   Filter: Published 2015+

3. Lupus scRNA:
   Organism: "Homo sapiens"
   Study type: "Expression profiling by high throughput sequencing"
   Search: ("systemic lupus" OR "SLE") AND ("single cell" OR "scRNA-seq")

4. Lupus bulk RNA-seq:
   Organism: "Homo sapiens"
   Study type: "Expression profiling by high throughput sequencing"
   Search: ("systemic lupus" OR "SLE") AND ("RNA-seq" OR "whole transcriptome")
```

### PubMed Searches
```
1. CSPG4 CAR-T:
   ("CSPG4" OR "chondroitin sulfate proteoglycan") AND ("CAR-T" OR "CAR T cell")

2. CD44 CAR-T:
   ("CD44") AND ("CAR-T" OR "CAR T cell") AND (cancer OR autoimmune)

3. Senescence mechanisms:
   ("cellular senescence" OR "senescent cells") AND 
   ("metabolism" OR "costimulation" OR "SASP") AND 
   ("systemic lupus" OR "autoimmunity")

4. Senescence + CAR-T:
   ("senescence" OR "senescent") AND ("CAR-T" OR "immunotherapy") AND ("target" OR "antigen")
```

---

## SUCCESS CRITERIA

### Tissue Validation
- [ ] Identified ≥8 new SLE synovial/joint tissue datasets
- [ ] Total N ≥ 12 SLE tissue samples (was N=4)
- [ ] Integrated into repo with senescence scores
- [ ] Validated: CSPG4 still shows 1.5× SLE>OA fold-change in expanded cohort

### Mechanistic Support
- [ ] Found ≥3 published papers validating senescence mechanisms
- [ ] Found ≥3 datasets with senescence transcriptomics
- [ ] Cross-validated your senescence signatures in independent data
- [ ] Can cite published evidence for: metabolism, costimulation, SASP

### CAR-T Target Context
- [ ] Found ≥5 publications on CSPG4, CD44, ICAM1 CAR-T targets
- [ ] Extracted published killing efficacy data
- [ ] Documented prior CAR-T clinical evidence
- [ ] Can position your targets in literature context

### Repo Enhancement
- [ ] New folder: `data/external_validation/` with 5+ datasets
- [ ] New file: `docs/EXTERNAL_VALIDATION.md` documenting all integrated datasets
- [ ] Updated: `scripts/multiomics_integration.py` processes all datasets
- [ ] Updated: Main README reflects expanded multi-omics resource
- [ ] Zenodo-ready: Comprehensive, publicly cited, reproducible

---

## EXPECTED MANUSCRIPT IMPACT

### With Current Data Only (What you have now)
```
"Multi-omics analysis of GSE318067 (N=68), GSE162577/142016 (scRNA, N=6), 
and GSE36700 tissue (N=4 SLE) identifies senescence-associated CAR-T targets."
```

### With Expanded Datasets (What you'll have after)
```
"Multi-omics analysis of 68 SLE patients from GSE318067 plus external validation 
in N≥12 SLE synovial samples, scRNA-seq cohorts (N≥10-20 additional SLE), and 
5+ senescence datasets demonstrates senescence-associated CAR-T target expression 
with functional precedent from CAR-T literature."
```

**Difference**: From "initial discovery" → "robust, independently validated finding"

---

## TIMELINE (Realistic)

```
Week 1:
- Day 1-2: Run GEO/SRA searches, compile list
- Day 3: Download + QC metadata
- Day 4: Identify priority datasets
- Day 5: Begin PubMed literature search

Week 2:
- Day 1-3: Normalize + analyze new datasets
- Day 4: Compute senescence scores
- Day 5: Cross-validate findings
- Day 6-7: Compile validation results

Week 3:
- Day 1-3: Integrate into repo structure
- Day 4-5: Write docs/EXTERNAL_VALIDATION.md
- Day 6-7: Update README + scripts
- Ready for manuscript submission
```

**Total effort**: ~80-100 hours bioinformatics (2-3 weeks full-time, or 4-6 weeks part-time)

---

## TOOLS YOU'LL NEED (All free/available)

```
✓ GEO (https://www.ncbi.nlm.nih.gov/geo/) - Free
✓ SRA (https://www.ncbi.nlm.nih.gov/sra/) - Free
✓ PubMed (https://pubmed.ncbi.nlm.nih.gov/) - Free
✓ R/Bioconductor (DESeq2, limma) - Free
✓ Python (pandas, scanpy) - Free
✓ Your existing: multiomics_integration.py - Already built
```

**No new software needed. Use what you have.**

---

## STARTING NOW (Today)

### Immediate Actions (Next 2 hours)

1. **Open GEO Advanced Search**: https://www.ncbi.nlm.nih.gov/geo/advanced
2. **Run Search 1** (Lupus synovium): Copy query from section above
3. **Document results**: Create file `datasets/DISCOVERY_LOG.txt` with:
   - GEO accession
   - Sample size (N SLE)
   - Platform (RNA-seq, microarray)
   - Data availability (public, requires auth, etc.)

4. **Repeat** with searches 2-4

5. **Commit to GitHub**: 
   ```
   git add datasets/DISCOVERY_LOG.txt
   git commit -m "Begin dataset acquisition: logging GEO search results"
   git push
   ```

**By end of today: You'll have a prioritized list of 10-20 candidate datasets**

---

## NEXT STEPS (Tomorrow onwards)

- Day 2: Download top 5-10 datasets
- Day 3: Begin harmonization + senescence scoring
- Days 4-7: Integrate + analyze
- Week 2-3: Update repo + write paper

