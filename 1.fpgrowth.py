
# coding: utf-8
### function: Get mutation pairs from ICGC data
### lyz and xyf

import pandas as pd
from pandas import DataFrame
import numpy as np
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument(
    '-m',help='donor ssm data')
parser.add_argument(
    '-i',help='fpgrowth input file')
parser.add_argument(
    '-o_1',help='fpgrowth output file m1n1')
parser.add_argument(
    '-o_2',help='fpgrowth output file m2n2')
parser.add_argument(
    '-o_3',help='fpgrowth output file m3n3')
parser.add_argument(
    '-supp',help='supp threshold >= int')
args = vars(parser.parse_args())

supp_threshold = int(args['supp'])
print("-"*40)
print("supp_threshold:", supp_threshold)
##input pancaner mutation info for each donor
donor_ssm = pd.read_csv(args['m'],sep='\t')
print('donor_num=',donor_ssm['icgc_donor_id'].unique().shape[0])
print('mut_num=',donor_ssm['icgc_mutation_id'].unique().shape[0])
##filter mutations affect few donor
donor_select_ssm = donor_ssm[['icgc_mutation_id','icgc_donor_id']].drop_duplicates().groupby('icgc_mutation_id').filter(lambda x : len(x) >= supp_threshold)
print('donor_filter_num=',donor_select_ssm['icgc_donor_id'].unique().shape[0])
print('mut_filter_num=',donor_select_ssm['icgc_mutation_id'].unique().shape[0])
##prepare fpgrowth input
data_ssm = donor_select_ssm[['icgc_mutation_id','icgc_donor_id']].drop_duplicates()
ssm_set = data_ssm.groupby('icgc_donor_id')['icgc_mutation_id'].apply(list).reset_index(name='ssm_set')
donor_ssm_list = []
for index,data in ssm_set.iterrows():
    donor_ssm_list.append(ssm_set.iloc[index,1])
##get fpgrowth input file
with open(args['i'],'at') as f:
    for i in donor_ssm_list:
    	print(*i,sep='\t',file = f)
##set min support rate
donor_num = donor_ssm['icgc_donor_id'].unique().shape[0]
mut_donor_unique = donor_ssm[['icgc_mutation_id','icgc_donor_id']].drop_duplicates()
##run fpgrowth in closed pattern
input_path = args['i']
output_path_1 = args['o_1']
output_path_2 = args['o_2']
output_path_3 = args['o_3']
print("")
cmd1 = 'fpgrowth -tc -v" %a" -s-{}m1n1 {} {}'.format(supp_threshold,input_path,output_path_1)
cmd2 = 'fpgrowth -tc -v" %a" -s-{}m2n2 {} {}'.format(supp_threshold,input_path,output_path_2)
cmd3 = 'fpgrowth -tc -v" %a" -s-{}m3n3 {} {}'.format(supp_threshold,input_path,output_path_3)

subprocess.run(cmd1, shell = True)
print('fpgrowth process m1n1 is done')
subprocess.run(cmd2, shell = True)
print('fpgrowth process m2n2 is done')
subprocess.run(cmd3, shell = True)
print('fpgrowth process m3n3 is done')