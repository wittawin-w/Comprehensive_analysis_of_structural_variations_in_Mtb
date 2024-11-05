#!/usr/bin/bash

#GATK needs to be installed

input_dir=$1

for file in $input_dir/*sort.bam; do
file_name=$(basename $file _sort.bam)
echo $file_name
gatk MarkDuplicates \
-I $input_dir/${file_name}_sort.bam \
-O $input_dir/${file_name}_sort_mkd.bam \
-M $input_dir/${file_name}_sort_mkd.txt
exit_value=$?
if [ $exit_value != 0 ]; then
echo "Marks duplicated reads: ERROR"
exit
else
echo "Marks duplicated reads: COMPLETED"
fi

done
echo "Marks duplicated reads: Finished"
