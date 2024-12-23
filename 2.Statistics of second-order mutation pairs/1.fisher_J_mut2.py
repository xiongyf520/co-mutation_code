### Function: Calculate Jaccard index and Fisher's exact test for second-order mutation pairs.
### Author: Yangfang Xiong

import pandas as pd
from pandas import DataFrame
import numpy as np
import scipy
from scipy.stats import fisher_exact
import argparse

### Input output file
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i_pair',help='input file - muation pair data (fp m2n2 out)')
parser.add_argument(
    '-i_single',help='input file - single mutation data (fp m1n1 out)')
parser.add_argument(
    '-n',help='donor number of cancer (int)')
parser.add_argument(
    '-o',help='output file with fisher and J')
parser.add_argument(
    '-error',help='error file no mut in data1')

### Arrange raw data
args = vars(parser.parse_args())
donor_number = int(args['n'])
print("Read input data...")
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
data3['donor_count'] = donor_number 
data3['J'] = np.nan
data3['fisher_p'] = np.nan
error_rows = []

### Calculate Jaccard index and Fisher's exact test
for row in data3.itertuples():
    mut_1 = row.mut_1
    mut_2 = row.mut_2
    try:
        supp_mut_2 = data1.loc[data1['mut'] == mut_2, 'supp'].iloc[0]
        supp_mut_1 = data1.loc[data1['mut'] == mut_1, 'supp'].iloc[0]
        data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'supp_mut_1'] = supp_mut_1
        data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'supp_mut_2'] = supp_mut_2
    except IndexError:
        print(f"Error: Mutations {mut_1}, {mut_2} not found in data1.")
        error_rows.append(row)
        data3.drop(row.Index, inplace=True)
        continue
    a = row.supp
    b = supp_mut_2 - a
    c = supp_mut_1 - a
    d = donor_number - a - b - c
    # Jaccard Index calculation
    jaccard_index = a / (a + b + c)
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'J'] = jaccard_index
    # Construct the contingency table
    table = [[a, max(b, 1)], [max(c, 1), d]]
    # Calculate Fisher's exact test
    fisher_p = fisher_exact([[a,b],[c,d]],alternative = 'greater')[1]
    # Store the Fisher's exact test p-value
    data3.loc[(data3['mut_1'] == mut_1) & (data3['mut_2'] == mut_2), 'fisher_p'] = fisher_p
if error_rows:
    error_df = pd.DataFrame(error_rows)
    error_df.to_csv(args['error'], index=False)
    print(f"Error file saved with {len(error_rows)} rows.")
# Save the modified data3 to a new file
data3.to_csv(args['o'], index=False)