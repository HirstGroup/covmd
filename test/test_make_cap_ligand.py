import filecmp
import os
import sys

sys.path.append('../')
from make_cap_ligand import *


def test_get_atoms_to_strip():

	strip_pattern, rename_list = get_atoms_to_strip('ads081_cap_ok.mol2')

	print(strip_pattern)

	assert strip_pattern == '58,59,60,69,71,72,68,76,77,78,79,80,81,82,83,84,85,'

	print(rename)

	assert rename_list == [53, 57, 67, 75]


def test_make_cap_ligand():
	
	os.chdir('output')

	os.system('cp ../ads081_cap_ok.mol2 .')

	make_cap_ligand('ads081_cap_ok.mol2', 'ads081_cap_ok_strip.pdb')


def test_rename_atoms():
	
	rename_atoms('ads081_cap_ok.pdb', [53, 57, 67, 75], 'output/ads081_cap_ok_renamed.pdb')


test_make_cap_ligand()