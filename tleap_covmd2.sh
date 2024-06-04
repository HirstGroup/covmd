set -e

lig=$1
pdb=$2

# REQUIRED FILES: $lig.frcmod, $lig.prepc, protein pdb with inserted modified residue, 
# no hydrogens on protein, and no CONNECT 
ls $lig.frcmod $lig.prepc
ls $pdb

# copy cov.frcmod with Amber-GAFF parameters from script directory
dirname=$(dirname "$0")
cp $dirname/cov.frcmod .

cat > tleap.in <<EOF
source leaprc.protein.ff19SB
source leaprc.phosaa19SB
source leaprc.gaff
loadamberparams $lig.frcmod
loadamberparams cov.frcmod
loadamberprep $lig.prepc
loadamberparams frcmod.ionsjc_tip3p
source leaprc.water.tip3p
complex = loadPDB $pdb
set default PBRadii mbondi2
solvatebox complex TIP3PBOX 10.0
savepdb complex $lig-box.pdb
saveAmberParm complex $lig.parm7 $lig.rst7
quit
EOF

tleap -f tleap.in