# Quality Control

---

For [human metagenomes](#(Human)-Metagenomes), we trim low-quality reads, remove barcodes/indices, and remove reads 
that align to a reference human genome in attempt to protect the genomic data for participants of the study. The
PREMIX metagenome files that are available on NCBI were depleted of human-aligning reads using bowtie2 and are labeled
as ID_human_removed_R[12].fastq.

We used [kneaddata](http://huttenhower.sph.harvard.edu/kneaddata) from the Huttenhower lab for this step since it
conveniently wraps trimmomatic (for read trimming) and BMTagger (for human read removal). 

---

## (Human) Metagenomes
## Isolate Genomes
