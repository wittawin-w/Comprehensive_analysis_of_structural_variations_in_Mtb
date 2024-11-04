# Comprehensive_analysis_of_structural_variations_in_Mtb
List of scripts
1. paired-end illumina short reads alignment (run_bwa_short_read_alignment.sh)
   
   This script aligns paired-end illumnia short reads that have been trimmed by trimmomatics to the Mtb reference genome (Genbank: NC_000962.3) using "bwa-mem".
   After alignment, this scirpt also sorts aligned reads and generates BAM and its index files.
   Note: Add line 44 and 45, you can change the end-of-file according to yours.
