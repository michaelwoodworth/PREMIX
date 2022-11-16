#!/usr/bin/env python

'''Parses inStrain genome coverage/breadth results to 
calculate summary statistics for each genome/MAG.

As input, this script requires:
	- path to inStrain IS/output/*.IS_genome_info.tsv file

The output produced is:
	- a summary of breadth and coverage
	  (depth) for the input gene set(s)

'''

import argparse, glob, os, csv
import pandas as pd
from statistics import mean, median
from collections import defaultdict

# define get record_IDs function
def parse_fasta(fasta, verbose):

	record_IDs = []

	print('Parsing gene set fasta file...')

	for record in SeqIO.parse(fasta, "fasta"):

		# if verbose:
		# 	print(f" - ID: {record.id}")
		record_IDs.append(record.id)

	print(f" - identified {len(record_IDs)} genes.")

	# print('')
	# print(deep_dict)
	return record_IDs

# define read_IS function
def read_IS(IS_file):

	print('Reading inStrain tsv file...')
	IS_df = pd.read_csv(IS_file, sep = '\t')

	return IS_df

# define pandas coverage parsing function
def deep_panda(IS_df, record_IDs, verbose):
	print('')
	print(f'Linking gene coverage & breadth from inStrain file for {len(record_IDs)} genes...')
	print(f'  (this can take some time)')

	# initialize variables
	deep_dict = defaultdict(dict)
	counter = 0
	no_coverage_count = 0
	
	for prodigal_ID in record_IDs: 	# loop over record IDs from gene set
				
		if (IS_df['gene']==prodigal_ID).any():
		
			IS_df_match = IS_df[IS_df.gene.eq(prodigal_ID)]
#			 coverage = IS_df_match.loc[:,['coverage']].astype(float)
#			 breadth = IS_df_match.loc[:,['breadth']].astype(float)
			
			coverage = IS_df_match["coverage"].iloc[-1]
			breadth = IS_df_match["breadth"].iloc[-1]
			
			deep_dict[prodigal_ID]['coverage'] = coverage
			deep_dict[prodigal_ID]['breadth']  = breadth
#			 deep_dict[prodigal_ID]['coverage'] = float(coverage)
#			 deep_dict[prodigal_ID]['breadth']  = float(breadth)
			
			counter += 1
			
		else:
			deep_dict[prodigal_ID]['coverage'] = float(0)
			deep_dict[prodigal_ID]['breadth']  = float(0)

			no_coverage_count += 1

	print(f' - found coverage & breadth for {counter} ({round(counter / len(record_IDs) * 100, 2)} %) genes.')
	print(f' - unable to find coverage & breadth for {no_coverage_count} ({round(no_coverage_count / len(record_IDs) * 100, 2)} %) genes.')
	
	# calculate mean coverage:
	total_coverage = 0
	total_breadth = 0
	with_coverage = 0
	mdedian_breadth = 0
	coverage_list = []
	breadth_list = []

	for values in deep_dict.values():
		total_coverage += float(values['coverage'])
		total_breadth += float(values['breadth'])
		coverage_list.append(float(values['coverage']))
		breadth_list.append(float(values['breadth']))

	mean_coverage = total_coverage / len(deep_dict)
	median_coverage = median(coverage_list)
	mean_breadth = total_breadth / len(deep_dict)
	median_breadth = median(breadth_list)

	# report statistics
	if no_coverage_count > 0:
		print(f" - inStrain coverage data missing for {no_coverage_count} ({round((no_coverage_count / len(record_IDs) *100), 2)} %) genes.")
		print('')
		print(f"	WARNING - coverage & breadth for missing values imputed as 0")
		print('')

	print(f" - mean coverage for set of {len(deep_dict)} genes: {round(mean_coverage, 1)}")
	print(f" - median coverage for set of {len(deep_dict)} genes: {round(median_coverage, 1)}")
	print(f" - mean breadth for set of {len(deep_dict)} genes: {round(mean_breadth, 2) * 100}%")
	print(f" - median breadth for set of {len(deep_dict)} genes: {round(median_breadth, 2) * 100}%")
	
	return deep_dict, mean_coverage, median_coverage, mean_breadth, median_breadth, counter, no_coverage_count


# write output
def dict_writer(deep_dict, record_IDs, output_path, prefix, #query_set, 
	mean_coverage, median_coverage, mean_breadth, median_breadth, coverage_count, no_coverage_count):

	print('')
	print('-----------------------------------------------------------------------')
	print(f'Writing output with {len(deep_dict.keys())} genes...')

	# write output files 

	coverage_fieldnames = ('prodigal_ID', 'coverage', 'breadth')

	outfile=f"{output_path}/{prefix}_coverage.tsv"
	# outfile=f"{output_path}/{prefix}_{query_set}_coverage.tsv"	
	with open(outfile, 'w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=coverage_fieldnames, delimiter='\t')
		writer.writeheader()
		for k in deep_dict:
			writer.writerow({field: deep_dict[k].get(field) or k for field in coverage_fieldnames})

	# write coverage summary statistics file:
	outfile=f"{output_path}/{prefix}_coverage_summary.tsv"
	# outfile=f"{output_path}/{prefix}_{query_set}_coverage_summary.tsv"
	total_gene_count=len(deep_dict.keys())

	with open(outfile, 'w', newline='') as f:
		f.write(f"Prefix\tTotal Gene Count\tN Imputed Coverage\tN inStrain Coverage\tMedian Coverage\tMean Coverage\tMedian Breadth\tMean Breadth\n")
		f.write(f"{prefix}\t{total_gene_count}\t{no_coverage_count}\t{coverage_count}\t{median_coverage}\t{mean_coverage}\t{median_breadth}\t{mean_breadth}")

		# f.write(f"Prefix\tQuery Set\tTotal Gene Count\tN Imputed Coverage\tN inStrain Coverage\tMedian Coverage\tMean Coverage\tMean Breadth\n")
		# f.write(f"{prefix}\t{query_set}\t{total_gene_count}\t{coverage_count}\t{no_coverage_count}\t{median_coverage}\t{mean_coverage}\t{mean_breadth}")

	print(f' - output written to {output_path}/{prefix}_coverage.tsv')
	# print(f' - output written to {output_path}/{prefix}_{query_set}_coverage.tsv')

def main():
	# configure argparse arguments & pass to method_filter
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class = argparse.RawDescriptionHelpFormatter
		)
	parser.add_argument(
		'-o', '--output_path',
		help = 'path to write files containing annotated gene coverage data.',
		type=str,
		required=True
		)
	parser.add_argument(
		'-i','--IS_file',
		help = 'path to inStrain *gene_info.tsv file',
		type = str,
		required=True
		)
	parser.add_argument(
		'-f','--fasta',
		help = 'path to gene set fasta file (AA or nucl ok)',
		type = str,
		required=True
		)
	parser.add_argument(
		'-p','--prefix',
		help = 'prefix for output naming',
		required=True
		)
	parser.add_argument(
		'-v', '--verbose',
		required=False,
		action='store_true'
		)
	args=vars(parser.parse_args())

	print('')
	if args['verbose']:
		print('Input parameters:')		
		print(f" - output path:	{args['output_path']}")
		print(f" - fasta file: {args['fasta']}")
		print(f" - IS_file: {args['IS_file']}")
		print('')

	IS_df = read_IS(args['IS_file'])

	record_IDs = parse_fasta(args['fasta'], 
		args['verbose'])

	deep_dict, mean_coverage, median_coverage, mean_breadth, median_breadth, coverage_count, no_coverage_count = deep_panda(IS_df,
		record_IDs,
		args['verbose'])

	dict_writer(deep_dict, 
		record_IDs,
		args['output_path'],
		args['prefix'],
		# args['query_set'],
		mean_coverage, 
		median_coverage, 
		mean_breadth,
		median_breadth, 
		coverage_count,
		no_coverage_count)

	print('')
	print(f'Looks like everything completed.')

if __name__ == "__main__":
	main()