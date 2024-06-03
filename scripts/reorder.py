import sys, os

import make_cap_ligand

name = sys.argv[1]

sys.path.append('/home/pczbf/cdk_scripts')

import md

new_order = make_cap_ligand.reorder_atoms_pdb(input=f'{name}_cap.pdb', output=f'{name}_cap_reorder.pdb')

make_cap_ligand.reorder_atoms_mol2_from_new_order(input=f'{name}_cap_opt.mol2', new_order=new_order, output=f'{name}_cap_opt_reorder.mol2')

os.system(f'obabel {name}_cap_opt_reorder.mol2 -opdb | grep ATOM > {name}_cap_opt_reorder.pdb')

md.create_resp2_file(infile=f'{name}_cap_opt_reorder.pdb', outfile=f'{name}_cap_opt_reorder_esp.gau', charge=0, cpu=8, format='pdb')

os.system(f'g16 {name}_cap_opt_reorder_esp.gau')

os.system(f'obabel {name}_cap_reorder.pdb -O {name}_cap_reorder.mol2')

md.create_resp3_file(infile=f'{name}_cap_opt_reorder_esp.log', outfile1=f'{name}_cap_reorder_resp.mol2', outfile2=f'{name}_cap_reorder_resp_crd.mol2', auxfile=f'{name}_cap_reorder.mol2', resname='LIG')