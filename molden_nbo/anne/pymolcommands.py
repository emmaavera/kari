##Mar 10 2017
#N.Seelam

#Important PyMOL commands!

#Literally everything I will show you is better taught here: 

https://pymolwiki.org/index.php/Practical_Pymol_for_Beginners


#####################
#Loading a structure
#####################

#If you're in a folder of the protein, or you have a path to the pdb of interest, do the following:

load /path/to/protein.pdb

#If you're trying to get a structure from the PDB (protein data bank), you can use the awesome command 'fetch' to just get a structure given it's 3-4 letter code

fetch 3ltp #this is my baby <3<3<3 alas not the protein you'll be working on but still marvel how cute it is dawwwww


#####################
#Viewing a sequence
#####################
#Sometime it is helpful to figure out wtf is going on in the protein. The pdb is a sequence of atoms and their respective atomic positions. However, all atoms belong to a specific 'chain', and 'resi'due (amino acid). To see the sequence of amino-acids in a protein, or the names of small molecules that might be attached to it (such as waters, ions, sometimes even a small drug) we use the command 'seq_view':

set seq_view, on

#This should pop up a sequence view on the top of the screen.

#Alternatively, if you figure out what you want or simply hate screen clutter:

set seq_view, off 


#####################
#Viewing a sequence
#####################

#Pymol has several visualization tricks. Proteins, small molecules, and atoms can be seen in 'line', 'stick', 'cartoon', and 'ball' mode. The default is a fairly thick line.

hide everything #don't see any part of the protein. It is NOT GONE, but it will probably terrify you at first. Don't be scared, we're gonna get it back.

show cartoon #make everything in cartoon form, which should appear like secondary + tertiary form for you.

show sticks,

hide sticks,

show lines

#Note pymol default is Carbon == green, Nitrogen == blue, oxygen == red, hydrogen == white, sulfur == yellow (cysteine is probably what you see). Unnatural atoms have some varying colors (ex Mg. or whatever)

#####################
#Selecting a sequence
#####################

#You want to learn how to select things, such as picking a residue of interest in your active-site, or your ligand

sele <target name>, <identifier name of identifier>

#suppose you have the PS and you want to select all the asparagines (R) in chain B and chain a

sele args, resn args and (chain B or chain A)

#you don't need a name necessarily, because it will default to 'sele'

#The following names that you need to know:

#resn == amino acid 3 letter name (like Arginine is Arg or TIP3 for water)
#resi == amino acid position (like R203 is resi 203)
#chain == protein chain, should be like A, B, C etc.
#name == name of the atom (like waters are typically OH for oxygen)

#####################
#Changing a Viewpoint
#####################

#you can use the zoom command to look into a particular region. This can be done as such:

zoom <selection>

#so suppose we want to select in the ligand of interest, then we do

sele substrate, chain c and resn AC6 #note chain c alone is sufficient
zoom substrate

zoom #this takes you back to large view