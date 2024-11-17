import sys

filename = str(sys.argv[1])

with open(filename) as variant_file:
	for line in variant_file:
		line = line.replace("\n", "")
		line_l = line.split("\t")
		if "#" in line_l[0]:
			print("\t".join(line_l))

		else: #Each variant
			after_correction = line_l[0:9] #CHR - FORMAT
			for i in line_l[9:]: #Each indv
				indv_format = i.split(":")
				GT = "./."
				if indv_format[0] == "0/1":
					GT = "./."
				elif indv_format[0] == "./.":
					GT = "./."
				elif indv_format[0] == ".|.":
					GT = "./."
				elif indv_format[0] == "0|1":
					GT = "./."
				else: #Genotype field
					if int(indv_format[2]) < 10:
						GT = "./."
					else:
						if indv_format[0] == "0/0" or indv_format[0] == "0|0": #identify as reference sample
							AD = indv_format[1].split(",")
							
							if int(indv_format[2]) < 10:
								GT = "./."
							# Check alternative allele count
							#90% cut-off
							else:
								if round(int(AD[1])/int(indv_format[2]), 4) >= 0.1:
									GT = "./."
								else:
									GT = "0/0"
						elif indv_format[0] == "1/1" or indv_format[0] == "1|1": #identify as alternative sample
							AD = indv_format[1].split(",")
							
							if int(indv_format[2]) < 10:
								GT = "./."
							# Check reference allele count
							else:
								if round(int(AD[0])/int(indv_format[2]), 4) >= 0.1:
									GT = "./."
								else:
									GT = "1/1"

				indv_format[0] = GT
				indv_format_str = ":".join(indv_format) # all indv are added to new line
				after_correction.append(indv_format_str)
			print("\t".join(after_correction))
