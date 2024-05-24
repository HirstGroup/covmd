import argparse
import ast
import os
import sys
import textwrap

from run import run

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

	# hardcoded input
	ligname_list = ['UNL', 'UNK']
	headname = 'ASP'
	covname = 'CYS'
	tailname = 'HIS'

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








