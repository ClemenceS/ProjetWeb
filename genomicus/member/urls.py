from django.urls import path,include

from . import views

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('updateInformation/', views.updateInformation, name='updateInformation'),
]

app_name = "member"
