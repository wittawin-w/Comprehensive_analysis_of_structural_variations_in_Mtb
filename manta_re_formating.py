import sys

vcf = open(sys.argv[1])

################ MANTA VCF format 

#vcf
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	mtb_ERR718192
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INS,Description="Insertion">
##ALT=<ID=DUP:TANDEM,Description="Tandem Duplication">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##SVTYPE=BND
#bed-like
#CHROM	type	str	stp	len	QUAL	FILTER	INFO	FORMAT	mtv_ERR718192
#str = start position of variant = POS + 1

################
for line in vcf:
	line = line.replace("\n", "")
	line_l = line.split("\t")
	startpoint = []
	svtype = []
	endpoint = []
	le = []
	if "#" in line_l[0]:
		continue
	else:
		info_f = line_l[7].split(";")
		if "DEL" in info_f[1]:
			sv = 'DELETION'
			start = str(int(line_l[1]) + 1)
			end = info_f[0].split("=")
			svl = info_f[2].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[4], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
		elif "DUP" in info_f[1]:
			sv = 'TANDEM_DUP'
			start = str(int(line_l[1]) +1)
			end = info_f[0].split("=")
			svl = info_f[2].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[4], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
		elif "INS" in info_f[1]:
			sv = 'INSERTION'
			start = str(int(line_l[1]) + 1)
			if "SVLEN=" in info_f[2]:
				svl = info_f[2].split("=")
				end = int(int(line_l[1]) + int(svl[1]) - 1)
				endpoint.append(str(end))
				le.append(str(abs(int(svl[1]))))
			else:
				end = 'n/a'
				endpoint.append(end)
				svl = 'n/a'
				le.append(svl)
			startpoint.append(start)
			svtype.append(sv)
			print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[4], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
		elif "BND" in info_f[0]:
			sv = info_f[0].split("=")
			start = str(int(line_l[1]) + 1)
			end = 'n/a'
			svl = 'n/a'
			startpoint.append(start)
			endpoint.append(end)
			svtype.append(sv[1])
			le.append(svl)
			print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[4], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
