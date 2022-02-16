# Metagenomic Coverage Analyses

After [quality control](quality-control.md) and [assembly-based work](metagenomic-analyses.md), when interested in the coverage of genomes or genes within a metagenome, there are a number of metagenomic coverage approaches we can take.

A granular approach that allows a high degree of control but is more manual is the [coverage magic](https://github.com/rotheconrad/00_in-situ_GeneCoverage) workflow from Roth Conrad. This is the approach described below for the analysis of gene coverage, using antimicrobial resistance genes as an example.

Other tools to resolve the coverage of genomes of closely related strains and their microdiversity that are also extremely useful for tracking genome coverage (with some option for gene coverage analyses) within metagenomes (see inStrain and StrainGE).

## Overview
- Rename reads
- Assemble contigs (see steps in [metagenomic analyses](metagenomic-analyses.md))
- Predict proteins (Prodigal)
- Annotate genes (with AMRFinder Plus as motivating example)
- Build magicblast database with assembled scaffolds (Magicblast)
- Map renamed metagenome reads vs renamed scaffolds (Magicblast)
- Run coverage magic python scripts to get coverage (TAD80 & RPKM) of scaffolds, genes (python)
- Run python scripts to validate genes from AMRFinder & coverage magic and pull their coverage (python)
- Analyze & Visualize (R)

## Rename reads

To facilitate linking reads, scaffolds, genes, and MAGs/genomes, we will rename reads prior to protein prediction or annotation.

See documentation and scripts at [Roth Conrad's Github](https://github.com/rotheconrad/00_in-situ_GeneCoverage#check-sequence-names-in-reference-fasta-files-and-rename-if-needed)

Input: fastq read file and/or scaffold fasta file, ID for renaming
Output: renamed fastq/fasta overwritten in place

```console
01a_Fasta_rename_sequences.py -i ${outdir}/${ID}_scaffolds.fasta -p $ID

# or
#01a_Fastq_rename_sequences.py -i ${outdir}/${ID}_scaffolds.fasta -p $ID

```

---

## Predict proteins

Protein-coding genes are predicted with [Prodigal](https://github.com/hyattpd/Prodigal). **We used Prodigal V2.6.3.**

- Input: SPAdes assembled scaffold fasta file with renamed reads
- Output: directory containing scaffolds.fasta, contigs.fasta, leogfiles, and assembly graphs/statistics.

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
