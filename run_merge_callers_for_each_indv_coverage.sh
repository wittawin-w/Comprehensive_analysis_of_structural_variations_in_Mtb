#!/usr/bin/bash

sample_list=$1 #one line for one sample; name of samples in list must be identical with variant calling result file name of each sample
input_dir=$2 #directory contains sub directories of each caller
output_dir=$3
variant=$4 #DELETION/INSERTION/TENDEM_DUP/BND
min_size=$5
max_size=$6
crit_cov=$7

if [ ! -d $output_dir ]; then
	mkdir $output_dir
	echo "create output directory for merging variants"
fi

tmp_dir=$output_dir/tmp_dir
if [ ! -d $tmp_dir ]; then
        mkdir $tmp_dir
fi

while IFS='\t' read f1; do
        echo "sample name = $f1"
        sample_name=`echo $f1`
        for file in path/to/*_${sample_name}_addname.txt; do
                ls -lrt $file
                caller=$(basename $file _${sample_name}_addname.txt)
                echo "caller name = $caller"
                if [ $caller != "I" ]; then
                        echo "Non-IMSindel callers"
                        echo "Select size and type of $caller"
                        sleep 2
                        grep "$variant" $file | sort -k5,5n -k6,6n > $tmp_dir/int1_${caller}_${sample_name}.txt
                        python3 path/to/pre_select_var.py $tmp_dir/int1_${caller}_${sample_name}.txt $caller $variant $min_size $max_size > $tmp_dir/int2_${caller}_${sample_name}.txt
                        exit_value=$?
                        if [ $exit_value != 0 ]; then
                                echo "ERROR with selection size and type of $caller file"
                                exit
                        else
                                echo "Select size and type of $caller: OK"
                        fi
                else
                        echo "IMSindel"
                        echo "Select size and type of $caller"
                        sleep 1
                        python3 path/to/remove_headline.py $file > $tmp_dir/int0_${caller}_${sample_name}.txt
                        exit_value=$?
                        if [ $exit_value != 0 ]; then
                                echo "ERROR with remove headline of IMSindel file"
                                exit
                        else
                                echo "Remove headline of IMSindel file: OK"
                        fi
                        python3 path/to/pre_select_var.py $tmp_dir/int0_${caller}_${sample_name}.txt $caller $variant $min_size $max_size > $tmp_dir/int1_${caller}_${sample_name}.txt
                        exit_value=$?
                        if [ $exit_value != 0 ]; then
                                echo "ERROR with selection size and type"
                                exit
                        else
                                echo "Select size and type of IMSindel file: OK"
                        fi
                        sort -k5,5n -k6,6n $tmp_dir/int1_${caller}_${sample_name}.txt > $tmp_dir/int2_${caller}_${sample_name}.txt
                fi
        done
        echo "Concatenate list of variants called from 4 SV callers of $sample_name"
        cat $tmp_dir/int2_*_${sample_name}.txt | sort -k5,5n -k6,6n > $output_dir/${sample_name}_all_callers_pos_sorted.txt
        echo "Making unified SV set of sample: $sample_name"
        python3 path/to/merge_callers_for_each_indv_coverage.py $output_dir/${sample_name}_all_callers_pos_sorted.txt $crit_cov > $output_dir/${sample_name}_all_callers_merged.txt
        echo "Finish"
        sleep 2
done < $sample_list
rm -r $tmp_dir

