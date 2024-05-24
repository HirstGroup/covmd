import filecmp
import os
import sys

sys.path.append('../')
from make_cap_ligand import *


def test_get_atoms_to_strip():

	head_keep = [0,1,2,3,4,9] # atoms from head to keep
	tail_keep = [0,1,2,4,5,16] # atoms from tail to keep
	head_rename = [0, 4]
	tail_rename = [2,5]

	strip_pattern, rename_list = get_atoms_to_strip('input/ads081_precap.mol2', head_keep, head_rename, tail_keep, tail_rename)

	print(strip_pattern)

	assert strip_pattern == '58,59,60,69,71,72,68,76,77,78,79,80,81,82,83,84,85,'

	print(rename_list)

	assert rename_list == [53, 57, 67, 75]


def test_make_cap_ligand():
	
	os.chdir('output')

	os.system('cp ../input/ads081_precap.mol2 .')

	head_keep = [0,1,2,3,4,9] # atoms from head to keep
	tail_keep = [0,1,2,4,5,16] # atoms from tail to keep
	head_rename = [0, 4]
	tail_rename = [2,5]

	make_cap_ligand('ads081_precap.mol2', 'ads081_cap.pdb', head_keep, head_rename, tail_keep, tail_rename)

	assert filecmp.cmp('../input/ads081_cap.pdb', 'ads081_cap.pdb') is True

	os.chdir('../')


def test_rename_atoms():
	
	rename_atoms('input/ads081_cap.pdb', [53, 57, 67, 75], 'output/ads081_cap_renamed.pdb')

	assert filecmp.cmp('input/ads081_cap_renamed.pdb', 'output/ads081_cap_renamed.pdb') is True


def test_grep_ligand_and_cap():
	
	grep_ligand_and_cap('input/ADS158081.pdb', 'output/ADS158081_precap.pdb', ['UNL', 'UNL1', 'UNK', 'UNK1', 'ASP A 316', 'CYS A 317', 'HIS A 318'])

	assert filecmp.cmp('input/ADS158081_precap.pdb', 'output/ADS158081_precap.pdb') is True


# repeat tests for right ligand, ADS158081_right.mol2:

def test_grep_ligand_and_cap():
	
	grep_ligand_and_cap('input/ADS158081_right.pdb', 'output/ADS158081_right_precap.pdb', ['UNL', 'ASP A 314', 'CYS A 315', 'HIS A 316'])

	assert filecmp.cmp('input/ADS158081_right_precap.pdb', 'output/ADS158081_right_precap.pdb') is True


def test_get_atoms_to_strip():

	head_keep = [0,1,2,3,5,11] # atoms from head to keep
	tail_keep = [0,1,2,4,5,15] # atoms from tail to keep
	head_rename = [0, 5]
	tail_rename = [2, 5]

	strip_pattern, rename_list = get_atoms_to_strip('input/ADS158081_right_precap.mol2', head_keep, head_rename, tail_keep, tail_rename)

	print(strip_pattern)

	assert strip_pattern == '65,69,70,71,72,73,64,76,77,78,79,80,81,82,83,84,86,'

	print(rename_list)

	assert rename_list == [53, 68, 63, 75]


def test_make_cap_ligand():
	
	os.chdir('output')

	os.system('cp ../input/ADS158081_right_precap.mol2 .')

	head_keep = [0,1,2,3,5,11] # atoms from head to keep
	tail_keep = [0,1,2,4,5,15] # atoms from tail to keep
	head_rename = [0, 5]
	tail_rename = [2, 5]

	make_cap_ligand('ADS158081_right_precap.mol2', 'ADS158081_right_cap.mol2', head_keep, head_rename, tail_keep, tail_rename)

	assert filecmp.cmp('../input/ADS158081_right_cap.mol2', 'ADS158081_right_cap.mol2') is True

	os.chdir('../')

