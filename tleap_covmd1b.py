import argparse
import textwrap

# hardcoded input
ligname = 'LIG'

def insert_lig(aux, input, output):
	"""
	Insert ligand prepc file into protein pdb file (with deleted hydrogens)

	Parameters
	----------
	aux : str
		Auxiliary ligand prepc file in PDB format to insert into protein PDB
	input : str
		Input PDB file of protein with deleted hydrogens and model ligand
	output : str
		Output PDB file
	"""

	with open(aux) as f:
		liglines = f.readlines()

	with open(input) as infile, open(output, 'w') as outfile:

		inserted = False

		for line in infile:
			if ligname in line and inserted is False:
				for ligline in liglines:
					outfile.write(ligline)
				inserted = True
			if ligname not in line:
				outfile.write(line)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=textwrap.dedent('''
        Insert ligand prepc file into protein pdb file (with deleted hydrogens) 
        '''), formatter_class=argparse.RawTextHelpFormatter)

    # required arguments
    parser.add_argument('-a','--aux', help='Auxiliary ligand prepc file in PDB format to insert into protein PDB', required=True)
    parser.add_argument('-i','--input', help='Input PDB file of protein with deleted hydrogens and model ligand', required=True)
    parser.add_argument('-o','--output', help='Output PDB file', required=True)

    args = parser.parse_args()

    insert_lig(args.aux, args.input, args.output)

