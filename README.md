# Co-mutation Scripts
## Introduction
This project contains a set of scripts for co-mutation analysis, covering the functionalities of Frequent Pattern Growth (FP-Growth) algorithm, calculation of Jaccard index, and Fisher's exact test. These scripts are designed to analyze mutation pairs in cancer data and their statistical significance.

## File Structure
- `1.fpgrowth.py`: Data preprocessing and implements the FP-Growth algorithm to mine frequent itemsets.
- `1.fpgrowth.sh`: Shell script to run `1.fpgrowth.py`.
- `2.mut2_J_calcu.py`: Calculates the Jaccard index for second-order mutation pairs.
- `2.mut2_J_calcu.sh`: Shell script to run `2.mut2_J_calcu.py`.
- `3.mut2_fisher_test.py`: Performs Fisher's exact test on second-order mutation pairs.
- `4.mut2_fisher_test.sh`: Shell script to run `3.mut2_fisher_test.py`.
- `5.mut3_J_calcu.py`: Calculates the Jaccard index for third-order mutation pairs.

## Usage

### Run FP-Growth Algorithm
```bash
bash 1.fpgrowth.sh
```
- This script will run `1.fpgrowth.py` to generate frequent itemsets.
- Ensure to modify the `dt_dir` and `output_dir` variables in `1.fpgrowth.sh` to match your data directory and output directory.
- You can change the threshold in the script at will, and finally get a frequent mutation set of length 1, 2, and 3.
- The threshold of FP-growth can be edited in the 1.fpgrowth.py script

### Calculate Jaccard Index for Mutation Pairs
```bash
bash 2.mut2_J_calcu.sh
```
- This script will run `2.mut2_J_calcu.py` to calculate the Jaccard index and generate result files.
- Ensure to modify the `output_dir`, `fp_out_dir`, and `cancaertype_dir` variables in `2.mut2_J_calcu.sh` to match your directory structure.

### Perform Fisher's Exact Test on Mutation Pairs
```bash
bash 4.mut2_fisher_test.sh
```
- This script will run `3.mut2_fisher_test.py` to perform Fisher's exact test and generate result files.
- Ensure to specify the correct input file paths and output directory in the script.

### Calculate Jaccard Index for Third-order Mutation Pairs
```bash
bash 5.mut3_J_calcu.py
```
- This script need both second-order and third-order mutation pairs frequency data.

## Dependencies
- Python 3.x
- Required Python libraries: can be found at the top of each Python script
- Please install FP-growth from: https://borgelt.net/doc/fpgrowth/fpgrowth.html 
- Unix/Linux operating system (to run the shell scripts)
