#!/bin/bash
#################
#SBATCH --job-name=ST_10
#################  
#SBATCH --output=VCF_10.out
#################
#SBATCH --error=VCF_10.err
#################
#SBATCH --time=30-00:00:00
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

sh bam2vcf.sh /data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_6.5mm_Visium_CytAssist_FFPE/CytAssist_FFPE_Protein_Expression_Human_Breast_Cancer_possorted_genome_bam.bam ./data/ /data/maiziezhou_lab/Softwares/refdata-GRCh38-2.1.0/fasta/genome.fa