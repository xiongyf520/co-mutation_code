#!/bin/bash

### Functions: Change hg19 to hg38, and filter mutations in repeat regions.
### Author: Yangfang Xiong

# input 
chain_file="~/software/hg19ToHg38.over.chain.gz" 
### Download from UCSC: https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz
repeatmasker_bed="~/ref/repeatmasker_hg38.bed"
### Download from UCSC Table Broswer
input_file="../data/simple_somatic_mutation.cut.tsv"
### Download from ICGC Data Portal

# output
temp_bed="../data/ssm_hg19_liftover_input.bed"
lifted_bed="../data/ssm_hg38_lifted.bed"
unlifted_bed="../data/ssm_unlifted.bed"
filtered_bed="../data/ssm_filtered_repeat.bed"
output_file="../data/ssm_filtered_repeat.tsv"

echo "Begin... $(date)"
# Step 1:  Arrange the input file into BED format
awk -F'\t' 'NR > 1 {
    # Merge all columns except chromosome, start position, and end position
    info = $1; 
    for (i = 2; i <= NF; i++) {
        if (i != 4 && i != 5 && i != 6) {
            info = info ";" $i;
        }
    }
    print "chr"$4, $5-1, $6, info;  # BED format
}' OFS='\t' "$input_file" > "$temp_bed"


# Step 2: Converting genome versions using the LiftOver tool
 liftOver "$temp_bed" "$chain_file" "$lifted_bed" "$unlifted_bed"

# Step 3: Filter out mutations in repeat regions while retaining original information
bedtools intersect -v -a "$lifted_bed" -b "$repeatmasker_bed" > "$filtered_bed"

echo "Filter repeat done.$(date)"