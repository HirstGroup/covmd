import filecmp
import sys

sys.path.append('../')
from make_mc_file import *

def test_parse_input():

	d = parse_input('make_mc_file_input.txt')

	print(d)

	assert d == {'OMIT_NAME': [66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78], 'HEAD_NAME': 1, 'TAIL_NAME': 3, 'MAIN_CHAIN': 2}


def test_parse_mol2():

	d = parse_mol2('make_mc_file.mol2')

	print(d)

	assert d == {1: 'N1', 2: 'C1', 3: 'C2', 4: 'O1', 5: 'C3', 6: 'S1', 7: 'C4', 8: 'C5', 9: 'C6', 10: 'C7', 11: 'C8', 12: 'C9', 13: 'C10', 14: 'C11', 15: 'C12', 16: 'C13', 17: 'C14', 18: 'C15', 19: 'C16', 20: 'C17', 21: 'C18', 22: 'C19', 23: 'C20', 24: 'C21', 25: 'C22', 26: 'C23', 27: 'C24', 28: 'C25', 29: 'C26', 30: 'N2', 31: 'N3', 32: 'N4', 33: 'N5', 34: 'N6', 35: 'N7', 36: 'N8', 37: 'O2', 38: 'O3', 39: 'H1', 40: 'H2', 41: 'H3', 42: 'H4', 43: 'H5', 44: 'H6', 45: 'H7', 46: 'H8', 47: 'H9', 48: 'H10', 49: 'H11', 50: 'H12', 51: 'H13', 52: 'H14', 53: 'H15', 54: 'H16', 55: 'H17', 56: 'H18', 57: 'H19', 58: 'H20', 59: 'H21', 60: 'H22', 61: 'H23', 62: 'H24', 63: 'H25', 64: 'H26', 65: 'H27', 66: 'C27', 67: 'H28', 68: 'O4', 69: 'C28', 70: 'H29', 71: 'H30', 72: 'H31', 73: 'N9', 74: 'C29', 75: 'H32', 76: 'H33', 77: 'H34', 78: 'H35'}


def test_make_mc_file():

	atom_number_name = parse_mol2('make_mc_file.mol2')

	parts = parse_input('make_mc_file_input.txt')

	print(atom_number_name)
	print(parts)

	lines = make_mc_file(atom_number_name, parts, 'make_mc_file_output.txt')

	#assert filecmp.cmp('make_mc_file_output.txt', 'test_make_mc_file_output.txt')

	print(lines)


def test_get_pre_head_post_tail():

	parts = parse_input('make_mc_file_input.txt')

	atom_number_name = parse_mol2('make_mc_file.mol2')

	parts = get_pre_head_post_tail(parts, atom_number_name)

	print(parts)

	assert parts == {'OMIT_NAME': [66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78], 'HEAD_NAME': 1, 'TAIL_NAME': 3, 'MAIN_CHAIN': 2, 'PRE_HEAD_TYPE': 'C', 'POST_TAIL_TYPE': 'N'}


def test_parse_input_mol2():

	d = parse_input_mol2('input/ADS158081_cap_ok_gas.mol2')

	print(d)

	assert d == {'OMIT_NAME': [53, 54, 55, 56, 57, 62, 63, 64, 65, 67, 68, 69], 'HEAD_NAME': 58, 'TAIL_NAME': 60, 'MAIN_CHAIN': 59}



test_get_parts_auto()
