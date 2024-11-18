import sys

imsindel = open(sys.argv[1])
sample_name = str(sys.argv[2])
caller = str(sys.argv[3])

for line in imsindel:
        line = line.replace("\n", "")
        line_l = line.split("\t")
        if ">indel_type" in line_l[0]:
                continue
        else:
                print(caller, sample_name, "\t".join(line_l), sep = "\t")

