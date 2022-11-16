# Integrated Genomic and Metagenomic Analyses

After [quality control](quality-control.md) and [assembly-based work](metagenomic-analyses.md), when interested in the coverage of genomes or genes within a metagenome, there are a number of metagenomic coverage approaches we can take.

The general approach is to map reads from a metagenome to a reference genome (cultured isolate, reference from public repositories, or metagenome-assembled genome (i.e. MAG)), or gene. The proportion of a reference that is covered by mapped reads (i.e. coverage breadth) provides information about detection, with increasing specificity of confident detection with increasing breadth. The number of reads that map to a position (i.e. coverage depth) provide quantiative information about how representative that sequence is of a sample, which typically implies that it is either highly conserved or highly abundant.

We used [inStrain](https://instrain.readthedocs.io/en/latest/) because it is very well documented and provides useful output datasets that are straightforwad to parse with custom scripts.

## Overview
- Assemble contigs (see steps in [metagenomic analyses](metagenomic-analyses.md))
- Predict proteins (Prodigal)
- Annotate genes (with AMRFinder Plus as motivating example)
- Map metagenome reads vs reference (Bowtie2)
- Filter reads and estimate coverage and diversity statistics (inStrain)
- Analyze & Visualize (R)

## Assemble contigs

See steps in [metagenomic analyses](metagenomic-analyses.md)

## Predict proteins

Protein-coding genes are predicted with [Prodigal](https://github.com/hyattpd/Prodigal). **We used Prodigal V2.6.3.**

- Input: SPAdes assembled scaffold fasta file with renamed reads
- Output: directory containing scaffolds.fasta, contigs.fasta, logfiles, and assembly graphs/statistics.

- Define tool / step variables
```console
indir=${path_to_renamed_scaffolds.fasta}
outdir=${path_to_Prodigal_output}
scaffold=${indir}/${ID}_scaffolds.fasta
```

- Run Prodigal
```console
prodigal -a ${outdir}/${ID}.faa -d ${outdir}/${ID}.fna -f gff -i ${scaffold} -o ${outdir}/${ID}.gff $args
```

## Annotate genes


## Map metagenome reads


## Calculate coverage for genes & scaffolds

