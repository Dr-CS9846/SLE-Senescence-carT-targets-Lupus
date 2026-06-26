# Literature Research Repository

**Purpose:** Systematic, reproducible literature research for all 10 critical research questions (Q1-Q10) that support manuscript writing.

**Maintained by:** [Your name]  
**Last updated:** 2026-06-26

---

## Overview

This directory contains detailed literature research tracking for each of the 10 critical research questions. Each question has its own `.md` file with:

- **Search queries** used (PubMed, Clinical Trials.gov, Google Scholar)
- **Papers found** (title, authors, year, DOI, link)
- **Acceptance criteria** (what counts as "question answered")
- **Key findings** (extracted from papers)
- **Critical papers** (which papers are essential for each section)
- **To-do list** (next searches to run)

---

## Master Question Index

| Q # | Question | Status | Papers Found | For Sections | Priority |
|-----|----------|--------|--------------|--------------|----------|
| Q1 | SLE Epidemiology & Burden | [ ] NOT STARTED | 0/5+ | Intro 1.1 | HIGH |
| Q2 | CAR-T Landscape | [ ] NOT STARTED | 0/4+ | Intro 1.3 | HIGH |
| Q3 | Senescence in Autoimmunity | [ ] NOT STARTED | 0/5+ | Intro 1.2 | HIGH |
| Q4 | CD38 on Senescent Cells | [ ] NOT STARTED | 0/4+ | Discussion 4.4 | MEDIUM |
| Q5 | CD44 on Senescent Cells | [ ] NOT STARTED | 0/4+ | Discussion 4.4 | MEDIUM |
| **Q6** | **CSPG4 on Immune Cells** | [ ] **CRITICAL** | 0/5+ | **Discussion 4.4** | **CRITICAL** |
| Q7 | ICAM1 & VCAM1 in Lupus | [ ] NOT STARTED | 0/4+ | Discussion 4.3 | MEDIUM |
| Q8 | EGFR as CAR-T Target | [ ] NOT STARTED | 0/3+ | Methods 2.5 | LOW |
| Q9 | SenMayo Panel Validation | [ ] NOT STARTED | 0/5+ | Methods 2.5 | MEDIUM |
| Q10 | Batch Correction Methods | [ ] NOT STARTED | 0/4+ | Methods 2.2 | MEDIUM |

---

## How to Use This Repository

### Phase 1: Research (Week 1)

For each question:

1. **Open the Q file** (e.g., `Q1_SLE_Epidemiology_Burden.md`)
2. **Copy PubMed search queries** into PubMed
3. **Save URLs** of relevant papers into the file
4. **Read papers** and extract key findings
5. **Fill in acceptance criteria** as you go
6. **Check off** when all criteria are met
7. **Update status** from `[ ] NOT STARTED` → `[ ] IN PROGRESS` → `[ ] COMPLETE`

### Phase 2: Writing (Weeks 2-5)

For each manuscript section:

1. **Check dependencies** in `MASTER CHECKLIST.md`
2. **Verify required Q's are COMPLETE**
3. **Use papers from Q files** as citations
4. **Reference key findings** from summary sections

### Ongoing: Updates

After manuscript sections are written:

1. **Link back** from sections to Q files: "See [Q1](Q1_SLE_Epidemiology_Burden.md) for epidemiology foundation"
2. **Update status** if new papers found
3. **Add notes** on which papers were most useful
4. **Version-control** all changes

---

## File Structure

```
LITERATURE_RESEARCH/
├── README.md (this file)
├── MASTER_PROGRESS.md (overall tracking)
├── Q1_SLE_Epidemiology_Burden.md
├── Q2_CAR_T_Landscape.md
├── Q3_Senescence_in_Autoimmunity.md
├── Q4_CD38_on_Senescent_Cells.md
├── Q5_CD44_on_Senescent_Cells.md
├── Q6_CSPG4_on_Immune_Cells.md (CRITICAL PRIORITY)
├── Q7_ICAM1_VCAM1_in_Lupus.md
├── Q8_EGFR_as_CAR_T_Target.md
├── Q9_SenMayo_Validation.md
└── Q10_Batch_Correction_Methods.md
```

---

## Citation Format

All papers found in these Q files should be cited in the final manuscript. Format:

```
Author A, Author B (Year). "Title of Paper." Journal. DOI: https://doi.org/xxxxx
```

Example:
```
Saul D, Chambers JE, et al. (2022). "A senescence gene signature (SenMayo) predicts immune-oncology response." Nature Aging. DOI: https://doi.org/10.1038/s43587-022-00331-2
```

---

## Progress Tracking

### Week 1 Target: Complete All Q1-Q10

```
Target: 50+ papers total found
├─ Q1-Q3: Foundation questions (epidemiology, pathogenesis) - HIGH PRIORITY
├─ Q4-Q7: Target validation questions - MEDIUM PRIORITY
├─ Q6: CSPG4 novelty - CRITICAL BLOCKER
├─ Q8-Q10: Methodological justification - LOWER PRIORITY
```

### Acceptance Criteria

Each Q is **COMPLETE** when **ALL** acceptance criteria are checked off.

**Blocking gate:** Cannot start writing Introduction until Q1-Q3 are COMPLETE.  
**Blocking gate:** Cannot start writing Discussion until Q4-Q7 are COMPLETE.  
**Blocking gate:** Cannot start writing Methods until Q8-Q10 are COMPLETE.  
**CRITICAL BLOCKER:** Q6 (CSPG4 novelty) must be answered before Discussion 4.4 novelty claims.

---

## Version History

| Date | Event | Researcher |
|------|-------|-----------|
| 2026-06-26 | Created Q1-Q10 templates | [Your name] |
| [DATE] | Completed Q1 research | |
| [DATE] | Completed Q2-Q10 research | |
| [DATE] | Final review and validation | |

---

## Notes

- **Parallel searching encouraged**: You can work on multiple Q's simultaneously
- **Link papers back to code**: If you find a paper that refutes a finding, update analysis files
- **Iterative updates**: These Q files will grow over weeks 1-5; that's normal
- **Transparency**: Git will track all changes, showing exactly when each paper was added

---

## Quick Links to Sections

**Critical Priority (START HERE):**
- [Q6: CSPG4 on Immune Cells](Q6_CSPG4_on_Immune_Cells.md) ⚠️ BLOCKS DISCUSSION

**Foundation Questions (HIGH PRIORITY):**
- [Q1: SLE Epidemiology & Burden](Q1_SLE_Epidemiology_Burden.md)
- [Q2: CAR-T Landscape](Q2_CAR_T_Landscape.md)
- [Q3: Senescence in Autoimmunity](Q3_Senescence_in_Autoimmunity.md)

**Target Validation (MEDIUM PRIORITY):**
- [Q4: CD38 on Senescent Cells](Q4_CD38_on_Senescent_Cells.md)
- [Q5: CD44 on Senescent Cells](Q5_CD44_on_Senescent_Cells.md)
- [Q7: ICAM1 & VCAM1 in Lupus](Q7_ICAM1_VCAM1_in_Lupus.md)

**Methods Justification (MEDIUM-LOW PRIORITY):**
- [Q8: EGFR as CAR-T Target](Q8_EGFR_as_CAR_T_Target.md)
- [Q9: SenMayo Validation](Q9_SenMayo_Validation.md)
- [Q10: Batch Correction Methods](Q10_Batch_Correction_Methods.md)

