# Comprehensive_analysis_of_structural_variations_in_Mtb
## These scripts were used for analysis in Worakitchanon, Wittawin et al. Cell Host & Microbe, Volume 32, Issue 11, 1972 - 1987.e6 (DOI: 10.1016/j.chom.2024.10.004)

1. Paired-end illumina short reads alignment (`run_bwa_short_read_alignment.sh`)
   
    This script aligns paired-end illumnia short reads that have been trimmed by trimmomatics to the Mtb reference genome (Genbank: NC_000962.3) using "bwa-mem".
    After alignment, this scirpt also sorts aligned reads and generates BAM and its index files.
    Note: Add line 44 and 45, you can change the end-of-file according to yours.

 2. Single nucleotide variants (SNVs) and small deletions/Insertions (small INDELs) calling

      In this step, variant calling was performed using GATK4 (https://gatk.broadinstitute.org/hc/en-us).

      2.1 Marks duplicated reads: (`mark_duplicated_reads.sh`)

      This script marks the duplicated reads in sorted aligned reads files and creates BAM file as the output.

      2.2 Variant calling (`gatk_haplotypecaller.sh`)

      This script calls SNVs and small INDELs from BAM file that were marked the duplicated reads then outputs in g.vcf.gz format. In the study, we used NC_000962.3 as
      the reference genome. Then, we set-up ploidy parameter as 2 and mapping minimum quality (mbq) parameter as 20.

      2.3 Joint genotyping (`gatk_join_genotyping.sh`)

      This script will join-genotype all g.vcf.gz files in input direcotory and create multi samples VCF file as output.

      2.4 Variant selection (`gatk_selectvariant.sh`)

      This script will filter SNVs or small INDELs that were called by GATK4 into separated VCF file.

      2.5.1 Variant filtering (`gatk_variant_filtering.sh`)

      This script will use gatk tool to filter variant according to the desired parameters (please see the detail in paper)

      2.5.2 Heterozygous filtering (`heterozygous_filtering.py`)

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

   3.1 SV calling
   
   3.1.1 IMSindel (`imsindel_svcall.sh`): This script will run imsindel to call INDELs from bamfile. Please ensure that all dependencies of IMSindel have been provided in line
         31 and 44 - 47 of script before running.

   3.1.2 Manta (`manta_svcall.sh`): This script will run manta to call SVs from bamfile. Noted that manta needs python2 for executing and please ensure that path in line 7 of
         this script has been provided before running.

   3.1.3 LUMPY (`lumpy_svcall.sh`): This script will run LUMPY to call SVs from bamfile. Samtools is required for this script.
         Noted that LUMPY needs python2 for executing and please ensure that path to LUMPY in line 43 has been provided before running.

   3.1.4 Wham (`wham_svcall.sh`): THis script will run Wham to call SVs from bamfile. Please ensure to provide path to wham in line 12 and 15 before running.

   3.2 Genotype calling for LUMPY and Wham outputs (`svtyper.sh`)

   This script identify variants genotypes in samples that were called by LUMPY and Wham.

   3.3 Create the similar output format across all SV callers

   3.3.1 IMSindel (`imsindel_re_formating.sh` and `imsindel_re_formating.py`): Running script is `imsindel_re_formating.sh`. Please provide the path to imsindel_re_formating.py in line 17 of `imsindel_re_formating.sh` before running.

   3.3.2 MANTA (`run_change_format_manta.sh`, `manta_reformating.sh` and `manta_re_formating.py`): Runing script is `run_change_format_manta.sh`. Please provide path to `manta_reformating.sh` in line 19 of `run_change_format_manta.sh` and provide path to `manta_reformating.py` in line 26 of `manta_reformating.sh` before running.

   3.3.3 LUMPY (`run_change_format_lumpy.sh`, `lumpy_re_formating.py`): Running script is `run_change_format_lumpy.sh`. Please provide the path to `lumpy_re_formating.py` in line 21 of `run_change_format_lumpy.sh` before running

   3.3.4 Wham (`run_change_format_wham.sh`, `wham_re_formating.py`): Running script is `run_change_format_wham.sh`. Please provide the path to `wham_re_formating.py` in line 21 of `run_change_format_wham.sh` before running

4. Merge reformatted result of each sample for large insertions and deletions

   4.1 Merge deletion calls from four SV callers in each sample (`run_merge_callers_for_each_indv_coverage.sh`, `pre_select_var.py`, `remove_headline.py`, `merge_callers_for_each_indv_coverage.py`): Running script is `run_merge_callers_for_each_indv_coverage.sh`. Please setup path to each reformatted file in line 24, path to `pre_select_var.py` in line 33 and 53, path to `remove_headline.py` in line 45 and path to `merge_callers_for_each_indv_coverage.py` in line 67 in the running script be for run it

   4.2 Merge insertion calls from SV callers in each sample (`run_merge_callers_for_each_indv_bp.sh`, `pre_select_var.py`, `remove_headline.py`, `merge_callers_for_each_indv_bp.py`): Running script is `run_merge_callers_for_each_indv_bp.sh`. Please setup path to each reformatted file in line 23, path to `pre_select_var.py` in line 32 and 52, path to `remove_headline.py` in line 44 and path to `merge_callers_for_each_indv_bp.py` in line 66 in the running script be for run it

5. Merge all samples into one table

  5.1 Deletions (`run_unify_callset_allsample_coverage.sh`, `unify_callset_remove_headline.py`, `unify_callset_allsam_coverage.py`): Running script is `run_unify_callset_allsample_coverage.sh` please make sure to set path to `unify_callset_remove_headline.py` in line 18 and path to `unify_callset_allsam_coverage.py` in line 30 before running

 



         
        
