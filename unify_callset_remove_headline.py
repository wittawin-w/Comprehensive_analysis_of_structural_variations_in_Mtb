import sys

indv_file = open(sys.argv[1])

for line in indv_file:
        line = line.replace("\n", "")
        line_l = line.split("\t")
        if "Sample_ID" == line_l[0]:
                continue
        else:
                print("\t".join(line_l[0:2]), round(float(line_l[2])), round(float(line_l[3])), "\t".join(line_l[4:]), sep = "\t")