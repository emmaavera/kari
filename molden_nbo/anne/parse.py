#!/usr/bin/python
#Emma Bernstein

def get_atom_coords(file, number):
	f = open(file, 'r')
	x = f.readlines() #returns list of lines read
	f.close()
	#loop thorugh the list x and split into sublists w/each element as a column
	j = 0
	for i in range(0, len(x)):
		if str(number) in x[i]:
			x[i] = x[i].split(" ")
			while '' in x[i]:
				x[i].remove('')
			if x[i][1] == str(number):
				print "file: "+ file + " | Coordinates of atom #" + str(number) + ": "
				return x[i][6], x[i][7], x[i][7]
	print "Atom #" + str(number) + " not found in " + file
	x = ''
	return x


print "Testing get_atom_coords" 
print get_atom_coords('RS.pdb', 8099)
print get_atom_coords('RS.pdb', 7087)
print get_atom_coords('RS.pdb', 0000)
print get_atom_coords('PS.pdb', 8099)
print get_atom_coords('PS.pdb', 7087)
print get_atom_coords('PS.pdb', 0000)