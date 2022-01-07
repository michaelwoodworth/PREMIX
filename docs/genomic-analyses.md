# Genomic Analyses

After [quality control](quality-control.md), we proceed to assembly for assembly-based analyses, gene prediction, annotation, and comparative genomic analyses.

## Overview
- Assembly (SPAdes)
- Gene prediction (Prodigal)
- Antimicrobial resistance genes analyses (AMRFinder)
- Annotation (prokka | MicrobeAnnotator)
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
args='-p single'       # for single genome gene prediction
```

- Run Prodigal
```console
prodigal -a ${outdir}/${ID}.faa -d ${outdir}/${ID}.fna -f gff -i ${scaffold} -o ${outdir}/${ID}.gff $args
```

## Antimicrobial resistance genes analyses (AMRFinder)
[AMRFinderPlus](https://github.com/ncbi/amr) is an NCBI developed/maintained tool that has a robust method of detecting antimicrobial resistance (AMR) genes with blast queries and hidden markov model searches. We have also [written some additional filtering and summarizing scripts](https://github.com/michaelwoodworth/AMRFinder_scripts) that may streamline some analyses with the output of AMRFinder. **We used AMRFinderPlus v3.10.18.**

- Define tool / step variables
```console
indir=${path_to_prodigal_output}
outdir=${path_to_amrfinder_output}
protein=${indir}/${ID}.faa
```

- Run AMRFinder
```console
amrfinder -p ${protein} --plus -o ${outdir}/${ID}_amrfinder.tsv
```

## Annotation (prokka)
[prokka](https://github.com/tseemann/prokka) is a rapid prokaryotic genome annotation tool. It accepts contigs (produced in earlier assembly step by SPAdes), predicts proteins, and annotates predicted genes. The output can be used directly as input for roary for comparative genomic analyses. **We used Prokka v1.14.6.**

- Define tool / step variables
```console
indir=${path_to_contigs}
outdir=${path_to_prokka_output}
contigs=${indir}/${ID}_contigs.fasta
```

- Run Prokka
```console
prokka --outdir ${outdir}/${ID} --prefix $ID $contigs
```

## Clustered Gene Analysis (Roary)
[Roary](https://github.com/sanger-pathogens/Roary) is a fairly simple tool for clustered gene comparisons across prokaryote genomes. The simplest way to run Roary is to copy/link gff files of interest from Prokka in a single directory and running Roary from that directory. Unfortunately, it is no longer being supported by the developer. **We used Roary v3.13.0.**

- Define tool / step variables
```console
indir=${path_to_gff_files_from_prokka}
args="-p 8 -o ${ID}_clustered_proteins -e -v"
```

- Run Roary
```console
roary $args ${indir}/*gff
```

## Average Nucleotide Identity (ANI) Tests (FastANI)
[FastANI](https://github.com/ParBLiSS/FastANI) is a fast and simple tool to calculate average nucleotide identity for complete or draft genomes. **We used v1.32.**

It's best to review the documentation on the FastANI github site, but we created a list of all genomes and ran all vs all comparisons as below.

- Define tool / step variables
```console
indir=${path_to_isolate_genome_contigs}
outdir=${path_to_write_output}
genome_list=${path_to_text_file_list_of_genomes}
```

- Run FastANI
```console
fastANI --ql $genome_list --rl $genome_list -o ${outdir}/output.txt
```
