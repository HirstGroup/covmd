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