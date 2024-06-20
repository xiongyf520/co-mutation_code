#!/bin/bash
dt_dir=YOUR_DATA_DIR
output_dir=YOUR_OUTPUT_DIR
if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
else
  echo "目录 $output_dir 已存在"
fi
python 1.fpgrowth.py -m ${dt_dir}/cancertype_donor_ssm.txt \
       -i ${output_dir}/cancertype_fp_5_input.txt \
       -o_1 ${output_dir}/cancertype_fp_5_m1n1_output.txt \
       -o_2 ${output_dir}/cancertype_fp_5_m2n2_output.txt \
       -o_3 ${output_dir}/cancertype_fp_5_m3n3_output.txt \
       -supp 5
echo "Done. $(date)"

