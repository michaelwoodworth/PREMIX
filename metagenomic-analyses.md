# Metagenomic Analyses

After [quality control](quality-control.md), we proceed to assembly for assembly-based analyses and short-read taxonomic classification.
Assembly is the most time-consuming step so it can be helpful to get this started first and then proceed with other analyses.

## Overview
- Assembly (metaSPAdes)
- Short-read taxonomic classification (kraken2/bracken)
- Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)
- Estimates of MAG coverage breadth and depth within metagenomes
- Competitive recruitment plots
- Coverage visualization as line plots and heatmaps in R / ggplot2

## Assembly (metaSPAdes)

[metaSPAdes](https://github.com/ablab/spades) is a commonly-used de novo assembler with an option for assembly of contigs from metagenomic sequencing data.
The metagenomic assembly mode only accepts a single library, so in our case, where additional sequencing effort for the samples from run 2
was performed in run 3, we will concatenate the 'left' R1, 'right' R2, and single read files U as follows:

```console
cat ${ID}_library1_R1.fastq ${ID}_library2_R1.fastq >> ${ID}_concatenated_R1.fastq
```

- Input: trimmed paired end and singleton fastq files (e.g. PM01-C1D01_trimmed_R1.fastq, 
PM01-C1D01_trimmed_R2.fastq, PM01-C1D01_trimmed_U.fastq)
- Output: directory containing scaffolds.fasta, contigs.fasta, logfiles, and assembly graphs/statistics.

- Define tool / step variables
```console
indir=${path_to_keaddata_processed_reads}
outdir=${path_to_metaSPAdes_output}
R1=${indir}/${ID}_P1.fastq
R2=${indir}/${ID}_P2.fastq
U=${indir}/${ID}_U.fastq
args='--meta -t 20 -m ${integer with available memory}'
```

- Run metaSPAdes
```console
spades.py $args -1 $R1 -2 $R2 -s $U -o ${outdir}/${ID}
```

- Examine output

## Short-read taxonomic classification (kraken2/bracken)

## Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)
## Estimates of MAG coverage breadth and depth within metagenomes
## Competitive recruitment plots
## Coverage visualization as line plots and heatmaps in R / ggplot2
