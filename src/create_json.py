import re
import json
from Bio import SeqIO
import sys

NAME_APPLI = 'genomApp'

def get_id(fasta):
    return fasta.id

def get_seq(fasta):
    return str(fasta.seq)

def get_chromosome(fasta):
    for match in re.finditer(r'chromosome:(\w+)', fasta.description):
        return match.group(1)
    for match in re.finditer(r'plasmid:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_start(fasta):
    for match in re.finditer(r'Chromosome:(\d+)', fasta.description):
        return int(match.group(1))
    for match in re.finditer(r'plasmid:\w+:\w+:(\d+)', fasta.description):
        return int(match.group(1))
    return None

def get_end(fasta):
    for match in re.finditer(r'Chromosome:\d+:(\d+)', fasta.description):
        return int(match.group(1))
    for match in re.finditer(r'plasmid:\w+:\w+:\d+:(\d+)', fasta.description):
        return int(match.group(1))
    return None

def get_gene(fasta):
    for match in re.finditer(r'gene:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_transcript(fasta):
    for match in re.finditer(r'transcript:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_geneBiotype(fasta):
    for match in re.finditer(r'gene_biotype:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_transcriptBiotype(fasta):
    for match in re.finditer(r'transcript_biotype:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_geneSymbol(fasta):
    for match in re.finditer(r'gene_symbol:(\w+)', fasta.description):
        return match.group(1)
    return None

def get_description(fasta):
    for match in re.finditer(r'description:([\w ]+)', fasta.description):
        return match.group(1)
    return None

def get_size(fasta):
    return get_end(fasta) - get_start(fasta) + 1

def get_phase(fasta):
    for match in re.finditer(r'Chromosome:\d+:\d+:-?(\d+)', fasta.description):
        return int(match.group(1))
    for match in re.finditer(r'plasmid:\w+:\w+:\d+:\d+:-?(\d+)', fasta.description):
        return int(match.group(1))

def is_plasmid(fasta):
    for match in re.finditer(r'plasmid:', fasta.description):
        return True

def get_espece(address):
    for match in re.finditer(r'\/?(\w+)(_cds)\.', address):
        return match.group(1)
    for match in re.finditer(r'\/?(\w+)(_pep)\.', address):
        return match.group(1)
    for match in re.finditer(r'\/?(\w+)\.', address):
        return match.group(1)
    return None

def get_gc_rate(fasta):
    seq = get_seq(fasta)
    G = seq.count('G')
    C = seq.count('C')
    return (G+C)/len(seq)*100

def fa_2_json(file_address, cds=True):

    cds = False
    for match in re.finditer(r'_cds.', file_address):
        cds = True

    dico_info = []
    dico_seq = []


    fasta_sequences = SeqIO.parse(open(file_address),'fasta')
    for fasta in fasta_sequences:
        temp={}
        if(cds):
            temp['pk'] = f'cds_{get_id(fasta)}'
        else:
            temp['pk'] = f'pep_{get_id(fasta)}'

        temp['model'] = f"{NAME_APPLI}.CodantInfo"
        
        fields = {}
        fields['taille'] = get_size(fasta)
        fields['phaseLecture'] = get_phase(fasta)
        fields['espece'] = get_espece(file_address)
        fields['gc_rate'] = 0

        #fields['seq'] = get_seq(fasta)
        fields['chromosome'] = get_chromosome(fasta)
        if(cds):
            fields['codant_type'] = 1
        else:
            fields['codant_type'] = 2
        fields['gene'] = get_gene(fasta)

        fields['start'] = get_start(fasta)
        fields['stop'] = get_end(fasta)
        fields['transcript'] = get_transcript(fasta)
        fields['gene_biotype'] = get_geneBiotype(fasta)
        fields['transcript_biotype'] = get_transcriptBiotype(fasta)
        fields['gene_symbol'] = get_geneSymbol(fasta)
        fields['description'] = get_description(fasta)
        fields['is_plasmid'] = is_plasmid(fasta)
        temp['fields'] = fields
        dico_info.append(temp)

        temp={}
        if(cds):
            temp['pk'] = f'cds_{get_id(fasta)}'
        else:
            temp['pk'] = f'pep_{get_id(fasta)}'
        temp['model'] = f"{NAME_APPLI}.SequenceCodant"
        fields = {}
        fields['sequence'] = str(fasta.seq).upper()
        temp['fields'] = fields
        dico_seq.append(temp)
    
    with open(f"{file_address[:-3]}_dico.json", "w") as write_file:
        json.dump(dico_info, write_file, indent=4)

    with open(f"{file_address[:-3]}_seq.json", "w") as write_file:
        json.dump(dico_seq, write_file, indent=4)


def genome_2_fasta(file_address):
    dico_genome = []
    dico_seq = []

    fasta_sequences = SeqIO.parse(open(file_address),'fasta')
    for fasta in fasta_sequences:
        temp={}
        temp['pk'] = get_chromosome(fasta)
        temp['model'] = f"{NAME_APPLI}.Genome"
        fields = {}
        fields['taille'] = get_size(fasta)
        fields['phaseLecture'] = get_phase(fasta)
        fields['espece'] = get_espece(file_address)
        fields['gc_rate'] = get_gc_rate(fasta)
        temp['fields'] = fields
        dico_genome.append(temp)

        temp={}
        temp['pk'] = get_chromosome(fasta)
        temp['model'] = f"{NAME_APPLI}.SequenceGenome"
        fields = {}
        fields['sequence'] = str(fasta.seq).upper()
        temp['fields'] = fields
        dico_seq.append(temp)
    
    with open(f"{file_address[:-3]}_genome.json", "w") as write_file:
        json.dump(dico_genome, write_file, indent=4)

    with open(f"{file_address[:-3]}_seq.json", "w") as write_file:
        json.dump(dico_seq, write_file, indent=4)


entry = sys.argv[1]

genome_2_fasta(f"data/{entry}.fa")
fa_2_json(f'data/{entry}_cds.fa')
fa_2_json(f'data/{entry}_pep.fa')


