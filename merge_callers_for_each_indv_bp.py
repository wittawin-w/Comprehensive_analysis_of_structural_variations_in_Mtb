import sys
import statistics
import operator
def define_var_group(var_group_list):
        var_group_list.sort(key = operator.itemgetter(4))
        group_str = []
        #group_stp = []
        shared_callers = []
        shared_callers_str = ""
        rep_str = ""
        rep_stp = ""
        output = []
        for i in var_group_list:
                if not i[0] in shared_callers:
                        shared_callers.append(i[0])
                else:
                        continue
                group_str.append(int(i[4]))
                #group_stp.append(int(i[5]))
        
        if len(group_str) == 1:
                group_str_2 = []
                for j in group_str:
                        group_str_2.append(str(j))
                rep_str = "".join(group_str_2)
        elif len(group_str) > 1:
                rep_str = str(round(statistics.median(group_str)))
        #if len(group_stp) == 1:
        #        group_stp_2 = []
        #        for j in group_stp:
        #                group_stp_2.append(str(j))
        #        rep_stp = "".join(group_stp_2)
        #elif len(group_stp) > 1:
        #        rep_stp = str(round(statistics.median(group_stp)))
        if len(shared_callers) == 1:
                shared_callers_str = "".join(shared_callers)
        elif len(shared_callers) > 1:
                shared_callers_str = ",".join(shared_callers)
        output.append(var_group_list[0][1])
        output.append(var_group_list[0][2])
        output.append(rep_str)
        output.append(rep_str) #one breakpoint
        output.append(str(len(shared_callers)))
        output.append(shared_callers_str)
        print( "\t".join(output))

cat_file = open(sys.argv[1])
bp = int(sys.argv[2])

shared_caller = []
for line in cat_file:
        line = line.replace("\n", "")
        line_l = line.split("\t")
        if not line_l[0] in shared_caller:
                shared_caller.append(line_l[0])

print("Sample_ID", "Chr", "Rep_str", "Rep_stp", "N_shared", "Caller", sep = "\t")

cat_file = open(sys.argv[1])
bp = int(sys.argv[2])

line_prev = []
var_group_list = []

for line in cat_file:
        line = line.replace("\n", "")
        line_cur = line.split("\t")
        if len(line_prev) > 0:
                if abs(int(line_cur[4]) - int(line_prev[4])) > bp:
                        define_var_group(var_group_list)
                        var_group_list = []
        var_group_list.append(line_cur)
        line_prev = line_cur
define_var_group(var_group_list)
var_group_list = []
