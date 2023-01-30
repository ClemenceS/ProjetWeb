cd genomicus

python3 manage.py flush
python3 manage.py migrate genomApp zero
python3 manage.py migrate member zero

rm -rf db.sqlite3
rm -rf genomApp/migrations/0*.py
rm -rf member/migrations/0*.py

cd ..

rm data/*.json