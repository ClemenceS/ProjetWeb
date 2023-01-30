from django import forms

from django.core.validators import RegexValidator
regexNumberTel = RegexValidator(regex = r"0\d (\d{2} ){3}\d{2}")

class CreationMemberForm(forms.Form):
    email = forms.CharField(max_length=255, label='email', widget=forms.TextInput(attrs={'placeholder':"xyz@exemple.com"}))

    #define that the field pasword must be hidden
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password1')
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password2')

    firstName = forms.CharField(max_length=100, label='firstName')
    lastName = forms.CharField(max_length=100, label='lastName')

    phone = forms.CharField(validators=[regexNumberTel], max_length=14, label='phone', required=False, widget=forms.TextInput(attrs={'placeholder':"XX XX XX XX XX"}))


class ConnexionMemberForm(forms.Form):
    email = forms.CharField(max_length=255, label='email', widget=forms.TextInput(attrs={'placeholder':"xyz@exemple.com"}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password')

class UpdateMemberForm(forms.Form):
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password1', required=False)
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder':'********'}), label='password2', required=False)

    firstName = forms.CharField(max_length=100, label='firstName', required=False)
    lastName = forms.CharField(max_length=100, label='lastName', required=False)

    phone = forms.CharField(validators=[regexNumberTel], max_length=14, label='phone', required=False, widget=forms.TextInput(attrs={'placeholder':"XX XX XX XX XX"}))