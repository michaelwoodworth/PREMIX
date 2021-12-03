# Metagenomic Analyses

After [quality control](quality-control.md), we proceed to assembly for assembly-based analyses and short-read taxonomic classification.
Assembly is the most time-consuming step so it can be helpful to get this started first and then proceed with other analyses.

## Overview
- Assembly (metaSPAdes)
- Short-read taxonomic classification (kraken2/bracken)
- Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)

## Assembly (metaSPAdes)

[metaSPAdes](https://github.com/ablab/spades) is a commonly-used de novo assembler with an option for assembly of contigs from metagenomic sequencing data. **We used spades v3.14.1.**

**Note**: The metagenomic assembly mode only accepts a single library, so in our case, when working with the PREMIX metagenomes where additional sequencing effort for the samples from run 2 was performed in run 3, we will concatenate the 'left' R1, 'right' R2, and single read files U as follows:

```console
cat ${ID}_library1_R1.fastq ${ID}_library2_R1.fastq >> ${ID}_concatenated_R1.fastq
cat ${ID}_library1_R2.fastq ${ID}_library2_R2.fastq >> ${ID}_concatenated_R2.fastq
cat ${ID}_library1_U.fastq ${ID}_library2_U.fastq >> ${ID}_concatenated_U.fastq
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
There are a number of ways to examine the quality of contigs assembled from metagenomic data (e.g. N50 and other statistics, map reads back to contigs with a tool like bowtie2 to estimate the proportion of reads that were assembled and those that did not end up in contigs, reports from [(meta)QUAST](http://quast.sourceforge.net/metaquast.html), etc.). 

## Short-read taxonomic classification (kraken2/bracken)

[kraken2](https://github.com/DerrickWood/kraken2) is a k-mer based short-read taxonomic classification tool. [bracken](https://github.com/jenniferlu717/Bracken) is companion tool that reestimates read at a given taxonomic rank (e.g. species). [Benchmarks of use of kraken2/bracken together](https://doi.org/10.1016/j.cell.2019.07.010) has been shown to perform well. **We used kraken2 v2.1.1 and bracken v2.6.2**.

**Kraken2**
- Input: trimmed paired end fastq files (e.g. PM01-C1D01_trimmed_R1.fastq, 
PM01-C1D01_trimmed_R2.fastq) from kneaddata.
- Output: report and output file to input to bracken.

- Define tool / step variables
```console
indir=${path_to_keaddata_processed_reads}
outdir=${path_to_kraken2_output}
R1=${indir}/${ID}_P1.fastq
R2=${indir}/${ID}_P2.fastq
db=${path_to_kraken2_database}
args="--threads 8 --use-names --paired"
```

- Run kraken2
```console
kraken2 --db $db --output ${outdir}/${ID}.kraken2 $args --report ${outdir}/${ID}.kreport $R1 $R2
```

- Examine output

---

**Bracken**
- Input: kraken2 report
- Output: bracken report with reestimated reads/percents

- Define tool / step variables
```console
indir=${path_to_kraken2_report}
outdir=${path_to_bracken_output}
kreport=${indir}/${ID}.kreport
db=${path_to_kraken2_database}
args="--threads 8 --use-names --paired"
```

- Run bracken
```console
bracken -d $db -i $kreport -o ${outdir}/${ID}_S_.bracken -w ${outdir}/kraken2_reports/${ID}_S_.kb
```

## Metagenome-assembled genome binning & classification (maxbin2 / metabat2 / DASTool / gtdbtk)

Assembled contigs can be evaluated using a number of characteristics (e.g. coverage, GC content, tetramer frequency, etc.) to group them by similarity into 'bins' that attempt to represent a population of a given taxon within a metagenomically sequenced sample. These bins (especially when considered to be [high quality](https://www.nature.com/articles/nbt.3893)) can be further evaluated as metagenome-assembled genomes (referred to as MAGs). MAGs can be evaluated for quality metrics like completeness and contamination (often measured by detection of necessary universal single copy genes). This area of bioinformatics can be expected to change rapidly and MAG-based inferences should be couched in caveats.

For the purposes of the PREMIX study, the primary MAG-based analyses performed were to **estimate engraftment of donor-derived strains**. Since one stool donor was used for the study, we co-assembled contigs from six metagenomes that represented each of the FMT dose lots used in the trial. A dose lot consisted of a variable number of bottles of stool suspended in sterile saline and 10% glycerol manufactured from a single stool specimen. Metagenome reads were concatenated and assembled using metaSPAdes. We then used scripts in the [CoverageMagic](https://github.com/rotheconrad/00_in-situ_GeneCoverage) workflow written by Roth E. Conrad to estimate coverage breadth as well as relative abundance of donor MAGs within participant and FMT dose metagenomes.
