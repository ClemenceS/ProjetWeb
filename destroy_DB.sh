cd Genomicus

python3 manage.py flush
python3 manage.py migrate appli zero

rm -rf db.sqlite3
rm -rf appli/migrations/0*.py

cd ..

rm data/*.json