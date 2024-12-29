import sys
import pysam
import statistics
from scipy import stats
from tqdm import tqdm
import re

SV_filename = str(sys.argv[1])
pos_dis_file = str(sys.argv[2]) #generate from get_indv_pos_short_read.py
HAP1_bam_dir = str(sys.argv[3])
HAP2_bam_dir = str(sys.argv[4])

Med_distance = int(sys.argv[5])
Min_depth = int(sys.argv[6])
Min_clip_cnt = int(sys.argv[7])
Min_clip_rat = float(sys.argv[8])
Max_INS_rat = float(sys.argv[9])
depth_pval = float(sys.argv[10])
clip_pval = float(sys.argv[11])

VAR_TYPE = str(sys.argv[12])


pos_dict = {}
with open(pos_dis_file) as indv_pos_tab:
        for line in indv_pos_tab:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if "Rep_str" == line_l[0]:
                        pos_dict[line_l[0]] = line_l[1:-2]
                else:
                        if not int(line_l[0]) in pos_dict:
                                pos_dict[int(line_l[0])] = line_l[1:-2]

total_analysis_loci = 0
with open(SV_filename) as tab_file:
        for line in tab_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if "Chr" == line_l[0]:
                        continue
                else:
                        if float(pos_dict[int(line_l[1])][4]) > Med_distance:
                                continue

                        for i in line_l[9:]:
                                if i == "-":
                                        total_analysis_loci += 1

def get_filter_status(START, STOP, SAMPLE_NAME, BAM_DIR, MIN_D, MIN_C_cnt, MIN_C_rat, MAX_I_rat, MIN_D_pval, MIN_C_pval, VAR):
        bam_file_name = BAM_DIR + "/" + SAMPLE_NAME + "/" + SAMPLE_NAME + "_sort_mkd.bam" #bamfile name
        BAM_FILE = pysam.AlignmentFile(bam_file_name, 'rb', check_sq = False) #create alignment object using pysam
        filtering_str = ""
        if VAR == "INS":
                Up_MQ0, Up_PASSED_read = 0, 0
                Up_L_clipped_reads, Up_R_clipped_reads, Up_both_sided_clipped_reads = 0, 0, 0
                Up_INS_read_below_50, Up_INS_read_above_50 = 0, 0

                Down_MQ0, Down_PASSED_read = 0, 0
                Down_L_clipped_reads, Down_R_clipped_reads, Down_both_sided_clipped_reads = 0, 0, 0
                Down_INS_read_below_50, Down_INS_read_above_50 = 0, 0

                qname_up = [] #list of read name that have been analyzed
                start_ana01, stop_ana01 = START - 10, START - 10 + 1 #Analysis position is 10 bp upstream of breakpoint
                for read in BAM_FILE.fetch("NC_000962.3", start_ana01, stop_ana01):
                        read_l = str(read).split("\t")
                        if int(read_l[4]) == 0: #low MQ
                                Up_MQ0 += 1
                                continue
                        if int(read_l[4]) >= 20:
                                if read_l[0] in qname_up: #two mates in same region count as 1
                                        continue
                                if int(read_l[1]) & 0x100: #secondary alignment
                                        continue
                        
                                qname_up.append(read_l[0]) #record read name
                                Up_PASSED_read += 1
                                cigar_len = re.split('\D', read_l[5])
                                cigar_type = re.split('[0-9]+', read_l[5])
                                del cigar_len[-1]
                                del cigar_type[0]
                                #one read one event assignment
                                if "H" in cigar_type or "S" in cigar_type:
                                        clip_len = 0
                                        if (cigar_type[0] == "H" or cigar_type[0] == "S") and not (cigar_type[-1] == "H" or cigar_type[-1] == "S"):#Left-clipped reads
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        Up_L_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and not (cigar_type[0] == "H" or cigar_type[0] == "S"):#Right-clipped reads
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        Up_R_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and (cigar_type[0] == "H" or cigar_type[0] == "S"):#Both-sided clipped reads
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        Up_both_sided_clipped_reads += 1

                                elif "I" in cigar_type:
                                        ins_size = []
                                        for i,v in enumerate(cigar_type):
                                                if v == "I":
                                                        ins_size.append(int(cigar_len[i]))
                                        if max(ins_size) >= 50:
                                                Up_INS_read_above_50 += 1
                                        else:
                                                Up_INS_read_below_50 += 1
                
                start_ana02, stop_ana02 = START + 10, START + 10 + 1
                qname_down = []
                for read in BAM_FILE.fetch("NC_000962.3", start_ana02, stop_ana02):
                        read_l = str(read).split("\t")
                        if int(read_l[4]) == 0:
                                Down_MQ0 += 1
                                continue
                        if int(read_l[4]) >= 20:
                                if read_l[0] in qname_down: #two mates in same region count as 1
                                        continue
                                if int(read_l[1]) & 0x100: #secondary alignment
                                        continue
                                qname_down.append(read_l[0])
                                Down_PASSED_read += 1
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
                                                        Down_L_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and not (cigar_type[0] == "H" or cigar_type[0] == "S"):#Right clipped reads
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        Down_R_clipped_reads += 1
                                        elif (cigar_type[-1] == "H" or cigar_type[-1] == "S") and (cigar_type[0] == "H" or cigar_type[0] == "S"):#Both-sided clipped reads
                                                for i,v in enumerate(cigar_type):
                                                        if v == "H" or v == "S":
                                                                clip_len += int(cigar_len[i])
                                                if clip_len >= 5:
                                                        Down_both_sided_clipped_reads += 1

                                elif "I" in cigar_type:
                                        ins_size = 0
                                        for i,v in enumerate(cigar_type):
                                                if v == "I":
                                                        ins_size += int(cigar_len[i])
                                        if ins_size >= 50:
                                                Down_INS_read_above_50 += 1
                                        else:
                                                Down_INS_read_below_50 += 1
                
                #Summary statistics
                AVG_COV = round((Up_PASSED_read + Down_PASSED_read)/2)
                AVG_L = round((Up_L_clipped_reads + Down_L_clipped_reads)/2)
                AVG_R = round((Up_R_clipped_reads + Down_R_clipped_reads)/2)
                AVG_B = round((Up_both_sided_clipped_reads + Down_both_sided_clipped_reads)/2)
                Toatal_clip = AVG_L + AVG_R
                #Clip ratio
                AVG_rat = 0
                if AVG_COV > 0:
                        AVG_rat = round(Toatal_clip/AVG_COV,3)
                
                AVG_INS_above_50 = round((Up_INS_read_above_50 + Down_INS_read_above_50)/2)
                AVG_INS_below_50 = round((Up_INS_read_below_50 + Down_INS_read_below_50)/2)

                #Skew of left- and right-clipped reads
                clip_observed = [AVG_L, AVG_R]
                clip_expected = [Toatal_clip/2, Toatal_clip/2] #L + R
                c_stat_val, c_pval = stats.fisher_exact([clip_observed, clip_expected])
                #Skew of up- and downstream coverage
                dep_observed = [Up_PASSED_read, Down_PASSED_read]
                dep_expected = [AVG_COV, AVG_COV] #AVG depth
                d_stat_val, d_pval = stats.fisher_exact([dep_observed, dep_expected])
                #INS below 50 bp ratio
                INS_rat = 0
                if AVG_COV > 0:
                        INS_rat = AVG_INS_below_50/AVG_COV
                
                filtering = ["F", "F", "F", "F", "F", "F"]
                if AVG_COV >= MIN_D:
                        filtering[0] = "P"
                if AVG_L >= MIN_C_cnt or AVG_R >= MIN_C_cnt:
                        filtering[1] = "P"
                if AVG_rat >= MIN_C_rat:
                        filtering[2] = "P"
                if INS_rat < MAX_I_rat:
                        filtering[3] = "P"
                if d_pval > MIN_D_pval:
                        filtering[4] = "P"
                if c_pval > MIN_C_pval:
                        filtering[5] = "P"
                filtering_str = "".join(filtering)
        return filtering_str
progress_bar = tqdm(total=total_analysis_loci, desc="Processing", unit="loci")
with open(SV_filename) as tab_file:
        sample_index = {}
        for line in tab_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if "Chr" == line_l[0]:
                        for i,v in enumerate(line_l[9:]):
                                if not i in sample_index:
                                        sample_index[i] = v
                        print("\t".join(line_l[1:5]), "N_ref", "N_SV", "N_na", "MAF", "\t".join(line_l[9:]), sep = "\t")
                else:
                        if float(pos_dict[int(line_l[1])][4]) > Med_distance:
                                continue
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

                                        Filter_code = get_filter_status(int(line_l[1]), int(line_l[2]), sample_name, bam_dir, Min_depth, Min_clip_cnt, Min_clip_rat, Max_INS_rat, depth_pval, clip_pval, VAR_TYPE)
                                        if Filter_code[0] == "F" or Filter_code[3] == "F" or Filter_code[4] == "F" or Filter_code[5] == "F":
                                                N_NOCALL += 1
                                                recovery.append("na")
                                        else:
                                                if Filter_code == "PPPPPP":
                                                        N_SV += 1
                                                        recovery.append("SV_r")
                                                else:
                                                        N_REF += 1
                                                        recovery.append("REF")
                        MAF = min(round(N_SV/Total, 4), round(N_REF/Total, 4))
                        recovery.insert(4, str(N_REF))
                        recovery.insert(5, str(N_SV))
                        recovery.insert(6, str(N_NOCALL))
                        recovery.insert(7, str(MAF))
                        print("\t".join(recovery))
                        progress_bar.update(1)
progress_bar.close()