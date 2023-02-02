from django.contrib.auth import login, authenticate, logout

from django.http import HttpResponse

from django.template import loader

from django.contrib.auth.models import User

from . import forms

from .models import Member


# Create your views here.


def inscription(request):
    """
    Fonction view pour l'inscription d'un nouvel utilisateur
        - verifie les champs renseignés et si besoin rajout d'un message d'erreur
        - renvoie différentes pages selon le cas (bien inscrit ou erreur lors de l'inscription)
    """

    form = forms.CreationMemberForm()
    template = loader.get_template('member/inscription.html')

    if request.method == 'POST':
        form = forms.CreationMemberForm(request.POST)

        if form.is_valid():
            email      = form.cleaned_data['email']
            password1  = form.cleaned_data['password1']
            password2  = form.cleaned_data['password2']
            firstName  = form.cleaned_data['firstName']
            lastName   = form.cleaned_data['lastName']
            phone      = form.cleaned_data['phone']

            if Member.objects.filter(email=email).exists():
                message = ("Cette adresse email ne peut pas être utilisée pour s'inscrire ! ")
                return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}, 'messageError':message}, request))
            if password2 != password1 :
                message = ("Compte non crée :  Les deux mots de passes renseignés ne sont pas identiques ! ")
                return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}, 'messageError':message}, request))


            elif password2 == password1:
                member = Member.objects.create_member(
                    email,
                    password1,
                    firstName,
                    lastName,
                    phone
                )

                message = 'Votre compte a bien été crée ! Connectez-vous pour profiter encore plus de votre visite sur notre site !!'
                templateA = loader.get_template('genomApp/accueil.html')
                return HttpResponse(templateA.render({'form':form, 'people':{"profile":0, 'connecte':False}, 'messageAccueil': message}, request))

        
    template = loader.get_template('member/inscription.html')
    return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}}, request))



def connexion(request):
    """
    Fonction view pour la connexion d'un utilisateur
        - verifie les champs renseignés et si besoin rajout d'un message d'erreur
        - renvoie différentes pages selon le cas (bien connecte ou erreur lors de la connexion)
    """    

    form = forms.ConnexionMemberForm()
    template = loader.get_template('member/connexion.html')

    if request.method == 'POST':
        form = forms.ConnexionMemberForm(request.POST)
    
        if form.is_valid():
            member = authenticate(
                email=form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )

            email=form.cleaned_data['email']
            password = form.cleaned_data['password']

            if member is not None:
                login(request,member)
                Member.objects.filter(email=email,password=password).update(connecte=True)
                templateA = loader.get_template('genomApp/accueil.html')

                m = Member.objects.filter(connecte=True)
                if len(m) != 0:
                    perso = m[0].firstName + ' ' + m[0].lastName

                    if m[0].user_type == 4 and len(User.objects.filter(email=email)) == 0: 
                        aa = User()
                        aa = User.objects.create_superuser(email, email, password)
                        aa.save()

                    people = {"profile":m[0].user_type, 'connecte':m[0].connecte, 'who':perso }
                else :
                    people = {"profile":0, 'connecte':False}
            
                return HttpResponse(templateA.render({'form':form, 'people':people}, request)) 

            else : 
                message = ("Vous n'avez pas pu être identifié. Vérifiez votre adresse mail et/ou votre mot de passe ! ")
                return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}, 'messageError':message}, request))
    
    people = {"profile":0, 'connecte':False}
    return HttpResponse(template.render({'form':form, 'people':people}, request))

def deconnexion(request):
    """
    Fonction view pour la deconnexion d'un utilisateur
        - renvoie la page d'accueil
    """ 

    Member.objects.filter(connecte=True).update(connecte=False)
    logout(request)
    template = loader.get_template('genomApp/accueil.html')
    people = {"profile":0, 'connecte':False}
    return HttpResponse(template.render({'form':{},'people':people}, request))


def updateInformation(request):
    """
    Fonction view pour l'affichage des informations d'un utilisateur et leur mise à jour
        - verifie les champs renseignés et si besoin rajout d'un message d'erreur
        - renvoie différentes pages selon le cas (retour à l'accueil ou la même page avec un message d'erreur
    """ 

    m = Member.objects.filter(connecte=True)

    init = {}
    init['firstName'] = m[0].firstName
    init['lastName'] = m[0].lastName
    init['phone'] = m[0].phone

    email = m[0].email

    form = forms.UpdateMemberForm(initial=init)
    
    template = loader.get_template('member/updateInformation.html')
    people = {"profile":m[0].user_type, 'connecte':m[0].connecte, 'who':  m[0].firstName + ' ' +m[0].lastName}

    if request.method == 'POST':
        form = forms.UpdateMemberForm(request.POST)

        if form.is_valid():

            password1  = form.cleaned_data['password1']
            password2  = form.cleaned_data['password2']
            firstName  = form.cleaned_data['firstName']
            lastName   = form.cleaned_data['lastName']
            phone      = form.cleaned_data['phone']

            #si aucune modif 
            if password1 == '' and password2 == '' and firstName == m[0].firstName and lastName == m[0].lastName and phone == m[0].phone : 
                return HttpResponse(template.render({'form':form, 'people':people, 'email':email}, request)) 
            elif (password1 != '' and password2 == '') or (password1 == '' and password2 != '') : 
                messageError = 'Mise à jour de vos données non sauvergardées : Veuillez remplir les deux champs de mot de passe ! '
                return HttpResponse(template.render({'form':form, 'people':people, 'email':email, 'messageError':messageError}, request)) 
            #sinon
            else:
                if password1 != '' and password2 != '':
                    if password1 == password2:
                        m.update(password=password1)
                    else : 
                        messageError = 'Mise à jour de vos données non sauvergardées : Les deux mots de passe donnés ne correspondent pas ! '
                        return HttpResponse(template.render({'form':form, 'people':people, 'email':email, 'messageError':messageError}, request))
                if firstName != '':
                    m.update(firstName=firstName)
                if lastName != '':
                    m.update(lastName=lastName)

                m.update(phone=phone)

                message = 'Votre compte a bien été mis à jour !'
                templateA = loader.get_template('genomApp/accueil.html')
                return HttpResponse(templateA.render({'form':form, 'people':people, 'messageAccueil': message}, request))

    return HttpResponse(template.render({'form':form, 'people':people, 'email':email}, request))