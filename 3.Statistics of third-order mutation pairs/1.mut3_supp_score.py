# Functions: Frequency arrangement and co-scores calculation of third-order mutation pairs
# Author: Yangfang Xiong

import pandas as pd
from pandas import DataFrame
import numpy as np
import scipy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i_pair3',help='input file - muation pair mut ratio file mut3')
parser.add_argument(
    '-i_single',help='input file - single mutation mut ratio file')
parser.add_argument(
    '-o',help='output file with single and pair mut supp')
parser.add_argument(
    '-n',required=True, help='cancer donor count')
parser.add_argument(
    '-m',required=True, help='cancer mean mutation count')
args = vars(parser.parse_args())

print("Read input data...")

donor_count = int(args['n'])
mean_mut = float(args['m'])
data2 = pd.read_csv(args['i_pair3'],sep=' ',header=None)
data2.columns = ['mut_1','mut_2','mut_3','supp']
print("mut_pair shape:", data2.shape)

data2 = data2.drop_duplicates()
print("drop duplicaties, mut_pair shape:", data2.shape)

data1 = pd.read_csv(args['i_single'],sep=' ',header=None)
print("mut_single shape:",data1.shape)
data1.columns = ['mut','supp']

data3 = data2.copy()

data3['supp_mut_1'] = ''
data3['supp_mut_2'] = ''
data3['supp_mut_3'] = ''

print("-"*30)
for row in data3.itertuples(index=False):
    mut_1 = row.mut_1
    mut_2 = row.mut_2
    mut_3 = row.mut_3
    ### 
    supp_mut_2 = data1.loc[data1['mut'] == mut_2, 'supp']
    supp_mut_1 = data1.loc[data1['mut'] == mut_1, 'supp']
    supp_mut_3 = data1.loc[data1['mut'] == mut_3, 'supp']
    if supp_mut_1.empty:
        print(mut_1, "no supp in m1n1_file")
        continue  
    if supp_mut_2.empty:
        print(mut_2, "no supp in m1n1_file")
        continue  
    if supp_mut_3.empty:
        print(mut_3, "no supp in m1n1_file")
        continue
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2) & (data3['mut_3'] == mut_3),'supp_mut_1'] = supp_mut_1.values[0]
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2) & (data3['mut_3'] == mut_3), 'supp_mut_2'] = supp_mut_2.values[0]
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2) & (data3['mut_3'] == mut_3), 'supp_mut_3'] = supp_mut_3.values[0]

data3['donor_count'] = donor_count
data3['mean_mut'] = mean_mut
data3['co-score'] = data3['supp'] / (np.log10(data3['donor_count']) + np.log10(data3['mean_mut']))
data3.to_csv(args['o'], index=False)

print("Done.")
