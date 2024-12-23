#!/bin/bash

# Funtion: Batch submit co-scores calculation of third-order mutation pairs for each cancer type
# Author: Yangfang Xiong

echo "Begin ... $(date)"
project_dir=~/project/co-mutation/co-mut_icgc
input_dir=${project_dir}/results/fp_out_filter_repeat
output_dir="${project_dir}/results/mut3_scores"
cancertype_file="${project_dir}/data/cancer_donor_count.csv"
mean_mut_file="${project_dir}/data/mean_mut_count.csv"
job_dir="${project_dir}/bin/.mut3_scores_jobs"

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

while IFS=$',' read -r cancertype count
  do
  mean_mut=$(awk -F',' -v cancer="$cancertype" '$1 == cancer {print $2}' "$mean_mut_file")
  echo "Processing cancertype: $cancertype, count: ${count}, mean_mut: ${mean_mut}"
  error_file=${error_dir}/${cancertype}_error.csv
  script_file="${job_dir}/submit_${cancertype}.sh"
  cat > "$script_file" <<EOL
#!/bin/bash
#SBATCH --job-name=mut3_${cancertype}
#SBATCH --get-user-env
#SBATCH --partition=C064M0256G
#SBATCH --nodes=1
#SBATCH -c 10
#SBATCH --output=./slurm_out/mut3_${cancertype}.out

python 1.mut3_supp_score.py\
    -i_single ${input_dir}/${cancertype}_s2m1n1.txt\
    -i_pair3 ${input_dir}/${cancertype}_s2m3n3.txt\
    -o ${output_dir}/${cancertype}_scores.csv\
    -n ${count}\
    -m ${mean_mut}
EOL
  # Submit the job
  sbatch "$script_file"
done < "$cancertype_file"
echo "All cancers have been submitted. $(date)"
