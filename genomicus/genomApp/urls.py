from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('recherche_genome/', views.resultatsFormulaireGenome, name="formulaire_genome"),
    path('visualisation_<result_id>/', views.visualisationGenome, name="visualisation"),
    path('recherche_proteine_gene/', views.resultatsFormulaireProteineGene, name="prot_gene"),
    path('recherche_proteine_gene/<result_id>/', views.informationsRelativesProteineGene, name="info_relatives"),
    path('annotation/', views.accueil_annotateur, name = 'accueil_annotateur'),
    path('validation/', views.accueil_validateur, name = 'accueil_validateur'),
    path('admin/', views.accueil_admin, name = 'accueil_admin'),
    path('connexion/', views.connexion, name = 'connexion'),
    path('inscription/', views.inscription, name = 'inscription'),
    path('valider/', views.valider, name = 'valider'),
    path('deja_affectees/', views.seq_deja_affectees, name = 'seq_deja_affectees'),
    path('affectations_annotations/', views.affectation_annotation, name = 'aff_ann'),
]


app_name = "genomApp"