import sys
import re
import operator
import statistics
import numpy as np

cat_file = str(sys.argv[1])
bp_int = int(sys.argv[2])

line_prev = []
var_group_list = []


def define_var_group(var_group_list, total_sample):
        sample_list = []
        pos_list = []
        dif_list = []
        for indv in var_group_list:
                sample_list.append(indv[0])
                pos_list.append(int(indv[2]))
        Pop_cnt = len(sample_list)
        Pop_freq = round(Pop_cnt/total_sample, 4)
        rep_breakpoint = statistics.mode(pos_list)
        #Distance from represent breakpoint
        for pos in pos_list:
                dif_list.append(abs(rep_breakpoint - pos))
        min_dif = min(dif_list)
        max_dif = max(dif_list)
        mean_dif = "-"
        median_dif = "-"
        q1_dif = "-"
        q3_dif = "-"
        #distribution of distance in each variant position
        if len(pos_list) > 1:
                q1_dif = np.percentile(dif_list, 25)
                mean_dif = statistics.mean(dif_list)
                median_dif = np.percentile(dif_list, 50)
                q3_dif = np.percentile(dif_list, 75)
        indv = []
        for i in range(0, len(sample_list)):
                indv.append(sample_list[i] + ":" + str(pos_list[i]))
        indv_str = ""
        if len(indv) > 1:
                indv_str = ",".join(indv)
        else:
                indv_str = "".join(indv)

        return [str(rep_breakpoint), str(Pop_cnt), str(Pop_freq), str(min_dif), str(q1_dif), str(median_dif), str(q3_dif), str(max_dif), str(mean_dif), indv_str]

print("Rep_str", "N_alt_indv", "Pop_freq", "Min_Dis", "Q1_Dis", "Med_Dis", "Q3_Dis", "Max_Dis", "AVG_Dis", "indv_info", sep = "\t")
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
                        if abs(int(line_cur[2]) - int(line_prev[2])) > bp_int:
                                pos_data = define_var_group(var_group_list, len(sample_list))
                                var_group_list = []
                                print("\t".join(pos_data))
                #for the first line
                var_group_list.append(line_cur) #[[sample_ID, chr, str, stp, N_SVcaller, Name_SVcaller], ..., ..., ...]
                line_prev = line_cur
        #for the last line
        pos_data = define_var_group(var_group_list, len(sample_list))
        print("\t".join(pos_data))
        
