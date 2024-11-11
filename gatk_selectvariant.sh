#!/usr/bin/bash

input_file=$1
output_dir=$2
reference_genome=$3
var_type=$4 #SNP or INDEL

#GATK needs to be installed

if [ ! -d $output_dir ]; then
	mkdir $output_dir
else
	echo "Output directory is available"
fi

outfile_name1=$(basename $input_file .vcf.gz)

echo "gunzip -c $input_file > $output_dir/${outfile_name1}.vcf"
gunzip -c $input_file > $output_dir/${outfile_name1}.vcf
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR with gunzip"
	exit
else
	echo "gunzip: Complete"
fi

vcf=`echo $output_dir/${outfile_name1}.vcf`

gatk SelectVariants \
-R $reference_genome \
-V $vcf \
--select-type-to-include $var_type \
-O $output_dir/${outfile_name1}_${var_type}.vcf

exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR with GATK-SelectVariants"
	exit
else
	echo "GATK-SelectVariants: Complete"
fi

rm $output_dir/${outfile_name1}.vcf  
