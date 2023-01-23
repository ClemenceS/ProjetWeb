from django.shortcuts import render, redirect
from .forms import SearchGenomeForm, SearchProteineGeneForm
from django.template import loader
from django.http import HttpResponse
from .models import SequenceGenome, SequenceCodant,Genome, CodantInfo

#Connexion, inscription
def connexion(request):
    return render(request, 'genomApp/connexion.html')

def inscription(request):
    return render(request, 'genomApp/inscription.html')

#Pages d'accueil
def accueil(request):
    return render(request, 'genomApp/accueil.html')

def accueil_validateur(request):
    return render(request, 'genomApp/validation.html')

def accueil_annotateur(request):
    return render(request, 'genomApp/annotation.html')

def accueil_admin(request):
    return render(request, 'genomApp/admin.html')

#Annotations

def seq_deja_affectees(request):
    return render(request, 'genomApp/affecte.html')

def soumission_annotation(request):
    return render(request, 'genomApp/a_annoter.html')

def affectation_annotation(request):
    return render(request, 'genomApp/a_affecter.html')

def annotation_possible(request):
    return render(request, 'genomApp/annotation.html')

def valider(request):
    return render(request, 'genomApp/valider.html')

    #Formulaire
def resultatsFormulaireGenome(request):
    if request.method == 'POST':
        form = SearchGenomeForm(request.POST)
            
        if form.is_valid():
            id = form.cleaned_data['ID']
            motif = form.cleaned_data['motif']
            espece = form.cleaned_data['espece']
            tailleMin = form.cleaned_data['tailleMin']
            tailleMax = form.cleaned_data['tailleMax']

            criterias = []
            
            q = Genome.objects.all()
            id_list = q.values_list('id', flat=True)

            if id != "" :
                criterias.append({'key': 'ID', 'value':id})
                q = q.filter(id=id)
                id_list = q.values_list('id', flat=True)
                    
            if espece != "":
                criterias.append({'key': 'Espèce', 'value':espece})
                q = q.filter(espece=espece)
                id_list = q.values_list('id', flat=True)
                    
            if tailleMin != None:
                criterias.append({'key': 'Taille minimale', 'value':tailleMin})
                q = q.filter(taille__gte=tailleMin)
                id_list = q.values_list('id', flat=True)
                    
            if tailleMax != None:
                criterias.append({'key': 'Taille maximale', 'value':tailleMax})
                q = q.filter(taille__lte=tailleMax)
                id_list = q.values_list('id', flat=True)

            if motif != "":
                motif= motif.upper()
                criterias.append({'key': 'Motif ', 'value':motif})
                q2 = SequenceGenome.objects.filter(sequence__contains=motif)
                id_list2 = q2.values_list('id', flat=True)
                id_list = [value for value in id_list if value in id_list2]

            context = {**form.cleaned_data, **{'id_results' : id_list}, **{'criterias':criterias}}
            #print(context)
            
            template = loader.get_template('genomApp/resultat_genome.html')
            return HttpResponse(template.render(context, request))

    else:
        form = SearchGenomeForm()
    return render(request, 'genomApp/accueil_genome.html', {'form':form})

def resultatsFormulaireProteineGene(request):
    if request.method == 'POST':
        form = SearchProteineGeneForm(request.POST)
            
        if form.is_valid():
            id = form.cleaned_data['ID']
            id_chr = form.cleaned_data['ID_chr']
            gene = form.cleaned_data['gene']
            motif = form.cleaned_data['motif']
            espece = form.cleaned_data['espece']
            start = form.cleaned_data['start']
            stop = form.cleaned_data['stop']
            tailleMin = form.cleaned_data['tailleMin']
            tailleMax = form.cleaned_data['tailleMax']
            type = form.cleaned_data['type']
            
            criterias = []

            q = CodantInfo.objects.all()
            id_list = q.values_list('id', flat=True)


            if type != "" :
                if type == 'CDS' :
                    type = 1
                    criterias.append({'key': 'Type', 'value':'CDS'})
                else :
                    type = 2
                    criterias.append({'key': 'Type', 'value':'Peptide'})
                q = q.filter(codant_type=type)
                id_list = q.values_list('id', flat=True)


            if id != "" :
                criterias.append({'key': 'ID', 'value':id})
                q = q.filter(id=id)
                id_list = q.values_list('id', flat=True)
            
                
            if id_chr != "":
                criterias.append({'key': 'ID du chromosome', 'value':id_chr})
                q = q.filter(chromosome=id_chr)
                id_list = q.values_list('id', flat=True)

            if gene != "":
                criterias.append({'key': 'Gène', 'value':gene})
                q = q.filter(gene=gene)
                id_list = q.values_list('id', flat=True)
                    
            if espece != "":
                criterias.append({'key': 'Espèce', 'value':espece})
                q = q.filter(espece=espece)
                id_list = q.values_list('id', flat=True)

            if start != None:
                criterias.append({'key': 'Position du start', 'value':start})
                q = q.filter(start=start)
                id_list = q.values_list('id', flat=True)

            if stop != None:
                criterias.append({'key': 'Position du stop', 'value':stop})
                q = q.filter(stop=stop)
                id_list = q.values_list('id', flat=True)
                    
            if tailleMin != None:
                criterias.append({'key': 'Taille minimale', 'value':tailleMin})
                q = q.filter(taille__gte=tailleMin)
                id_list = q.values_list('id', flat=True)
                    
            if tailleMax != None:
                criterias.append({'key': 'Taille maximale', 'value':tailleMax})
                q = q.filter(taille__lte=tailleMax)
                id_list = q.values_list('id', flat=True)

            if motif != "":
                criterias.append({'key': 'Motif ', 'value':motif})
                q2 = SequenceCodant.objects.all().filter(sequence__contains=motif)
                id_list2 = q2.values_list('id', flat=True)
                id_list = [value for value in id_list if value in id_list2]

            #TODO -> this is not an optimal way of doing this
            #Since we wanna show for each id it's type -> we need to create a list of dicos
            #Storing the ids and the types (relation 1 à 1)
            results = []
            for i in range(len(id_list)):
                p = CodantInfo.objects.get(id=id_list[i])
                type = p.codant_type
                if type == 1 :
                    type = 'CDS'
                else :
                    type = 'Peptide'
                results.append({'id' : id_list[i], 'codant_type':type, 'taille':p.taille})
            

            context = {**form.cleaned_data, **{'id_results' : results}, **{'criterias':criterias}}
            template = loader.get_template('genomApp/resultat_gene_transcrit.html')
            return HttpResponse(template.render(context, request))

    else:
        form = SearchProteineGeneForm()
    return render(request, 'genomApp/accueil_prot_gene.html', {'form':form})

def informationsRelativesProteineGene(request, result_id):
    p = CodantInfo.objects.get(id=result_id)

    type = p.codant_type
    if type == 1 :
        type = 'CDS'
    else :
        type = 'Peptide'
    id_chr = p.chromosome
    start = p.start
    stop = p.stop
    gene = p.gene
    description = p.description
    symbol = p.gene_symbol
    sequence = SequenceCodant.objects.all().filter(id=result_id).values_list('sequence', flat=True)[0]
    context = {'id' : result_id, 'type' : type, 'id_chr' : id_chr, 'start' : start, 'stop' : stop, 'gene' : gene, 'description' : description, 'seq':sequence, 'symbol':symbol}
    return render(request, 'genomApp/info.html', context)

def visualisationGenome(request, result_id):
    context = {'id_genome' : result_id}
    return render(request, 'genomApp/visualisation.html', context)