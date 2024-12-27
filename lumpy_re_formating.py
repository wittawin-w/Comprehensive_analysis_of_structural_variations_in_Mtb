import sys

vcf_lumpy = open(sys.argv[1])
#VCF
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  MTBCR170031_01_S26      mtb_MTBCR170031_01_S26
#bed-like
#CHROM  type    str     stp     len     QUAL    FILTER  INFO    FORMAT  mtv_ERR718192

##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DUP:TANDEM,Description="Tandem duplication">
##ALT=<ID=INS,Description="Insertion of novel sequence">
##ALT=<ID=CNV,Description="Copy number variable region">
#INFO_filed
#SVTYPE;SVLEN;END
#SVTYPE=BND


for line in vcf_lumpy:
	line = line.replace("\n", "")
	line_l = line.split("\t")
	startpoint = []
	endpoint = []
	svtype = []
	le = []
	if "#" in line_l[0]:
		continue
	else:
		info_f = line_l[7].split(";")
		if "DEL" in info_f[0]:
			sv = 'DELETION'
			start = str(int(line_l[1]) + 1)
			end = info_f[2].split("=")
			svl = info_f[1].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
		elif "DUP" in info_f[0]:
			sv = 'DUPLICATION'
			start = str(int(line_l[1]) + 1)
			end = info_f[2].split("=")
			svl = info_f[1].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "INV" in info_f[0]:
			sv = 'INVERSION'
			start = str(int(line_l[1]) + 1)
			end = info_f[2].split("=")
			svl = info_f[1].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "DUP:TANDEM" in info_f[0]:
			sv = 'DUP:TANDEM'
			start = str(int(line_l[1]) + 1)
			end = info_f[2].split("=")
			svl = info_f[1].split("=")
			starpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "INS" in info_f[0]:
			sv = 'INSERTION'
			start = str(int(line_l[1]) + 1)
			if "SVLEN" in info_f[1]:
				svl = info_f[1].split("=")
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
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "CNV" in info_f[0]:
			sv = 'CNV'
			start = str(int(line_l[1]) + 1)
			end = info_f[2].split("=")
			svl = info_f[1].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "BND" in info_f[0]:
			sv = info_f[0].split("=")
			start = str(int(line_l[1]) + 1)
			end = 'n/a'
			svl = 'n/a'
			startpoint.append(start)
			endpoint.append(end)
			svtype.append(sv[1])
			le.append(svl)
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")	
