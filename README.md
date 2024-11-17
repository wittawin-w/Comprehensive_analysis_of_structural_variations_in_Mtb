# Comprehensive_analysis_of_structural_variations_in_Mtb
These scripts were used for analysis in Worakitchanon, Wittawin et al. Cell Host & Microbe, Volume 32, Issue 11, 1972 - 1987.e6 (DOI: 10.1016/j.chom.2024.10.004)
 1. Paired-end illumina short reads alignment (run_bwa_short_read_alignment.sh)
   
    This script aligns paired-end illumnia short reads that have been trimmed by trimmomatics to the Mtb reference genome (Genbank: NC_000962.3) using "bwa-mem".
    After alignment, this scirpt also sorts aligned reads and generates BAM and its index files.
    Note: Add line 44 and 45, you can change the end-of-file according to yours.

 2. Single nucleotide variants (SNVs) and small deletions/Insertions (small INDELs) calling

      In this step, variant calling was performed using GATK4 (https://gatk.broadinstitute.org/hc/en-us).

      2.1 Marks duplicated reads: (mark_duplicated_reads.sh)

      This script marks the duplicated reads in sorted aligned reads files and creates BAM file as the output.

      2.2 Variant calling (gatk_haplotypecaller.sh)

      This script calls SNVs and small INDELs from BAM file that were marked the duplicated reads then outputs in g.vcf.gz format. In the study, we used NC_000962.3 as
      the reference genome. Then, we set-up ploidy parameter as 2 and mapping minimum quality (mbq) parameter as 20.

      2.3 Joint genotyping (gatk_join_genotyping.sh)

      This script will join-genotype all g.vcf.gz files in input direcotory and create multi samples VCF file as output.

      2.4 Variant selection (gatk_selectvariant.sh)

      This script will filter SNVs or small INDELs that were called by GATK4 into separated VCF file.

      2.5.1 Variant filtering (gatk_variant_filtering.sh)

      This script will use gatk tool to filter variant according to the desired parameters (please see the detail in paper)

      2.5.2 Heterozygous filtering (heterozygous_filtering.py)

      Since Mycobacterium tuberculosis genome is haploid, therefore, this script will check genotype of each individual across all variant positions.

      Genotypes that are assigned as heterozygous are changed to missing genotype (./.).

      For reference/alternative homoszygous calls (0/0 or 1/1) at any variant positions,
      this script replace genotype of individual by missing genotype (./.) if depth of coverage less than 10.

      For reference homozygous calls that their depth of coverages are eqaul or more than 10, this script will check the variant allele frequency (VAF; ratio of reads that
      supports allele to total depth of coverage). If VAF of identified allele is equal to or less than 0.9, the genotype will be change to missing genotype.

3. Large deletions/insertions (large INDELs) calling

   In this study, we use four strucatural variant (SV) callers for calling large INDELs including
   - IMSindel (https://github.com/NCGG-MGC/IMSindel)
   - Manta (https://github.com/Illumina/manta)
   - LUMPY (https://github.com/arq5x/lumpy-sv)
   - Wham (https://github.com/zeeev/wham)

   3.1 IMSindel (imsindel_svcall.sh): This script will run imsindel to call INDELs from bamfile. Please ensure that all dependencies of IMSindel have been provided in line
       31 and 44 - 47 of script before running.

   3.2 Manta (manta_svcall.sh): This script will run manta to call SVs from bamfile. Noted that this manta needs python2 for executing and ensure that path in line 7 of
       this script has been provided before running. 
        
