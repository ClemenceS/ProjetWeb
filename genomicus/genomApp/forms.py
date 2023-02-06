from django import forms

class SearchGenomeForm(forms.Form):
    ID = forms.CharField(label='ID', max_length=100, required=False)
    motif = forms.CharField(label='motif', max_length=500, required=False)
    espece = forms.CharField(label='espece', max_length=100, required=False)
    tailleMin = forms.IntegerField(label='tailleMin', required=False)
    tailleMax = forms.IntegerField(label='tailleMax', required=False)
    gcMin = forms.IntegerField(label='gcMin', required=False)
    gcMax = forms.IntegerField(label='gcMax', required=False)
    nomBDD = forms.ChoiceField(label='nomBDD', widget=forms.RadioSelect, choices = (('Genomicus', 'Genomicus'), ('NCBI Genome', 'NCBI Genome')))
    

class SearchProteineGeneForm(forms.Form):
    ID = forms.CharField(label='ID', max_length=100, required=False)
    ID_chr = forms.CharField(label='ID_chr', max_length=100, required=False)
    gene = forms.CharField(label='gene', max_length=100, required=False)
    motif = forms.CharField(label='motif', max_length=500, required=False)
    espece = forms.CharField(label='espece', max_length=100, required=False)
    tailleMin = forms.IntegerField(label='tailleMin', required=False)
    tailleMax = forms.IntegerField(label='tailleMax', required=False)
    nomBDD = forms.ChoiceField(label='nomBDD', widget=forms.RadioSelect, choices = (('Genomicus', 'Genomicus'), ('NCBI Proteine', 'NCBI Proteine')))

class SearchAnnotationForm(forms.Form):
    espece = forms.CharField(label='espece', max_length=100, required=False)
    nom_gene = forms.CharField(label='nom_gene', max_length=100, required=False)
    symbol_gene = forms.CharField(label='symbol_gene', max_length=100, required=False)
    description = forms.CharField(label='description', max_length=100, required=False)

class SearchAnnotation(forms.Form):
    ID = forms.CharField(label='ID', max_length=100, required=False)

class AddCommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=1000, required=False)
    auteur = forms.CharField(label='auteur', max_length=100, required=False)
    date = forms.DateField(label='date', required=False)
    forum = forms.CharField(label='id_forum', max_length=100, required=False)

class SearchForumForm(forms.Form):
    id_prot = forms.CharField(label='id_prot', max_length=100, required=False)
    id_chr = forms.CharField(label='id_chr', max_length=100, required=False)

class UpdateCommentForm(forms.Form):
    updated_text = forms.CharField(label='updated_text', max_length=1000, required=False)
    updated_date = forms.DateField(label='updated_date', required=False)
    auteur = forms.CharField(label='auteur_up', max_length=100, required=False)
    forum = forms.CharField(label='id_forum_up', max_length=100, required=False)

class ContactUsForm(forms.Form):
    auteur_nom = forms.CharField(label='auteur_nom', max_length=100, required=True)
    auteur = forms.CharField(label='auteur', max_length=100, required=True)
    sujet = forms.CharField(label='sujet', max_length=100, required=True)
    message = forms.CharField(label='message', max_length=1000, required=True)

