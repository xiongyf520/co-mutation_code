import pandas as pd
### df1 3mut supp merged data; df2 2mut supp merged data
df1 = pd.read_csv("Third-order mutation pais results file")
df2 = pd.read_csv("Second-order mutation pairs results file")
# Jaccard Index
jaccard_indices = []
for index, row in df1.iterrows():
    cancer_type = row['cancer']
    mut1, mut2, mut3 = row['mut_1'], row['mut_2'], row['mut_3']
    supp_1, supp_2, supp_3 = row['supp_mut_1'], row['supp_mut_2'], row['supp_mut_3']
    supp_triplet = row['supp']
    df2_filtered = df2[df2['cancer'] == cancer_type] 
    supp_pair1 = df2_filtered[(df2_filtered['mut_1'] == mut1) & (df2_filtered['mut_2'] == mut2)]['supp'].values
    supp_pair1 = supp_pair1[0] if len(supp_pair1) > 0 else 0
    supp_pair2 = df2_filtered[(df2_filtered['mut_1'] == mut1) & (df2_filtered['mut_2'] == mut3)]['supp'].values
    supp_pair2 = supp_pair2[0] if len(supp_pair2) > 0 else 0
    supp_pair3 = df2_filtered[(df2_filtered['mut_1'] == mut2) & (df2_filtered['mut_2'] == mut3)]['supp'].values
    supp_pair3 = supp_pair3[0] if len(supp_pair3) > 0 else 0
    union_size = supp_1 + supp_2 + supp_3 - supp_pair1 - supp_pair2 - supp_pair3 + supp_triplet
    # Jaccard
    jaccard_index = supp_triplet / union_size if union_size > 0 else 0
    jaccard_indices.append(jaccard_index)

# save
df1['jaccard_index'] = jaccard_indices

df1.to_csv("YOUR_OUTPUT_FILE_NAME", index=False)
