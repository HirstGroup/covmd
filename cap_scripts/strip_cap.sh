# create cap mol2 from docking mol2, including ligand, covalent cys and neighboring residues

input=$1

output=${input%.*}_cap.mol2

cat > strip.ptraj <<EOF
trajin $input
strip !(:UNL,UNL1,ASP1038,CYS1039,HIS1040)
trajout $output
EOF

cpptraj $input strip.ptraj