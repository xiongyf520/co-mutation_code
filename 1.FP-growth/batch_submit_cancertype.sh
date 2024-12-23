#!/bin/bash
# Funtion: Submit FP-growth tasks in batches by cancers using the slurm job system.
# Author: Yangfang Xiong
#
# input:
# prefix: prefix of the submit file, e.g. "fp_cancertype.sh"
# sample_list: a list of cancer names, e.g. "cancertype.txt"
#
# output:
# submit_file: a submit file, e.g. "fp_cancertype.cancertype.txt.submit.sh"
# than you can submit the submit file by "sh fp_cancertype.cancertype.txt.submit.sh"


prefix=$1
### FP-growth template
sample_list=$2
### cancer names list

prefix=`echo ${prefix} | sed 's/.sh//g' -`
sample_list_prefix=`echo ${sample_list} | sed 's/.txt//g' -`
submit_file=${prefix}.${sample_list_prefix}.submit.sh

jobs_dir=./${prefix}_jobs/
if [ ! -d "./${prefix}_jobs/" ];then
    mkdir ./${prefix}_jobs/
else
    echo "./${prefix}_jobs/ already exists."
fi
if [ -f ${submit_file} ]; then
    rm -i ${submit_file};
fi

if [ -f ${submit_file} ]; then
    echo "${submit_file} exist"
else
    template=${prefix}.sh
    for i in $(cat ${sample_list});
    do id=${i}
        cp ${template} ${jobs_dir}${prefix}.${id}.sh;
        sed -i "s/cancertype/${id}/g" ${jobs_dir}${prefix}.${id}.sh;
	echo "sbatch ${jobs_dir}${prefix}.${id}.sh" >> ${submit_file};
    done
    chmod 770 ${submit_file}
    echo "template: ${prefix}.sh"
    echo "sample list: ${sample_list}"
    echo "to submit: ${submit_file}"
fi
