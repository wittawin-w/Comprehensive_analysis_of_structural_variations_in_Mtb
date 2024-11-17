#!/usr/bin/bash

bamfile=$1
ref=$2
output_dir=$3

python2 /path/to/manta-1.6.0/build/bin/configManta.py \
--bam $bamfile \
--referenceFasta $ref \
--runDir $output_dir
exit_value=$?
if [ $exit_value != 0 ]; then
echo "ERROR with configManta.py $exit_value"
exit
else
echo "configManta.py status OK"
fi 

python2 $output_dir/runWorkflow.py
exit_value=$?
if [ $exit_value != 0 ]; then
echo "ERROR with runWorkflow.py $exit_value"
exit
else
echo "Complete MANTA SV caller"
fi

