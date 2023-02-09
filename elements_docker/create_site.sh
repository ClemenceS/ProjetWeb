#Clone Project
git clone https://github.com/ClemenceS/ProjetWeb.git

#Moving into the directory
cd ProjetWeb/

#Installing the requirements
pip install -r requirements.txt

#Creating and filling the database with the prototype data 
#If you don't want to fill the database with the prototy data
#You only need makemigrate and migrate
./create_DB.sh
#Run the application
cd genomicus/

python manage.py runserver 0.0.0.0:8000

#TO access the page, follow the following link
#http://localhost:8000/


