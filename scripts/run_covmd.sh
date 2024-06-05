set -e

lig=$1

python ~/covmd/make_mc_file.py -i ${lig}_cap_reorder_babel.mol2 -fi mol2 -a ${lig}_cap_reorder_resp_crd.mol2 -o ${lig}_cap_reorder.mc

bash ~/covmd/tleap_covmd1.sh ${lig}_cap_reorder LIG

# for left redock
python ~/covmd/tleap_covmd1b.py -i ADS158081_cap_reorder_min1_al_strip.pdb -a ${lig}_cap_reorder_prepc.pdb -o ${lig}_cap_reorder_protein.pdb

# for right redock
#python ~/covmd/tleap_covmd1b.py -i ADS158156_complete_min2_strip_ab.pdb -a ${lig}_cap_reorder_prepc.pdb -o ${lig}_cap_reorder_protein.pdb -l LIG

bash ~/covmd/tleap_covmd2.sh ${lig}_cap_reorder ${lig}_cap_reorder_protein.pdb