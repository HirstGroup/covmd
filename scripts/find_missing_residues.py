
def get_residue_list(chain, input):
	"""
	Get lists of residue names and IDs from chain in input PDB

	Parameters
	----------
	chain : char
		Input chain character
	input : str
		Input PDB protein file

	Returns
	-------
	resname_list : list of str
		List of residue names
	resid_list : list of in
		List of residue IDs
	"""

	resname_list = []
	resid_list = []

	with open(input) as f:

		first = True

		for line in f:

			if not line.startswith('ATOM'):
				continue

			resname = line[17:20]
			resid = int(line[22:26])
			chain_line = line[21]

			if chain_line != chain:
				continue

			# skip ligand since it's not part of the protein
			if resname == 'LIG':
				continue

			if not first:

				if resid != resid_list[-1]:

					resid_list.append(resid)
					resname_list.append(resname)

			if first:

				resid_list.append(resid)
				resname_list.append(resname)
				first = False

	return resname_list, resid_list	


def find_missing_residues(chain, input):
	"""
	Find missing residues (resids) in a protein chain

	Parameters
	----------
	chain : char
		Input chain character
	input : str
		Input PDB protein file

	Returns
	-------
	missing_residues : list of int
		List of resids missing in protein chain
	"""

	resname_list, resid_list = get_residue_list(chain=chain, input=input)

	resid_list_full = list(range(resid_list[0], resid_list[-1] + 1))

	missing_residues = [i for i in resid_list_full if i not in resid_list]

	return missing_residues


def add_missing_residues(aux, chain_aux, chain_input, input, missing_residues_input, output):

	resname_list_aux, resid_list_aux = get_residue_list(chain=chain_aux, input=aux)

	residues_to_add = [i for i in missing_residues_input if i in resid_list_aux]

	print(aux, residues_to_add)

	missing_residues_input_new = [i for i in missing_residues_input if i not in residues_to_add]

	return missing_residues_input_new


def add_missing_residues_loop(chain, input, aux_list, output):

	missing_residues_input = find_missing_residues(chain=chain, input=input)

	for aux in aux_list:

		missing_residues_input = add_missing_residues(aux=aux, chain_aux=chain, chain_input=chain, input=input, missing_residues_input=missing_residues_input, output=output)

	missing_residues_input_range = list_to_range(missing_residues_input)

	return missing_residues_input_range


def list_to_range(L):
	"""
	Shorten a list to show ranges
	"""

	from itertools import count, groupby

	G=(list(x) for _,x in groupby(L, lambda x,c=count(): next(c)-x))

	return ",".join("-".join(map(str,(g[0],g[-1])[:len(g)])) for g in G)




		
