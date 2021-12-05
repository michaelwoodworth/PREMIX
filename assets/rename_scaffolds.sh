#!/bin/bash

# script to copy spades scaffolds/contigs.fasta files to single directory
# and rename deflines for downstream use

# dependencies:
#	- 01b_Fasta_rename_sequences.py script (see https://github.com/rotheconrad/00_in-situ_GeneCoverage)
#	- Python >3.6

# define input variables
indir=$1	# directory with spades output
outdir=$2	# directory to write renamed files
list_pth=$3	# directory with IDlist.txt

# talk to human

echo "###############################################"
echo " ______ _______ _______ _______ _______ _______ "
echo "|   __ \    ___|    |  |   _   |   |   |    ___|"
echo "|      <    ___|       |       |       |    ___|"
echo "|___|__|_______|__|____|___|___|__|_|__|_______|"
echo "###############################################"
echo ""

if [[ ! -z $indir ]] && [[ ! -z $outdir ]] && [[ ! -z $list_pth ]] # test if required input parameter is empty
then

	# loop renaming
	for ID in `cat ${list_pth}/IDlist.txt`
	do echo "starting ${ID} ..."
	cp ${indir}/${ID}/scaffolds.fasta ${outdir}/${ID}_scaffolds.fasta
	#do cp ${indir}/${ID}/contigs.fasta ${outdir}/${ID}_contigs.fasta
	echo "	- ${ID} scaffolds copied to outdir."

        echo "	- renaming read deflines for copied $ID files ..."
        s_path=/storage/home/hcoda1/0/mwoodworth8/p-ktk3-0/rich_project_bio-konstantinidis/Software/rothscripts/01a_Fasta_rename_sequences.py 
	        # run Roth's fastq rename sequence script
        python ${s_path} -i ${outdir}/${ID}_scaffolds.fasta -p $ID
        echo "          ... ${outdir}/${ID}_scaffolds.fasta deflines renamed"
	echo $ID renamed
	echo ""
	echo "=============================================================="
	done

else
        echo ""
        echo "ERROR: Check input parameters..."
        echo "  example usage: rename_scaffolds.sh {indir} {outdir} {list_pth}"
        echo "  indir - input directory containing spades output
        echo "          e.g. "02.spades"
        echo ""
        echo "  outdir - directory to write renamed scaffolds"
        echo "          e.g. renamed_scaffolds."
	echo ""
        echo "  list_pth - directory containing IDlist.txt with unique ID prefixes"

fi
