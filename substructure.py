import os
import sys

from rdkit import Chem

input = sys.argv[1]

#m = Chem.MolFromMolFile(input) #mol2
m = Chem.MolFromPDBFile(input)

#sub = m.GetSubstructMatches(Chem.MolFromSmarts('[#6](-[#6]=[#8])(-[#7])-[#6]-[#16]-[#6]-[#6]-[#6]=[#8]'))
sub = m.GetSubstructMatches(Chem.MolFromPDBFile('warhead.pdb'))

print(sub)
