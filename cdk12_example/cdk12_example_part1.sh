set -e

lig=ADS158081

rm output/*

cp input/${lig}.mol2 output/

cd output

# make capped ligand (ADS158081_cap.mol2) from docking output (ADS158081.mol2)
python ../../make_cap_ligand.py -i ${lig}.mol2 -o ${lig}_cap.mol2 -p "{'grep_pattern_list':['UNL', 'ASP A 314', 'CYS A 315', 'HIS A 316'], 'head_keep':[0,1,2,3,5,11], 'tail_keep':[0,1,2,4,5,15], 'head_rename':[0, 5], 'tail_rename':[2, 5]}"

# run charge calculation
echo "Must now create inputs and run RESP calculation"

cd ..