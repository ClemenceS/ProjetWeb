from django import forms
from django.core import validators

from django.core.validators import RegexValidator
regexNumberTel = RegexValidator(regex = r"0\d (\d{2} ){3}\d{2}")

class CreationMemberForm(forms.Form):
    """
    Classe pour la creation d'un membre
        - email : devant respecter son format
        - password : demander deux fois pour la verification
        - prenom et nom
        - numero de telephone (optionnel + dans un certain format donné par le placeholder XX XX XX XX XX)
        - information supplémentaires ajoutées par le nouveau membre (optionnel)
    """

    email = forms.CharField(max_length=255, label='email', widget=forms.TextInput(attrs={'placeholder':"xyz@exemple.com"}), validators=[validators.EmailValidator(message="Adresse email incorrecte")])

    #define that the field pasword must be hidden
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password1')
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password2')

    firstName = forms.CharField(max_length=100, label='firstName')
    lastName = forms.CharField(max_length=100, label='lastName')

    phone = forms.CharField(validators=[regexNumberTel], max_length=14, label='phone', required=False, widget=forms.TextInput(attrs={'placeholder':"XX XX XX XX XX"}))

    #a txt field to add complementary information : send to the admin
    infoPlus = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Par exemple : souhait d'un rôle supérieur (annotateur, validateur)", 'rows':3, 'cols':20, 'style':'resize:none;'}), required=False)


class ConnexionMemberForm(forms.Form):
    """
    Classe pour la connexion
        - email
        - password 
    """

    email = forms.CharField(max_length=255, label='email', widget=forms.TextInput(attrs={'placeholder':"xyz@exemple.com"}), validators=[validators.EmailValidator(message="Adresse email incorrecte")])
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password')

class UpdateMemberForm(forms.Form):
    """
    Classe pour la mise à jour des données
        - password (x2) pour vérification
        - prenom et nom 
        - numero de telephone (dans un certain format donné par le placeholder XX XX XX XX XX)
    """

    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password1', required=False)
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password2', required=False)

    firstName = forms.CharField(max_length=100, label='firstName', required=False)
    lastName = forms.CharField(max_length=100, label='lastName', required=False)

    phone = forms.CharField(validators=[regexNumberTel], max_length=14, label='phone', required=False, widget=forms.TextInput(attrs={'placeholder':"XX XX XX XX XX"}))
