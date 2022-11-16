import sys
import numpy as np

mutation,fn1,fn2,d_res,fo1,fo2 = sys.argv[1:]

residue_letter_1_to_3_dict = {'A':'ALA','C':'CYS','D':'ASP','E':'GLU','F':'PHE','G':'GLY','H':'HIS','I':'ILE','K':'LYS','L':'LEU','M':'MET','N':'ASN','P':'PRO','Q':'GLN','R':'ARG','S':'SER','T':'THR','V':'VAL','W':'TRP','Y':'TYR'}

def get_the_list(mutation):
    if 'G' not in mutation and 'P' not in mutation:
        if 'Y' in mutation and 'F' in mutation:
            return ['CA','C','O','N','H','HA','CB','HB2','HB3','CG','CD1','HD1','CE1','HE1','CZ','CE2','HE2','CD2','HD2']
        else:
            return ['CA','C','O','N','H','HA','CB']
    elif 'P' in mutation:
        return []
    else:
        return ['CA','C','O','N','H']

def check_diff(fn1,fn2,d_res,fo1,fo2):
    t1 = open(fn1).readlines()
    t2 = open(fn2).readlines()
    l1 = []
    d1 = {}
    l2 = []
    d2 = {}
    diff_dir = {}
    diff_mut_dir = {}
    for line in t1[1:]:
        if line.startswith('ATOM'):
            l1.append([line[11:27],line[29:55].split(),line])
            d1[line[11:27]] = list(map(float,line[29:55].split()))
        else:
            l1.append([line[11:27], line[29:55].split(), line])
    for line in t2[1:]:
        if line.startswith('ATOM'):
            l2.append([line[11:27], line[29:55].split(), line])
            d2[line[11:27]] = list(map(float,line[29:55].split()))
        else:
            l2.append([line[11:27], line[29:55].split(), line])
    for key in d1:
        n_num = int(key.split()[-1])
        if n_num != int(d_res):
            if d1[key] != d2[key]:
                diff_dir[key] = np.array(d1[key])
        else:
            if key.split()[0] in get_the_list(mutation):
                diff_mut_dir[key.split()[0]] = np.array(d1[key])

    print(diff_dir)
    w1 = open(fo1,'w')
    w2 = open(fo2,'w')
    for item in l1:
        if item[0] in diff_dir:
            w1.write(item[2][:30]+'%8.3f%8.3f%8.3f%s'% (float(diff_dir[item[0]][0]), float(diff_dir[item[0]][1]), float(diff_dir[item[0]][2]),item[2][54:]))
        else:
            w1.write(item[2])
    for item in l2:
        if len(item[0]) >0 and int(item[0].split()[-1])==int(d_res) and item[0].split()[0] in diff_mut_dir:
            w2.write(item[2][:30].replace(residue_letter_1_to_3_dict[mutation[-1]],residue_letter_1_to_3_dict[mutation[0]])+'%8.3f%8.3f%8.3f%s'% (float(diff_mut_dir[item[0].split()[0]][0]), float(diff_mut_dir[item[0].split()[0]][1]), float(diff_mut_dir[item[0].split()[0]][2]),item[2][54:]))
        else:
            if item[0] in diff_dir:
                w2.write(item[2][:30]+'%8.3f%8.3f%8.3f%s'% (float(diff_dir[item[0]][0]), float(diff_dir[item[0]][1]), float(diff_dir[item[0]][2]),item[2][54:]))
            else:
                w2.write(item[2])

check_diff(fn1,fn2,d_res,fo1,fo2)