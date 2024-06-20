#!/bin/bash

echo "Begin ... $(date)"
output_dir=YOUR_OUTPUT_DIR
fp_out_dir="../results/fp_out_cancertype"  
cancaertype_dir="../data/ssm_in_cancertype"

if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "目录 $output_dir 已存在,重新创建."
  rm -r "$output_dir"
  mkdir -p "${output_dir}"
fi

if [ -f "../results/cancertype_donor_count.txt" ]; then
    rm "../results/cancertype_donor_count.txt"
fi

for file in "$cancaertype_dir"/*.txt; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")  
    filename="${filename%.*}"  
    cancertype="${filename%%_*}" 
    echo "cancertype: $cancertype"
    ### donor count:
    count=$(awk 'NR>1{print $2}' "$file" | sort -u | wc -l)
    echo "${cancertype} ${count}" >> ../results/cancertype_donor_count.txt
    python 2.mut2_J_calcu.py \
	    -i_pair ${fp_out_dir}/${cancertype}_fp_2_m2n2_output.txt \
	    -i_single ${fp_out_dir}/${cancertype}_fp_2_m1n1_freq.txt \
	    -o ${output_dir}/${cancertype}_J.csv \
	    -n ${count}
    echo "Done. $(date)"
  fi
done
echo "All done. $(date)"
