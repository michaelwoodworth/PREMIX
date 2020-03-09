# w-c

configfile:
	"config.json"

mSAMPLES, = glob_wildcards(config'data'+"{id}_L001_R1_001.fastq.gz")
gSAMPLES, = glob_wildcards(config'data'+"{id}_L001_R1_001.fastq.gz")

