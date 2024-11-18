#!/usr/bin/bash

vcf_file=$1
output_dir=$2
caller_id=$3

if [ ! -d $output_dir ]; then
	mkdir $output_dir
	echo "creat output directory"
fi

dir_name=$(dirname $vcf_file)
echo $dir_name
file_name=$(echo $dir_name | cut -d'/' -f 7) #edit this base on your path to vcf file
echo $file_name
echo $vcf_file

gunzip -c $vcf_file > $output_dir/${file_name}.vcf
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "error with unzip"
	exit
	echo "unzip: OK"
fi

python3 /path/to/manta_re_formating.py $output_dir/${file_name}.vcf > $output_dir/${file_name}.txt
exit_value=$?
if [ $exit_value != 0 ]; then
        echo "error with reformat file"
        exit
else
        echo "reformat: OK"
fi

awk -v name="$file_name" -v OFS='\t' '{print name,$0}' $output_dir/${file_name}.txt > $output_dir/${file_name}_addname.txt
awk -v svcaller="$caller" -v OFS='\t' '{print svcaller,$0}' $output_dir/${file_name}_addname.txt > $output_dir/${caller_id}_${file_name}_addname.txt
rm $output_dir/${file_name}_addname.txt
rm $output_dir/${file_name}.txt
rm $output_dir/${file_name}.vcf
