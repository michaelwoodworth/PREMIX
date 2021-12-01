# PREMIX
The primary motivation for hosting this repository to support the reproducibility of the analyses and visualizations from the PREMIX study.

At each step in analysis, we post the tools, versions, and annotated code used with expected input and output for metagenomic data from human samples with or without paired data from cultured isolates. We use the genomic and metagenomic analyses from the paper **Randomized trial: Fecal microbiota transplant promotes reduction of antimicrobial resistance by strain replacement** as a practical example. 

Data for the analyses in the PREMIX paper that will be used for this repository are available through the NCBI Bioproject (accession PRJNA728680), which will be made available at time of publication.

---

### Overview
- [Background](background.md)
- [Quality Control](quality-control.md)
  - [(human) stool metagenomes](quality-control.md#(Human)-Metagenomes)
  - isolate genomes
- [Metagenomic Analyses](./metagenomic-analyses.md)
  - [Assembly (metaSPAdes)](./metagenomic-analyses.md#Assembly-(metaSPAdes))
  - Short-read taxonomic classification (kraken2/bracken)
  - Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)
- Genomic Analyses
  - Assembly (SPAdes)
  - Taxonomic classification / evaluation for contamination (kraken2)
  - Gene prediction (Prodigal)
  - Gene annotation (Prokka / MicrobeAnnotator / AMRFinder)
  - Comparative analyses: Average nucleotide identity (ANI), Multi-locus sequence typing (MLST), SNP counts, Roary
- (Meta)Genomic Analyses
  - Estimate breadth/depth of coverage of reference genome in metagenome (inStrain)
  - Estimates of MAG coverage breadth and depth within metagenomes
  - Coverage visualization as line plots and heatmaps in R / ggplot2
