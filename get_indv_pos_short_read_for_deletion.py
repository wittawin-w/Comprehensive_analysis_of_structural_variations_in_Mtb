import sys
import re
import operator
import statistics
import numpy as np

cat_file = str(sys.argv[1])
crit_cov = float(sys.argv[2])

line_prev = []
var_group_list = []

def define_var_group(var_group_list, total_sample):
        sample_list = []
        STR_pos_list = []
        STR_dif_list = []

        STP_pos_list = []
        STP_dif_list = []
        for indv in var_group_list:
                sample_list.append(indv[0])
                STR_pos_list.append(int(indv[2]))
                STP_pos_list.append(int(indv[3]))

        Pop_cnt = len(sample_list)
        Pop_freq = round(Pop_cnt/total_sample, 4)
        STR_rep_breakpoint = statistics.mode(STR_pos_list)
        STP_rep_breakpoint = statistics.mode(STP_pos_list)
        #Distance from represent breakpoint
        for pos in STR_pos_list:
                STR_dif_list.append(abs(STR_rep_breakpoint - pos))
        STR_min_dif = min(STR_dif_list)
        STR_max_dif = max(STR_dif_list)
        STR_mean_dif = 0
        STR_median_dif = 0
        STR_q1_dif = 0
        STR_q3_dif = 0
        #distribution of distance in each variant position
        if len(STR_pos_list) > 1:
                STR_q1_dif = np.percentile(STR_dif_list, 25)
                STR_mean_dif = statistics.mean(STR_dif_list)
                STR_median_dif = np.percentile(STR_dif_list, 50)
                STR_q3_dif = np.percentile(STR_dif_list, 75)
        
        for pos in STP_pos_list:
                STP_dif_list.append(abs(STP_rep_breakpoint - pos))
        STP_min_dif = min(STP_dif_list)
        STP_max_dif = max(STP_dif_list)
        STP_mean_dif = 0
        STP_median_dif = 0
        STP_q1_dif = 0
        STP_q3_dif = 0
        if len(STR_pos_list) > 1:
                STP_q1_dif = np.percentile(STP_dif_list, 25)
                STP_mean_dif = statistics.mean(STP_dif_list)
                STP_median_dif = np.percentile(STP_dif_list, 50)
                STP_q3_dif = np.percentile(STP_dif_list, 75)
        ov_dat = [str(STR_rep_breakpoint), str(STP_rep_breakpoint), str(Pop_cnt), str(Pop_freq)]
        STR_dat = [str(STR_min_dif), str(STR_q1_dif), str(STR_median_dif), str(STR_q3_dif), str(STR_max_dif), str(STR_mean_dif)]
        STP_dat = [str(STP_min_dif), str(STP_q1_dif), str(STP_median_dif), str(STP_q3_dif), str(STP_max_dif), str(STP_mean_dif)]
        
        return ov_dat + STR_dat + STP_dat

print("Rep_str", "Rep_stp", "N_alt_indv", "Pop_freq", "STR_Min_Dis", "STR_Q1_Dis", "STR_Med_Dis", "STR_Q3_Dis", "STR_Max_Dis", "STR_AVG_Dis", "STP_Min_Dis", "STP_Q1_Dis", "STP_Med_Dis", "STP_Q3_Dis", "STP_Max_Dis", "STP_AVG_Dis", sep = "\t")
with open(cat_file) as cat_tab:
        sample_list = []
        for line in cat_tab:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if not line_l[0] in sample_list:
                        sample_list.append(line_l[0])

with open(cat_file) as cat_tab:
        line_prev = []
        var_group_list = []
        for line in cat_tab:
                line = line.replace("\n", "")
                line_cur = line.split("\t")
                #print(line_cur)
                if len(line_prev) > 0:
                        lc = int(line_cur[3]) - int(line_cur[2]) + 1
                        lp = int(line_prev[3]) - int(line_cur[2]) + 1
                        if int(line_cur[2]) == int(line_prev[2]):
                                if int(line_cur[3]) > int(line_prev[3]) and float(lp/lc) < crit_cov:
                                        pos_data = define_var_group(var_group_list, len(sample_list))
                                        var_group_list = []
                                        print("\t".join(pos_data))
                        elif int(line_cur[2]) > int(line_prev[2]):
                                if int(line_cur[3]) < int(line_prev[3]) and float(lc/lp) < crit_cov:
                                        pos_data = define_var_group(var_group_list, len(sample_list))
                                        var_group_list = []
                                        print("\t".join(pos_data))
                                elif int(line_cur[3]) == int(line_prev[3]) and float(lc/lp) < crit_cov:
                                        pos_data = define_var_group(var_group_list, len(sample_list))
                                        var_group_list = []
                                        print("\t".join(pos_data))
                                elif int(line_cur[3]) > int(line_prev[3]) and int(line_cur[2]) < int(line_prev[3]):
                                        ov = int(int(line_prev[3]) - int(line_cur[2]) + 1)
                                        if float(ov/lp) < crit_cov and float(ov/lc) < crit_cov:
                                                pos_data = define_var_group(var_group_list, len(sample_list))
                                                var_group_list = []
                                                print("\t".join(pos_data))
                                        elif float(ov/lp) >= crit_cov and float(ov/lc) < crit_cov:
                                                pos_data = define_var_group(var_group_list, len(sample_list))
                                                var_group_list = []
                                                print("\t".join(pos_data))
                                        elif float(ov/lp) < crit_cov and float(ov/lc) >= crit_cov:
                                                pos_data = define_var_group(var_group_list, len(sample_list))
                                                var_group_list = []
                                                print("\t".join(pos_data))
                                elif int(line_cur[3]) > int(line_prev[3]) and int(line_cur[2]) > int(line_prev[3]):
                                        pos_data = define_var_group(var_group_list, len(sample_list))
                                        var_group_list = []
                                        print("\t".join(pos_data))
                #for the first line
                var_group_list.append(line_cur) #[[sample_ID, chr, str, stp, N_SVcaller, Name_SVcaller], ..., ..., ...]
                line_prev = line_cur
        #for the last line
        pos_data = define_var_group(var_group_list, len(sample_list))
        print("\t".join(pos_data))