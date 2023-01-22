from django import forms

class SearchGenomeForm(forms.Form):
    ID = forms.CharField(label='ID', max_length=100, required=False)
    motif = forms.CharField(label='motif', max_length=100, required=False)
    espece = forms.CharField(label='espece', max_length=100, required=False)
    tailleMin = forms.IntegerField(label='tailleMin', required=False)
    tailleMax = forms.IntegerField(label='tailleMax', required=False)
    nomBDD = forms.ChoiceField(label='nomBDD', widget=forms.RadioSelect, choices = (('Genomicus', 'Genomicus'), ('BDD1', 'BDD1')))

class SearchProteineGeneForm(forms.Form):
    type = forms.ChoiceField(label='type', widget=forms.RadioSelect, choices = (('Peptide', 'Peptide'),('CDS', 'CDS')), required=False)
    ID = forms.CharField(label='ID', max_length=100, required=False)
    ID_chr = forms.CharField(label='ID_chr', max_length=100, required=False)
    gene = forms.CharField(label='gene', max_length=100, required=False)
    motif = forms.CharField(label='motif', max_length=100, required=False)
    start = forms.IntegerField(label='start', required=False)
    stop = forms.IntegerField(label='stop', required=False)
    espece = forms.CharField(label='espece', max_length=100, required=False)
    tailleMin = forms.IntegerField(label='tailleMin', required=False)
    tailleMax = forms.IntegerField(label='tailleMax', required=False)
    nomBDD = forms.ChoiceField(label='nomBDD', widget=forms.RadioSelect, choices = (('Genomicus', 'Genomicus'), ('BDD1', 'BDD1')))
