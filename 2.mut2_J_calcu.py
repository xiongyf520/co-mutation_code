### function:calculate J of second-order mutatoin pairs
### xyf
### 1.import
import pandas as pd
from pandas import DataFrame
import numpy as np
import scipy
import argparse

### 2.input output file
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i_pair',help='input file - muation pair mut ratio file')
parser.add_argument(
    '-i_single',help='input file - single mutation mut ratio file')

parser.add_argument(
    '-n',help='donor number all (int)')
parser.add_argument(
    '-o',help='output file with pair odds ratio and confidence')

args = vars(parser.parse_args())
donor_number = int(args['n'])
print("Read input data...")
### 3.arrange raw data
data2 = pd.read_csv(args['i_pair'],sep=' ',header=None)
data2.columns = ['mut_1','mut_2','supp']
print("mut_pair shape:", data2.shape)
data2 = data2.drop_duplicates()
print("drop duplicaties, mut_pair shape:", data2.shape)

data1 = pd.read_csv(args['i_single'],sep=' ',header=None)
print("mut_single shape:",data1.shape)
data1.columns = ['mut','supp']

data3 = data2.copy()

data3['supp_mut_1'] = ''
data3['supp_mut_2'] = ''
data3['J'] = np.nan
### 4.J
print("-"*30)
print("start J ...")
for row in data3.itertuples(index=False):
    mut_1 = row.mut_1
    mut_2 = row.mut_2
    ### 
    supp_mut_2 = data1.loc[data1['mut'] == mut_2, 'supp']
    supp_mut_1 = data1.loc[data1['mut'] == mut_1, 'supp']
    if supp_mut_1.empty:
        print(mut_1, "no supp in m1n1_file")
        continue  
    if supp_mut_2.empty:
        print(mut_2, "no supp in m1n1_file")
        continue  
    a = row.supp
    b = supp_mut_2.values[0] - a
    c = supp_mut_1.values[0] - a 
    # Jaccard Index
    jaccard_index = a / (a + b + c)
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'supp_mut_1'] = supp_mut_1.values[0]
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'supp_mut_2'] = supp_mut_2.values[0]
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'J'] = jaccard_index

# save data3
data3.to_csv(args['o'], index=False)

print("Jaccard index done.")




