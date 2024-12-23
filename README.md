# Co-mutation Scripts
## Introduction
This project provides a set of scripts for mining of co-occurring mutation pairs, which includes steps for data preprocessing, applying the Frequent Pattern Growth (FP-Growth) algorithm, calculating co-scores, and computing the Jaccard index and Fisher's exact test.

## File Description
### 0.SSM_preprocessing
- `1.ssm_liftover_and_filter_repeat.sh`: - Use liftOver to convert the genome version; Filter simple somatic mutations (SSMs) located in repeat regions
- `2.ssm_data_arrange.py`: Filter out cancer types with fewer than 100 donors; Split the SSMs data by cancer type to prepare the input for the FP-growth algorithm.
### 1.FP-growth
- `fp_cancers.py`: FP-growth input arrangement and running.
- `fp_cancers.sh`: Template to use the `fp_cancers.py`
- `batch_submit_cancertype.sh`: Submit FP-growth tasks in batches by cancers using the slurm job system.
### 2.Statistics of second-order mutation pairs
- `1.fisher_J_mut2.py`: Calculate Jaccard index and Fisher's exact test for second-order mutation pairs.
- `2.fisher_J_mut2_batch.sh`: Batch submit `1.fisher_J_mut2.py` script for each cancer.
- `3.co-scores_calcu.py`: Calculate co-scores for each second-order mutation pair.
- `4.co-scores_calcu_batch.sh`: Batch submit `3.co-scores_calcu.py` script for each cancer.
### 3.Statistics of third-order mutation pairs
- `1.mut3_supp_score.py`: Calculate co-scores for each third-order mutation pair.
- `2.mut3_supp_score.sh`: Batch submit `1.mut3_supp_score.py` script for each cancer.
## Dependencies
- Python 3.x
- Required Python modules: pandas, numpy, subprocess, argparse, os, scipy.
- Please install FP-growth from: https://borgelt.net/doc/fpgrowth/fpgrowth.html 
- Unix/Linux operating system.
## Citation
Coming soon...
