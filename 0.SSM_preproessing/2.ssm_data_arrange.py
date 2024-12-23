
### Functions: Filter cancers with donors less than 100; split ssm data by cancers for FP-growth input.
### Author: Yangfang Xiong

import pandas as pd
import numpy as np
import os

output_folder = '../data/ssm_filter_repeat_cancer'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Step 1: Read ssm data that have been filtered.
ssm_repeat_filtered = pd.read_table("../data/ssm_filtered_repeat.bed", 
                                    sep = "\t", header = None)
print(ssm_repeat_filtered.shape)
# Separate the fourth column with a semicolon and generate new columns
split_columns = ssm_repeat_filtered[3].str.split(';', expand=True)
# Merge the split columns with the original data
ssm_dt = pd.concat([ssm_repeat_filtered.iloc[:, :3], split_columns], axis=1)
# Rename columns
ssm_dt.columns = ["chr", "start", "end", "icgc_mutation_id", "icgc_donor_id",
                 "project_code", "chromosome_strand", "ref_allele",
                  "mutated_from_allele","mutated_to_allele","consequence_type"]

ssm_dt_raw = ssm_dt[["icgc_mutation_id", "icgc_donor_id", "project_code"]]
ssm_dt_raw['cancer'] = ssm_dt_raw['project_code'].str.extract(r'([A-Za-z]+)-')

# Step 2: Remove cancers with donor count less than 100 
# Get the count of unique donors for each cancer
cancer_donor_count = ssm_dt_raw.groupby('cancer')['icgc_donor_id'].nunique()
# Filter out cancers with donor count less than 100
cancers_to_keep = cancer_donor_count[cancer_donor_count >= 100].index
ssm_dt_raw = ssm_dt_raw[ssm_dt_raw['cancer'].isin(cancers_to_keep)]
# Save
donor_count = ssm_dt_raw.groupby('cancer')['icgc_donor_id'].nunique().reset_index()
donor_count.columns = ['cancer', 'donor_count']
donor_count.to_csv('cancer_donor_count.csv')

# Step 3: Remove duplicate rows
ssm_dt_raw_uniq = ssm_dt_raw.drop_duplicates()
ssm_dt_raw_uniq.to_csv("../data/ssm_repeat_filtered.tsv", sep="\t",header=True, index=False)
print("ssm_dt_raw_uniq shape:", ssm_dt_raw_uniq.shape)

# Step 4: Split the data by cancers and save it.
for cancer, group in ssm_dt_raw_uniq.groupby('cancer'):
    # Create a tsv file for each cancer, with the file name being the cancer name
    output_file = os.path.join(output_folder, f'{cancer}.tsv')
    group.to_csv(output_file, sep='\t', index=False)
    print(f"Save {cancer} data to {output_file}.")
