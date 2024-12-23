#!/bin/bash

# Funtion: Batch submit fisher J test for each cancer type
# Author: Yangfang Xiong

echo "Begin ... $(date)"
project_dir=~/project/co-mutation/co-mut_icgc
input_dir=${project_dir}/results/fp_out_filter_repeat
output_dir="${project_dir}/results/mut2_fisher_filter_repeat"
cancertype_file="${project_dir}/data/cancer_donor_count.txt"
job_dir="${project_dir}/bin/.mut2_fisher_jobs"
error_dir="${project_dir}/results/mut2_fisher_filter_repeat_error"

# Check if the output directory exists, if not, create it
if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "$output_dir already exists. Deleting and recreating..."
  rm -r "$output_dir"
  mkdir -p "${output_dir}"
fi

if [ ! -d "$job_dir" ]; then
  mkdir -p "$job_dir"
fi
if [ ! -d "$error_dir" ]; then
  mkdir -p "$error_dir"
fi
# Constrcut slurm jobs for each cancer type
while IFS=$'\t' read -r cancertype count
  do
  echo "Processing cancertype: $cancertype, count: ${count}"
  error_file=${error_dir}/${cancertype}_error.csv
  script_file="${job_dir}/submit_${cancertype}_fisherJ.sh"
  cat > "$script_file" <<EOL
#!/bin/bash
#SBATCH --job-name=fisher_${cancertype}
#SBATCH --get-user-env
#SBATCH --partition=C064M0256G
#SBATCH --nodes=1
#SBATCH -c 20
#SBATCH --time=3-00:00:00
#SBATCH --output=./slurm_out/fisher_${cancertype}.out

python 1.fisher_J_mut2.py\
    -i_single ${input_dir}/${cancertype}_s2m1n1.txt\
    -i_pair ${input_dir}/${cancertype}_s2m2n2.txt\
    -o ${output_dir}/${cancertype}_fisher.csv\
    -n ${count}\
    -error ${error_file}
EOL
  # Submit the job
  sbatch "$script_file"
done < "$cancertype_file"
echo "All cancer fisher j submit. $(date)"