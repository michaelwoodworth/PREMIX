# Integrated Genomic and Metagenomic Analyses

After [quality control](quality-control.md) and [assembly-based work](metagenomic-analyses.md), when interested in the coverage of genomes or genes within a metagenome, there are a number of metagenomic coverage approaches we can take.

The general approach is to map reads from a metagenome to a reference genome (cultured isolate, reference from public repositories, or metagenome-assembled genome (i.e. MAG)), or gene. The proportion of a reference that is covered by mapped reads (i.e. coverage breadth) provides information about detection, with increasing specificity of confident detection with increasing breadth. The number of reads that map to a position (i.e. coverage depth) provide quantiative information about how representative that sequence is of a sample, which typically implies that it is either highly conserved or highly abundant.

We used [inStrain](https://instrain.readthedocs.io/en/latest/) because it is very well documented and provides useful output datasets that are straightforwad to parse with custom scripts.

## Overview
- Assemble contigs (see steps in [metagenomic analyses](metagenomic-analyses.md))
- Predict proteins (Prodigal)
- Annotate genes (with AMRFinder Plus as motivating example)
- Calculate coverage statistics (inStrain)
- Calculate average genome size (MicrobeCensus)
- Parse and link output for gene RPKG estimates

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

Predicted proteins can be annotated (using tools like [eggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper), [bakta](https://github.com/oschwengers/bakta), [prokka](https://github.com/tseemann/prokka) or [MicrobeAnnotator](https://github.com/cruizperez/MicrobeAnnotator)). Our group uses [AMRFinder Plus](https://github.com/ncbi/amr/wiki/Installing-AMRFinder) to annotate antimicrobial resistance and virulence genes, which we will use as a motivating example.

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

## Calculate coverage statistics

At this point, you have what you need (metagenome reads, reference genome, predicted genes) to create an inStrain profile following [their tutorial](https://instrain.readthedocs.io/en/latest/tutorial.html):

- create Bowtie2 index
- map metagenome reads to create SAM file
- run inStrain profile with SAM, genome, and genes


## Calculate average genome size [MicrobeCensus](https://github.com/snayfach/MicrobeCensus)

- Define tool / step variables
```console
indir=${path_to_metagenome_reads}
outdir=${path_to_write_microbecensus_output}
ID=${unique sample id}
args="-n 100000000 -t 16" # sample 100,000,000 reads and run on 16 threads
```

- Run MicrobeCensus
```console
run_microbe_census.py $args ${R1},${R2} ${outdir}/${ID}.census
```

- Summarize MicrobeCensus output files from multiple metagenomes

We wrote a helper python script [summarize_microbecensus.py](PREMIX/assets/summarize_microbecensus.py) to summarize a directory containing multiple .census output files as a single tsv file that contains average genome size for normalization.

## Parse inStrain output

The inStrain output file of interest will depend on your study question. For AMR gene coverage depth analyses we used the resulting gene_info.tsv files. We wrote a helper script for parsing and summarizing these output files: [gene_validate_and_summarize_RPKG.py](../assets/gene_validate_and_summarize_RPKG.py).

### Parse and validate AMR genes

This step expects the following input files:
- filtered AMRFinder results (see [AMRFinder_scripts](https://github.com/michaelwoodworth/AMRFinder_scripts/blob/master/README.md#6-post-processing))
- inStrain gene_info.tsv files in a single directory with each file relabeled as ${uniqueID}_gene_info.tsv.
- a MicrobeCensus summary file

*Note the -V flag, which will write an additional file of genes that need further validation/inspection if they were not in both the AMRFinder and inStrain files as well as genes that were deduplicated for coverage depth totals.*

- Run gene_validate_and_summarize_RPKG.py
```console
02_amrfinder_validate_and_summarize_RPKG.py -a ${filtered_AMRFinder_file_directory} -i ${inStrain_gene_info_tsvs} -m ${microbecensus_summary.tsv} -o ${output_directory} -V
```
