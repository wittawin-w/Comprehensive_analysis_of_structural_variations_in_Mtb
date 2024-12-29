import sys
import pysam
import statistics
from scipy import stats
import re
from tqdm import tqdm

SV_filename = str(sys.argv[1])
#pos_dis_file = str(sys.argv[2]) #generate from get_indv_pos_short_read.py
HAP1_bam_dir = str(sys.argv[2])
HAP2_bam_dir = str(sys.argv[3])

Min_flank_depth = int(sys.argv[4])
Max_depth_pval = round(float(sys.argv[5]), 4)
Max_STR_clip_pval = round(float(sys.argv[6]), 4)
Max_STP_clip_pval = round(float(sys.argv[7]), 4)

VAR_TYPE = str(sys.argv[8])

total_analysis_loci = 0
with open(SV_filename) as tab_file:
        for line in tab_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if "Chr" == line_l[0]:
                        continue
                else:
                        for i in line_l[9:]:
                                if i == "-":
                                        total_analysis_loci += 1

def get_filter_status(STR, END, SAMPLE_NAME, BAM_DIR, MIN_flank_depth, MAX_depth_pval, MAX_STR_clip_pval, MAX_END_clip_pval, var_type):
        bam_file_name = BAM_DIR + "/" + SAMPLE_NAME + "/" + SAMPLE_NAME + "_sort_mkd.bam" #bamfile name
        BAM_FILE = pysam.AlignmentFile(bam_file_name, 'rb', check_sq = False) #create alignment object using pysam
        filtering_str = ""
        if var_type == "DEL":
                #start breakpoint
                ##upstream region parameters
                STR_Up_L_clipped_reads, STR_Up_R_clipped_reads = 0, 0
                qname = []
                STR_start_ana01, STR_stop_ana01 = STR - 50, STR - 50 + 1
                for read in BAM_FILE.fetch("NC_000962.3", STR_start_ana01, STR_stop_ana01):
                        #if read.is_supplementary:
                        #        continue

                        read_l = str(read).split("\t")
                        if int(read_l[4]) >= 20:
                                if read_l[0] in qname:
                                        continue

                                if int(read_l[1]) & 0x100:
                                        continue

                                if int(read_l[1]) & 0x800:
                                        continue

                                qname.append(read_l[0])
                                cigar_len = re.split('\D', read_l[5])
                                cigar_type = re.split('[0-9]+', read_l[5])
                                del cigar_len[-1]
                                del cigar_type[0]
                                if "H" in cigar_type or "S" in cigar_type:
                                        clip_len = 0
                                        if (cigar_type[0] == "H" or cigar_type[0] == "S") and not (cigar_type[-1] == "H" or cigar_type[-1] == "S"):
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        STR_Up_L_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and not (cigar_type[0] == "H" or cigar_type[0] == "S"):
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        STR_Up_R_clipped_reads += 1

                #end breakpoint
                ##Downstream of breakpoint
                STP_Down_L_clipped_reads, STP_Down_R_clipped_reads= 0, 0
                qname = []
                STP_start_ana02, STP_stop_ana02 = END + 50, END + 50 + 1
                for read in BAM_FILE.fetch("NC_000962.3", STP_start_ana02, STP_stop_ana02):
                        #if read.is_supplementary:
                        #        continue

                        read_l = str(read).split("\t")
                        if int(read_l[4]) >= 20:
                                if read_l[0] in qname:
                                        continue

                                if int(read_l[1]) & 0x100:
                                        continue

                                if int(read_l[1]) & 0x800:
                                        continue

                                qname.append(read_l[0])
                                cigar_len = re.split('\D', read_l[5])
                                cigar_type = re.split('[0-9]+', read_l[5])
                                del cigar_len[-1]
                                del cigar_type[0]
                                if "H" in cigar_type or "S" in cigar_type:
                                        clip_len = 0
                                        if (cigar_type[0] == "H" or cigar_type[0] == "S") and not (cigar_type[-1] == "H" or cigar_type[-1] == "S"):
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        STP_Down_L_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and not (cigar_type[0] == "H" or cigar_type[0] == "S"):
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        STP_Down_R_clipped_reads += 1

                #In deletion region
                In_del_PASSED_read = 0
                Middle_Mismatch01, Middle_Mismatch03, Middle_Mismatch05, Middle_Mismatch07 = 0, 0, 0, 0
                for pileupcolumn in BAM_FILE.pileup("NC_000962.3", STR, END):
                        Inpile_Middle_Mismatch01, Inpile_Middle_Mismatch03, Inpile_Middle_Mismatch05, Inpile_Middle_Mismatch07 = 0, 0, 0, 0
                        depth = 0
                        if pileupcolumn.pos >= STR and pileupcolumn.pos <= END:
                                qname = []
                                for pileupread in pileupcolumn.pileups:
                                        read = pileupread.alignment
                                        if read.is_supplementary:
                                                continue
                                        read_l = str(read).split("\t")
                                        if int(read_l[4]) >= 20:
                                                if read_l[0] in qname:
                                                        continue
                                                if int(read_l[1]) & 0x100:
                                                        continue
                                                if int(read_l[1]) & 0x800:
                                                        continue
                                                qname.append(read_l[0])
                                                depth += 1
                        In_del_PASSED_read += depth
                
                #Flanking region coverage
                STR_Up_PASSED_read = 0
                Up_flank = []
                STR_start_ana, STR_stop_ana = STR - 200, STR - 200 + 1
                for read in BAM_FILE.fetch("NC_000962.3", STR_start_ana, STR_stop_ana):
                        read_l = str(read).split("\t")
                        if int(read_l[4]) >= 20:
                                if read_l[0] in Up_flank:
                                        continue

                                if int(read_l[1]) & 0x100:
                                        continue

                                if int(read_l[1]) & 0x800:
                                        continue

                                Up_flank.append(read_l[0])
                                STR_Up_PASSED_read += 1
                
                STP_Down_PASSED_read = 0
                Down_flank = []
                STP_start_ana, STP_stop_ana = END + 200, END + 200 + 1
                for read in BAM_FILE.fetch("NC_000962.3", STP_start_ana, STP_stop_ana):
                        read_l = str(read).split("\t")
                        if int(read_l[4]) >= 20:
                                if read_l[0] in Down_flank:
                                        continue

                                if int(read_l[1]) & 0x100:
                                        continue

                                if int(read_l[1]) & 0x800:
                                        continue

                                Down_flank.append(read_l[0])
                                STP_Down_PASSED_read += 1

                #Depth
                Flanking_cov = round((STR_Up_PASSED_read + STP_Down_PASSED_read)/2)
                In_del_cov = round(In_del_PASSED_read/(END - STR))
                Cov_observed = [Flanking_cov, In_del_cov]
                Cov_expected = [Flanking_cov, Flanking_cov]
                D_stat_val, D_pval = stats.fisher_exact([Cov_observed, Cov_expected])

                #Clipped read
                STR_total_clipped_reads = STR_Up_L_clipped_reads + STR_Up_R_clipped_reads
                STR_clipped_observed = [STR_Up_L_clipped_reads, STR_Up_R_clipped_reads]
                STR_clipped_expected = [round(STR_total_clipped_reads/2), round(STR_total_clipped_reads/2)]
                STR_C_stat_val, STR_C_pval = stats.fisher_exact([STR_clipped_observed, STR_clipped_expected])

                STP_total_clipped_reads = STP_Down_L_clipped_reads + STP_Down_R_clipped_reads
                STP_clipped_observed = [STP_Down_L_clipped_reads, STP_Down_R_clipped_reads]
                STP_clipped_expected = [round(STP_total_clipped_reads/2), round(STP_total_clipped_reads/2)]
                STP_C_stat_val, STP_C_pval = stats.fisher_exact([STP_clipped_observed, STP_clipped_expected])

                # 0 -> flanking depth
                # 1 -> depth pval
                # 2 -> str clipped pval
                # 3 -> stp clipped pval
                filtering = ["F", "F", "F", "F"]
                if Flanking_cov >= MIN_flank_depth:
                        filtering[0] = "P"
                if D_pval <= MAX_depth_pval:
                        filtering[1] = "P"
                if STR_C_pval <= MAX_STR_clip_pval:
                        filtering[2] = "P"
                if STP_C_pval <= MAX_END_clip_pval:
                        filtering[3] = "P"
                filtering_str = "".join(filtering)

        return filtering_str

progress_bar = tqdm(total=total_analysis_loci, desc="Processing", unit="loci")
with open(SV_filename) as tab_file:
        sample_index = {}
        for line in tab_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if "Chr" == line_l[0]:
                        for i, v in enumerate(line_l[9:]):
                                if not i in sample_index:
                                        sample_index[i] = v
                        print("\t".join(line_l[1:5]), "N_ref", "N_SV", "N_na", "MAF", "\t".join(line_l[9:]), sep = "\t")
                else:
                        N_SV = 0
                        N_REF = 0
                        N_NOCALL = 0
                        Total = 0
                        recovery = line_l[1:5]
                        for i, v in enumerate(line_l[9:]):
                                Total += 1
                                if v != "-":
                                        N_SV += 1
                                        recovery.append("SV_c")
                                elif v == "-":
                                        sample_name = sample_index[i]
                                        bam_dir = ""
                                        if "ERR" in sample_name:
                                                bam_dir = HAP1_bam_dir
                                        else:
                                                bam_dir = HAP2_bam_dir

                                        Filter_code = get_filter_status(int(line_l[1]), int(line_l[2]), sample_name, bam_dir, Min_flank_depth, Max_depth_pval, Max_STR_clip_pval, Max_STP_clip_pval, VAR_TYPE)

                                        if Filter_code[0] == "F":
                                                N_NOCALL += 1
                                                recovery.append("na")
                                        
                                        else:
                                                if Filter_code[1] == "P" and (Filter_code[2] == "P" or Filter_code[3] == "P"):
                                                        N_SV += 1
                                                        recovery.append("SV_r")
                                                else:
                                                        N_REF += 1
                                                        recovery.append("REF")
                                progress_bar.update(1)
                        MAF = min(round(N_SV/Total, 4), round(N_REF/Total, 4))
                        recovery.insert(4, str(N_REF))
                        recovery.insert(5, str(N_SV))
                        recovery.insert(6, str(N_NOCALL))
                        recovery.insert(7, str(MAF))
                        print("\t".join(recovery))
progress_bar.close()
