# PREMIX
Annotated code with expected input and output for analyses of metagenomic data from human samples with or without paired genomic data from cultured isolates. We use the genomic and metagenomic analyses from the paper **Randomized trial: Fecal microbiota transplant promotes reduction of antimicrobial resistance by strain replacement** as a practical example. The primary motivation is to support the reproducibility of, and clarify steps in, the analyses and visualizations from this study.

### Background
Apply next-generation sequencing (NGS) analytic tools to genomes from clinical isolates, patient-associated, and environmental-associated metagenomes using workflows to estimate changes over time.  Workflow was developed in context of two fecal microbiota transplant clinical trials.

### Overview
- specify file paths
  - suggested file naming convention, workarounds
  - suggested scripts for renaming files obtained from Illumina sequencers
- dependencies 
  - hardware
  - software
- environment-specific applications
  - single (server) node vs cluster environments

---

#### A: Isolates 
- QC
  - [kneaddata] (wraps [trimmomatic] & [Bowtie2] decontamination)
- Assembly [SPAdes]
- Taxonomy
  - [MiGA] - taxonomy assignment, quantitative estimates of novelty, genome/MAG quality
  - [kraken2] - taxonomy assignment (prokaryote, viral, fungal)
  - [bracken] - relative abundance estimates from kraken2 tables
  - [metaphlan3] - for benchmarking purposes
- Isolate Analyses
  - clonality
    - ANI
    - SNP analyses
- Gene prediction
  - [Prodigal]
  - [Prokka]
- Gene annotation
  - TrEMBL database
  - [AMRFinder] - antibiotic resistance genes, virulence factors
- Pangenome analyses
  - Panaroo vs Roary

#### B: Metagenomes
- QC
  - [kneaddata] (wraps [trimmomatic] & [Bowtie2] decontamination of human reads)
- Assembly [metaSPAdes]
- Binning [Maxbin2] or [metabat2]
  - [Bowtie2] estimates of proportion of reads in bins
- MAG analyses
  - [MiGA]
  - [checkM]
  - Optimization/vizualization in Anvio
- Iterative assembly / binning

#### C: Metagenome contextualization of isolate genomes
- Competitive recruitment plots
- Strainsifter / Strainfinder / Phylophlan
- Baseline MAGs + genomes of interest from A
- PERMANOVA tests of trend (from R [vegan package])
- Heatmaps (from R [pheatmap package] scripts)
