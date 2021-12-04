# Genomic Analyses

After [quality control](quality-control.md), we proceed to assembly for assembly-based analyses, gene prediction, annotation, and comparative genomic analyses.

## Overview
- Assembly (SPAdes)
- Gene prediction (Prodigal)
- Annotation (prokka | MicrobeAnnotator)
- Antimicrobial resistance genes analyses (AMRFinder)
- Clustered gene analyses (Roary)
- Average nucleotide identity (FastANI)

## Assembly (SPAdes)
[SPAdes](https://github.com/ablab/spades) is a commonly-used de novo assembler. For isolate assembly, we used the isolate option. **We used spades v3.14.1.**

- SPAdes accepts two paired end read files and an unpaired read file. Since trimmomatic splits the unpaired read files, we'll concatenate them and supply them as one file to SPAdes for assembly.

```console
cat ${ID}_U1.fastq ${ID}_U2.fastq >> ${ID}_U.fastq
```
- Define tool / step variables
```console
indir=${path_to_trimmomatic_processed_reads}
outdir=${path_to_SPAdes_output}
R1=${indir}/${ID}_P1.fastq
R2=${indir}/${ID}_P2.fastq
U=${indir}/${ID}_U.fastq
args=args='--isolate -t 20 -m 80'
```
- Run SPAdes
```console
spades.py $args -1 $R1 -2 $R2 -s $U -o ${outdir}/${ID}
```

- Rename scaffolds (optional)
Scaffolds can be renamed and copied/linked to a new directory using the [rename_scaffolds.sh](../assets/rename_scaffolds.sh) bash script.

## Gene prediction (Prodigal)
[Prodigal](https://github.com/hyattpd/Prodigal) is a tool to predict protein-coding genes from prokaryotic genomes. We typically run prodigal and keep the amino acid, nucleic acid, and gff files for downstream use. **We used Prodigal v2.6.3.**

- Define tool / step variables
```console
indir=${path_to_spades_assembled scaffolds}
outdir=${path_to_prodigal_output}
  # scaffold=${indir}/${ID}_scaffolds.fasta # if renamed with rename_scaffolds.sh script above
  # scaffold=$(indir}/${ID}/scaffolds.fasta # if SPAdes scaffolds used in original output directories
args=args='--isolate -t 20 -m 80'
```
