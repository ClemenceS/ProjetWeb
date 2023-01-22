rm data/*.json

entries=(Escherichia_coli_cft073 Escherichia_coli_o157_h7_str_edl933 Escherichia_coli_str_k_12_substr_mg1655 new_coli)


for e in ${entries[*]};do
    python3 src/create_json.py ${e}
done

cd genomicus

python3 manage.py makemigrations
python3 manage.py migrate

for e in ${entries[*]};do
    python3 manage.py loaddata ../data/${e}_genome.json
    python3 manage.py loaddata ../data/${e}_seq.json
    python3 manage.py loaddata ../data/${e}_cds_dico.json
    python3 manage.py loaddata ../data/${e}_cds_seq.json
    python3 manage.py loaddata ../data/${e}_pep_dico.json
    python3 manage.py loaddata ../data/${e}_pep_seq.json
done

cd ..

