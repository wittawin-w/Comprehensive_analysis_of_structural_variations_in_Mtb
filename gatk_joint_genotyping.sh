#!/usr/bin/bash

input_dir=$1
output_dir=$2
ref=$3

#GATK needs to be installed

echo "start making sample list for GenomicDBImport"
for file in $input_dir/*.g.vcf.gz; do
echo "$file"
sample_name=$(bcftools query -l $file)
echo -e "$sample_name\t$file" >> $output_dir/samples.map
exit_value=$?
if [ $exit_value != 0 ]; then
	echo "ERROR $exit_value"
	exit
fi
done

echo "Finish creat sample.map file"


echo "start GenomicsDBImport"
gatk \
GenomicsDBImport \
--genomicsdb-workspace-path $output_dir/my_database_genomicsDBImport \
--batch-size 25 \
-L NC_000962.3 \
-sample-name-map $output_dir/samples.map
exit_value=$?
if [ $exit_value != 0 ]; then
        echo "ERROR with GenomicsDBImport: $exit_value"
        exit
else
        echo "GenomicsDBImport COMPLETE"
fi

echo "RUN: GenotypeGVCFs"
gatk \
GenotypeGVCFs \
-R $ref \
-V gendb://$output_dir/my_database_genomicsDBImport \
-O $output_dir/mtb_genotypeGVCF.vcf.gz
exit_value=$?
if [ $exit_value != 0 ]; then
        echo "ERROR with GenotypeGVCFs: $exit_value"
        exit
else
        echo "GenotypeGVCFs COMPLETE"
fi
echo "Finish"
