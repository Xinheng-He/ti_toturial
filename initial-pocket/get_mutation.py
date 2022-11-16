import sys
mutation = sys.argv[1]

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

print(",".join(get_the_list(mutation)))