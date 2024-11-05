#!/usr/bin/bash

ref=$1
bamfile=$2
out_dir=$3

#GATK needs to be installed

if [ ! -d $out_dir ]; then
	echo "NEED output directory!!!"
	exit
else
	echo "directory for HaplotypeCaller is exist"
fi

file_name=$(basename $bamfile _sort_mkd.bam)
echo "start running samtools index with $file_name"
samtools index $bamfile 
exit_value=$?
if [ $exit_value != 0 ]; then
        echo "ERROR in samtools index: $exit_value"
        exit
else
        echo "samtools index finish status: OK"
fi

echo "start running GATK Haplotypecaller with $file_name"
java -Xmx64m -jar /home/ww160494/tools/gatk-4.2.0.0/gatk-package-4.2.0.0-local.jar HaplotypeCaller \
-ploidy 2 \
-mbq 20 \
-A MappingQualityRankSumTest \
-A ReadPosRankSumTest \
-R $ref \
-I $bamfile \
-O $out_dir/${file_name}.g.vcf.gz \
-ERC GVCF

exit_value=$?
if [ $exit_value != 0 ]; then
        echo "ERROR in haplotypecaller: $exit_value"
        exit
else
        echo "Haplotypecaller finish status: OK"
fi

