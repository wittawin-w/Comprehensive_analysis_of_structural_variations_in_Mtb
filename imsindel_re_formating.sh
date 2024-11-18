#!/usr/bin/bash


input_dir=$1 #path to output directory of IMSindel (main output directory)
output_dir=$2 #path to output directory
caller_id=$3 # provide I (IMSindel)

if [ ! -d $output_dir ];then
	echo "NEED output directory"
	exit
fi

dir_name=$(dirname $ims_file)
file_name=$(basename $dir_name)

for file in $input_dir/*/*.out; do
python3 /path/to/imsindel_re_formating.py $file $file_name $caller_id > $output_dir/${caller}_${file_name}_addname.txt
done


