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

#initiale the bdd with a superuser - you can change the information
DJANGO_SUPERUSER_PASSWORD='admin' \
DJANGO_SUPERUSER_USERNAME='admin' \
DJANGO_SUPERUSER_EMAIL='clemence.22.sebe@gmail.com' \
python3 manage.py createsuperuser --no-input

# add members in the bdd

echo "from member.models import Member; Member.objects.create_member(email='clemence.sebe@universite-paris-saclay.fr', password='clemence', lastName='Sebe', firstName='Clémence')" | python3 manage.py shell

echo "from member.models import Member; Member.objects.create_member(email='ambre.baumann@universite-paris-saclay.fr', password='ambre', lastName='Baumann', firstName='Ambre')" | python3 manage.py shell
echo "from member.models import Member; m = Member.objects.filter(email='ambre.baumann@universite-paris-saclay.fr'); m.update(user_type=2) " | python3 manage.py shell

echo "from member.models import Member; Member.objects.create_member(email='lindsay.goulet@universite-paris-saclay.fr', password='lindsay', lastName='Goulet', firstName='Lindsay')" | python3 manage.py shell
echo "from member.models import Member; m = Member.objects.filter(email='lindsay.goulet@universite-paris-saclay.fr'); m.update(user_type=3) " | python3 manage.py shell

echo "from member.models import Member; Member.objects.create_member(email='george.marchment@universite-paris-saclay.fr', password='george', lastName='Marchment', firstName='George')" | python3 manage.py shell
echo "from member.models import Member; m = Member.objects.filter(email='george.marchment@universite-paris-saclay.fr'); m.update(user_type=4) " | python3 manage.py shell

echo "Members created sucessfully."

# add an annotation
#Donc Ambre elle a 3 annotations à faire (une qui à déjà été) -> 2 à validé pour George (compris celui qui a déjà était annoté) et l'autre pour Lindsay
echo 'from genomApp.models import Annotation, CodantInfo; from member.models import Member; Annotation(id= CodantInfo.objects.get(id="cds_AAN80781"), gene = "", gene_symbol = "", description = "", annotateur = Member.objects.get(email="ambre.baumann@universite-paris-saclay.fr"), validateur = Member.objects.get(email="lindsay.goulet@universite-paris-saclay.fr"), already_annotated =False).save() ' | python3 manage.py shell
echo 'from genomApp.models import Annotation, CodantInfo; from member.models import Member; Annotation(id= CodantInfo.objects.get(id="cds_ABG68043"), gene = "", gene_symbol = "", description = "", annotateur = Member.objects.get(email="ambre.baumann@universite-paris-saclay.fr"), validateur = Member.objects.get(email="george.marchment@universite-paris-saclay.fr"), already_annotated =False ).save() ' | python3 manage.py shell
echo 'from genomApp.models import Annotation, CodantInfo; from member.models import Member; Annotation(id= CodantInfo.objects.get(id="cds_ABG68044"), gene = "Gene test", gene_symbol = "Test symbol", description = "Description", annotateur = Member.objects.get(email="ambre.baumann@universite-paris-saclay.fr"), validateur = Member.objects.get(email="george.marchment@universite-paris-saclay.fr"), already_annotated =True ).save() ' | python3 manage.py shell
echo "Annotations created sucessfully."

cd ..