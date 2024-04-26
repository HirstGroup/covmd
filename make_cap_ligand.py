import argparse
import os
import sys
import textwrap


def get_atoms_to_strip(input):
	"""
	Get atoms to strip to make capped ligand

	Parameters
	----------
	input : str
		Input MOL2 file

	Returns
	-------
	strip_pattern : str
		Strip pattern of atoms to strip for cpptraj
	rename_list : list of int
		List of atom numbers to rename to H
	"""

	# hardcoded input
	ligname = 'UNL'
	headname = 'ASP'
	covname = 'CYS'
	tailname = 'HIS'
	head_keep = [0, 1, 2, 3, 4, 17] # atoms from head to keep
	tail_keep = [0, 1, 2, 9, 10, 21] # atoms from tail to keep
	head_rename = [0, 4]
	tail_rename = [2, 10]

	with open(input) as f:
		lines = f.readlines()

	lig = []
	cov = []
	head = []
	tail = []
	strip = []

	sel = False

	for line in lines:

		if sel:

			if line.startswith('@<TRIPOS>BOND'):
				break

			resname = line.split()[7][0:3]
			atom_number = int(line.split()[0])

			if resname == ligname:
				lig.append(atom_number)
			if resname == covname:
				cov.append(atom_number)
			if resname == headname:
				head.append(atom_number)
			if resname == tailname:
				tail.append(atom_number)

		if line.startswith('@<TRIPOS>ATOM'):
			sel = True

	# update head and tail atom numbers based on first atom number in list	
	head_keep = [i+head[0] for i in head_keep]
	tail_keep = [i+tail[0] for i in tail_keep]
	head_rename = [i+head[0] for i in head_rename]
	tail_rename = [i+tail[0] for i in tail_rename]

	strip = []

	# populate strip list with atom numbers that should be stripped out
	for i in head:
		if i not in head_keep:
			strip.append(i)

	for i in tail:
		if i not in tail_keep:
			strip.append(i)

	strip_pattern = ''

	for i in strip:
		strip_pattern += f'{i},'

	return strip_pattern, head_rename + tail_rename


def rename_atoms(input, rename_list, output):
	"""
	Rename atoms in PDB to H

	Parameters
	----------
	input : str
		Input PDB file
	rename_list : list of in
		List of atom numbers to rename to H
	output : str
		Output PDB file
	"""

	with open(input) as f:
		lines = f.readlines()	

	with open(output, 'w') as f:

		for line in lines:

			if line.startswith('ATOM'):

				atom_number = int(line.split()[1])

				if atom_number in rename_list:

					line = line[:12] + ' H   ' + line[17:77] + 'H  \n'

			f.write(line)


def make_cap_ligand(input, output):
	"""
	Make capped ligand from MOL2 file containing ligand, 
	head residue (previous residue), cov residue (covalently bonded residue),
	and tail residue (next residue)

	Parameters
	----------
	input : str
		Input MOL2 file
	output : str
		Output file name
	"""

	strip_pattern, rename_list = get_atoms_to_strip(input)

	pdb_file_name = input[:-5] + '.pdb'
	renamed_file_name = input[:-5] + '_renamed.pdb'

	os.system(f'obabel {input} -O {pdb_file_name}')

	rename_atoms(pdb_file_name, rename_list, renamed_file_name)

	with open('strip.ptraj', 'w') as f:
		f.write(f'trajin {renamed_file_name}\n')
		f.write(f'strip @{strip_pattern}\n')
		f.write(f'trajout {output}\n')

	os.system(f'cpptraj {renamed_file_name} strip.ptraj')




