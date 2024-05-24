import filecmp
import os
import sys

sys.path.append('../')
from make_cap_ligand import *


def test_get_atoms_to_strip():

	strip_pattern, rename_list = get_atoms_to_strip('input/ads081_precap.mol2')

	print(strip_pattern)

	assert strip_pattern == '58,59,60,69,71,72,68,76,77,78,79,80,81,82,83,84,85,'

	print(rename_list)

	assert rename_list == [53, 57, 67, 75]


def test_make_cap_ligand():
	
	os.chdir('output')

	os.system('cp ../input/ads081_precap.mol2 .')

	make_cap_ligand('ads081_precap.mol2', 'ads081_cap.pdb')

	assert filecmp.cmp('../input/ads081_cap.pdb', 'ads081_cap.pdb') is True

	os.chdir('../')


def test_rename_atoms():
	
	rename_atoms('input/ads081_cap.pdb', [53, 57, 67, 75], 'output/ads081_cap_renamed.pdb')

	assert filecmp.cmp('input/ads081_cap_renamed.pdb', 'output/ads081_cap_renamed.pdb') is True


def test_grep_ligand_and_cap():
	
	grep_ligand_and_cap('input/ADS158081.pdb', 'output/ADS158081_precap.pdb')

	assert filecmp.cmp('input/ADS158081_precap.pdb', 'output/ADS158081_precap.pdb') is True

test_grep_ligand_and_cap()


