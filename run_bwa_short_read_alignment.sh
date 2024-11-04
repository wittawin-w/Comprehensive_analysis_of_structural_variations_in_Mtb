#!/usr/bin/bash

input_dir=$1
output_dir=$2
reference_genome=$3

if [ ! -d $output_dir ]; then
mkdir $output_dir
echo "Create output directory"
else
echo "This name has been used for other directory"
echo "Try new one"
exit
fi

reference_dir=$(dirname $reference_genome)
reference_filename=$(basename $reference_genome)
echo "Check index files of reference genome in directory: $reference_dir"
index_files_status=false
bwt_filename=${reference_dir}/${reference_filename}.bwt
pac_filename=${reference_dir}/${reference_filename}.pac
ann_filename=${reference_dir}/${reference_filename}.ann
amb_filename=${reference_dir}/${reference_filename}.amb
sa_filename=${reference_dir}/${reference_filename}.sa
if [ -f $bwt_filename ] && [ -f $pac_filename ] && [ -f $ann_filename ] && [ -f $amb_filename ] && [ -f $sa_filename ]; then
index_files_status=true
fi

if [ $index_files_status = false ]; then
echo "At least one of index files is missing"
echo "Create index files for $reference_genome"
bwa index $reference_genome
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Create index files for reference genome: ERROR"
exit
else
echo "Create index files for reference genome: Completed"
fi
else
echo "All index files are available"
fi

for file in $input_dir/*_R1.paired.fq.gz; do
sample_id=$(basename $file _R1.paired.fq.gz)
fastq1=$file
fastq2=$input_dir/${sample_id}_R2.paired.fq.gz
echo "Sample_id: $sample_id"
output_dir2=$output_dir/$sample_id
if [ ! -d $output_dir2 ]; then
mkdir $output_dir2
fi

echo "Check available of fastq files"
fastq_files_status=false
if [ -f $fastq1 ] && [ -f $fastq2 ]; then
fastq_files_status=true
fi

if [ $fastq_files_status = false ]; then
echo "One of fastq files of $sample_id is missing"
continue
else
echo "Both forward and reverse fastq files are available"
fi

echo "Align reads to reference genome"
bwa mem $reference_genome $fastq1 $fastq2 -t 8 -R "@RG\tID:${sample_id}\tSM:${sample_id}\tSQ:bwa" > $output_dir/${sample_id}.sam
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Align reads of $sample_id to reference genome: ERROR"
continue
else
echo "Align reads of $sample_id to reference genome: Completed"
fi

echo "Convert SAM to BAM"
samtools view -S -b $output_dir/${sample_id}.sam > $output_dir/${sample_id}.bam
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Convert SAM of $sample_id to BAM: ERROR"
continue
else
echo "Convert SAM of $sample_id to BAM: Completed"
fi

echo "Sort BAM"
samtools sort -o $output_dir/${sample_id}_sorted.bam $output_dir/${sample_id}.bam
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Sort BAM of $sample_id: ERROR"
continue
else
echo "Sort BAM of $sample_id: Completed"
fi

echo "Index sorted BAM" 
samtools index $output_dir/${sample_id}_sorted.bam
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Index sorted BAM of $sample_id: ERROR"
continue
else
echo "Index sorted BAM of $sample_id: Completed"
fi

rm $output_dir/${sample_id}.sam
rm $output_dir/${sample_id}.bam
done

echo "Finish"











