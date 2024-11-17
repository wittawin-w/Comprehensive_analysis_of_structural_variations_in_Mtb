bamfile=$1 # path to input bamfile
output_dir=$2 # path to output directory
tmp_dir=$3 # path to temporary directory
ref=$4 # path to fasta file of reference genome
ref_id=$5 # reference chromosome ID

if [ -d $output_dir ]; then
echo "output directory $output_dir exist!!"
else
echo "ERROR: cannot detect output directory"
exit
fi

if [ -d $tmp_dir ]; then
echo "directory for temporary files $tmp_dir exist!!!"
else
echo "ERROR: cannot detect directory for temporary files"
exit
fi

module  use /usr/local/package/modulefiles/
module load samtools/1.9

echo "Indexing bamfile :$bamfile"
samtools index $bamfile
exit_value=$?
if [ $exit_value != 0 ]; then
echo "ERROR with indexing bamfile: $exit_value"
exit
else
echo "Indexing bamfile finish status: OK"
fi
echo "start running IMSindel"
/home/ww160494/tools/IMSindel/bin/imsindel \
--bam $bamfile \
--chr $ref_id \
--outd $output_dir \
--indelsize 10000 \
--baseq 20 \
--mapq 20 \
--within 3 \
--alt-read-depth 2 \
--support-reads 2 \
--clip-length 5 \
--support-clip-length 5 \
--temp $tmp_dir \
--glsearch /path/to/glsearch36 \
--glsearch-mat /path/to/IMSindel/data/mydna.mat \
--samtools /path/to/samtools \
--mafft /path/to/mafft \
--output-consensus-seq $output_dir \
--reffa $ref
exit_value=$?
if [ $exit_value != 0 ]; then
echo "ERROR with IMSindel: $exit_value"
exit
else
echo "IMSindel SV calling finish status: OK"
fi

