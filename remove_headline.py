import sys

ims_res = open(sys.argv[1])

#caller	sample_name	>indel_type     call_type       chr     sttpos  endpos  indel_length    indel_str       #indel_depth    #ttl_depth      details(indelcall_indeltype_depth)      clip_sttpos     depth(>=10)
for line in ims_res:
	line = line.replace("\n", "")
	line_l = line.split("\t")
	if "sample_name" in line_l[0]:
		continue
	else:
		if "DEL" in line_l[2]:
			sv = "DELETION"
			print("\t".join(line_l[0:2]), sv, "\t".join(line_l[3:]), sep = "\t")
		elif "INS" in line_l[2]:
			sv = "INSERTION"
			print("\t".join(line_l[0:2]), sv, "\t".join(line_l[3:]), sep = "\t")
