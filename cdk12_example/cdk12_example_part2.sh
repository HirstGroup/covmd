set -e

lig=ADS158081

cp input/${lig}_cap_esp.log output/
cp input/ADS158156_complete_min2_strip_ab.pdb output/

cd output

# calculate RESP charges from ESP output 
antechamber -i ${lig}_cap_esp.log -fi gout -gv 1 -o ${lig}_cap_resp.mol2 -fo mol2 -c resp -rn LIG -dr no

# update coordinates of ligand to original ones
antechamber -i ${lig}_cap_resp.mol2 -fi mol2 -o ${lig}_cap_resp_crd.mol2 -fo mol2 -a ${lig}_cap.mol2 -fa mol2 -ao crd -dr no

# create MC file
python ../../make_mc_file.py -i ${lig}_cap.mol2 -fi mol2 -a ${lig}_cap_resp_crd.mol2 -o ${lig}_cap.mc

bash ../../tleap_covmd1.sh ${lig}_cap LIG

# for left redock
#python ~/covmd/tleap_covmd1b.py -i ADS158081_cap_min1_al_strip.pdb -a ${lig}_cap_prepc.pdb -o ${lig}_cap_protein.pdb

# for right redock
python ../../tleap_covmd1b.py -i ADS158156_complete_min2_strip_ab.pdb -a ${lig}_cap_prepc.pdb -o ${lig}_cap_protein.pdb -l LIG

bash ../../tleap_covmd2.sh ${lig}_cap ${lig}_cap_protein.pdb

cd ..
