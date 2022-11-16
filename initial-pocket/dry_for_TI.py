import sys
imp_pdb = sys.argv[1]
out_wat = sys.argv[2]
out_part = sys.argv[3].split(',')
text = open(imp_pdb).readlines()
dic_resi = {'ALA': 'A',
            'ARG': 'R',
            'ASP': 'D',
            'CYS': 'C',
            'CYX': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'HIS': 'H',
            'HIE': 'H',
            'HSD': 'H',
            'ILE': 'I',
            'GLY': 'G',
            'ASN': 'N',
            'LEU': 'L',
            'NLN': 'N',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V',
            'LIG': 'LIG',
            'NAG': 'NAG', }
line_num_list = []
for num,line in enumerate(text[:-1]):
    if line[:3] == 'TER':
        if text[num-1][17:20] in dic_resi:
            line_num_list.append(num)
assert len(line_num_list) == len(out_part)
count = 0
for num,i in enumerate(line_num_list):
    with open(out_part[num],'w') as w:
        w.writelines(text[count:i+1])
        count = i+1
with open(out_wat,'w') as w:
    w.writelines(text[count:])
