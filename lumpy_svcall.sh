#!/usr/bin/bash

bamfile=$1 # input bamfile
output_dir=$2 #path to output directory
tmp_dir=$3 #path to temporary directory
ref=$4 #path to fasta file of reference genome
if [ -d $output_dir ]; then
	echo "output directory for LUMPY is exist!!!"
else
	echo "NEED output directory !!!"
	exit
fi

if [ -d $tmp_dir ]; then
	echo "temporary directory for LUMPY is exist!!!"
else
	echo "NEED temporary directory for LUMPY"
	exit
fi

sample_name=$(basename $bamfile _sort_mkd.bam)
samtools view -b -F 1294 $bamfile > $tmp_dir/${sample_name}_discord.bam
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR: samtools view -b -F 1294: $exit_value"
	exit
else
	echo "Discordant pair bam: OK"
fi

samtools view -h $bamfile \
| /path/to/lumpy-sv/scripts/extractSplitReads_BwaMem -i stdin \
| samtools view -Sb - > $tmp_dir/${sample_name}_spliter.bam
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR: slpit read bam: $exit_value"
	exit
else
	echo "Split read bam: OK"
fi

echo "apply lumpyexpress"
/path/to/lumpyexpress \
-B $bamfile \
-S $tmp_dir/${sample_name}_spliter.bam \
-D $tmp_dir/${sample_name}_discord.bam \
-R $ref \
-o $output_dir/${sample_name}_lumpy.vcf
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR: lumpyexpress svcaller: $exit_value"
	exit
else
	echo "lumpyexpress finish status: OK"
fi

#echo "remove temporary directory"
echo "Finish LUMPY"
