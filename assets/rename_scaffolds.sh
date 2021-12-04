#!/bin/bash

# define input variables
indir=$1        # directory with spades output
outdir=$2       # directory to write renamed files
list_pth=$3     # directory with IDlist.txt

# talk to human

echo "###############################################"
echo " ______ _______ _______ _______ _______ _______ "
echo "|   __ \    ___|    |  |   _   |   |   |    ___|"
echo "|      <    ___|       |       |       |    ___|"
echo "|___|__|_______|__|____|___|___|__|_|__|_______|"
echo "###############################################"
echo ""

# loop renaming
for ID in `cat ${list_pth}/IDlist.txt`
#do cp ${indir}/${ID}/scaffolds.fasta ${outdir}/${ID}_scaffolds.fasta
do cp ${indir}/${ID}/contigs.fasta ${outdir}/${ID}_contigs.fasta
echo $ID renamed
done
