#!/usr/bin/bash

input_dir=$1 #path to VCF files
bam_dir=$2 #path to bam files
output_dir=$3 #path to output directory

if [ ! -d $output_dir ]; then
mkdir $output_dir
echo "Create output directory for genotyping variants"
else
echo "Directory is already available"
fi

for file in $input_dir/*/*.vcf; do

sample_name=$(basename $file .vcf)
echo $sample_name
bamfile=$bam_dir/$sample_name/${sample_name}_sort_mkd.bam
if [ ! -f $bamfile ]; then
echo "Cannot find $bamfile"
exit
fi

output_dir2=$output_dir/$sample_name
if [ ! -d $output_dir2 ]; then
mkdir $output_dir2
fi

python /path/to/svtyper/svtyper/classic.py \
-i $file \
-B $bamfile \
-l $output_dir2/${sample_name}_sort_mkd.bam.json > $output_dir/${sample_name}.gt.vcf

exit_value=$?
if [ $exit_value != 0 ]; then
echo "SVtyper: ERROR"
else
echo "SVtyper: Finished"
fi

done
echo "All done"
