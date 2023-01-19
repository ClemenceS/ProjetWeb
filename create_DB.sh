rm data/*.json
python3 create_json.py

cd Genomicus

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py loaddata ../data/Escherichia_coli_cft073_genome.json
python3 manage.py loaddata ../data/Escherichia_coli_cft073_seq.json
python3 manage.py loaddata ../data/Escherichia_coli_cft073_cds_dico.json
python3 manage.py loaddata ../data/Escherichia_coli_cft073_cds_seq.json
python3 manage.py loaddata ../data/Escherichia_coli_cft073_pep_dico.json
python3 manage.py loaddata ../data/Escherichia_coli_cft073_pep_seq.json


#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_genome.json
#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_seq.json
#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_cds_dico.json
#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_cds_seq.json
#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_pep_dico.json
#python3 manage.py loaddata ../data/Escherichia_coli_o157_h7_str_edl933_pep_seq.json
#
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_genome.json
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_seq.json
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_cds_dico.json
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_cds_seq.json
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_pep_dico.json
#python3 manage.py loaddata ../data/Escherichia_coli_str_k_12_substr_mg1655_pep_seq.json
#
#python3 manage.py loaddata ../data/new_coli_genome.json
#python3 manage.py loaddata ../data/new_coli_seq.json
#python3 manage.py loaddata ../data/new_coli_cds_dico.json
#python3 manage.py loaddata ../data/new_coli_cds_seq.json
#python3 manage.py loaddata ../data/new_coli_pep_dico.json
#python3 manage.py loaddata ../data/new_coli_pep_seq.json

cd ..

