from django.shortcuts import render, redirect
from .forms import SearchGenomeForm, SearchProteineGeneForm, SearchAnnotationForm
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import SequenceGenome, SequenceCodant, Genome, CodantInfo, Annotation
import requests
from fuzzywuzzy import fuzz
import re
from django.contrib import admin


from member.models import Member

#Define auxiliary functions
#Function to remove header from ID
def remove_header(id):
    return id[4:]

def similarite(seq, motif, ratio):
    ratio = fuzz.partial_ratio(seq, motif)
    if ratio > ratio:
        return True
    return False

def seq_type(sequence):
    amino_acid_regex = re.compile("^[ARNDCEQGHILKMFPSTWYV]+$")
    nucleotide_regex = re.compile("^[ACGT]+$")
    if nucleotide_regex.match(sequence):
        return "Nucleotide"
    elif amino_acid_regex.match(sequence):
        return "Amino Acid"
    else:
        return "Unknown"

def get_users():
    m = Member.objects.filter(connecte=True)
    if len(m) != 0:
        perso = m[0].firstName + ' ' + m[0].lastName
        people = {"profile":m[0].user_type, 'connecte':m[0].connecte, 'who':perso }
    else :
        people = {"profile":0, 'connecte':False}

    return people

# ------------------------------------------------------------------------------       

#Pages d'accueil
def accueil(request):
    people = get_users()
    template = loader.get_template('genomApp/accueil.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/accueil.html')


def accueil_validateur(request):
    people = get_users()
    template = loader.get_template('genomApp/validation.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/validation.html')


def accueil_annotateur(request):
    people = get_users()

    #List des annotations possible pour l'utilisateur
    #TODO -> définir fonction qui retourne la liste IDs dans il a droit d'annoter
    gene_a_annoter = ['ABG68043', 'AAG58066']


    info_gene = []
    num=1
    for g in gene_a_annoter:
        dico = {}
        p = CodantInfo.objects.get(id='cds_'+g)
        dico['id'] = g
        dico['start'] = p.start
        dico['stop'] = p.stop
        dico['chromosone'] = p.chromosome
        dico['espece'] = p.espece
        dico['num'] = num

        num+=1
        info_gene.append(dico)

    context = {'genes' : info_gene, 'people':people}
    template = loader.get_template('genomApp/annotation.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/annotation.html', context)


#Annotations

def seq_deja_affectees(request):
    people = get_users()
    template = loader.get_template('genomApp/affecte.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/affecte.html')

def soumission_annotation(request):
    people = get_users()
    template = loader.get_template('genomApp/a_annoter.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/a_annoter.html')

def affectation_annotation(request):
    people = get_users()
    template = loader.get_template('genomApp/a_affecter.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/a_affecter.html')

def annotation_possible(request):
    people = get_users()
    template = loader.get_template('genomApp/annotation.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/annotation.html')

def valider(request):
    people = get_users()
    template = loader.get_template('genomApp/valider.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/valider.html')


def resultatsFormulaireGenome(request):
    people = get_users()

    if request.method == 'POST':
        form = SearchGenomeForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['ID']
            motif = form.cleaned_data['motif']
            ratio = form.cleaned_data['ratio']
            espece = form.cleaned_data['espece']
            tailleMin = form.cleaned_data['tailleMin']
            tailleMax = form.cleaned_data['tailleMax']
            choixBDD = form.cleaned_data['nomBDD']
            gcMin = form.cleaned_data['gcMin']
            gcMax = form.cleaned_data['gcMax']

            if choixBDD == 'Genomicus':
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

                if gcMin != None:
                    criterias.append({'key': 'GC minimal (%)', 'value':gcMin})
                    q = q.filter(gc_rate__gte=gcMin)
                    id_list = q.values_list('id', flat=True)
                        
                if gcMax != None:
                    criterias.append({'key': 'GC maximal (%)', 'value':gcMax})
                    q = q.filter(gc_rate__lte=gcMax)
                    id_list = q.values_list('id', flat=True)

                if motif != "":
                    motif= motif.upper()
                    criterias.append({'key': 'Motif ', 'value':motif})
                    criterias.append({'key': 'Similarité (%)', 'value':ratio})
                    for id in q:
                        seq = SequenceGenome.objects.get(id=id).sequence
                        if similarite(seq, motif, ratio):
                            id_list.append(seq)

                context = {**form.cleaned_data, **{'id_results' : id_list}, **{'criterias':criterias}, **{'people':people}}
                #print(context)
                
                template = loader.get_template('genomApp/resultat_genome.html')
                return HttpResponse(template.render(context, request))

            else :
                query = id+" "+espece
                data = {'term' : query}
                response = requests.get("https://www.ncbi.nlm.nih.gov/genome", params=data)
                return HttpResponseRedirect(response.url)
    else:
        form = SearchGenomeForm()
    template = loader.get_template('genomApp/accueil_genome.html')
    return HttpResponse(template.render({'form':form, 'people':people}, request))
    #return render(request, 'genomApp/accueil_genome.html', {'form':form})

def resultatsFormulaireProteineGene(request):
    people = get_users()

    if request.method == 'POST':
        form = SearchProteineGeneForm(request.POST)
            
        if form.is_valid():
            id = form.cleaned_data['ID']
            id_chr = form.cleaned_data['ID_chr']
            gene = form.cleaned_data['gene']
            motif = form.cleaned_data['motif']
            ratio = form.cleaned_data['ratio']
            espece = form.cleaned_data['espece']
            tailleMin = form.cleaned_data['tailleMin']
            tailleMax = form.cleaned_data['tailleMax']
            choixBDD = form.cleaned_data['nomBDD']

            if choixBDD == 'Genomicus':
                criterias = []

                q = CodantInfo.objects.all()
                id_list = q.values_list('id', flat=True)

                if id != "" :
                    criterias.append({'key': 'ID', 'value': id})
                    q = q.filter(id='cds_'+id) | q.filter(id='pep_'+id)
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
                    criterias.append({'key': 'Similarité (%)', 'value':ratio})
                    if seq_type(motif) == 'Amino Acid':
                        for id in id_list:
                            if id.startswith("pep_"):
                                seq = SequenceCodant.objects.get(id=id).sequence
                                if similarite(seq, motif, ratio):
                                    id_list.append(seq)

                    elif seq_type(motif) == 'Nucleotide':
                        for id in id_list:
                            if id.startswith("cds_"):
                                seq = SequenceCodant.objects.get(id=id).sequence
                                if similarite(seq, motif, ratio):
                                    id_list.append(seq)

                shown_id = [remove_header(id) for id in id_list]
                shown_id = list(set(shown_id))

                context = {**form.cleaned_data, **{'id_results' : id_list}, **{'shown_id' : shown_id}, **{'criterias':criterias}, **{'people':people}}
                template = loader.get_template('genomApp/resultat_gene_transcrit.html')
                return HttpResponse(template.render(context, request))
            
            else :
                query = id+" "+id_chr+" "+espece
                data = {'term' : query}
                response = requests.get("https://www.ncbi.nlm.nih.gov/all/search", params=data)
                return HttpResponseRedirect(response.url)

    else:
        form = SearchProteineGeneForm()
    template = loader.get_template('genomApp/accueil_prot_gene.html')
    return HttpResponse(template.render({'form':form, 'people':people}, request))
    #return render(request, 'genomApp/accueil_prot_gene.html', {'form':form})

def informationsRelativesProteineGene(request, result_id):
    people = get_users()

    #p = CodantInfo.objects.get(id="cds_"+result_id)
    p = CodantInfo.objects.get(id="pep_"+result_id)

    #TODO -> define function that gets the info if the user is allowed to annote page
    show_annotation = True

    annotating = False

    id_chr = p.chromosome
    start = p.start
    stop = p.stop
    gene = p.gene
    description = p.description
    symbol = p.gene_symbol
    espece = p.espece
    sequence_aa = SequenceCodant.objects.all().filter(id="pep_"+result_id).values_list('sequence', flat=True)[0]
    sequence_nucl = SequenceCodant.objects.all().filter(id="cds_"+result_id).values_list('sequence', flat=True)[0]
    
    context = {'id_cds' : "cds_"+result_id, 'id_pep' : "pep_"+result_id, 'id_chr' : id_chr, 'start' : start, 
    'stop' : stop, 'gene' : gene, 'description' : description, 'seq_aa':sequence_aa, 'seq_nucl' : sequence_nucl, 
    'symbol':symbol, 'espece' : espece, 'shown_id' : result_id, 'show_annotation' : show_annotation,
    'annotating' :annotating, 'people': people}

    template = loader.get_template('genomApp/info.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/info.html', context)

def visualisationGenome(request, result_id):
    people = get_users()
    context = {'id_genome' : result_id, 'people':people}
    template = loader.get_template('genomApp/visualisation.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/visualisation.html', context)

def blastRedirection(request, result_id):
    type = CodantInfo.objects.filter(id=result_id).values_list('codant_type', flat=True)[0]
    print(type)
    if type == 1 :
        program = 'blastn'
    else :
        program = 'blastp'
    
    query = SequenceCodant.objects.filter(id=result_id).values_list('sequence', flat=True)
    data = {'PROGRAM' : program, 'PAGE_TYPE' : 'BlastSearch', 'LINK_LOC' : 'blasthome', 'QUERY': query}
    response = requests.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi", params=data)
    return HttpResponseRedirect(response.url)

#Autocomplétion
def speciesGenomeAutocomplete(request):
    query = request.GET.get("term", "")
    suggestions = Genome.objects.filter(espece__icontains=query)
    espece =  [obj.espece for obj in suggestions]
    suggestions_list = [{"label": s} for s in set(espece)]
    return JsonResponse(suggestions_list, safe=False)

def idGenomeAutocomplete(request):
    query = request.GET.get("term", "")
    suggestions = Genome.objects.filter(id__icontains=query)
    id =  [obj.id for obj in suggestions]
    suggestions_list = [{"label": i} for i in set(id)]
    return JsonResponse(suggestions_list, safe=False)

def speciesProteineAutocomplete(request):
    query = request.GET.get("term", "")
    suggestions = CodantInfo.objects.filter(espece__icontains=query)
    espece =  [obj.espece for obj in suggestions]
    suggestions_list = [{"label": s} for s in set(espece)]
    return JsonResponse(suggestions_list, safe=False)

def geneProteineAutocomplete(request):
    query = request.GET.get("term", "")
    suggestions = set(list(CodantInfo.objects.filter(gene__icontains=query)))
    gene =  [obj.gene for obj in suggestions]
    suggestions_list = [{"label": g} for g in set(gene)]
    print(suggestions_list)
    return JsonResponse(suggestions_list, safe=False)

def protein_annotation(request, result_id):
    people = get_users()

    if request.method == 'POST':
        form = SearchAnnotationForm(request.POST)

        if form.is_valid():
            espece = form.cleaned_data['espece']
            nom_gene = form.cleaned_data['nom_gene']
            symbol_gene = form.cleaned_data['symbol_gene']
            description = form.cleaned_data['description']
            print(result_id, espece, nom_gene, symbol_gene, description)
            print(CodantInfo.objects.filter(id='cds_'+result_id))
            annotation = Annotation(id= CodantInfo.objects.get(id="cds_"+result_id), annotateur = "George", gene = nom_gene, gene_symbol = symbol_gene, description = description)
            annotation.save()#Lorsqu'on fait ça -> ça écrase le dernier sauvegardd
            print(annotation.id)

        else:
            None
            

    else:
        p = CodantInfo.objects.get(id='cds_'+result_id)

        show_annotation = False
        annotating = True
        #TODO -> Define function to check if the user is allowed to annotate
        allowed_2_annotate = True

        id_chr = p.chromosome
        start = p.start
        stop = p.stop
        gene = p.gene
        description = p.description
        symbol = p.gene_symbol
        espece = p.espece
        sequence_aa = SequenceCodant.objects.all().filter(id="pep_"+result_id).values_list('sequence', flat=True)[0]
        sequence_nucl = SequenceCodant.objects.all().filter(id="cds_"+result_id).values_list('sequence', flat=True)[0]
        
        context = {'id_cds' : "cds_"+result_id, 'id_pep' : "pep_"+result_id, 'id_chr' : id_chr, 'start' : start, 
        'stop' : stop, 'gene' : gene, 'description' : description, 'seq_aa':sequence_aa, 'seq_nucl' : sequence_nucl, 
        'symbol':symbol, 'espece' : espece, 'shown_id' : result_id, 'show_annotation' : show_annotation,
        'annotating' :annotating, 'allowed_2_annotate':allowed_2_annotate, 'people':people}
        template = loader.get_template('genomApp/info.html')
        return HttpResponse(template.render(context, request))
        #return render(request, 'genomApp/info.html', context)

