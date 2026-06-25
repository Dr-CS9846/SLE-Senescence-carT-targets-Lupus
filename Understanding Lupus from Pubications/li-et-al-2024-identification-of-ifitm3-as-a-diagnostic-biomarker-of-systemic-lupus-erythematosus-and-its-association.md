

## Paper
## Lupus
## 2025, Vol. 34(1) 57–70
## © The Author(s) 2024
Article reuse guidelines:
sagepub.com/journals-permissions
## DOI: 10.1177/09612033241304454
journals.sagepub.com/home/lup
Identification of IFITM3 as a diagnostic
biomarker of systemic lupus erythematosus
and its association with disease activity based
on multi-omics and experimental
verification
## Yan Li
## 1,2,3,
## *
## 
## , Jimin Zhang
## 1,2,3,
## *, Xiaomei Liu
## 1,2,3
## , Xinwei Zhang
## 1,2,3
and Guixiu Shi
## 1,2,3
## Abstract
Background:Systemic lupus erythematosus is a clinically heterogeneous autoimmune disease that lacks reliable diagnostic
biomarkers. In our study, we aimed to identify a novel biomarker for the diagnosis and disease activity monitoring of SLE.
Methods:Bulk RNA and scRNA-seq datasets were obtained from the Gene Expression Omnibus database. In this study,
differential analysis, cell-cell communication algorithm, functional enrichment analysis, human protein map database
analysis, protein-protein interaction analysis and immune cell infiltration analysis were utilized to identify the hub genes
between SLE and healthy groups. Furthermore, clinical data from 68 SLE patients and 31 healthy controls were collected for
verification. Changes in IFITM3 levels were confirmed through quantitative real-time polymerase chain reaction, western
blotting, andflow cytometry analyses.
Result:Bioinformatic analyses showed that IFITM3 expression was significantly upregulated in peripheral monocytes from
patients with SLE. IFITM3 mRNA levels showed a significant diagnostic value for SLE, with an AUC value of 87.14%.
IFITM3 expression was associated with the systemic lupus erythematosus disease activity index, as well as C3, C4, and IgG
levels. The results of Chi-square test showed that those in the IFITM3-positive group had a higher percentage of several
clinical manifestations such as thrombocytopenia, leukopenia, low complement, and fever.
Conclusions:Thesefindings indicated an obviously increased expression of IFITM3 in peripheral blood monocytes of
patients with SLE and verified IFITM3 as a promising diagnostic marker for SLE and associated with disease activity.
## Keywords
Systemic lupus erythematosus, IFITM3, monocytes, multi-omics, disease activity
Date received: 18 May 2024; accepted: 6 November 2024
## 1
Department of Rheumatology and Clinical Immunology, The First Affiliated Hospital of Xiamen University, School of Medicine, Xiamen University,
## Xiamen, China
## 2
Xiamen Municipal Clinical Research Center for Immune Diseases, Xiamen, China
## 3
Xiamen Key Laboratory of Rheumatology and Clinical Immunology, Xiamen, China
*These authors contributed equally to this article.
Corresponding authors:
Xinwei Zhang, Department of Rheumatology and Clinical Immunology, the First Affiliated Hospital of Xiamen University, School of Medicine, Xiamen
University, No. 55, Zhenhai Road, Siming District, Xiamen, Fujian 361000, China.
## Email:zxw2021@xmu.edu.cn
Guixiu Shi, Department of Rheumatology and Clinical Immunology, the First Affiliated Hospital of Xiamen University, School of Medicine, Xiamen
University, No. 55, Zhenhai Road, Siming District, Xiamen, Fujian, 361000, China.
## Email:gshi@xmu.edu.cn

Key point
## ·
Bioinformatic analyses and molecular experiments
verified the elevated expression level of IFITM3 in
peripheral monocytes of SLE patients compared with
HC individuals.
## ·
The expression of IFITM3 was highly associated with
SLE disease activity and clinical features.
## Introduction
Systemic lupus erythematosus (SLE) is a multisystem au-
toimmune disease characterized by abnormal immune
system activity that affects multiple organs and is often
associated with a poor prognosis.
## 1–3
The clinical mani-
festations of SLE are complex and varied, which compli-
cates both diagnosis and treatment.
## 4
However, the current
SLE-related biomarkers still lack sufficient sensitivity,
specificity and predictive power for clinical application.
Although ANA tests in serum are essentially universal for
classifying patients with SLE, Pisetsky et al. reported that
up to 30% of patients with SLE screened in clinical trials for
new therapies are ANA-negative.
## 5
Serum C3 and C4 are
widely applied to assess the presence of biologically active
immune complexes, but, because of the low specificity of
C3 and C4 in diagnosing SLE, the reliability of C3 and
C4 levels as biomarkers for SLE diagnosis would be lim-
ited.
## 6
Anti-dsDNA antibodies are regarded as the important
biomarkers which are associated with SLE disease activity
and can predict the development of lupus nephritis.
## 7
## Anti-
dsDNA antibodies have a high specificity (96%) but low
diagnostic sensitivity (52%–70%) for SLE as the level of
anti-dsDNA antibodies wouldfluctuate over time.
## 8
## Con-
sequently, it is necessary to discover novel biomarkers for
SLE diagnosis and disease activity evaluation.
Type I interferon (IFN-I), particularly IFN-α, has been
demonstrated to have a crucial role in the pathogenesis of
## SLE,
## 9
which is largely produced by plasmacytoid dendritic
cell. Once produced, IFN-I interacts with the interferon-α/β
receptor (IFNAR, including subunits IFNAR1 and IF-
NAR2) expressed in most nucleated cells, and ultimately
initiates the transcription of interferon-stimulated genes
(ISGs) to generate IFN-I gene signature via JAK/ STAT
pathway,
## 10
which can cause aberrant autoimmune responses
and chronic inflammation. Moreover, genome wide asso-
ciation studies emphasized the contribution to SLE sus-
ceptibility of genes encoding molecules involved in nucleic
acid degradation and sensing as well as IFN-I signaling
pathways.
## 11
Zhao et al. found that DNA hypomethylation of
two CpG sites of IFI44 L promoter could cause the elevated
level of type-1 IFN in SLE patient, which might be helpful
in the diagnosis of SLE,
## 12
but this work did not link the
levels of IFI44 L methylation with SLE disease activity. In
addition, Shen et al. reported that four ISGs including IFI44,
USP18, RSAD2, and NRIR had good diagnostic efficacy
for identifying SLE patients according to traditional bulk
RNA-seq analyses and qRT PCR verification.
## 13
The traditional bulk RNA-seq method reflects average
gene expression but lacks single-cell resolution.
## 14
## Sepa-
rating distinct cell subsets for investigating the activities of
IFN signature could be more valuable for enriching
pathogeny and developing targeted therapy for SLE pa-
tients. Recently, single-cell RNA-seq (scRNA-seq) as an
innovative technology has been applied to study the tran-
scriptome of different cell types, which allows expression
profile of each cell type to be get rapidly.
## 15
There are many
differences in the disturbed cell subsets and proportions
between SLE and healthy controls (HCs),
## 16,17
so the
identification of changed immune cell types in SLE helps us
to understand the cellular results of the disease and establish
the appropriate diagnostic or treatment strategies.
Our study aimed to identify the molecular biomarkers for
SLE diagnosis through the integration of scRNA-seq and
bulk RNA-seq data from PBMC samples. We identified
8 cell types from the scRNA-seq datasets and revealed
alterations in several immune cell proportions between HCs
and patients with SLE. In addition, we uncovered the
differentially expressed genes (DEGs) between SLE and
HC group in different PBMC cell subsets and performed
GO and functional enrichment analyses to determine the
functional signaling pathways of DEGs. Moreover, bulk
RNA-seq data further aids in determining immune infil-
tration and hub genes, associated the predicting function of
potential biomarkers with clinical features via conducting
logistic analysis. Finally, qRT-PCR, Western blotting, and
flow cytometry were conducted to validate the bio-
informatic results.
Material and methods
Data collection
We downloaded scRNA-seq data of PBMC samples from
Gene Expression Omnibus (GEO) database. scRNA-seq data
included5SLEpatientsand5HC samples were obtained from
GSE142016, GSE162577, and GSE185857 dataset. In addi-
tion, we downloaded bulk RNA-seq of PMBCs of SLE and
HC samples from GEO database, including GSE160080 and
GSE139350. We used the GSE65391 dataset to explore the
traditional bulk RNA-seq links between clinical features and
selected potential biomarkers for SLE. GSE122459 was used
to perform weighted Gene Co-expression Network Analysis
## (WGCNA).
Human single-cell RNA sequencing analysis
Processing and preliminary analysis of scRNA-seq data from SLE
and HC group.After downloading scRNA-seq data from
58Lupus 34(1)

GEO database, atfirst, cells were excluded based on the
“Seurat”scRNA-seq analysis workflow criteria
## 18
## : (1) The
number of measured genes in each cell was less than 300.
(2) The mitochondrial contamination was more than 10%.
Thefiltered cells were selected for creating a Seurat object
and  normalized  using  the“NormalizeData”function,
3000 highly variable genes were screened employing the
“FindVariableFeatures”function. Then, the canonical cor-
rection analysis (CCA) method including the“FindInte-
grationAnchors”and“IntegrateData”functions  were
applied to remove batch effects after integrating three
scRNA-seq datasets. We obtained a total of 45,927 cells
after removing the batch effects. We then applied principal
component analysis (PCA) for dimensionality reduction,
selecting the top 50 principal components as input for the
uniform manifold approximation and projection (UMAP)
algorithm, and visualized thefirst two UMAP dimensions at
a clustering resolution of 0.5. Cell clusters were determined
using the“FindNeighbors”and“FindClusters”function and
categorized into 21 different subclusters. Next,“SingleR”
package was exploited to annotate each cell cluster to
recognize different subtypes.
## 19
“FindMarkers”function was
used to identify DEGs (|logFC| > .25) between SLE and HC
group.
Cell-cell communication analyses.R package“CellChat”was
adopted to identify and visualize cell–cell interaction of
distinct cell types under SLE and HC conditions.
## 20
## We
followed the official workflow to input the normalized count
from merged Seurat object into“CellChat”and started the
standard preprocessing steps. Then functions“identify Over
## Expressed Genes”,“identify Over Expressed Interactions”
and“project Data”with default parameters were applied to
obtain the processed data. Our work selected the“Cell-Cell
Contact”interaction from CellChatDB as referencing da-
tabase and used the precompiled human protein–protein
interactions (PPIs) as a priori network information. The
important functions including“compute CommunProb”,
“compute CommunProbPathway”and“aggregate Net”
were applied setting default parameters. Then we visualized
the count of interactions and showed the aggregated cell-cell
communication network and signaling sent from each
cell type.
Human bulk RNA sequencing analysis
Differentially  expressed  genes  identification.DEGs  from
RNA-seq werefiltered by using“DESeq2”R package,
## 21
the
“limma”package was applied to normalize and analyze the
DEGs from the microarray dataset. |log2FC| >2.0 and false
discovery rate (FDR) < 0.05 were set as the cut-off value.
Immune cell infiltration analysis.“CIBERSORT”algorithm is
commonly  used  to  perform  immune  cell  infiltration
analysis.
## 22
“CIBERSORT”R package was exploited to
calculate the proportion of 22 immune cells in all samples
from bulk RNA-seq.
## 22
The results of immune infiltration
proportion were visualized via the function of“barplot”.
Identification of the hub genes among bulk RNA-seq and scRNA-
seq datasets.Thefiltered DEGs were inputted into“Venny”
online tool (https://bioinfogp.cnb.csic.es/tools/venny/index.
html) for getting the overlapping genes among bulk RNA
seq and scRNA seq datasets. Then, PPI network of hub
genes was constructed via applying STRING (https://string-
db.org/).
## 23
Then, volcano plots were used to display the
distribution of the overlapping genes in two bulk RNA seq
datasets. In addition, the expression of IFITM3 in immune
cells at transcriptional and single-cell level was detected
using HPA database.
## 24
Weighted gene co-expression network analysis of IFITM3-low
and IFITM3-high groups.“WGCNA”method was performed
to identify gene modules related to IFITM3 expression
level. Co-expression gene modules were determined using
the“WGCNA”R package.
## 25
Atfirst, we constructed a
scatter plot of thefit index to determine an optimal soft
power and the most suitable weighting coefficientβto
establish a weighted adjacency matrix and then transformed
it into a topological overlap matrix (TOM). Modules ac-
quired using the TOM dissimilarity measure (1-TOM)
according to the hierarchical clustering tree algorithm.
Then, we calculated the module eigengene (ME) of every
module and the correlation between ME and IFITM3 ex-
pression level.
Functional enrichment analyses of significant IFITM3-related
gene modules.“ClusterProfiler”R package was applied to
conduct Gene Ontology (GO) enrichment analysis in-
cluding biological process (BP), cellular component (CC),
molecular function (MF) for significant IFITM3-related
gene modules,
## 26
the threshold was set atp< .05, and the
species was limited as Homo sapiens. Kyoto Encyclopedia
of Genes and Genomes (KEGG) is a widely used database
for systematic analyses of gene functions, which cluster
functional gene sets into different molecular mechanisms
and biological processes. We imported the gene sets into
“ClueGO”(a plug-in of“Cytoscape”software)
## 27
for the
KEGG and REACTOME pathway enrichment analyses,
p< .05 was set as a threshold.
Validation of mRNA expression of IFITM3 in
clinical samples
We collected PBMC samples of 68 SLE patients and
31 HCs from First Affiliated Hospital of Xiamen University.
The study was reviewed and approved by the Ethics
Li et al.59

Committee of the First Affiliated Hospital of Xiamen
University (KY-2019-023).
qRT-PCR was used to quantify the expression of
IFITM3. Total RNA was extracted from PBMCs using
TRIzol Reagent (ambion, USA). Reverse Transcription
System (Roche, Germany) was applied for perform reverse
transcription PCR. PCR was performed using a LightCycler
PCR cycler, qRT PCR with FastStart™Universal SYBR®
Green (ROX) (Roche, Germany) was performed. The cycle
threshold (CT) data was determined, and the mean CT was
determined from triplicate PCRs. Relative gene expression
was calculated with the equation 2
## –ΔΔCT
. The following are
primer sequences: IFITM3 (forward primer: TGCCTGGGC
TTCATAGCATT;  reserve  primer:  TCAGCACTGGGA
TGACGATG); ACTIN (forward primer: CATGTACGT
TGCTATCCAGGC; reserve primer: CTCCTTAATGTC
## ACGCACGAT).
Western blotting analysis
Total cellular proteins were extracted by RIPA (Solarbio,
China) with cOmplete protease inhibitor (Roche, Germany)
and phosphorylase inhibitor (Roche, Germany). BCA
(Thermo, USA) reagent was utilized to evaluate protein
concentration. The proteins were separated by 15% SDS
polyacrylamide gel electrophoresis (SDS-PAGE) and then
transferred onto the PVDF membrane (Millipore, Temecula,
CA, USA). The membranes containing proteins were
blocked with 5% not-fat milk at room temperature for 1h
and  the  membrane  was  incubated  with  diluted
IFITM3 polyclonal antibody (Proteintech, China) overnight
on the shaker at 4°C. After washing thrice with Tris-
buffered Saline with Tween, the membrane-containing
proteins were incubated on the shaker with the secondary
antibody for approximately 1 h at room temperature. After
cleaning the membrane, we used the ChemiDoc Imaging
Systems (Bio-Rad, USA) to detect targeted protein bands.
Validation of IFITM3 withflow cytometric analysis
PBMC samples from 5 healthy control, 5 SLE patients were
obtained from First Affiliated Hospital of Xiamen Uni-
versity. PBMC samples were incubated with conjugated
antibiotics including CD4-APC, CD8-PE-Cy™5.5, CD56-
PE-Cy™7, CD19-BV421, CD14-PE, IFITM3-FITC (Bi-
olegend, USA). For IFITM3 we used a two-step staining.
After the primary surface antigen staining, cells werefixed
withfixation  buffer  (BD,  USA)  for  20  min.  Per-
meabilization buffer (BD, USA) was then diluted at a ratio
of 1:10 with distilled water and cells were then incubated
with the diluted permeabilization buffer for 10 min. Then,
cells were incubated with the antibodies for intracellular
antigen staining, diluted in permeabilization buffer for
15 min. Data was acquired on a CytoFLEX Beckman
Coulterflow cytometer (Beckman Coulter, USA) and an-
alyzed with FlowJo V10. The expression of IFITM3 was
identified by meanfluorescence intensity (MFI).
Statistical analysis
Statistical analyses were conducted using R software (v
4.1.3), results were displayed and visualized using the R
packages. Differences between groups were analyzed by
ttest and Chi-squared test. The correlation studies were
analyzed  by  Spearman  Correlation  coefficient.  Ap
value <.05 was considered statistically significant.
## Results
Single cell clustering, cell subsets annotation and
identification of marker genes
10× scRNA-seq data of 5 SLE and 5 HC PBMC samples
were obtained from the GSE142016, GSE162577 and
GSE185857 datasets, a total of 45,927 cells were identified
after quality control. We implemented PCA analysis to
reduce technical noise in the scRNA-seq dataset. The most
appropriate number of PCs (50 PCs) was selected for
downstream analyses via computing the standard deviation
of all principal components. In addition, we applied UMAP
(a nonlinear dimensionality reduction algorithm) to visu-
alize the distribution of single-cell data, and 21 distinct
clusters were classified after PCA and UMAP analyses
(Figure 1(a)). Cell types were annotated using“SingleR”R
package and UMAP algorithm was used to visualize the cell
types after dimensionality reduction. These 21 clusters were
categorized into 8 cell types: CD4
## +
T cells, CD8
## +
T cells,
Monocytes, NK cells, B cells, dendritic cells, platelets, and
Neutrophils (Figure 1(b)). Then, we counted the frequency
of these 8 cell subclusters and revealed a higher proportion
of B cells and monocytes in SLE samples versus HC
samples (Figure 1(c)).
Differential and cell-cell communication analyses
We screened the DEGs for each cell type between the SLE
and HC group, and we identified 5921 DEGs. The top
5 significant DEGs of distinct cell types was shown in
Figure 1(d). The heatmap showed the top 5 upregulated and
downregulated DEGs of different SLE and HC PBMC
samples (Figure 1(e)). In addition, we investigated the cell-
cell communication network by computing communication
probabilities. Compared with the HC group, there were
more interactions between monocytes and B cells in the
SLE group and fewer interactions between T cells and NK
cells (Figure 1(f)).
60Lupus 34(1)

Bulk RNA-seq analysis and identification of the hub genes
Differential gene expression analysis of bulk RNA-seq
datasets identified DEGs between the SLE and HC
groups. We found 994 DEGs (p< .05 and log2FC >2 or less
than2) in GSE160080 dataset and 622 DEGs (p< .05 and
log2FC >2 or less than2) in GSE139350 dataset. Sub-
sequently, we adopted the CIBERSORT algorithm to cal-
culate the proportion of 22 immune cells in all samples. The
results demonstrated that the infiltration levels of B cells and
monocytes were increased in the SLE group compared with
HC group (Figure 2(a)). We used Venn plot to identify the
overlapping DEGs among two bulk RNA-seq datasets and
merged scRNA-seq dataset, 20 overlapping genes were
screened for later analyses (Figure 2(b)). Then, we excluded
the disconnected nodes in the network using“STRING”
tool and visualized the PPI network of the hub DEGs, in-
cluding IFIT3, IFITM3, RSAD2, S100A8, S100A12,
S100A9, EPSTI1, IFI27, and IFIT1 (Figure 2(c)). Finally,
volcano plots were utilized to exhibit the key biomarkers in
two bulk RNA-seq datasets (Figure 2(d)).
Associations between hub genes and systemic lupus
erythematosus disease activity index of SLE
We adopted correlation analyses to investigate associations
between hub genes and the SLEDAI score. The result
Figure 1.Single-cell clustering, annotation of cell subsets, and identification of marker genes. The UMAP visualization of 21 subclusters
(a). The UMAP visualization of 8 cell types (b). Bar plots showed the proportion of different cell types in each sample (c). The top
5 DEGs of each PBMC cell type between SLE and HC groups (d). The heatmap showed the top 5 upregulated and downregulated DEGs
of different SLE and HC PBMC samples (e). Cell-cell communication analysis between SLE and HC groups (f).
Li et al.61

showed that the expression levels of IFITM3, RSAD2,
S100A12, IFI27 and EPSTI1 were significantly positively
correlated with the SLEDAI score (Figure 3). Among them,
there is a strong correlation between IFITM3 and SLEDAI
score, so IFITM3 may play an important role in diagnosing
and predicting the disease activity of SLE. In addition, the
increased expression of IFITM3 in the monocytes of pa-
tients with SLE was identified by scRNA-seq transcriptome
analyses (Figure 4(a) and (b)). Finally, we used HPA da-
tabase to investigate which immune cells express IFITM3 at
transcriptional and single-cell level, and we found that
IFITM3 was highly expressed in monocytes compared with
other  immune  cells  according  to  the  HPA  dataset,
Schmiedel dataset, andflow sorted data. (Figure 4(c)).
Weighted co-expression network construction and
identification of IFITM3-related gene clusters
We applied the Pearson’s correlation coefficient to cluster
the SLE samples dataset. After removing outliers, we drew a
sample clustering tree (Supplemental Figure 1A). We then
obtained adjacency matrix and established the topological
overlap matrix (Supplemental Figure 1B). Next, 36 modules
were selected according to average hierarchical clustering
and dynamic tree clipping (Supplemental Figure 1C). Thep
value of each module less than 0.05 was selected as the
cluster highly related to the expression level of IFITM3 for
subsequent analyses.
Functional enrichment analyses of IFITM3-related
gene modules
Functional enrichment analyses including GO, KEGG, and
Reactome were performed on the IFITM3-related gene sets
to illustrate the specific biological functions and pathways.
Results of GO analysis indicated that IFITM3-related genes
might participate in the immune response-regulating sig-
naling pathway, regulation of immune effector process,
immune response-activating signaling pathway, regulation
of innate immune response, positive regulation of cytokine
production, activation of immune response (Supplemental
Figure 2A). The pathway enrichment analyses showed that
Figure 2.Bulk RNA-seq data analyses. Bar plots showed the proportion of different immune cell types in each sample (a). Venn plot
identified the overlapping DEGs among two bulk RNA-seq datasets and scRNA-seq dataset (b). PPI network of the overlapping DEGs
(c). Volcano plots exhibited the hub genes in two bulk RNA-seq datasets (d).
62Lupus 34(1)

IFITM3-related  genes  might  be  involved  in  antigen
processing-cross presentation, cytokine signaling in im-
mune system, adaptive immune system, innate immune
system, antigen processing: ubiquitination & proteasome
degradation, class I MHC mediated antigen processing &
presentation, signaling by the B Cell receptor and so on
(Supplemental Figure 2B).
Validation of the expression of IFITM3 in
clinical samples
PBMC samples of 68 patients with SLE and 31 HC were
collected to detect the expression of IFITM3. The qRT
PCR results showed that compared to the HC group, the
mRNA expression levels of IFITM3 in the PBMCs of the
SLE group were significantly increased (Figure 5(a)).
Further, the protein level of IFITM3 was significantly
increased in PBMC from patients with SLE (Figure 5(b)).
It suggests that IFITM3 in monocytes might be involved in
the development of SLE and serve as a key diagnostic
biomarker.
Evaluation and verification of the diagnostic effect of
IFITM3 on SLE
The Spearman correlation analysis was carried out to verify
the correlation between IFITM3 and clinical features. The
baseline characteristics of all samples analyzed in our study
are exhibited inTable 1. The results of correlation analysis
demonstrated that the expression of IFITM3 was signifi-
cantly  positively  correlated  with  SLEDAI  and  IgG
(Figure 5(c)), it was significantly negatively correlated with
C3, C4 (Figure 5(d) and (e)). In addition, the expression of
IFITM3 was significantly positively correlated with IgG
(Figure 5(f)). We used the ROC curves to evaluate
IFITM3 diagnostic efficiency. As shown inFigure 5(g), the
AUC value of IFITM3 was 87.14%, with sensitivity of
72.46% and specificity of 93.75%. As shown inFigure 5(h),
the ROC curve for IFITM3 demonstrates its potential as a
biomarker to stratify patients with SLEDAI >4 (high disease
activity) and SLEDAI≤4 (low disease activity). The AUC
value of IFITM3 was 88.96%, indicating excellent diag-
nostic performance. The sensitivity and specificity were
85% and 87.5%, respectively, further supporting the utility
Figure 3.Correlation analyses between hub genes and SLEDAI score.
Li et al.63

of IFITM3 as a marker for distinguishing between these two
subgroups. Chi-squared test showed that high expression of
IFITM3 was positively significantly associated with the rate
of thrombocytopenia, leukopenia, low complement, and
fever. Mean of HCs plus 2 times standard deviation was
used tofilter out the high and low IFITM3 expression
groups (Table 2). Moreover, we conductedflow cytometry
analysis to detect the expression of IFITM3 in different
PBMC subpopulations. The results showed a significantly
elevated level of IFITM3 in the monocytes of patients with
SLE compared with HC individuals (Figure 6).
## Discussion
SLE is a multisystem, heterogeneous autoimmune disease
characterized by abnormal immune system activity,
## 28
un-
derscoring the need to explore novel immune-related bio-
markers for SLE diagnosis and treatment. In this study, we
verified the elevated expression of IFITM3 in monocytes
from SLE group compared with HC group.
In addition to its role in SLE, IFITM3 has been impli-
cated in a variety of other diseases, including tumors,
autoimmune disorders, and degenerative diseases. In can-
cers, IFITM3 has been shown to promote tumor progression
by inhibiting apoptosis and promoting cell survival.
## 29
In the
context of Alzheimer’s disease, IFITM3 is involved in the
regulation ofγ-secretase, leading to the production of
β-amyloid plaques, a hallmark of the disease.
## 30
In auto-
immune diseases, IFITM3 is thought to be involved in the
regulation of immune cell function and chronic inflam-
mation.
## 29
While these associations highlight the multi-
functionality  of  IFITM3,  our  study  focuses  on  its
upregulation in SLE and its potential as a diagnostic marker.
Further research is warranted to delineate the specific
mechanisms through which IFITM3 contributes to the
pathogenesis of SLE and how it differs from its roles in
other diseases.
Wefiltered the IFITM3-related gene modules and per-
formed GO and pathway enrichment analyses to detect the
functional signaling pathways about these gene modules.
We found that IFITM3 could involve in B-cell receptor
(BCR) signaling, SLE is featured as losing B cell tolerance
and autoantibody production, specific pathways which
negatively regulate B cell signaling have been reported to be
Figure 4.The expression of IFITM3 in each cell subtype of PBMC from SLE patients and HCs. The violin plot shows the expression of
IFITM3 in each PBMC cell subset of SLE patients versus HCs based on the scRNA-seq data (a). The feature plot shows the distribution
of the expression of IFITM3 in each PBMC cell subset of SLE patients versus HCs based on the scRNA-seq data (b). Bar plots displayed
the expression of IFITM3 in different immune cells according to HPA, Schmiedel database andflow sorted data (c).
64Lupus 34(1)

impaired in some SLE patients.
## 31
In normal resting B-cells,
IFITM3 was minimally expressed and mainly localized in
endosomes. However, BCR engagement would induce
expression of IFITM3 and phosphorylation at Y20, re-
sulting in accumulation at the cell surface.
## 32
In addition, Jae
Woong Lee team reported that IFITM3-dependent ampli-
fication of PI3K signaling would play a critical role in
downstream of the BCR, it is important for the rapid ex-
pansion of B cells with high affinity to antigen.
## 33
Thus, we
consider that IFITM3 may relate to B cell tolerance losing
and autoantibody production.
In this study, we confirmed that IFITM3 expression is
significantly upregulated in patients with SLE and is
strongly correlated with disease activity and levels of serum
IgG. Based on thesefindings, IFITM3 may serve not only as
a diagnostic biomarker but also as a therapeutic target. One
study has shown that IFITM3 enhances BCR signaling,
promoting B cell activation and proliferation, which in turn
leads to autoantibody production.
## 33
Therefore, we hy-
pothesize that inhibition of IFITM3 could potentially reduce
BCR signaling activity, thereby decreasing autoantibody
generation. Moreover, inhibiting IFITM3 has shown ther-
apeutic potential in other immune-related diseases. For
instance, IFITM3 deletion has been demonstrated to at-
tenuate the antibody response after vaccination,
## 34
further
supporting the role of IFITM3 in regulating antibody
production. In the context of SLE, targeting IFITM3 with
specific inhibitors or gene-silencing techniques may help
Figure 5.Validation of the expression of IFITM3 in clinical samples. qRT PCR results showed that the mRNA expression levels of
IFITM3 in PBMCs of SLE patients compared with HCs (a). Western blotting results showed that the protein levels of IFITM3 in PBMC
samples from SLE patients compared with HCs (b). The possible correlation between the expression of IFITM3 and SLEDAI (c). The
possible correlation between the expression of IFITM3 and C3 (d). The possible correlation between the expression of IFITM3 and C4
(e). The possible correlation between the expression of IFITM3 and IgG (f). ROC curve demonstrating the diagnostic efficiency of
IFITM3 (g). ROC curve illustrating the potential of IFITM3 as a biomarker to stratify patients with SLEDAI >4 and SLEDAI≤4 (h).ttest
and Spearman correlation analyses were used to analyze data for differences. Data are representative of 3 independent experiments.
## (**p< .01; ****,p< .0001).
Li et al.65

reduce inflammation and autoantibody levels, thus ame-
liorating disease symptoms and slowing disease progres-
sion. Preclinical studies using animal models of SLE will be
critical to evaluating this therapeutic strategy.
SLE is a heterogeneous disease with a wide spectrum of
clinical manifestations, making it crucial to identify sub-
groups of patients who may respond differently to specific
treatments. There are emerging studies about a role of
endogenous production of type I IFNs in the pathogenesis
of neutropenia and lymphopenia in SLE,
## 35,36
elevated
serum levels of IFN-αhave been detected in SLE and it is
highly correlated with fever, skin rash and leucopenia.
## 36
Our study demonstrates that IFITM3 expression is sig-
nificantly correlated with key clinical features of SLE,
including fever, hematuria, proteinuria, low complement
levels,  leukopenia,  and  thrombocytopenia.  Notably,
IFITM3 expression is strongly associated with SLEDAI
scores, allowing us to stratify patients based on disease
activity. Patients with SLEDAI scores >4 (high disease
activity)   exhibit   significantly   higher   levels   of
IFITM3 expression and more severe clinical features. In
contrast, patients with SLEDAI scores≤4 (low disease
activity) show lower IFITM3 expression and milder
clinical  presentations.  Thesefindings  suggest  that
IFITM3 could serve as a biomarker to define subgroups of
SLE patients based on disease activity. Patients with high
IFITM3 expression may require more aggressive thera-
peutic strategies due to the greater severity of their clinical
manifestations. Further validation in larger patient cohorts
is necessary to confirm thesefindings and to explore the
therapeutic potential of targeting IFITM3 in different SLE
subgroups.
Monocytes play a particularly central role in the im-
mune dysregulation observed in SLE.
## 37
Their involve-
ment in antigen presentation, cytokine production, and
inflammation is widely reported in the context of SLE.
## 38
IFITM3 upregulation in monocytes has been closely
linked to their activation and inflammatory potential,
which are pivotal processes in SLE pathophysiology. In
addition, monocytes are one of the more abundant im-
mune cell populations in PBMCs,
## 39
which made them
more practical for experimental validation and data col-
lection. But it is important to recognize that IFITM3 is
also upregulated in other immune cell types, including
neutrophils and dendritic cells.
## 32,33,40
In particular, the
enhanced expression of IFITM3 in dendritic cells may
lead to enhanced presentation of self-antigens, thereby
exacerbating autoreactive T cell responses and driving
autoimmune inflammationinSLE.
## 41
Neutrophils in SLE
have been shown to produce neutrophil extracellular traps
(NETs), which can release DNA and nuclear components
thatpromoteautoantibodyproduction.
## 42
IFITM3 upregulation may lead to increased NET for-
mation. This may exacerbate autoimmunity by providing
additional autoantigens for recognition by the immune
system, leading to a vicious cycle of inflammation and
Table 1.Baseline characteristics of all subjects.
CharacteristicsPatients with SLE (n= 68)HCs (n= 31)p.Value
Age (mean ± SD)-years34.45 ± 13.3632.13 ± 6.621 0.6369
Sex (%)- female93.75%88.89%0.5347
## Height-cm161.7 ± 8.09163.1 ± 7.491 0.6268
## Weight-kg56.24 ± 11.7753.22 ± 9.148 0.4757
SLE disease duration (years), mean (SD)/median 5.92 (5.80)/5//
Renal failure (%)4.41%//
Disease activity, mean SLEDAI10.8 ± 7.95//
## SLEDAI≤4 (%)16 (25%)//
## SLEDAI >4 (%)52 (75%)//
Treatments (n)Prednisone:n= 24 hydroxychloroquine:n=30
mycophenolate:n= 6 rituximab:n= 3 Untreated:n=20
## //
Prednisone dose, mean (SD), mg/day14.43 (9.35)//
ANA positive (%)88.09%//
Anti-dsDNA antibody positive (%)42.85%//
Anti-Sm antibody positive (%)26.19%//
Anti-histone antibody positive (%)38.09%//
Anti-nucleosome antibody positive (%)55.00%//
Anti-SSA antibody positive (%)45.23%//
Anti-SSB antibody positive (%)9.52%//
Anti-Ro52 antibody positive (%)40.48%//
66Lupus 34(1)

tissue damage. Future studies should explore the specific
functions of IFITM3 in these various cell types and their
contribution to the overall immune dysregulation ob-
served in SLE.
There are several limitations in this work, as excellent
diagnostic biomarkers should be highly sensitive and
specific for a disease, IFITM3 as a potential diagnostic
biomarker only has high specificity but low in sensitivity,
so it should be combined with other ideal biomarkers
with high sensitivity in SLE diagnosis. In addition, the
cohort of SLE patients and HCs in our study was limited,
we plan to include larger numbers of patients and HCs in
Table 2.Associations between IFITM3 expression and clinicopathological characteristics of patients with SLE (n= 68) (*,p< .05).
Clinicopathological characteristicsNumber
## IFITM3
χ2p-valuePositive (42)Negative (26)
## Arthritis0.083030.7732
## Positive421131
## Negtive26620
## Thrombocytopenia4.720.0298*
## Positive421032
## Negtive26125
## Leukopenia5.8680.0154*
## Positive421428
## Negtive26224
## Hematuria3.3920.0655
## Positive421923
## Negtive26620
## Proteinuria2.8730.0901
## Positive422022
## Negtive26719
Skin lesions2.1020.1471
## Positive421527
## Negtive26521
Low complement5.2830.0215*
## Positive423111
## Negtive261214
## Fever4.7560.0292*
## Positive421923
## Negtive26521
Anti-dsDNA antibody1.7540.1854
## Positive421824
## Negtive26719
## Serositis3.2320.0722
## Positive42834
## Negtive26125
## Vasculitis0.75990.3834
## Positive42438
## Negtive26125
Oral ulcer3.2320.0722
## Positive42834
## Negtive26125
## Myositis0.71770.3969
## 42438
## 26125
## Alopecia1.0810.2985
## 42933
## 26323
Associations between IFITM3 expression and clinicopathological characteristics of patients with SLE (n= 68) cut off = mean of HC + 2 folds of SD (3.109).
Li et al.67

future studies to raise the accuracy and reliability of the
results.
## Conclusion
In conclusion, this work described the immune features of
PMBCs under SLE and HC conditions, which highlighted
the immune infiltration influences in the peripheral immune
environment in SLE. In addition, we identified and verified
the elevated expression level of IFITM3 in peripheral
monocytes of SLE patients compared with HC individuals
via bioinformatic analyses and molecular experiments.
Furthermore,  we  revealed  that  the  expression  of
IFITM3 was highly associated with SLE disease activity
and clinical features, which inferred that IFITM3 had the
potential to become a novel biomarker for SLE diagnosis
and disease activity evaluation. In summary, our work may
contribute to advances in the diagnostic and disease activity
evaluation of SLE patients.
## Acknowledgments
The  authors  sincerely  appreciate  National  Natural  Science
Foundation of China forfinancially supporting this research. We
thank Yuechi Sun for editing the manuscript, Yan He and Hongyan
Qian for clinical data analysis.
## Authors’contributions
Yan Li and Jimin Zhang contributed equally. YL and JM con-
tributed to write the manuscript and perform experiments. GS and
Figure 6.Flow cytometry analysis was applied to detect the expression of IFITM3 in different cell subsets of PBMC. Representative
graph and MFI of IFITM3 expression on CD14
## +
monocytes (a). Representative graph and MFI of IFITM3 expression on CD19
## +
B cells
(b). Representative graph and MFI of IFITM3 expression on CD56
## +
NK cells (c). Representative graph and MFI of IFITM3 expression on
## CD4
## +
T cells (d). Representative graph and MFI of IFITM3 expression on CD8
## +
T cells (e).ttest analysis was used to analyze data for
statistic differences (n= 5). Data are representative of 3 independent experiments. PBMC from different individuals were used for each
independent experiment. (**p< .01; ns, not significant).
68Lupus 34(1)

XW reviewed and edited the manuscript. XM contributed to
clinical sample collection. All authors reviewed the manuscript.
Declaration of conflicting interests
The author(s) declared no potential conflicts of interest with re-
spect to the research, authorship, and/or publication of this article.
## Funding
The author(s) disclosed receipt of the followingfinancial support
for the research, authorship, and/or publication of this article: This
work was supported by grants from the Natural Science Foun-
dation of China (82171779, 82371802, G.S., 82101841, X.Z.),
Scientific  and  Technological  Projects  of  Xiamen  City
## (2022XMSLCYX01, G.S.).
## Ethical Statement
## Ethical Approval
The study was reviewed and approved by the Ethics Committee of
the First Affiliated Hospital of Xiamen University (KY-2019-023).
## Informed Consent
All the participants have given approval for publication.
ORCID iD
## Yan Li
## 
https://orcid.org/0000-0003-3020-6424
## Supplemental Material
Supplemental Material for this article is available online.
## References
- Ruiz-Irastorza G, Khamashta MA, Castellino G, et al. Sys-
temic lupus erythematosus.Lancet (London, England)2001;
## 357: 1027–1032.
- Barber MRW, Drenkard C, Falasinnu T, et al. Global epi-
demiology  of  systemic  lupus  erythematosus.Nat   Rev
## Rheumatol2021; 17: 515–532.
- Aw YTV, Whiley PJ, Lorenzo AM, et al. Immunophenotyping
identifies distinct cellular signatures for systemic lupus er-
ythematosus and lupus nephritis.Rheumatology  &  Autoim-
munity2023; 3: 15–25.
- Mohamed A, Chen Y, Wu H, et al. Therapeutic advances in
the treatment of SLE.Int Immunopharm2019; 72: 218–223.
- Pisetsky DS, Rovin BH and Lipsky PE. New perspectives in
rheumatology: biomarkers as entry criteria for clinical trials of
new therapies for systemic lupus erythematosus: the example
of antinuclear antibodies and anti-DNA.Arthritis Rheumatol
## 2017; 69: 487–493.
- Ghiggeri GM, D’Alessandro M, Bartolomeo D, et al. An
update on antibodies to necleosome components as bio-
markers of sistemic lupus erythematosus and of lupusflares.
## Int J Mol Sci2019; 20: 5799.
- Wang Y, Xiao S, Xia Y, et al. The therapeutic strategies for
SLE by targeting anti-dsDNA antibodies.Clin Rev Allergy
## Immunol2022; 63: 152–165.
- Petri M, Orbai AM, Alarcón GS, et al. Derivation and val-
idation of the Systemic Lupus International Collaborating
Clinics classification criteria for systemic lupus eryth-
ematosus.Arthritis Rheum2012; 64: 2677–2686.
- Psarras A, Wittmann M and Vital EM. Emerging concepts of
type I interferons in SLE pathogenesis and therapy.Nat Rev
## Rheumatol2022; 18: 575–590.
- Jiang J, Zhao M, Chang C, et al. Type I interferons in the
pathogenesis and treatment of autoimmune diseases.Clin Rev
## Allergy Immunol2020; 59: 248–272.
- Langefeld CD, Ainsworth HC, Cunninghame Graham DS,
et al. Transancestral mapping and genetic load in systemic
lupus erythematosus.Nat Commun2017; 8: 16021.
- Zhao M, Zhou Y, Zhu B, et al. IFI44L promoter methylation
as a blood biomarker for systemic lupus erythematosus.Ann
## Rheum Dis2016; 75: 1998–2006.
- Shen M, Duan C, Xie C, et al. Identification of key interferon-
stimulated genes for indicatingthe condition of patients with
systemic lupus erythematosus.Front Immunol2022; 13: 962393.
- Bolton C, Smillie CS, Pandey S, et al. An integrated tax-
onomy for monogenic inflammatory bowel disease.Gas-
troenterology
## 2022; 162: 859–876.
- Kharchenko PV. The triumphs and limitations of computa-
tional methods for scRNA-seq.Nat  Methods2021; 18:
## 723–732.
- Wang Y, Xie X, Zhang C, et al. Rheumatoid arthritis, systemic
lupus erythematosus and primary Sj
## ̈
ogren’s syndrome shared
megakaryocyte expansion in peripheral blood.Ann  Rheum
## Dis2022; 81: 379–385.
- Ma Y, Chen J, Wang T, et al. Accurate machine learning
model to diagnose chronic autoimmune diseases utilizing
information from B cells and monocytes.Front  Immunol
## 2022; 13: 870531.
- Hao Y, Hao S, Andersen-Nissen E, et al. Integrated analysis of
multimodal single-cell data.Cell2021; 184: 3573–3587.
- Aran D, Looney AP, Liu L, et al. Reference-based analysis of
lung single-cell sequencing reveals a transitional profibrotic
macrophage.Nat Immunol2019; 20: 163–172.
- Jin S, Guerrero-Juarez CF, Zhang L, et al. Inference and
analysis of cell-cell communication using CellChat.Nat
## Commun2021; 12: 1088.
- Love MI, Huber W and Anders S. Moderated estimation of
fold change and dispersion for RNA-seq data with DESeq2.
## Genome Biol2014; 15: 550.
- Newman AM, Liu CL, Green MR, et al. Robust enumeration
of cell subsets from tissue expression profiles.Nat Methods
## 2015; 12: 453–457.
- Szklarczyk D, Gable AL, Nastou KC, et al. The STRING
database in 2021: customizable protein-protein networks, and
functional   characterization   of   user-uploaded   gene/
measurement sets.Nucleic Acids Res2021; 49: D605–D612.
Li et al.69

## 24. Karlsson M, Zhang C, M
## ́
ear L, et al. A single-cell type
transcriptomics map of human tissues.Sci  Adv2021; 7:
eabh2169.
- Langfelder P and Horvath S. WGCNA: an R package for
weighted correlation network analysis.BMC Bioinf2008; 9:
## 559.
- Wu T, Hu E, Xu S, et al. clusterProfiler 4.0: a universal
enrichment tool for interpreting omics data.Innovation2021;
## 2: 100141.
- Bindea G, Mlecnik B, Hackl H, et al. ClueGO: a Cytoscape
plug-in to decipher functionally grouped gene ontology and
pathway annotation networks.Bioinformatics2009; 25:
## 1091–1093.
- Zhao X, Wang S, Wang S, et al. mTOR signaling: a pivotal
player in Treg cell dysfunction in systemic lupus eryth-
ematosus.Clin Immunol2022; 245: 109153.
- Gómez-Herranz M, Taylor J and Sloan RD. IFITM proteins:
understanding their diverse roles in viral infection, cancer,
and immunity.J Biol Chem2023; 299: 102741.
- Hur JY, Frost GR, Wu X, et al. The innate immunity protein
IFITM3 modulatesγ-secretase in Alzheimer’s disease.Nature
## 2020; 586: 735–740.
- Jenks SA and Sanz I. Altered B cell receptor signaling in
human systemic lupus erythematosus.Autoimmun Rev2009;
## 8: 209–213.
- Clement M, Forbester JL, Marsden M, et al. IFITM3 restricts
virus-induced inflammatory cytokine production by limiting
Nogo-B mediated TLR responses.Nat Commun2022; 13:
## 5294.
- Lee J, Robinson ME, Ma N, et al. IFITM3 functions as a
PIP3 scaffold to amplify PI3K signalling in B cells.Nature
## 2020; 588: 491–497.
- Lei N, Li Y, Sun Q, et al. IFITM3 affects the level of antibody
response after influenza vaccination.Emerg  Microb  Infect
## 2020; 9: 976–987.
## 35. R
## ̈
onnblom L. Potential role of IFNαin adult lupus.Arthritis
Res Ther2010; 12(Suppl 1): S3.
- Hepburn AL, Narat S and Mason JC. The management of
peripheral blood cytopenias in systemic lupus erythematosus.
## Rheumatology2010; 49: 2243–2254.
## 37. Ferret
## ́
e-Bonastre AG, Mart
## ́
ınez-Gallo M, Morante-Palacios
O, et al. Disease activity drives divergent epigenetic and
transcriptomic reprogramming of monocyte subpopulations
in systemic lupus erythematosus.Ann Rheum Dis2024; 83:
## 865–878.
- Katsiari CG, Liossis SN and S
fikakis PP. The pathophysio-
logic role of monocytes and macrophages in systemic lupus
erythematosus: a reappraisal.Semin  Arthritis Rheum2010;
## 39: 491–503.
- Perez RK, Gordon MG, Subramaniam M, et al. Single-cell
RNA-seq reveals cell type-specific molecular and genetic
associations to lupus.Science (New York, N.Y.)2022; 376:
eabf1970.
- Liu X, Zhang W, Han Y, et al. FOXP3(+) regulatory T cell
perturbation mediated by the IFNγ-STAT1-IFITM3 feedback
loop is essential for anti-tumor immunity.Nat Commun2024;
## 15: 122.
- Liu J, Zhang X and Cao X. Dendritic cells in systemic lupus
erythematosus: from pathogenesis to therapeutic applications.
## J Autoimmun2022; 132: 102856.
## 42. D
## ̈
orner T. SLE in 2011: deciphering the role of NETs and
networks in SLE.Nat Rev Rheumatol2012; 8: 68–70.
## Appendix
## Abbreviations
SLE  Systemic lupus erythematosus
HC  Healthy control
qRT PCR  Quantitative real-time polymerase
chain reaction
scRNA  Single-cell RNA
DEGs  Differentially expressed genes
GEO  Gene Expression Omnibus
CCA  Canonical correction analysis
PCA  Principal component analysis
UMAP  Uniform manifold approximation and
projection
PPIs  Protein–protein interactions
FDR  False discovery rate
SLEDAI  Systemic lupus erythematosus disease
activity index
CT  Cycle threshold
MFI  Meanfluorescence intensity
BP  Biological progress
CC  Cellular component
MF  Molecular function
TLR  Toll-like receptor
IFITMs  Interferon-induced transmembrane
proteins
IFNs Interferons
JAK  Janus kinase
STAT  Signal transducer and activator of
transcription
ISGs  IFN-stimulated genes
WGCNA  Weighted gene co-expression network
analysis
GO  Gene ontology
KEGG  Kyoto encyclopedia of genes and
genomes
70Lupus 34(1)