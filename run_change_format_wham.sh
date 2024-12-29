#!/usr/bin/bash

input_dir=$1
output_dir=$2
caller=$3

if [ ! -d $input_dir ]; then
        echo "NEED input directory"
        exit
fi

if [ ! -d $output_dir ]; then
        mkdir $output_dir
        echo "Output directory has been created"
fi

for file in $input_dir/*.gt.vcf; do
file2=$file
echo $file2
file_name=$(basename $file2 .gt.vcf)
python /path/to/wham_re_formating.py $file2 > $output_dir/${file_name}.txt
awk -v name="$file_name" -v OFS='\t' '{print name, $0}' $output_dir/${file_name}.txt > $output_dir/${file_name}_addname.txt
awk -v svcaller="$caller" -v OFS='\t' '{print svcaller, $0}' $output_dir/${file_name}_addname.txt > $output_dir/${caller}_${file_name}_addname.txt
rm $output_dir/${file_name}.txt
rm $output_dir/${file_name}_addname.txt
done
echo "FINISH"
