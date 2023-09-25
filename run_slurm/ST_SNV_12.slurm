#!/bin/bash
#################
#SBATCH --job-name=ST_SNV
#################  
#SBATCH --output=VCF_all_12.out
#################
#SBATCH --error=VCF_all_12.err
#################
#SBATCH --time=7-00:00:00
#SBATCH --account=cgw_maizie3
#SBATCH --partition=cgw-maizie3
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=30
#################
#SBATCH --mem=500GB
#################
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=han.liu.1@vanderbilt.edu

#module load Anaconda3/2022.05
#module load GCC/11.3.0
#module load SAMtools/1.18

echo "SLURM_JOBID: " $SLURM_JOBID

python main.py