from django.shortcuts import render, redirect
from .forms import SearchGenomeForm, SearchProteineGeneForm, SearchAnnotationForm
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import SequenceGenome, SequenceCodant, Genome, CodantInfo, Annotation
import requests
from fuzzywuzzy import fuzz
import re
from django.contrib import admin
from .functionsVisualisationGenome import *
from django import forms



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
        people = {"profile":m[0].user_type, 'connecte':m[0].connecte, 'who':perso, 'email': m[0].email }
    else :
        people = {"profile":0, 'connecte':False}

    return people

#Fonction qui retourne la liste IDs dans il a droit d'annoter
def get_annotations(user):
    tab = list(Annotation.objects.filter(annotateur = Member.objects.get(email = user['email'])))
    res=[]
    annotated=[]
    for a in tab:
        res.append(str(a)[4:])#To remove the 'cds_' at the beginning
        annotated.append(a.already_annotated)
    return res, annotated

#Function that return true is the user is allowed to annotate the protein -> False if not
def allowed_to_annotate(user, id_prot):
    tab = list(Annotation.objects.filter(annotateur = Member.objects.get(email = user['email'])))
    res=[]
    for a in tab:
        if (str(a)[4:] == id_prot):
            return True
    return False

#Fonction qui retourne la liste des annotations dont l'utilisateur est validateur
def get_annotations_validateur(user):
    tab = list(Annotation.objects.filter(validateur = Member.objects.get(email = user['email'])))
    res=[]
    annotated=[]
    for a in tab:
        res.append(a)
    return res

#Function that return the first and last name of a user
def get_names(user):
    return f'{user.firstName} {user.lastName}'

#Function that return the first and last name of a user from the email
def get_names_from_email(email):
    return get_names(Member.objects.get(email=email))

#Function that returns the species of a protein from it's short id
def get_espece(id):
    return CodantInfo.objects.get(id='cds_'+id).espece

#Function that validates the annotations by updating the CodantInfo table and deleting the corresponding annotations
def validate_annotations(to_validate):
    for v in to_validate:
        cds = CodantInfo.objects.get(id='cds_'+v)
        pep = CodantInfo.objects.get(id='pep_'+v)
        annotation = Annotation.objects.get(id='cds_'+v)
        
        cds.gene = annotation.gene
        pep.gene = annotation.gene

        cds.gene_symbol = annotation.gene_symbol
        pep.gene_symbol = annotation.gene_symbol

        cds.description = annotation.description
        pep.description = annotation.description

        cds.save()
        pep.save()

        annotation.delete()

#Function that return the annotateurs (and their possible annotations) from the validateur
def annotateurs_from_validateur(validateur):
    tab = list(Annotation.objects.filter(validateur = Member.objects.get(email = validateur['email'])))
    dico ={}
    num ={}
    list_num ={}
    for t in tab:
        name = get_names_from_email(t.annotateur)
        try:
            dico[name].append(str(t.id)[4:])
            list_num[name].append(num[name])
            num[name]+=1
        except:
            dico[name] = []
            list_num[name] = []
            num[name] = 1
            dico[name].append(str(t.id)[4:])
            list_num[name].append(num[name])
            num[name]+=1
    
    tab=[]
    for d in dico:
        temp=[]
        for i in range(len(dico[d])):
            temp.append({'id':dico[d][i], 'num':list_num[d][i]})
        tab.append({'key':d, 'val':temp})

        
    return tab


#Function that returns the ids of the proteins which aren't being annotated
def protein_not_being_annotated(validateur):
    temp = list(CodantInfo.objects.exclude(id__in=Annotation.objects.values('id')).filter(codant_type = 1).values('id'))
    tab = []
    for t in temp:
        tab.append(t['id'][4:])
    return tab



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


#Function that shows the annotations possible for the user
def accueil_annotateur(request):
    people = get_users()

    #List des annotations possible pour l'utilisateur
    gene_a_annoter, already_annotated= get_annotations(people)

    info_gene = []
    num=1
    for i in range(len(gene_a_annoter)):
        g  = gene_a_annoter[i]
        annotated = already_annotated[i]
        dico = {}
        p = CodantInfo.objects.get(id='cds_'+g)
        dico['id'] = g
        dico['start'] = p.start
        dico['stop'] = p.stop
        dico['chromosone'] = p.chromosome
        dico['espece'] = p.espece
        dico['num'] = num
        dico['annotated'] = annotated

        num+=1
        info_gene.append(dico)

    context = {'genes' : info_gene, 'people':people}
    template = loader.get_template('genomApp/annotation.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/annotation.html', context)


#Function that shows the annotateurs that the validateur has affected pages to
def seq_deja_affectees(request):
    people = get_users()
    annotateurs = annotateurs_from_validateur(people)
    print(annotateurs)
    template = loader.get_template('genomApp/affecte.html')
    return HttpResponse(template.render({'people':people, 'annotateurs':annotateurs}, request))
    #return render(request, 'genomApp/affecte.html')

def soumission_annotation(request):
    people = get_users()
    template = loader.get_template('genomApp/a_annoter.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/a_annoter.html')

def affectation_annotation(request):
    people = get_users()
    print('HEERRREEE')
    if request.method == 'POST':
        print(request.POST.getlist('services'))
    else: 
        people = get_users()

        #Pour l'instant seumelement les 50 premier
        ids= protein_not_being_annotated(people)[:50]
        person = ['George', 'Clemence', 'Lindsay']



        services = [{'id':'George', 'name':'--George--'}, {'id':'Clemence', 'name':'--Clemence--'}, {'id':'Lindsay', 'name':'--Lindsay--'}]

        template = loader.get_template('genomApp/a_affecter.html')
        return HttpResponse(template.render({'people':people, 'services':services, 'ids':ids}, request))
    #return render(request, 'genomApp/a_affecter.html')

def annotation_possible(request):
    people = get_users()
    template = loader.get_template('genomApp/annotation.html')
    return HttpResponse(template.render({'people':people}, request))
    #return render(request, 'genomApp/annotation.html')

#Function that allows the validateur to validate annotations
def valider(request):
    people = get_users()

    if request.method == 'POST':
        to_validate = request.POST.getlist('to_validate')
        #print(request.POST.getlist('to_validate'))
        validate_annotations(to_validate)
        print(request.POST.getlist('to_validate'))

    annotations= get_annotations_validateur(people)

    a_valider, en_attente = [], []
    a_valider_num, en_attente_num = 1, 1
    for i in range(len(annotations)):
        id=str(annotations[i])[4:]
        v=annotations[i].already_annotated
        name = get_names(annotations[i].annotateur)
        espece = get_espece(id)
        if(not v):
            en_attente.append({'id':id, 'num':en_attente_num, 'name':name, 'espece':espece})
            en_attente_num+=1
        else:
            a_valider.append({'id':id, 'num':a_valider_num, 'name':name, 'espece':espece})
            a_valider_num+=1
    
    context = {**{'people':people}, **{'en_attente':en_attente}, **{'a_valider':a_valider}}
    template = loader.get_template('genomApp/valider.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/valider.html')

#Function that shows the formulaire Genome
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

                results = []
                for i in range(len(id_list)):
                    p = Genome.objects.get(id=id_list[i])
                    results.append({'id' : id_list[i], 'taille':p.taille, 'espece':p.espece, 'gc_rate':p.gc_rate})


                context = {**form.cleaned_data, **{'id_results' : results }, **{'criterias':criterias}, **{'people':people}}
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

#Function that shows the formulaire Proteine
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

#Function that shows corresponding info for a protein
def informationsRelativesProteineGene(request, result_id):
    people = get_users()

    #p = CodantInfo.objects.get(id="cds_"+result_id)
    p = CodantInfo.objects.get(id="pep_"+result_id)

    #Since the user is vewing they are not annotating
    annotating = False
    #Function to check if the user is allowed to annotate
    #If the user is not connected, they are not allowed to annotate anyway -> so we catch the error
    try:
        allowed_2_annotate = allowed_to_annotate(people, result_id)
    except:
        allowed_2_annotate = False
    #allowed_2_annotate = True

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
    'symbol':symbol, 'espece' : espece, 'shown_id' : result_id, 'annotating' :annotating, 'people': people,
    'allowed_2_annotate':allowed_2_annotate, 'view_annotation':False}

    template = loader.get_template('genomApp/info.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'genomApp/info.html', context)

def visualisationGenome(request, result_id):
    people = get_users()

    p = Genome.objects.get(id=result_id)
    espece = p.espece
    #Call functions to create files for the genome visualisation
    create_new_fa(result_id)
    create_gff(result_id)
    creat_fai(result_id)

    context = {'id_genome' : result_id, 'people':people, 'espece' : espece}
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

#Function that allows to modifie an annotation
def protein_annotation(request, result_id):
    people = get_users()

    if request.method == 'POST':
        form = SearchAnnotationForm(request.POST)

        if form.is_valid():
            #This bit of code updates the annotation
            nom_gene = form.cleaned_data['nom_gene']
            symbol_gene = form.cleaned_data['symbol_gene']
            description = form.cleaned_data['description']
            #print(result_id, nom_gene, symbol_gene, description)
            #print(CodantInfo.objects.filter(id='cds_'+result_id))
            annotation = Annotation(id= CodantInfo.objects.get(id="cds_"+result_id),gene = nom_gene, gene_symbol = symbol_gene, description = description, annotateur = Member.objects.get(email=people['email']), already_annotated =True, validateur = Annotation.objects.get(id="cds_"+result_id).validateur)
            annotation.save()#Lorsqu'on fait ça -> ça écrase le dernier sauvegardd
            #print(annotation.id, annotation.gene,  annotation.gene_symbol, annotation.description)
            return accueil_annotateur(request)

        else:
            None
            
    #Load the annotations available for the user
    else:
        p = CodantInfo.objects.get(id='cds_'+result_id)
        annotating = True #Mode annotating 
        #Function to check if the user is allowed to annotate
        #If the user is not connected, they are not allowed to annotate anyway -> so we catch the error
        try:
            allowed_2_annotate = allowed_to_annotate(people, result_id)
        except:
            allowed_2_annotate = False
        #allowed_2_annotate = True
        

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
        'symbol':symbol, 'espece' : espece, 'shown_id' : result_id, 'annotating' :annotating, 
        'allowed_2_annotate':allowed_2_annotate, 'people':people, 'view_annotation':False}
        template = loader.get_template('genomApp/info.html')
        return HttpResponse(template.render(context, request))
        #return render(request, 'genomApp/info.html', context)

#Function that allows to visualize an annotation
def view_annotation(request, result_id):
    people = get_users()
    #Function to check if the user is allowed to annotate
    #If the user is not connected, they are not allowed to annotate anyway -> so we catch the error
    try:
        allowed_2_annotate = allowed_to_annotate(people, result_id)
    except:
        allowed_2_annotate = False

    p = CodantInfo.objects.get(id='cds_'+result_id)

    id_chr = p.chromosome
    start = p.start
    stop = p.stop
    gene = p.gene
    description = p.description
    symbol = p.gene_symbol
    espece = p.espece
    sequence_aa = SequenceCodant.objects.all().filter(id="pep_"+result_id).values_list('sequence', flat=True)[0]
    sequence_nucl = SequenceCodant.objects.all().filter(id="cds_"+result_id).values_list('sequence', flat=True)[0]

    a = Annotation.objects.get(id='cds_'+result_id)
    annote_gene = a.gene
    annote_gene_symbol = a.gene_symbol 
    annote_description = a.description



    context = {'id_cds' : "cds_"+result_id, 'id_pep' : "pep_"+result_id, 'id_chr' : id_chr, 'start' : start, 
        'stop' : stop, 'gene' : gene, 'description' : description, 'seq_aa':sequence_aa, 'seq_nucl' : sequence_nucl, 
        'symbol':symbol, 'espece' : espece, 'shown_id' : result_id, 'annotating' :False, 
        'allowed_2_annotate':allowed_2_annotate, 'people':people, 'view_annotation':True,
        'annote_gene':annote_gene, 'annote_gene_symbol':annote_gene_symbol, 'annote_description':annote_description}

    
    template = loader.get_template('genomApp/info.html')
    
    return HttpResponse(template.render(context, request))

