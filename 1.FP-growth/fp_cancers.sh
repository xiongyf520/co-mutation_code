#!/bin/bash
#---------------------
# Funtion: FP-growth tasks template using the slurm job system.
# Author: Yangfang Xiong
#---------------------
#SBATCH --job-name=fp_cancertype
#SBATCH --get-user-env
#SBATCH --cpu-freq=high
#SBATCH --partition=C064M0256G
#SBATCH --nodes=1
#SBATCH -c 60
#SBATCH --ntasks-per-node=20
#SBATCH --output=./slurm_out/slurm_%x.%j.out

echo "Begin ... $(date)"
output_dir="../results/fp_out"
dt_dir="../data/ssm_filter_repeat_cancer"

if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "$output_dir already exists."
fi

python 1.fp_cancers.py -m ${dt_dir}/cancertype.tsv \
       -i ${output_dir}/cancertype_s2_input.txt \
       -o_1 ${output_dir}/cancertype_s2m1n1.txt \
       -o_2 ${output_dir}/cancertype_s2m2n2.txt \
       -o_3 ${output_dir}/cancertype_s2m3n3.txt \
       -supp 2

echo "cancertype Done. $(date)"
