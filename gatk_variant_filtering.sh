#!/usr/bin/bash

vcf_file=$1
output_dir=$2

if [ ! -d $output_dir ]; then
mkdir $output_dir
echo "Create output directory"
else
echo "Output directory is already available"
fi

module use /usr/local/package/modulefiles/
module load java/1.8.0_181

output_name=$(basename $vcf_file .vcf)
echo $output_name

echo "Apply GATK variant filtration"
java -Xmx64m -jar /home/ww160494/tools/gatk-4.2.0.0/gatk-package-4.2.0.0-local.jar VariantFiltration \
-V $vcf_file \
-O $output_dir/${output_name}_variantfiltration.vcf \
--filter-expression "QD < 2.00" --filter-name "QD2" \
--filter-expression "DP < 10.00" --filter-name "DP10" \
--filter-expression "FS > 200.00" --filter-name "FS200" \
--filter-expression "MQ < 20.00" --filter-name "MQ20" \
--filter-expression "ReadPosRankSum < -20.00" --filter-name "ReadPosRankSum-20" \
--filter-expression "ExcessHet > 5.68" --filter-name "ExcessHet5.68"


exit_value=$?
if [ $exit_value != 0 ]; then
echo "GATK variant filtration: ERROR"
exit
else
echo "GATK variant filtration: OK"
fi

