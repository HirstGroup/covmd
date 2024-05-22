set -e

lig=$1
RESNAME=$2

# REQUIRED FILES: mc file needed, generate with make_mc_file.py
ls $lig.mc

# generate ac file from mol2 file containing original coordinates and resp charges with capped modified residue
# -an n option prevents atom names being changed
antechamber -fi mol2 -i ${lig}_resp_crd.mol2 -fo ac -o ${lig}.ac -at gaff2 -an n -j 2

# generate prepin file (with cartesian coordinates)
prepgen -i $lig.ac -o $lig.prepc -f car -m $lig.mc -rn $RESNAME -j 2

# generate frcmod file, -a Y option writes all parameters to file
parmchk2 -i $lig.prepc -f prepc -o $lig.frcmod -a Y -s gaff2

# convert prepin to pdb and include in original protein PDB, updating resid
antechamber -i $lig.prepc -fi prepc -o ${lig}_prepc.pdb -fo pdb -j 0 -an n -dr no


