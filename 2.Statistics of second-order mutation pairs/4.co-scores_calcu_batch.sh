#!/bin/bash
#SBATCH --job-name=co-scores
#SBATCH --get-user-env
#SBATCH --partition=C064M0256G
#SBATCH --nodes=1
#SBATCH -n 8
#SBATCH --output=./slurm_out/co-scores.out

# Function: Calculate co-scores for each cancer type
# Author: Yangfang Xiong

project_dir="~/project/co-mutation/co-mut_icgc"
FISHER_FOLDER="${project_dir}/results/mut2_fisher_filter_repeat"  
cancer_mut_mean="${project_dir}/data/mean_mut_count.csv"
output_dir="${project_dir}/results/mut2_scores_filter_repeat"
slurm_jobs="./.scores_jobs"

if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "$output_dir already exists. Deleting and recreating..."
  rm -r "$output_dir"
  mkdir -p "${output_dir}"
fi
if [ ! -d "$slurm_jobs" ]; then
  mkdir -p "$slurm_jobs"
fi
PYTHON_SCRIPT="3.co-scores_calcu.py"  

echo "Begin...$(date)"
python ${PYTHON_SCRIPT} --fisher_folder ${FISHER_FOLDER}\
    --output_folder ${output_dir}\
    --cancer_mean_mut_file ${cancer_mut_mean}
echo "Done.$(date)"