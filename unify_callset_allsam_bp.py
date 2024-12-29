import sys
import operator
import statistics

def define_var_group(var_group_list):
        var_group_list.sort(key = operator.itemgetter(2))
        group_str = []
        #group_stp = []
        overall_group = []
        group_shared = []
        overall_group_str = ""
        chr = ""
        indv_shared = []
        sv_call = []
        sv_call_sum = []
        rep_str = ""
        #rep_stp = ""
        var_can = {}
        for var in var_group_list:
                group_str.append(int(var[2]))
                #group_stp.append(int(var[3]))
                group_shared.append(int(var[4]))
                chr  = str(var[1])
                sv_call = var[5].split(",")
                for i in sv_call:
                        if not i in sv_call_sum:
                                sv_call_sum.append(i)
        overall_group = [chr, str(statistics.mode(group_str)), str(statistics.mode(group_str)), str(max(group_shared)), ",".join(sv_call_sum)] 
        overall_group_str = "\t".join(overall_group)
        for name in sample_list:
                indv_shared_str = "-"
                name_dict = {}
                for var in var_group_list:
                        if name == var[0]:
                                indv_shared = [var[4]]
                                indv_shared_str = "".join(indv_shared)
                if overall_group_str in var_can.keys():
                        var_can.setdefault(overall_group_str, []).append(indv_shared_str)
                else:
                        var_can[overall_group_str] = [indv_shared_str]
        for can in sorted(var_can.keys()):
                total_indv = 0
                var_indv = 0
                for i in var_can[can]:
                        total_indv += 1
                        if not "-" == i:
                                var_indv += 1
                pop_freq = [round(var_indv/total_indv,3), 1 - round(var_indv/total_indv,3)]
                print(can, total_indv, var_indv, round(var_indv/total_indv,3), min(pop_freq), "\t".join(var_can[can]), sep = "\t")


cat_file = open(sys.argv[1])
bp = int(sys.argv[2])

sample_list = []
for line in cat_file:
        line = line.replace("\n", "")
        line_l = line.split("\t")
        if not line_l[0] in sample_list:
                sample_list.append(line_l[0])

sample_list = sorted(sample_list)
print("Chr", "Rep_str", "Rep_stp", "Max_N_shared", "Shared_callers", "Total_indv", "Var_indv", "Pop_freq", "MAF", "\t".join(sample_list), sep = "\t")

cat_file = open(sys.argv[1])
bp = int(sys.argv[2])

line_prev = []
var_group_list = []

for line in cat_file:
        line = line.replace("\n", "")
        line_cur = line.split("\t")
        if len(line_prev) > 0:
                if abs(int(line_cur[2]) - int(line_prev[2])) > bp:
                        define_var_group(var_group_list)
                        var_group_list = []
        var_group_list.append(line_cur)
        line_prev = line_cur
define_var_group(var_group_list)
var_group_list = []