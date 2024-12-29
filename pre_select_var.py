import sys

var_file = open(sys.argv[1])
caller = str(sys.argv[2])
var_type = str(sys.argv[3])
min_size = int(sys.argv[4])
max_size = int(sys.argv[5])

if var_type != "INSERTION":
        for line in var_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if caller == "I":
                        if line_l[3] == "Hete":
                                continue
                        else:
                                if line_l[2] == var_type:
                                        if abs(int(line_l[7])) >= min_size and abs(int(line_l[7])) <= max_size:
                                                print("\t".join(line_l[0:2]), line_l[4], line_l[2], line_l[5], line_l[6], line_l[7], ";".join(line_l[8:]), sep = "\t")
                elif caller == "M":
                        if "PASS" == line_l[8]:
                                info = line_l[11].split(":")
                                if "0/1" == info[0]:
                                        continue
                                else:
                                        if line_l[3] == var_type:
                                                if abs(int(line_l[6])) >= min_size and abs(int(line_l[6])) <= max_size:
                                                        print("\t".join(line_l[0:7]), ";".join(line_l[7:]), sep = "\t")
                elif caller == "W":
                        if "PASS" == line_l[8]:
                                info = line_l[11].split(":")
                                if "0/1" == info[0]:
                                        continue
                                else:
                                        if line_l[3] == var_type:
                                                if abs(int(line_l[6])) >= min_size and abs(int(line_l[6])) <= max_size:
                                                        print("\t".join(line_l[0:7]), ";".join(line_l[7:]), sep = "\t")
                elif caller == "L":
                        info = line_l[11].split(":")
                        if "1/1" != info[0]:
                                continue
                        else:
                                if line_l[3] == var_type:
                                        if abs(int(line_l[6])) >= min_size and abs(int(line_l[6])) <= max_size:
                                                print("\t".join(line_l[0:7]), ";".join(line_l[7:]), sep = "\t")
elif var_type == "INSERTION":
        for line in var_file:
                line = line.replace("\n", "")
                line_l = line.split("\t")
                if caller == "I":
                        if line_l[3] == "Hete":
                                continue
                        else:
                                if line_l[2] == var_type:
                                        if abs(int(line_l[7])) >= min_size:
                                                print("\t".join(line_l[0:2]), line_l[4], line_l[2], line_l[5], line_l[6], line_l[7], ";".join(line_l[8:]), sep = "\t")
                                        elif abs(int(line_l[7])) < min_size:
                                                if "ULI" in line_l[11]:
                                                        print("\t".join(line_l[0:2]), line_l[4], line_l[2], line_l[5], line_l[6], line_l[7], ";".join(line_l[8:]), sep = "\t")
                elif caller == "M":
                        if "PASS" == line_l[9]:
                                info = line_l[11].split(":")
                                if "0/1" == info[0]:
                                        continue
                                else:
                                        if line_l[3] == var_type:
                                                if not line_l[6] == "n/a":
                                                        if abs(int(line_l[6])) >= min_size:
                                                                print("\t".join(line_l[0:7]), ";".join(line_l[7:]), sep = "\t")
                                                else:
                                                        print("\t".join(line_l[0:7]), ";".join(line_l[7:]), sep = "\t")
