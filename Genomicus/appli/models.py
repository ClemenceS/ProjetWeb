from django.db import models


class SeqInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    taille = models.IntegerField(blank=False)
    phaseLecture = models.IntegerField(blank=True, null=True)
    espece = models.CharField(max_length=200, blank=False)
    

    class Meta:
        abstract = True

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'



class Genome(SeqInfo):

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'


class CodantInfo(SeqInfo):
    #Blank -> If True, the field is allowed to be blank. Default is False.
    chromosome = models.ForeignKey('Genome', on_delete=models.RESTRICT)
    TYPE_CHOICES = (
      (1, 'CDS'),
      (2, 'PEP'),
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


class SequenceBase(models.Model):
    sequence = models.TextField(blank=False)

    class Meta:
        abstract = True

class SequenceGenome(SequenceBase):
    id = models.ForeignKey('Genome', on_delete=models.RESTRICT, primary_key=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

class SequenceCodant(SequenceBase):
    id = models.ForeignKey('CodantInfo', on_delete=models.RESTRICT, primary_key=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'

        
    
