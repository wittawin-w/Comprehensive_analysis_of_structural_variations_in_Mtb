#!/usr/bin/bash
input_dir=$1
output_dir=$2
bp=$3

if [ ! -d $output_dir ]; then
	mkdir $output_dir
	echo "create output directory for merging variants"
fi

tmp_dir=$output_dir/tmp_dir
if [ ! -d $tmp_dir ]; then
        mkdir $tmp_dir
fi

for file in $input_dir/*_all_callers_merged.txt; do
        sample_name=$(basename $file _all_callers_merged.txt)
        python3 path/to/unify_callset_remove_headline.py $file > $tmp_dir/${sample_name}_rm_headline.txt
        exit_value=$?
        if [ $exit_value != 0 ]; then
                echo "ERROR with removing headline"
                exit
        else
                echo "Remove headline sample ID: $sample_name OK"
        fi
        sleep 1
done
echo "Concatenate and sort calls from all samples"
cat $tmp_dir/*_rm_headline.txt | sort -k3,3n -k4,4n > $tmp_dir/merge_int1.txt
python3 path/to/unify_callset_allsam_bp.py $tmp_dir/merge_int1.txt $bp > $output_dir/unify_callset_allsample_bp.txt
exit_value=$?
if [ $exit_value != 0 ]; then
        echo "ERROR with merging all samples"
        exit
else
        echo "Merging all samples: OK"
fi
