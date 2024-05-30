import argparse
import ast
import os
import sys
import textwrap

from run import run


# hardcoded input
ligname_list = ['UNL', 'UNK']
headname = 'ASP'
covname = 'CYS'
tailname = 'HIS'


def get_atoms_to_strip(input, head_keep, head_rename, tail_keep, tail_rename):
	"""
	Get atoms to strip to make capped ligand

	Parameters
	----------
	input : str
		Input MOL2 file
	head_keep : list of int
		List of int starting from zero of atoms from head to keep,
		numbered relative to residue
	head_rename : list of int
		Atoms from head to rename to H
	tail_keep : list of int
		Atoms from tail to keep
	tail_rename : list of int
		Atoms from tail to rename to H

	Returns
	-------
	strip_pattern : str
		Strip pattern of atoms to strip for cpptraj
	rename_list : list of int
		List of atom numbers to rename to H
	"""

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

			if resname in ligname_list:
				lig.append(atom_number)
			if resname == covname:
				cov.append(atom_number)
			if resname == headname:
				head.append(atom_number)
			if resname == tailname:
				tail.append(atom_number)

		if line.startswith('@<TRIPOS>ATOM'):
			sel = True

	print(head, tail)

	# update numbers for head and tail from relative numbers within residue
	# given as input to actual numbers in molecule

	head_keep = [head[i] for i in head_keep]
	head_rename = [head[i] for i in head_rename]
	tail_keep = [tail[i] for i in tail_keep]
	tail_rename = [tail[i] for i in tail_rename]

	strip = []

	# populate strip list with atom numbers that should be stripped out
	for i in head:
		if i not in head_keep:
			strip.append(i)

	for i in tail:
		if i not in tail_keep:
			strip.append(i)

	print(strip)

	strip_pattern = ''

	for i in strip:
		strip_pattern += f'{i},'

	return strip_pattern, head_rename + tail_rename


def grep_ligand_and_cap(input, output, grep_pattern_list):
	"""
	Grep ligand (UNL and UNL1) can cap (CYS, ASP and HIS) from PDB Glide output

	Parameters
	----------
	input : str
		Glide PDB output
	output :  str
		Output file with ligand and cap
	"""

	with open(input) as infile, open(output, 'w') as outfile:
		for line in infile:
			for grep_pattern in grep_pattern_list:
				if grep_pattern in line:
					outfile.write(line)


def make_cap_ligand(input, output, head_keep, head_rename, tail_keep, tail_rename):
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
	head_keep : list of int
		List of int starting from zero of atoms from head to keep,
		numbered relative to residue
	head_rename : list of int
		Atoms from head to rename to H
	tail_keep : list of int
		Atoms from tail to keep
	tail_rename : list of int
		Atoms from tail to rename to H	 	
	"""

	strip_pattern, rename_list = get_atoms_to_strip(input, head_keep, head_rename, tail_keep, tail_rename)

	pdb_file_name = input[:-5] + '.pdb'
	renamed_file_name = input[:-5] + '_renamed.pdb'

	os.system(f'obabel {input} -O {pdb_file_name}')

	rename_atoms(pdb_file_name, rename_list, renamed_file_name)

	with open('strip.ptraj', 'w') as f:
		f.write(f'trajin {renamed_file_name}\n')
		f.write(f'strip @{strip_pattern}\n')
		f.write(f'trajout {output}\n')

	os.system(f'cpptraj {renamed_file_name} strip.ptraj')


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


def reorder_atoms_mol2(input, output):
	"""
	Reorder atoms in MOL2 file

	Parameters
	----------
	input : str
		Input MOL2 file name
	output :  str
		Output MOL2 file name

	Returns
	-------
	new_order : list of int
		List of int starting from zero with new_order for atoms
	"""

	print('WARNING: bonds and atom numbers not valid in output mol2, only use for charges')

	lig_lines = {}
	head_lines = {}
	cov_lines = {}
	tail_lines = {}

	with open(input) as infile:
		n = 0
		sel = False
		for line in infile:

			if '@<TRIPOS>BOND' in line:
				break

			if sel:
				resname = line.split()[7][0:3]

				if resname in ligname_list:
					lig_lines[n] = line
				elif resname == headname:
					head_lines[n] = line
				elif resname == covname:
					cov_lines[n] = line
				elif resname == tailname:
					tail_lines[n] = line
				else:
					raise Exception('WARNING: resname not in ligname, headname, covname or tailname')
				n += 1

			if '@<TRIPOS>ATOM' in line:
				sel = True

	# write first part of mol2 file
	with open(input) as infile, open(output, 'w') as f:
		for line in infile:
			f.write(line)
			if '@<TRIPOS>ATOM' in line:
				break

	# write second part (atom part) of mol2 file
	with open(output, 'a') as f:

		new_order = []
		for n, line in head_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in cov_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in tail_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in lig_lines.items():
			f.write(line)
			new_order.append(n)	

	# write third part of mol2 file
	with open(input) as infile, open(output, 'a') as f:
		sel = False
		for line in infile:
			if '@<TRIPOS>BOND' in line:
				sel = True
			if sel:
				f.write(line)

	return new_order


def reorder_atoms_pdb(input, output):
	"""
	Reorder atoms in PDB file

	Parameters
	----------
	input : str
		Input PDB file name
	output :  str
		Output PDB file name

	Returns
	-------
	new_order : list of int
		List of int starting from zero with new_order for atoms
	"""

	lig_lines = {}
	head_lines = {}
	cov_lines = {}
	tail_lines = {}

	with open(input) as infile:
		n = 0
		for line in infile:
			if 'ATOM' in line:
				resname = line[17:20]

				if resname in ligname_list:
					lig_lines[n] = line
				elif resname == headname:
					head_lines[n] = line
				elif resname == covname:
					cov_lines[n] = line
				elif resname == tailname:
					tail_lines[n] = line
				else:
					raise Exception('WARNING: resname not in ligname, headname, covname or tailname')
				n += 1

	new_order = []

	with open(output, 'w') as f:
		for n, line in head_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in cov_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in tail_lines.items():
			f.write(line)
			new_order.append(n)
		for n, line in lig_lines.items():
			f.write(line)
			new_order.append(n)

	return new_order


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=textwrap.dedent('''
        Make capped ligand from Glide covalent docking MOL2 output 
        '''), formatter_class=argparse.RawTextHelpFormatter)

    # required arguments
    parser.add_argument('-i','--input', help='Input file: MOL2 output from Glide covalent docking', required=True)
    parser.add_argument('-o','--output', help='Output file with capped ligand', required=True)
    parser.add_argument('-p','--param', help='Parameters dictionary', required=True)
    
    args = parser.parse_args()

    if args.input == args.output:
    	sys.exit('Abort: same input and output file names')

    param = ast.literal_eval(args.param)

    name = os.path.splitext(args.input)[0]

    print(name)

    run(f'obabel {args.input} -O {name}.pdb')

    grep_ligand_and_cap(f'{name}.pdb', f'{name}_precap.pdb', grep_pattern_list = param['grep_pattern_list'])

    run(f'obabel {name}_precap.pdb -O {name}_precap.mol2')

    make_cap_ligand(f'{name}_precap.mol2', args.output, param['head_keep'], param['head_rename'], param['tail_keep'], param['tail_rename'])








