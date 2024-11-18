#!/usr/bin/bash

input_dir=$1 #Absolute path of MANTA output directory (the directory containing all sample directories)
output_dir=$2 #path to output directory
caller_id=$3 #provide M (MANTA)

if [ ! -d $input_dir ]; then
        echo "NEED input directory"
        exit
fi

if [ ! -d $output_dir ]; then
        mkdir $output_dir
        echo "Output directory has been created"
fi

for file in $input_dir/*/results/variants/diploidSV.vcf.gz; do
echo $file
sh /path/to/manta_re_formating.sh $file $output_dir $caller_id
done
echo "FINISH"

