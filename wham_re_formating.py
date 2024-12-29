import sys

vcf_lumpy = open(sys.argv[1])
#VCF
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  mtb_MTBCR170001_S9
#bed-like
#CHROM  type    str     stp	len     QUAL    FILTER  INFO    FORMAT  mtb_MTBCR170001_S9  
##0INFO=<ID=A,Number=1,Type=Integer,Description="Total pieces of evidence">
##1INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END for imprecise variants">
##2INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##3INFO=<ID=CF,Number=1,Type=Float,Description="Fraction of reads in graph that cluster with SVTYPE pattern">
##4INFO=<ID=CW,Number=5,Type=Float,Description="SVTYPE weight 0-1; DEL,DUP,INV,INS,BND">
##5INFO=<ID=D,Number=1,Type=Integer,Description="Number of reads supporting a deletion">
##6INFO=<ID=DI,Number=1,Type=Float,Description="Average distance of mates to breakpoint">
##7INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##8INFO=<ID=EV,Number=1,Type=Integer,Description="Number everted mate-pairs">
##9INFO=<ID=I,Number=1,Type=Integer,Description="Number of reads supporting an insertion">
##10INFO=<ID=SR,Number=1,Type=Integer,Description="Number of split-reads supporing SV">
##11INFO=<ID=SS,Number=1,Type=Integer,Description="Number of split-reads supporing SV">
##12INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##13INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##14INFO=<ID=T,Number=1,Type=Integer,Description="Number of reads supporting a BND">
##15INFO=<ID=TAGS,Number=.,Type=String,Description="SM tags with breakpoint support">
##16INFO=<ID=TF,Number=1,Type=Integer,Description="Number of reads mapped too far">
##17INFO=<ID=U,Number=1,Type=Integer,Description="Number of reads supporting a duplication">
##18INFO=<ID=V,Number=1,Type=Integer,Description="Number of reads supporting an inversion">
##19FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##20FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##21FORMAT=<ID=SP,Number=1,Type=Integer,Description="Per sample SV support">
#SVTYPE;SVLEN;END


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
		if "DEL" in info_f[13]:
			sv = 'DELETION'
			start = str(int(line_l[1]) + 1)
			end = info_f[7].split("=")
			svl = info_f[12].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "DUP" in info_f[13]:
			sv = 'DUPLICATION'
			start = str(int(line_l[1]) + 1)
			end = info_f[7].split("=")
			svl = info_f[12].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "INV" in info_f[13]:
			sv = 'INVERSION'
			start = str(int(line_l[1]) + 1)
			end = info_f[7].split("=")
			svl = info_f[12].split("=")
			startpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "DUP:TANDEM" in info_f[13]:
			sv = 'DUP:TANDEM'
			start = str(int(line_l[1]) + 1)
			end = info_f[7].split("=")
			svl = info_f[12].split("=")
			starpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "INS" in info_f[13]:
			sv = 'INSERTION'
			start = str(int(line_l[1]) + 1)
			if "SVLEN" in info_f[12]:
				svl = info_f[12].split("=")
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
		elif "CNV" in info_f[13]:
			sv = 'CNV'
			start = str(int(line_l[1]) + 1)
			end = info_f[7].split("=")
			svl = info_f[12].split("=")
			starpoint.append(start)
			endpoint.append(end[1])
			svtype.append(sv)
			le.append(str(abs(int(svl[1]))))
			if len(line_l) == 10:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[9], sep = "\t")
			elif len(line_l) == 11:
				print(line_l[0], svtype[0], startpoint[0], endpoint[0], le[0], line_l[5], line_l[6], line_l[7], line_l[8], line_l[10], sep = "\t")
		elif "BND" in info_f[13]:
			sv = info_f[13].split("=")
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
