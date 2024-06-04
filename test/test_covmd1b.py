import filecmp
import os
import sys

sys.path.append('../')
from tleap_covmd1b import *


def test_insert_lig():

	os.chdir('output')

	os.system('cp ../input/ADS158081_d.pdb .')
	os.system('cp ../input/ADS158081_cap_reorder_prepc.pdb .')

	insert_lig(aux='ADS158081_cap_reorder_prepc.pdb', input='ADS158081_d.pdb', output='ADS158081_d_lig.pdb')

	assert filecmp.cmp('ADS158081_d_lig.pdb', '../input/ADS158081_d_lig.pdb') is True

	os.chdir('../')


def test_insert_lig2():

	os.chdir('output')

	os.system('cp ../input/ADS158081_cap_reorder_prepc.pdb .')
	os.system('cp ../input/ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb .')

	insert_lig(aux='ADS158081_cap_reorder_prepc.pdb', input='ADS158156_1.95_A_AB_al_ok_d_ok_atom.pdb', output='ADS158081_cap_reorder_protein.pdb', ligname='F02')

	assert filecmp.cmp('ADS158081_cap_reorder_protein.pdb', '../input/ADS158081_cap_reorder_protein.pdb') is True

	os.chdir('../')