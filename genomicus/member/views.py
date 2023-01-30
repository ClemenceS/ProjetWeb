from django.shortcuts import render

from django.contrib.auth import login, authenticate, logout

from django.http import HttpResponse

from django.template import loader

from . import forms

from .models import Member


# Create your views here.

def inscription(request):
    form = forms.CreationMemberForm()
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
                pass
            elif password2 == password1:
                member = Member.objects.create_member(
                    email,
                    password1,
                    firstName,
                    lastName,
                    phone
                )
            
                template = loader.get_template('genomApp/accueil.html')
                return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}}, request))

    
    template = loader.get_template('member/inscription.html')
    return HttpResponse(template.render({'form':form, 'people':{"profile":0, 'connecte':False}}, request))
    #return render(request, 'member/inscription.html', context={'form':form}) 

def connexion(request):
    form = forms.ConnexionMemberForm()

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
                template = loader.get_template('genomApp/accueil.html')

                m = Member.objects.filter(connecte=True)
                if len(m) != 0:
                    perso = m[0].firstName + ' ' + m[0].lastName
                    people = {"profile":m[0].user_type, 'connecte':m[0].connecte, 'who':perso }
                else :
                    people = {"profile":0, 'connecte':False}
            
                return HttpResponse(template.render({'form':form, 'people':people}, request)) 
    
    people = {"profile":0, 'connecte':False}
    template = loader.get_template('member/connexion.html')
    return HttpResponse(template.render({'form':form, 'people':people}, request))
    #return render(request, 'member/connexion.html', context={'form':form})


def deconnexion(request):
    Member.objects.filter(connecte=True).update(connecte=False)
    logout(request)  # marche bien ou pas ?
    #template = loader.get_template('member/deconnexion.html')
    template = loader.get_template('genomApp/accueil.html')
    people = {"profile":0, 'connecte':False}
    return HttpResponse(template.render({'form':{},'people':people}, request))


def updateInformation(request):


    m = Member.objects.filter(connecte=True)

    init = {}
    init['firstName'] = m[0].firstName
    init['lastName'] = m[0].lastName
    init['phone'] = m[0].phone

    email = m[0].email

    form = forms.UpdateMemberForm(initial=init)
    

    template = loader.get_template('member/updateInformation.html')
    people = {"profile":m[0].user_type, 'connecte':m[0].connecte}

    if request.method == 'POST':
        form = forms.UpdateMemberForm(request.POST)

        if form.is_valid():

            password1  = form.cleaned_data['password1']
            password2  = form.cleaned_data['password2']
            firstName  = form.cleaned_data['firstName']
            lastName   = form.cleaned_data['lastName']
            phone      = form.cleaned_data['phone']

            if password1 != '' and password2 != '':
                if password1 == password2:
                    m.update(password=password1)
            if firstName != '':
                m.update(firstName=firstName)
            if lastName != '':
                m.update(lastName=lastName)
            if phone != '':
                m.update(phone=phone)

            return HttpResponse(template.render({'form':form, 'people':people, 'email' : email}, request))
        

        #renvoyer la page updateInfo avec un message disant quelles info ont ete maj

    return HttpResponse(template.render({'form':form, 'people':people, 'email':email}, request))

                
