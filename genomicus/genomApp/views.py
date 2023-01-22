from django.shortcuts import render, redirect
from .forms import SearchGenomeForm, SearchProteineGeneForm
from django.template import loader
from django.http import HttpResponse
from .models import SequenceGenome, Genome, CodantInfo

#Connexion, inscription
def connexion(request):
    return render(request, 'genomApp/connexion.html')

def inscription(request):
    return render(request, 'genomApp/inscription.html')

#Pages d'accueil
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
            
            q = Genome.objects.all()
            id_list = q.values_list('id', flat=True)

            if id != "" :
                q = q.filter(id=id)
                id_list = q.values_list('id', flat=True)
                    
            elif espece != "":
                q = q.filter(espece=espece)
                id_list = q.values_list('id', flat=True)
                    
            elif tailleMin != None:
                q = q.filter(taille__gt=tailleMin)
                id_list = q.values_list('id', flat=True)
                    
            elif tailleMax != None:
                q = q.filter(taille__lt=tailleMax)
                id_list = q.values_list('id', flat=True)

            elif motif != "":
                q2 = SequenceGenome.objects.filter(sequence__contains=motif)
                id_list2 = q2.values_list('id', flat=True)
                id_list = [value for value in id_list if value in id_list2]

            context = {**form.cleaned_data, **{'id_results' : id_list}}
            #print(context)
            
            template = loader.get_template('genomApp/resultat_genome.html')
            return HttpResponse(template.render(context, request))

    else:
        form = SearchGenomeForm()
    return render(request, 'genomApp/accueil.html', {'form':form})

def resultatsFormulaireProteineGene(request):
    if request.method == 'POST':
        form = SearchProteineGeneForm(request.POST)
            
        if form.is_valid():
            id = form.cleaned_data['ID']
            id_chr = form.cleaned_data['ID_chr']
            gene = form.cleaned_data['gene']
            motif = form.cleaned_data['motif']
            espece = form.cleaned_data['espece']
            start = form.cleaned_data['stop']
            stop = form.cleaned_data['start']
            tailleMin = form.cleaned_data['tailleMin']
            tailleMax = form.cleaned_data['tailleMax']
            type = form.cleaned_data['type']
            
            q = CodantInfo.objects.all()
            id_list = q.values_list('id', flat=True)

            if id != "" :
                q = q.filter(id=id)
                id_list = q.values_list('id', flat=True)

            if type != "" :
                if type == 'CDS' :
                    type = 1
                else :
                    type = 2
                q = q.filter(codant_type=type)
                id_list = q.values_list('id', flat=True)
                
            elif id_chr != "":
                q = q.filter(chromosome=id_chr)
                id_list = q.values_list('id', flat=True)

            elif gene != "":
                q = q.filter(gene=gene)
                id_list = q.values_list('id', flat=True)
                    
            elif espece != "":
                q = q.filter(espece=espece)
                id_list = q.values_list('id', flat=True)

            elif start != None:
                q = q.filter(start=start)
                id_list = q.values_list('id', flat=True)

            elif stop != None:
                q = q.filter(start=stop)
                id_list = q.values_list('id', flat=True)
                    
            elif tailleMin != None:
                q = q.filter(taille__gt=tailleMin)
                id_list = q.values_list('id', flat=True)
                    
            elif tailleMax != None:
                q = q.filter(taille__lt=tailleMax)
                id_list = q.values_list('id', flat=True)

            elif motif != "":
                q2 = SequenceGenome.objects.filter(sequence__contains=motif)
                id_list2 = q2.values_list('id', flat=True)
                id_list = [value for value in id_list if value in id_list2]

            context = {**form.cleaned_data, **{'id_results' : id_list}}
            #print(context)
            
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
    context = {'id' : result_id, 'type' : type, 'id_chr' : id_chr, 'start' : start, 'stop' : stop, 'gene' : gene, 'description' : description}
    return render(request, 'genomApp/info.html', context)

def visualisationGenome(request, result_id):
    context = {'id_genome' : result_id}
    return render(request, 'genomApp/visualisation.html', context)