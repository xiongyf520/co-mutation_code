
### 1.import
import pandas as pd
from pandas import DataFrame
import numpy as np
import scipy
from scipy.stats import fisher_exact
import argparse

### 2.input output file
parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',help='input file - muation pair results after J calculation')
parser.add_argument(
    '-n',help='donor number(int)')
parser.add_argument(
    '-o',help='output file with fisher p')
args = vars(parser.parse_args())
donor_number = int(args['n'])
print("Read input data...")
### 3.arrange raw data
data = pd.read_csv(args['i'])
print("input file shape:", data.shape)
data1 = data.copy()
data1['fisher_p'] = np.nan
### 4.fisher
print("-"*30)
print("start fisher...")
for row in data1.itertuples(index=False):
    mut_1 = row.mut_1
    mut_2 = row.mut_2
    supp_mut_2 = row.supp_mut_2
    supp_mut_1 = row.supp_mut_1
    a = row.supp
    b = supp_mut_2 - a
    c = supp_mut_1 - a
    d = donor_number - a - b - c
    if b == 0:
        b = b +1
    if c ==0 :
        c = c +1
    table = [[a, b], [c, d]]
    fisher_p = fisher_exact([[a,b],[c,d]],alternative = 'greater')[1]
    data1.loc[(data1['mut_1'] == mut_1) & (data1['mut_2'] == mut_2), 'fisher_p'] = fisher_p

data1.to_csv(args['o'], index=False)
print("Fisher test Done.")




