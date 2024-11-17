bamfile=$1 #input bam file
output_dir=$2 #path to output directory
ref=$3 #path to fasta of reference genome

if [ ! -d $output_dir ]; then
	echo "NEED output directory!!!"
	exit
fi

file_name=$(basename $bamfile .bam)

/path/to/wham/bin/whamg \
-a $ref \
-f $bamfile \
| perl /path/to/wham/utils/filtWhamG.pl > $output_dir/${file_name}.vcf

exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR with wham: $exit_value"
	exit
fi

