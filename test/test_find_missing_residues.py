import filecmp
import os
import sys

sys.path.append('../')
from scripts.find_missing_residues import *


def test_get_residue_list():

	resname_list, resid_list = get_residue_list(chain='A', input='./input/ADS158081_2.48_A_AB_al.pdb')

	print(resname_list)


def test_find_missing_residues():

	os.chdir('output')

	os.system('cp ../input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb .')

	missing_residues = find_missing_residues(input='ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', chain='A')

	assert missing_residues == [761, 762, 797, 798, 799, 800, 801, 802]

	os.chdir('../')


def test_find_missing_residues2():

	os.chdir('output')

	os.system('cp ../input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb .')

	missing_residues = find_missing_residues(input='ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', chain='B')

	assert missing_residues == [264]

	os.chdir('../')


def test_find_missing_residues_all():

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		missing_residues = find_missing_residues(input=f'./input/{file}', chain='A')

		print(file, missing_residues)


def test_add_missing_residues():

	os.chdir('output')

	os.system('cp ../input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb .')
	os.system('cp ../input/ADS158081_2.48_A_AB_al.pdb .')

	missing_residues_input = find_missing_residues(chain='A', input='ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb')

	missing_residues_input_new = add_missing_residues(aux='ADS158081_2.48_A_AB_al.pdb', chain_aux='A', chain_input='A', input='ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', missing_residues_input=missing_residues_input)

	print('still missing', missing_residues_input_new)

	os.chdir('../')


def test_add_missing_residues_all():

	missing_residues_input = find_missing_residues(chain='A', input='./input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb')

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		missing_residues_input_new = add_missing_residues(aux=f'./input/{file}', chain_aux='A', chain_input='A', input='./input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', missing_residues_input=missing_residues_input)


def test_add_missing_residues_all_156_b():

	missing_residues_input = find_missing_residues(chain='B', input='./input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb')

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		missing_residues_input_new = add_missing_residues(aux=f'./input/{file}', chain_aux='B', chain_input='B', input='./input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', missing_residues_input=missing_residues_input)


def test_add_missing_residues_all_081_a():

	missing_residues_input = find_missing_residues(chain='A', input='./input/ADS158081_2.48_A_AB_al.pdb')

	print('missing 081', missing_residues_input)

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		missing_residues_input_new = add_missing_residues(aux=f'./input/{file}', chain_aux='A', chain_input='A', input='./input/ADS158081_2.48_A_AB_al.pdb', missing_residues_input=missing_residues_input)


def test_add_missing_residues_all_081_b():

	missing_residues_input = find_missing_residues(chain='B', input='./input/ADS158081_2.48_A_AB_al.pdb')

	print('missing 081', missing_residues_input)

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		missing_residues_input_new = add_missing_residues(aux=f'./input/{file}', chain_aux='B', chain_input='B', input='./input/ADS158081_2.48_A_AB_al.pdb', missing_residues_input=missing_residues_input)


def test_add_missing_residues_loop_a():

	os.chdir('output')

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:
		os.system(f'cp ../input/{file} .')

	missing_residues_input = add_missing_residues_loop(chain='A', input='ADS158081_2.48_A_AB_al.pdb', aux_list=files)

	assert missing_residues_input == ''

	print(missing_residues_input)

	os.chdir('../')


def check_resnames():
	"""
	Check that resnames the same for same resids
	"""

	resname_list_a, resid_list_a = get_redidue_list(chain='A', input='input/NOT0002_2.07_A_AB_al.pdb')

	resname_list_b, resid_list_b = get_redidue_list(chain='A', input='input/ADS160919_1.92_A_AB_al.pdb')

	for index_a, resid_a in enumerate(resid_list_a):
		if resid_a in resid_list_b:
			index_b = resid_list_b.index(resid_a)
			assert resid_list_a[index_a] == resid_list_b[index_b]

	print('All resnames the same for common resids')


def check_resnames_loop():
	"""
	Check that resnames the same for same resids for all files
	"""

	resname_list_a, resid_list_a = get_redidue_list(chain='A', input='input/NOT0002_2.07_A_AB_al.pdb')

	files = ['NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb', 'ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:

		resname_list_b, resid_list_b = get_redidue_list(chain='A', input='input/ADS160919_1.92_A_AB_al.pdb')

		for index_a, resid_a in enumerate(resid_list_a):
			if resid_a in resid_list_b:
				index_b = resid_list_b.index(resid_a)
				assert resid_list_a[index_a] == resid_list_b[index_b]

		print('All resnames the same for common resids', file)

def test_list_to_range():

	input = [1,2,3,6,7,9]

	output = list_to_range(input)

	assert output == '1-3,6-7,9'

	print(output)


def test_complete_ads081_a():
	"""
	Run loop for ads081 chain a to complete it with missing residues
	"""

	os.chdir('output')

	files = ['ADS160082_1.88_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb'] #, 'NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', ''ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:
		os.system(f'cp ../input/{file} .')

	missing_residues_input = add_missing_residues_loop(chain='A', input='ADS158081_2.48_A_AB_al.pdb', aux_list=files)

	assert missing_residues_input == ''

	print(missing_residues_input)

	os.chdir('../')	


def test_complete_ads081_b():
	"""
	Run loop for ads081 chain b to complete it with missing residues
	"""

	os.chdir('output')

	files = ['ADS160082_1.88_A_AB_al.pdb', 'NOT0016_1.88_A_AB_al.pdb'] #, 'NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', ''ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:
		os.system(f'cp ../input/{file} .')

	missing_residues_input = add_missing_residues_loop(chain='B', input='ADS158081_2.48_A_AB_al.pdb', aux_list=files)

	assert missing_residues_input == ''

	print(missing_residues_input)

	os.chdir('../')	


def test_complete_ads156_a():
	"""
	Run loop for ads156 chain a to complete it with missing residues
	"""

	os.chdir('output')

	files = ['NOT0016_1.88_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb'] #, 'NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', ''ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:
		os.system(f'cp ../input/{file} .')

	missing_residues_input = add_missing_residues_loop(chain='A', input='ADS158156_1.95_A_AB_al.pdb', aux_list=files)

	assert missing_residues_input == ''

	print(missing_residues_input)

	os.chdir('../')	


def test_complete_ads156_b():
	"""
	Run loop for ads156 chain b to complete it with missing residues
	"""

	os.chdir('output')

	files = ['NOT0016_1.88_A_AB_al.pdb', 'ADS160082_1.88_A_AB_al.pdb'] #, 'NOT0002_2.07_A_AB_al.pdb', 'ADS160919_1.92_A_AB_al.pdb', 'ADS160918_2.74_A_AB_al.pdb', ''ADS160243_2.55_A_AB_al.pdb', 'ADS158081_2.48_A_AB_al.pdb', 'NOT0001_2.50_A_AB_al.pdb', 'ADS160790_2.59_A_AB_al.pdb', 'ADS158156_1.95_A_AB_al.pdb']

	for file in files:
		os.system(f'cp ../input/{file} .')

	missing_residues_input = add_missing_residues_loop(chain='B', input='ADS158156_1.95_A_AB_al.pdb', aux_list=files)

	assert missing_residues_input == ''

	print(missing_residues_input)

	os.chdir('../')	


test_complete_ads156_b()

