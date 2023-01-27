from django import forms

class SearchGenomeForm(forms.Form):
    ID = forms.CharField(label='ID', max_length=100, required=False)
    motif = forms.CharField(label='motif', max_length=500, required=False)
    ratio = forms.IntegerField(label='ratio', required=False)
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
    motif = forms.CharField(label='motif', max_length=100, required=False)
    espece = forms.CharField(label='espece', max_length=100, required=False)
    tailleMin = forms.IntegerField(label='tailleMin', required=False)
    tailleMax = forms.IntegerField(label='tailleMax', required=False)
    nomBDD = forms.ChoiceField(label='nomBDD', widget=forms.RadioSelect, choices = (('Genomicus', 'Genomicus'), ('NCBI Proteine', 'NCBI Proteine')))
