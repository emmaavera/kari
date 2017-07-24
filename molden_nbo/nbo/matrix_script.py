#!/usr/bin/python
#Emma Bernstein

from energy_and_npa_script import coord_fix


'''
returns an output string
'''
def array_2d_to_string(array_2d, col_wid):
	output = ""
	for i in range(0, len(array_2d)):
		for j in range(0, len(array_2d[i])):
			output += space(array_2d[i][j], col_wid)
		output += "\n"
	return output

'''
FIRST VERSION DOES NOT WORK
Print out changes in orbital occupancy (data drawn from "Bond orbital/ 
Coefficients/ Hybrids") and note changes in the following manner:
Bond Occupancy Changes for BD, BD*, and LP
------------TS - REAC--------------------------------PROD - TS------------
    occupancy    percent difference        occupancy    percent difference
Assumes that occ data already went through coord_fix
'''

def occupancy_changes(occupancy_data, col_wid):
	matrix = populate_occupancy_matrix("reac/reac_nbo.qcin.out", "ts/ts_nbo.qcin.out", "prod/prod_nbo.qcin.out", col_wid)
	#look thtorugh TS bonds and compare with REAC and PROD
	delta = [['BOND_TYPE ATOMS'], ['REAC'], ['TS'], ['PROD'],['TS-REAC'], ['% CHANGE'], ['PROD-TS'], ['% CHANGE']]
	reac = matrix[0][1]
	ts   = matrix[1][1]
	prod = matrix[2][1]
	#x[0] = bt atms, x[1] = occ
	#join bt and atm for easier search
	i = 0
	while i < len(reac[1]):
		reac[1][i] = reac[0][i] + "   " + reac[1][i]
		i+=1
	del reac[0]	
	i = 0
	while i < len(ts[1]):
		ts[1][i] = ts[0][i] + "   " + ts[1][i]
		i+=1
	del ts[0]	
	i = 0
	while i < len(prod[1]):
		prod[1][i] = prod[0][i] + "   " + prod[1][i]
		i+=1
	del prod[0]	

	#print matrix

	i = 1 #skip labels
	index = 0
	reac_occ = 0
	ts_occ = 0 
	prod_occ = 0

	r_is_num = 1 
	p_is_num = 1

	bond_id = ""
	atom_id = ""
	#print "HI MY NAME IS PROD \n\n\n\n" 
	#print prod
	while i < len(ts[0]):
		#collect information from the bond looking for...
		bond_id = ts[0][i]
		if ("RY" in bond_id):
			i+=1
		else:
			delta[0].append(bond_id)

			index = my_index(reac[0], bond_id)
			if index != -1:
				delta[1].append(reac[1][index])
				reac_occ = float(reac[1][index])
			else:
				delta[1].append("VALUE NOT FOUND")
				r_is_num = 0

			ts_occ  = float(ts[1][i])
			delta[2].append(ts_occ)

			index = my_index(prod[0], bond_id)
			if index != -1:
				delta[3].append(prod[1][index])
				prod_occ = float(prod[1][index])
			else:
				delta[3].append("VALUE NOT FOUND")
				p_is_num = 0

			if (r_is_num):
				delta[4].append(ts_occ-reac_occ)
				delta[5].append((ts_occ-reac_occ)/reac_occ)
			else:
				delta[4].append("N/A")
				delta[5].append("N/A")
				r_is_num = 1

			if (p_is_num):
				delta[6].append(prod_occ-ts_occ)
				delta[7].append((prod_occ-ts_occ)/ts_occ)
			else:
				delta[6].append("N/A")
				delta[7].append("N/A")
				p_is_num = 1
		i+=1
		#print delta
	text_file = open("occupancy_delta.txt", "w")
	text_file.write(array_2d_to_string(zip(*delta), col_wid))
	text_file.close()

'''
literally just index w/o the exception
'''
def my_index(my_list, x):
	try:
		index_value = my_list.index(x)
	except ValueError:
	    index_value = -1
	return index_value

'''
Adds spaces to the end of a string to make it have len col_wid
'''
def space(mystr, col_wid):
	mystr = str(mystr).strip()
	mystr[0:15]
	while (len(mystr) < col_wid):
		mystr += " "
	return mystr

'''
Returns an array of BOND_TYPE, ATOMS, OCCUPANCY for REAC, TS, ~or~ PROD
'''
def populate_occupancy_matrix_column(file):
	f = open(file, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	info = [['BOND_TYPE'], ['ATOMS'], ['OCCUPANCY']]
	i = x.index("     (Occupancy)   Bond orbital/ Coefficients/ Hybrids\n")
	i+=2; #skip over dashed line
	while (i < len(x)):
		#end condition
		if (x[i] == " NHO DIRECTIONALITY AND BOND BENDING (deviations from line of nuclear centers)\n"):
			i = len(x)
		else:
			if x[i][4:5] == ".":
				info[0].append(x[i][16:19]) #Bond type
				info[1].append(x[i][24:35]) #Atoms
				info[2].append(x[i][7:14])  #Occupancy
				i+=1
			else:
				i+=1
	return info

'''
Returns an array of BOND_TYPE, ATOMS, OCCUPANCY for REAC, TS, ~and~ PROD
*Set col_wid to a multiple of three 
returns the matrix fo data
'''
def populate_occupancy_matrix(file_first, file_second, file_third, col_wid):
	matrix = [['REAC'], ['TS  '],['PROD']]
	output = ""
	matrix[0].append(populate_occupancy_matrix_column(file_first))
	matrix[1].append(populate_occupancy_matrix_column(file_second))
	matrix[2].append(populate_occupancy_matrix_column(file_third))
	output += space('REAC', col_wid) + space('TS', col_wid) + space('PROD', col_wid) + "\n"
	i = 0
	'''
	print "MATRIX:\n"
	print matrix[0][1][1]
	'''
	while i < len(matrix[0][1][0]): #matrix[0][1] gives list of len three B-type, atoms, and occ
		for j in range(0,3):
			for k in range(0,3):
				output += space(matrix[j][1][k][i], (col_wid/3))
		output += "\n"
		i+=1
	text_file = open("occupancy_data.txt", "w")
	text_file.write(output)
	text_file.close()
	return matrix
'''
input: occupancy_data.txt ()
'''
def test_me():
	#fix all the coords
	col_wid = 20
	coord_fix("REAC", "reac/reac_nbo.qcin.out", "universal_coords.txt")
	coord_fix("TS", "ts/ts_nbo.qcin.out", "universal_coords.txt")
	occupancy_changes("occupancy_data.txt", col_wid)
test_me()


