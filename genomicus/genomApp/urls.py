from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('recherche_genome/', views.resultatsFormulaireGenome, name="formulaire_genome"),
    path('recherche_genome/visualisation_<result_id>/', views.visualisationGenome, name="visualisation"),
    path('recherche_proteine_gene/', views.resultatsFormulaireProteineGene, name="prot_gene"),
    path('recherche_proteine_gene/info_<result_id>/', views.informationsRelativesProteineGene, name="info_relatives"),
    path('annotation/', views.accueil_annotateur, name = 'accueil_annotateur'),
    path('validation/', views.accueil_validateur, name = 'accueil_validateur'),
    path('valider/', views.valider, name = 'valider'),
    path('deja_affectees/', views.seq_deja_affectees, name = 'seq_deja_affectees'),
    path('affectations_annotations/', views.affectation_annotation, name = 'aff_ann'),
    path('blast_<result_id>/', views.blastRedirection, name='blastRedirection'),
    path('recherche_genome/species_genome_autocomplete/', views.speciesGenomeAutocomplete, name='speciesGenomeAutocomplete'),
    path('recherche_genome/id_genome_autocomplete/', views.idGenomeAutocomplete, name='idGenomeAutocomplete'),
    path('recherche_proteine_gene/id_chr_proteine_autocomplete/', views.idGenomeAutocomplete, name='idChrProteineAutocomplete'),
    path('recherche_proteine_gene/gene_proteine_autocomplete/', views.geneProteineAutocomplete, name='geneProteineAutocomplete'),
    path('recherche_proteine_gene/species_proteine_autocomplete/', views.speciesProteineAutocomplete, name='speciesProteineAutocomplete'),
    path('protein_annotation/<result_id>/', views.protein_annotation, name='protein_annotation'),
    path('view_annotation/<result_id>/', views.view_annotation, name='view_annotation'),
]


app_name = "genomApp"