cd genomicus

python3 manage.py flush
python3 manage.py migrate genomApp zero

rm -rf db.sqlite3
rm -rf genomApp/migrations/0*.py

cd ..

rm data/*.json