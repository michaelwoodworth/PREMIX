# workflow-clinical
pilot workflow for genomes + metagenomes to estimate temporal dynamics of pathogens and genetic antibiotic resistance and virulence determinants in clinical settings

### Background
Apply next-generation sequencing (NGS) analytic tools to genomes from clinical isolates, patient-associated, and environmental-associated metagenomes using snakemake workflows to estimate chnages over time.  Workflow was developed in context of two fecal microbiota transplant clinical trials (PREMIX and FAIR).

Wrapped tools are indicated in square brackets e.g. [ ], which should be cited.

### Overview
- specify file paths
  - suggested file naming convention, workarounds
- dependencies 
  - hardware
  - software
  - cluster vs cluster environments

---
The files you will need to run this workflow are:
- config.json: modified with paths to your fastq or fastq.gz files
- genome files: raw fastq (or fastq.gz) files from isolate genomes
- metagenome files: raw fastq (or fastq.gz) files from metagenomes

---

#### A: Isolates 
- QC
  - [kneaddata] (wraps [trimmomatic] & [bowtie2] decontamination)
- Assembly [SPAdes]
- Taxonomy
  - [MiGA] - taxonomy assignment, quantitative estimates of novelty, genome/MAG quality
  - [kraken2] - taxonomy assignment (prokaryote, viral, fungal)
  - [bracken] - relative abundance estimates from kraken2 tables
  - [metaphlan2] - for benchmarking purposes
- Isolate Analyses
  - clonality
    - ANI
    - SNP analyses
- Gene prediction
  - [Prodigal]
- Gene annotation
  - TrEMBL database
  - [AMRFinder] - antibiotic resistance genes, virulence factors

#### B: Metagenomes
- QC
  - [kneaddata] (wraps [trimmomatic] & [Bowtie2] decontamination of human reads)
- Assembly [metaSPAdes]
- Binning [Maxbin2] or [metabat2]
  - [Bowtie2] estimates of proportion of reads in bins (maybe this could be done in Roth script)
- MAG analyses
  - Drop into isolate subflow at Taxonomy step
  - [MiGA]
  - [checkM]
- Iterative assembly / binning?

#### C: Metagenome contextualization of isolate genomes
- Competitive recruitment plots
- Baseline MAGs + genomes of interest from A
- PERMANOVA tests of trend (from R [vegan package])
- Heatmaps (from R [pheatmap package] scripts)
