from .models import SequenceGenome, SequenceCodant, Genome, CodantInfo
import os
from pyfaidx import Faidx


#Creates fasta file needed in the format for genome visualisation
def create_new_fa(id):
    """Fonction pour la création des fichiers fasta nécessaire pour la visualisation du génome
    
    :parameter id:
    """
    #Get genome
    g = Genome.objects.get(id = id)
    #Get species
    espece = g.espece
    #Get sequence
    seq = SequenceGenome.objects.get(id = g)
    sequence = seq.sequence
    #Write
    with open(f'static/{espece}.fa', 'w') as fasta:
        fasta.write(f'>{id}\n')
        fasta.write(sequence)

#Function that creates the gff file following the correct format
def create_gff(id):
    """Fonction pour la création des fichiers au format GFF nécessaire pour la visualisation du génome

    :parameter id:
    """
    #Get genome
    g = Genome.objects.get(id = id)
    cds_list = list(CodantInfo.objects.filter(chromosome = g, codant_type = 1))
    name_file = f'{g.espece}.gff'
    os.system('pwd')
    os.system(f'rm -rf static/{name_file} || true')

    for cds in cds_list:
        start =cds.start
        stop = cds.stop
        phaseLecture = cds.phaseLecture
        cds_id = cds.id[4:]
        gene_symbol = f'Gene_symbol={cds.gene_symbol}'
        gene_biotype = f'Gene_biotype={cds.gene_biotype}'
        description = cds.description
        id_9col = 'ID='+cds_id+'_'+str(start)+'-'+str(stop)+'_'+str(phaseLecture)+'_CDS'


        with open(f'static/{name_file}', 'a') as gff_file:
        
            gff_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s;%s;%s;%s;%s\n' % (id, 'Genomicus', 'CDS', str(
            start), str(stop), '.', '+', str(phaseLecture), id_9col, gene_symbol, gene_biotype, f'Description {description}', f'Name {cds_id}'))

#Function that creates the .fai file using the Faidx function
def creat_fai(id):
    """Fonction pour la création des fichiers fai (fasta indexé) nécessaire pour la visualisation du génome

    :parameter id:
    """
    #Get genome
    g = Genome.objects.get(id = id)
    #Get species
    espece = g.espece
    Faidx(f'static/{espece}.fa')#ABG70353
    