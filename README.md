# Comprehensive_analysis_of_structural_variations_in_Mtb
List of scripts
1. Paired-end illumina short reads alignment (run_bwa_short_read_alignment.sh)
   
   This script aligns paired-end illumnia short reads that have been trimmed by trimmomatics to the Mtb reference genome (Genbank: NC_000962.3) using "bwa-mem".
   After alignment, this scirpt also sorts aligned reads and generates BAM and its index files.
   Note: Add line 44 and 45, you can change the end-of-file according to yours.

2. Single nucleotide variants (SNVs) and small deletions/Insertions (small INDELs) calling

      In this step, variant calling was performed using GATK4 (https://gatk.broadinstitute.org/hc/en-us)

      2.1 Marks duplicated reads: (mark_duplicated_reads.sh)

      This script marks the duplicated reads in sorted aligned reads files and creates BAM file as the output.

      2.2 Variant calling (gatk_haplotypecaller.sh)

      This script calls SNVs and small INDELs from BAM file that were marked the duplicated reads then outputs in g.vcf.gz format. In the study, we used NC_000962.3 as
      the reference genome. Then, we set-up ploidy parameter as 2 and mapping minimum quality (mbq) parameter as 20.

      2.3 Joint genotyping (gatk_join_genotyping.sh)

      This script will join-genotype all g.vcf.gz files in input direcotory and create multi samples VCF file as output.
