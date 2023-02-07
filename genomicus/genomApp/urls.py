from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('recherche_genome/', views.resultatsFormulaireGenome, name="formulaire_genome"),
    path('contact/', views.contact, name="contact"),
    path('qui_sommes_nous/', views.qui_sommes_nous, name="qui_sommes_nous"),
    path('email_envoye/', views.email_envoi, name="email_envoi"),
    path('forum/', views.accueil_forum, name="accueil_forum_genome"),
    path('forum/<id>/', views.forum, name="forum"),
    path('delete_comment/<id_forum>_<id_com>', views.deleteComment, name="deleteComment"),
    path('update_comment/<id_forum>_<id_com>', views.updateComment, name="updateComment"),
    path('recherche_genome/visualisation/<result_id>/', views.visualisationGenome, name="visualisation"),
    path('recherche_proteine_gene/', views.resultatsFormulaireProteineGene, name="prot_gene"),
    path('recherche_proteine_gene/info_<result_id>/', views.informationsRelativesProteineGene, name="info_relatives"),
    path('annotation/', views.accueil_annotateur, name = 'accueil_annotateur'),
    path('validation/', views.accueil_validateur, name = 'accueil_validateur'),
    path('valider/', views.valider, name = 'valider'),
    path('deja_affectees/', views.seq_deja_affectees, name = 'seq_deja_affectees'),
    path('affectations_annotations', views.recherche_affectation_annotation, name = 'aff_ann'),
    path('affectations_annotations/<result_id>/', views.affectation_annotation, name = 'aff_ann_res'),
    path('blast_<result_id>/', views.blastRedirection, name='blastRedirection'),
    path('recherche_genome/species_genome_autocomplete/', views.speciesGenomeAutocomplete, name='speciesGenomeAutocomplete'),
    path('recherche_genome/id_genome_autocomplete/', views.idGenomeAutocomplete, name='idGenomeAutocomplete'),
    path('recherche_proteine_gene/id_chr_proteine_autocomplete/', views.idGenomeAutocomplete, name='idChrProteineAutocomplete'),
    path('recherche_proteine_gene/gene_proteine_autocomplete/', views.geneProteineAutocomplete, name='geneProteineAutocomplete'),
    path('recherche_proteine_gene/species_proteine_autocomplete/', views.speciesProteineAutocomplete, name='speciesProteineAutocomplete'),
    path('recherche_proteine_gene/id_proteine_autocomplete/', views.idProteineAutocomplete, name='idProteineAutocomplete'),
    path('/forum/id_proteine_forum_autocomplete/', views.idProteineAutocomplete, name='idProteineAutocompleteForum'),
    path('protein_annotation/<result_id>/', views.protein_annotation, name='protein_annotation'),
    path('view_annotation/<result_id>/', views.view_annotation, name='view_annotation'),
]


app_name = "genomApp"