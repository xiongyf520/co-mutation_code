# Functions: Calculate co-scores for each mutation pair.
# Author: Yangfang Xiong

import argparse
import pandas as pd
import os
import numpy as np

def process_fisher_file(fisher_file, cancer_mean_mut_file, output_folder):
    # Read cancer_mean_mut.txt（includes cancer amd mean_mut）
    cancer_mean_mut = pd.read_csv(cancer_mean_mut_file)
    cancer_mean_mut.set_index('cancer', inplace=True)
    # Read fisher.csv
    fisher_df = pd.read_csv(fisher_file)
    cancer_name = os.path.basename(fisher_file).split('_')[0]
    # Check if cancer_name exists in cancer_mean_mut
    if cancer_name in cancer_mean_mut.index:
        mean_mut = cancer_mean_mut.loc[cancer_name, 'mu_count']
    else:
        print(f"Warning: {fisher_file} do not have the mean_mut data for {cancer_name}.")
        mean_mut = np.nan
    # Add mean_mut to the DataFrame
    fisher_df['mean_mut'] = mean_mut
    # Calculate co-scores
    fisher_df['co-score'] = fisher_df['supp'] / (np.log10(fisher_df['donor_count']) + np.log10(fisher_df['mean_mut']))
    # Create output file path
    output_file = os.path.join(output_folder, os.path.basename(fisher_file).replace('.csv', '_scores.csv'))
    # Save
    fisher_df.to_csv(output_file, index=False)
    print(f"Processed: {output_file}")

def main():
    #  argparse input
    parser = argparse.ArgumentParser(description='Process Fisher statistics files and add mean mutation rates.')
    parser.add_argument('--fisher_folder', required=True, help='Folder containing the cancer_fisher.csv files')
    parser.add_argument('--output_folder', required=True, help='Folder to save processed files')
    parser.add_argument('--cancer_mean_mut_file', required=True, help='File containing cancer mean mutation rates')
    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    for file in os.listdir(args.fisher_folder):
        if file.endswith('.csv'):
            fisher_file = os.path.join(args.fisher_folder, file)
            process_fisher_file(fisher_file, args.cancer_mean_mut_file, args.output_folder)
if __name__ == "__main__":
    main()
