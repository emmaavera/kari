#!/usr/bin/python
#Emma Bernstein

'''Not tested on three centered bonds'''
import time

def remove_paren(mystr):
	#takes out text between parens
	#Assume none nested 
	#print mystr
	if (mystr.find("(") == -1 or mystr.find(")") == -1):
		return mystr
	else:
		end = mystr.find(")")
		start = mystr.find("(")
		mystr = mystr[:start] + mystr[end+1:] 
		#print mystr
		#time.sleep(.4)
		return remove_paren(mystr)

def npa_summary_matrix(file):
	f = open(file, 'r')
	x = f.readlines()
	f.close()
	data = [["ATOM"], ["CHARGE"], ["CORE"], ["VALENCE"], ["RYDBERG"], ["TOTAL"]]
	i = 0
	while (i < len(x)):
		if (x[i] == " Summary of Natural Population Analysis:\n"):
			i+=6;
			while (i < len(x)):
					if ("=" in x[i][4:9]):
						i = len(x)
					else:
						data[0].append(x[i][4:9])
						data[1].append(x[i][11:19])
						data[2].append(x[i][24:32])
						data[3].append(x[i][36:44])
						data[4].append(x[i][47:55])
						data[5].append(x[i][59:67])
						i+=1
		else:
			i+=1
	return data

'''
file name will indicate bond type
'''
def npa_data_by_orbital_type(reac_file, ts_file, prod_file, bond_type):
	reac_data = zip(*npa_summary_matrix(reac_file))
	print reac_data
	ts_data = zip(*npa_summary_matrix(ts_file))
	print ts_data
	prod_data = zip(*npa_summary_matrix(prod_file))
	#sort them use zip(*output)
	#note that zip(*my_list) will return a list of tuples, which are IMMUTABLE
	i = 0
	while i < len(reac_data):
		reac_data[i] = list(reac_data[i])
		ts_data[i] = list(ts_data[i])
		prod_data[i] = list(prod_data[i])
		i+=1

	#sort
	bucket = [[],[],[]] #reac, ts, prod
	i = 0
	j = 0
	ts_filled = 0
	prod_filled = 0
	while i < len(reac_data):
		#print "i = " + str(i) +"\n"
		bucket[0].append(reac_data[i])
		j = 0
		ts_filled = 0
		prod_filled = 0
		while j < len(ts_data):
			#print "j = " + str(j) +"\n"
			if (reac_data[i][0] == ts_data[j][0]):
				bucket[1].append(ts_data[j])
				ts_filled = 1
			if reac_data[i][0] == prod_data[j][0]:
				bucket[2].append(prod_data[j])
				prod_filled = 1
			if prod_filled and ts_filled:
				j = len(ts_data)
			j+=1
		if not prod_filled:
			bucket[2].append(['NONE'])
		if not ts_filled:
			bucket[2].append(['NONE'])
		i+=1

	reac_data = bucket[0]
	focus_index = 0
	try:
		focus_index = reac_data[0].index(bond_type)
	except:
		print "The bond type you have entered is invalid.  Try one of the following:" 
		print reac_data[0]
		return
	#write to file
	reac_data = zip(*bucket[0])
	ts_data = zip(*bucket[1])
	prod_data = zip(*bucket[2])
	output = []
	output.append(reac_data[0]) #atoms
	output.append(reac_data[focus_index])
	output.append(ts_data[focus_index])
	output.append(prod_data[focus_index])
	output = zip(*output)
	i = 0
	while i < len(output):
		output[i] = list(output[i])
		i+=1

	output[0].append("TS - REAC")
	output[0].append("% CHANGE")
	output[0].append("PROD - TS")
	output[0].append("% CHANGE")
	#find these vals
	i = 1
	while i < len(output):
		reac_val = float(output[i][1])
		ts_val = float(output[i][2])
		prod_val = float(output[i][3])
		output[i].append(str(ts_val - reac_val))
		if reac_val == 0:
			output[i].append('division by zero')
		else:
			output[i].append(str(100*(ts_val - reac_val)/reac_val))
		output[i].append(str(prod_val - ts_val))
		if ts_val == 0:
			output[i].append('division by zero')
		else:
			output[i].append(str(100*(prod_val - ts_val)/ts_val))
		i += 1
	text_file = open("atom_npa_"+bond_type+".txt", "w")
	text_file.write(ret_2D(output))
	text_file.close()






def print_orbitals(file, output_name):
	#output = "~~~  HYDRIDIZATION  ~~~\n"
	output = ""
	section = []
	f = open(file, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	#loop thorugh the list x and split into sublists w/each element as a column
	i = 0
	#pull out section with occupancy data
	while (i < len(x)):
		if (x[i] == "     (Occupancy)   Bond orbital/ Coefficients/ Hybrids\n"):
			i+=2; #skip over dashed line
			while (i < len(x)):
				#end condition
				if (x[i] == " NHO DIRECTIONALITY AND BOND BENDING (deviations from line of nuclear centers)\n"):
					i = len(x)
					#print section
				else:
					section.append(x[i])
					i+=1
		else:
			i+=1
	i = 0
	#print section
	is_ryd = 0
	while (i < len(section)):
		if ("." in section[i][:6]): #each numbered line
			#bond type
			if (" BD " in section[i]):
				output += "2-C Bond    "
			elif (" CR " in section[i]):
				output += "Core        "
			elif (" 3C " in section[i]):
				output += "**WARNING: please see scripts.py**\n3-C Bond    "
			elif (" BD*" in section[i]):
				output += "2-C Antibond"
			elif (" RY " in section[i]):
				is_ryd = 1
				#output += "Ryd         "
			elif ("RY*" in section[i]):
				is_ryd = 1
				#output += "Ryd Antibond"
			elif (" LP " in section[i]):
				output += "Lone Pair   "
			else:
				output += "***UNIDENTIFIED BOND TYPE***"
			#who is the bond between
			#hybridization 
			#INCOMPLETE
			if is_ryd == 0:
				output += " | " + section[i][24:35] +"\n"
				if ("-" in section[i]): #pull data from two lines
					curr = i
					i+=1
					while (i-curr < 7):
						if ("(" in section[i]): #line w/hydridization
							output += "  *" + section[i][27:33] + "*  " + remove_paren(section[i][35:])
							i+=1
						else:
							i+=1
				else: #pull data from this line
					output += "   " + remove_paren(section[i][41:])
			is_ryd = 0
			i+=1
		else:
			i+=1
	text_file = open("output_"+output_name+".txt", "w")
	text_file.write(output)
	text_file.close()
	#print output

def split_every(str, num):
	#split a str every num indexes and return a list
	curr = 0
	out = []
	while curr + num < len(str):
		out.append(str[curr:curr+num].strip())
		curr += num
	out.append(str[curr:].strip())
	return out

def file_replace(file_to_replace, old, new):
	f = open(file_to_replace, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	i = 0
	output = ""
	while (i < len(x)):
		output += x[i].replace(old, new)
		#print str(i) + ": " + output + "\n"
		i+=1
	text_file = open(file_to_replace, "w")
	#print output.rstrip()
	text_file.write(output.strip())  #changed from rstrip
	text_file.close()

def coord_fix(keyword, file_to_replace, guide_file):
	#print "Call to coord_fix"
	#parse guide file, make dictionary from input lexicon to univ
	f = open(guide_file, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	#split every 7 characters
	i = 0
	list_key = []
	list_val=[]
	while i < len(x):
		if keyword in x[i]:
			list_key = split_every(x[i], 7)
			i+=1
		elif "UNIV" in x[i]:
			list_val = split_every(x[i], 7)
			i+=1
		else:
			i+=1
	if (list_key == [] or list_val==[]):
		print "  ***  WARNING  ***  \nsomething has gone wrong with keyword!\n"
	i = 0
	if (len(list_key) != len(list_val)):
		print "  ***  WARNING  ***  \nlen of list_key != len of list_val\n"
	while i < len(list_key):
		file_replace(file_to_replace, list_key[i], list_val[i])
		#print "- success: replaced " + list_key[i] + " with " + list_val[i]
		i+=1
'''   combinds output files to a single file that 
      traces bond by bond changes from reac to ts
      to prod
'''
def synthesize(file_1, file_1_key, file_2, file_2_key, file_3, file_3_key):
	#4 spaces = indent
	#open all files
	search_key = ""
	#2D
	name_1 = file_1
	name_2 = file_2
	name_3 = file_3
	output = []
	output.append([file_1_key])
	output.append([file_2_key])
	output.append([file_3_key])
	f_1 = open(file_1, 'r')
	file_1 = f_1.readlines() #returns list of lines read
	f_1.close()
	f_2 = open(file_2, 'r')
	file_2 = f_2.readlines() #returns list of lines read
	f_2.close()
	f_3 = open(file_3, 'r')
	file_3 = f_3.readlines() #returns list of lines read
	f_3.close()
	i = 0
	j = 1
	f2_index = 0
	f3_index = 0
	#work through f_1, looking @ lines where char[0] != " "
	#and finding them in other two files
	while (i < len(file_1)):
		if file_1[i][0] != " ": #line contains bond label
			search_key = file_1[i]
			#look for following lines & add to correct output
			if search_key in file_2:
				f2_index = file_2.index(search_key)
			else:
				print "  ***  WARNING  ***  \n" + search_key + "not found in "+ str(name_2) + "\n"
			if search_key in file_3:
				f3_index = file_3.index(search_key)
			else:
				print "  ***  WARNING  ***  \n" + search_key + "not found in"+ str(name_3) +"\n"
			while i+j<len(file_1) and file_1[i+j][0] == " ":
				output[0].append(file_1[i+j])
				output[1].append(file_2[f2_index+j])
				output[2].append(file_3[f3_index+j])
				j += 1
				#print str(i+j) + ": " + str(output) + "\n\n\n\n"
			i += j
			j = 1
		else: 
			i+=1
	output = zip(*output)
	text_file = open("synth.txt", "w")
	text_file.write(ret_2D(output))
	text_file.close()

def ret_2D(my_list):
	output = ""
	i = 0
	j = 0
	while (i < len(my_list)):
		j=0
		while (j < len(my_list[i])):
			output += left_justified_str_of_len(my_list[i][j], 25)
			j+=1
		i+=1
		output += "\n"
	return output

def left_justified_str_of_len(mystr, col_wid):
	mystr = mystr.strip()
	while (len(mystr) < col_wid):
		mystr += " "
	return mystr


def print_energy(file, output_name, keyword):
	#output = "~~~  HYDRIDIZATION  ~~~\n"
	output = ""
	info = []
	info.append(["BOND TYPE"])
	info.append(["ATOMS"])
	info.append(["ENERGY"])
	f = open(file, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	#loop thorugh the list x and split into sublists w/each element as a column
	i = 0
	#pull out section with occupancy data
	#print "LENGTH OF ENERGY FILE: " + str(len(x))
	while (i < len(x)):
		if (x[i] == " NATURAL BOND ORBITALS (Summary):\n"):
			i+=6; #skip over dashed line & headers
			#pull out the info 
			while (i < len(x)):
				if ("          -------------------------------" in x[i]):
					i = len(x)
					#print "~END of ENERGY~"
				elif (x[i][3] == " "):
					i+=1
					#print "successful skip!"
				if (i != len(x)):
					#print "LENGTH OF ENERGY FILE: " + str(len(x))
					#print "i = " + str(i)
					#print x[i]
					#print "LENGTH of x[i]: " + str(len(x[i]))
					info[0].append(x[i][6:9])
					info[1].append(x[i][14:24])
					info[2].append(x[i][43:51])
					i+=1;
		else:
			i+=1
	info = zip(*info)
	text_file = open("energy_"+output_name+".txt", "w")
	text_file.write(ret_2D(info))
	text_file.close()
	coord_fix(keyword, "energy_"+output_name+".txt", "universal_coords.txt")
	#print output

def delt(reac_file, ts_file, prod_file):
	info = []
	info.append(["BOND TYPE"])      #0
	info.append(["ATOMS"])          #1
	info.append(["R"])				#2
	info.append(["TS"])				#3
	info.append(["P"])				#4
	info.append(["TS-R"])			#2 --> 5
	info.append(["% CHANGE"])		#6
	info.append(["P-TS"])  			#3 --> 7
	info.append(["% CHANGE"])		#8

	f = open(reac_file, 'r')
	reac = f.readlines() #returns list of lines read
	f.close()	
	f = open(ts_file, 'r')
	ts = f.readlines() #returns list of lines read
	f.close()
	f = open(prod_file, 'r')
	prod = f.readlines() #returns list of lines read
	f.close()

	i = 1
	bt = "" #bond type
	atoms = ""
	ts_energy = ""
	reac_energy = ""
	prod_energy = ""

	while (i < len(ts)): #ts is longest file
		if ts[i][0] == " ":
			i+=1
		else:
			bt = ts[i][:20].strip()
			atoms = ts[i][20:40].strip()
			ts_energy = ts[i][40:].strip()
			info[0].append(bt) #add bond type
			info[1].append(atoms)
			#search for same bond in reac
			energy_reac = 0
			energy_ts = 0
			energy_prod =0
			j = 0
			is_val = 0
			while (j<len(reac)):
				energy_ts = float(ts[i][40:].strip())
				info[3].append(str(energy_ts))
				if bt in reac[j] and atoms in reac[j]:
					energy_reac = float(reac[j][40:].strip())
					info[2].append(str(energy_reac))
					info[5].append(str(energy_ts - energy_reac))
					info[6].append(str(100*(energy_ts - energy_reac)/energy_reac))
					is_val = 1
				j+=1
			if is_val == 0:
				info[2].append("N/A")				
				info[5].append("N/A")
				info[6].append("N/A")
			#search for same bond in prod
			k = 0
			is_val = 0			
			while (k<len(prod)):
				if bt in prod[k] and atoms in prod[k]:
					energy_prod = float(prod[k][40:].strip())
					info[4].append(str(energy_prod))
					info[7].append(str(energy_prod - energy_ts))
					info[8].append(str(100*(energy_prod - energy_ts)/energy_ts))
					is_val = 1
				k+=1
			if is_val == 0:
				info[4].append("N/A")
				info[7].append("N/A")
				info[8].append("N/A")
			i+=1
	info = zip(*info)
	text_file = open("energy_delta.txt", "w")
	text_file.write(ret_2D(info))
	text_file.close()

#print npa_summary_matrix("reac/reac_nbo.qcin.out")
npa_data_by_orbital_type("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", "CHARGE")
npa_data_by_orbital_type("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", "VALENCE")
npa_data_by_orbital_type("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", "RYDBERG")
npa_data_by_orbital_type("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", "TOTAL")
npa_data_by_orbital_type("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", "CORE")


'''
print "---  NPA                                             ---"
print "***  print_orbitals for irc_reac, irc, ts, and prod  ***"
print_orbitals("irc_reac/irc_reac_nbo_with_charge.qcin.out", "irc_9reac")
print_orbitals("reac/reac_nbo.qcin.out", "reac")
print_orbitals("ts/ts_nbo.qcin.out", "ts")
print_orbitals("prod/prod_nbo.qcin.out", "prod")
print "***  print_orbitals complete!                        ***"
print "***  coord_fix for irc, ts, and prod                 ***"
coord_fix("REAC", "output_reac.txt", "universal_coords.txt")
coord_fix("TS", "output_ts.txt", "universal_coords.txt")
coord_fix("PROD", "output_prod.txt", "universal_coords.txt")
print "***  coord_fix complete!                             ***"
print "***  synthesize for irc, ts, and prod                ***"
synthesize('output_reac.txt', 'REAC', 'output_ts.txt', 'TS  ', 'output_prod.txt', 'PROD')
print "***  synthesize complete!                            ***"
print "---  ENERGY                                          ---"
print "***  print_energy                                    ***"
print_energy("reac/reac_nbo.qcin.out", "reac", 'REAC')
print_energy("ts/ts_nbo.qcin.out", "ts", 'TS  ')
print_energy("prod/prod_nbo.qcin.out", "prod",'PROD')
print "***  print_energy complete!                          ***"
print "***  delt                                            ***"
delt("energy_reac.txt", "energy_ts.txt", "energy_prod.txt")
print "***  delt complete!                                  ***"
'''

