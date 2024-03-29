# Quality Control

For [human metagenomes](#(Human)-Metagenomes), we trim low-quality reads, remove barcodes/indices, and remove reads 
that align to a reference human genome in attempt to protect the genomic data for participants of the study. The
PREMIX metagenome files that are available on NCBI were depleted of human-aligning reads using bowtie2 and are labeled
as ID_human_removed_R[12].fastq.

We used [kneaddata](http://huttenhower.sph.harvard.edu/kneaddata) from the Huttenhower lab for this step since it
conveniently wraps trimmomatic (for read trimming) and BMTagger (for human read removal). 

For [isolate genomes](#Isolate-Genomes), we trim low-quality reads and remove barcodes/indices with trimmomatic alone.

## (Human) Metagenomes

**We used kneaddata v0.7.4**

- Input: Illumina paired end read fastq files (e.g. PM01-C1D01_human_removed_R1.fastq, PM01-C1D01_human_removed_R2.fastq)
- Output: Trimmed files depleted of human-genome aligning reads (${ID}_paired_1.fastq, ${ID}_paired_2.fastq, ${ID}_unmatched_1.fastq, ${ID}_unmatched_2.fastq), human-aligning reads, and a log file.

- Define tool / step variables
```console
indir=${path_to_read_files}
R1=${indir}/${ID}_human_removed_R1.fastq.gz
R2=${indir}/${ID}_human_removed_R2.fastq.gz
db=${path_to_reference_human_genome}
args="-db $db --output-prefix $ID -t 8 --run-bmtagger --remove-intermediate-output --trimmomatic /storage/home/hcoda1/0/mwoodworth8/.conda/envs/biobakery/share/trimmomatic-0.39-1"
outdir=${path_for_kneaddata_output}
```

- Run kneaddata
```console
kneaddata -i $R1 -i $R2 -o $outdir $args
```

- Examine/clean output

**Note:** Kneaddata and trimmomatic can both accept .gz compressed files as input.

## Isolate Genomes

**We used trimmomatic v0.39**

- Input: Illumina paired end read fastq files (e.g. p20105-s033_R1.fastq, p20105-s033_R2.fastq)
- Output: Trimmed files (e.g. p20105-s033_P1.fastq, p20105-s033_P2.fastq, p20105-s033_U1.fastq, p20105-s033_U2.fastq)

- Define tool / step variables
```console
indir=${path_to_read_files}
R1=${indir}/${ID}_R1.fastq.gz
R2=${indir}/${ID}_R2.fastq.gz
PE_args="-threads 5 -phred33 -summary ${outdir}/summary_files/${ID}_PE_summary.txt"
outstems="${outdir}/${ID}_P1.fastq ${outdir}/${ID}_U1.fastq ${outdir}/${ID}_P2.fastq ${outdir}/${ID}_U2.fastq"
PE_trim="ILLUMINACLIP:/storage/home/hcoda1/0/mwoodworth8/.conda/pkgs/trimmomatic-0.39-1/share/trimmomatic-0.39-1/adapters/TruSeq3-SE.fa:2:30:10 SLIDINGWINDOW:4:20 MINLEN:50"
```

- Run trimmomatic
```console
trimmomatic PE $PE_args $R1 $R2 $outstems $PE_trim
```
