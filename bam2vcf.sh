module load GCC/10.2.0
module load SAMtools/1.16.1


inbam=$1 # input bam file
prefix=`basename ${inbam} .bam`
echo $prefix
wkdir=$2 # output dir
reference=$3 # reference file when alining the bam file

outdir="${wkdir}/${prefix}" # output folder (modify this if you want to have different output folders for each input file)
#reference="/data/maiziezhou_lab/Softwares/refdata-GRCh38-2.1.0/fasta/genome.fa" # if using other reference, please change it here

# create output dir
if [ -d "$outdir" ]; then
    echo "Directory $outdir already exists. Reuse it."
else
    echo "Directory $outdir does not exist. Created it."
    mkdir -p "$outdir"
fi

# sort bam file
samtools sort "$inbam" -o "$outdir/sorted.bam"
samtools index "$outdir/sorted.bam"

#extract chrom1-22 and X Y
#modify mapq and base quality
samtools view -H "$inbam" > "$outdir/raw.sam"

samtools view "$outdir/sorted.bam" \
    chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11 chr12 chr13 chr14 chr15 chr16 chr17 chr18 chr19 chr20 chr21 chr22 chrX chrY \
    | awk 'BEGIN{FS=OFS="\t"} {len=length($10); str=sprintf("%*s", len, ""); gsub(/ /, "F", str); $11=str;$5=60; print }' \
    >> "$outdir/raw.sam"

samtools sort "$outdir/raw.sam" -o "$outdir/new.bam"
samtools index "$outdir/new.bam"
rm "$outdir/raw.sam"
rm $outdir/sorted.bam

# add read group
ml picard/2.17.10
java -jar "$EBROOTPICARD/picard.jar" AddOrReplaceReadGroups \
    I="$outdir/new.bam" \
    O="$outdir/new_rg.bam" \
    RGID=4 \
    RGLB=lib1 \
    RGPL=ILLUMINA \
    RGPU=unit1 \
    RGSM=20
samtools index "$outdir/new_rg.bam"

# gatk variant call
java -Xmx4g -jar "/gpfs52/data/maiziezhou_lab/Summer_research2023/bam2vcf//gatk/gatk-package-4.0.3.0-local.jar" HaplotypeCaller \
    --input "$outdir/new_rg.bam" \
    --output "$outdir/new_rg.vcf" \
    --reference "$reference" \
    --disable-tool-default-read-filters true \
    --disable-sequence-dictionary-validation true \
    --bam-output "$outdir/new_rg_cover_variants.bam"

