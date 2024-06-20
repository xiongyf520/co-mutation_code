#!/bin/bash

echo "Begin ... $(date)"
input_file_path=""
output_dir=""
cancer_donor_count_file=""

if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "目录 $output_dir 已存在,重新创建."
  rm -r "$output_dir"
  mkdir -p "${output_dir}"
fi
while IFS=' ' read -r cancertype count
do
echo "cancertype: $cancertype"
python 4.mut2_fisher_test.py \
	-i ${input_file_path}/${cancertype}_J.csv \
	-o ${output_dir}/${cancertype}_fisher.csv \
	-n ${count}
done <  cancertype_donor_count.txt
echo "Done. $(date)"












