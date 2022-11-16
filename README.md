# PREMIX
The primary motivation for this repository to support the reproducibility of the analyses and figures from the PREMIX study.

At each step in analysis, we post the tools, versions, and annotated code used with (in most cases) the expected input and output for metagenomic data from human samples with or without paired data from cultured isolates. We use the genomic and metagenomic analyses from the paper **Randomized trial: Fecal microbiota transplant promotes reduction of antimicrobial resistance by strain replacement** as a practical example. 

Data for the analyses in the PREMIX paper that will be used for this repository are available through the NCBI Bioproject (accession PRJNA728680).

---

### Overview
- [Background](docs/background.md)
- [Quality Control](docs/quality-control.md)
  - [(human) stool metagenomes](docs/quality-control.md#(Human)-Metagenomes)
  - isolate genomes
- [Metagenomic Analyses](docs/metagenomic-analyses.md)
  - Assembly (metaSPAdes)
  - Short-read taxonomic classification (kraken2/bracken)
  - Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)
- [Genomic Analyses](docs/genomic-analyses.md)
  - Assembly (SPAdes)
  - Gene prediction (Prodigal)
  - Antimicrobial resistance genes analyses (AMRFinder)
  - Annotation (prokka | MicrobeAnnotator)
  - Clustered gene analyses (Roary)
  - Average nucleotide identity (FastANI)
- [Integrated Genomic and Metagenomic Analyses](docs/integrated-analyses.md)
  - Estimate breadth/depth of coverage of reference genome in metagenome (inStrain)
  - Estimates of gene coverage within metagenomes (inStrain)
  - Coverage visualization in R / ggplot2
