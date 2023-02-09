from django.db import models
from member.models import Member

class SeqInfo(models.Model):
    """
    Classe pour les informations relatives à une séquence
        - identifiant 
        - taille
        - phase de lecture 
        - espèce 
        - taux de GC
    """
    id = models.CharField(primary_key=True, max_length=200)
    taille = models.IntegerField(blank=False)
    phaseLecture = models.IntegerField(blank=True, null=True)
    espece = models.CharField(max_length=200, blank=False)
    gc_rate = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'


class Genome(SeqInfo):
    """
    Classe qui hérite de la classe SeqInfo donc pour les informations relatives à une séquence
        - identifiant 
        - taille
        - phase de lecture 
        - espèce 
        - taux de GC
    """
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'


class CodantInfo(SeqInfo):
    """
    Classe qui hérite de la classe SeqInfo donc pour les informations relatives à une séquence
        - identifiant 
        - taille
        - phase de lecture 
        - espèce 
        - taux de GC

    Et pour les informations relatives aux séquences codantes (protéines & CDS)
        - identifiant du chromosome
        - type de séquences (CDS ou Peptide)
        - identifiant du gène
        - start
        - stop
        - transcript
        - ...
    """
    #Blank -> If True, the field is allowed to be blank. Default is False.
    chromosome = models.ForeignKey('Genome', on_delete=models.RESTRICT)
    TYPE_CHOICES = (
      (1, 'CDS'),
      (2, 'Peptide'),
    )
    codant_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, blank=False)
    gene = models.CharField(max_length=200, blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    stop = models.IntegerField(blank=True, null=True)
    transcript = models.CharField(max_length=200, blank=True, null=True)
    gene_biotype = models.CharField(max_length=200, blank=True, null=True)
    transcript_biotype = models.CharField(max_length=200, blank=True, null=True)
    gene_symbol = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_plasmid = models.BooleanField(blank=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class Annotation(models.Model):
    """
    Classe pour les annotations de séquences
        - identifiant du chromosome
        - identifiant du gène 
        - symbole du gène 
        - description
        - identifiant de l'annotateur
        - identifiant du validateur 
        - déjà annoté ou non
    """
    #On suppose qu'un seul annotateur peut annoter -> d'où qu'un seul clé primaire et non double
    id = models.ForeignKey('CodantInfo', on_delete=models.RESTRICT, primary_key=True)
    gene = models.CharField(max_length=200, blank=True, null=True)
    gene_symbol = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    #On suppose qu'un seul annotateur peut annoter -> mais il nous faut toujours un foreign clé 
    annotateur = models.ForeignKey('member.Member', on_delete=models.RESTRICT, related_name='annotateur')
    #On suppose qu'un seul validateur peut donner droit a un annotateur 
    validateur = models.ForeignKey('member.Member', on_delete=models.RESTRICT, related_name='validateur')
    already_annotated = models.BooleanField(blank=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'


class SequenceBase(models.Model):
    """Classe pour les séquences
    """
    sequence = models.TextField(blank=False)

    class Meta:
        abstract = True

class SequenceGenome(SequenceBase):
    """Classe qui hérite de la classe SequenceBase et pour les séquences génomiques
    """
    id = models.ForeignKey('Genome', on_delete=models.RESTRICT, primary_key=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class SequenceCodant(SequenceBase):
    """Classe qui hérite de la classe SequenceBase et pour les séquences codantes
    """
    id = models.ForeignKey('CodantInfo', on_delete=models.RESTRICT, primary_key=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class Forum(models.Model):
    """
    Classe pour les forums
        - identifiant du forum (correspond à un id de protéine)
        - identifiant du chromosome
        - auteur du forum
        - date de création
    """
    id = models.ForeignKey('CodantInfo', on_delete=models.RESTRICT, primary_key=True)
    id_chromosome = models.ForeignKey('Genome', on_delete=models.RESTRICT)
    auteur = models.ForeignKey('member.Member', on_delete=models.RESTRICT, related_name='auteur_forum')
    date = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class Commentaire(models.Model):
    """
    Classe pour les commentaires
        - identifiant du forum (correspond à un id de protéine)
        - texte du commentaire
        - auteur du commentaire
        - date de création du commentaire
        - date de modification du commentaire
    """
    id_forum = models.ForeignKey('Forum', on_delete=models.RESTRICT, related_name='id_forum', null=True)
    text = models.TextField(blank=True, null=True)
    auteur = models.ForeignKey('member.Member', on_delete=models.RESTRICT, related_name='auteur_commentaire')
    date = models.DateField()
    date_update = models.DateField(blank=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'