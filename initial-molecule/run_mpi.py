import sys,os,time

fn_in = sys.argv[1]
max_steps = int(sys.argv[2])
run_type = sys.argv[3]

current_dir = os.getcwd()

def get_complete(fn):
    for line in open(fn).readlines():
        if line.startswith('| Total'):
            return int(line.split()[6])

def if_still_running():
    # get all the time for last changed files, check if 5 min has passed
    # if so, return False
    # if not, return True
    ti_list = []
    for i in os.listdir('.'):
        if i.endswith('.out') and i.startswith('ti'):
            ti_list.append(int(i.split('.')[0].split('ti')[1]))
            if time.time() - os.path.getmtime(i) < 300:
                return True,max(ti_list)
    return False,max(ti_list)

def get_nstlim(fn):
    return int(open(fn).readlines()[2].split()[5][:-1])


for i1 in os.listdir(current_dir+'/'+fn_in):
    for i2 in os.listdir(current_dir+'/'+fn_in+'/'+i1):
        os.chdir('%s/%s/%s/%s' % (current_dir,fn_in,i1,i2))
        if not if_still_running()[0]:
            number = str(if_still_running()[1])
            try:
                finished_steps = get_complete('ti{}.info'.format(number.zfill(3)))
            except:
                number = str(int(number)-1)
                finished_steps = get_complete('ti{}.info'.format(number.zfill(3)))
            if finished_steps < max_steps:
                if number == '1':
                    nts_lim = get_nstlim('ti.in')
                    current_text = open('ti.in').read()
                else:
                    nts_lim = get_nstlim('ti{}.in'.format(number.zfill(3)))
                    current_text = open('ti{}.in'.format(number.zfill(3))).read()
                with open('ti{}.in'.format(str((int(number)+1)).zfill(3)),'w') as f:
                    f.write(current_text.replace('nstlim = {}'.format(nts_lim),'nstlim = {}'.format(max_steps-finished_steps)))
                if run_type == 'mpi':
                    with open('ti{}.slurm'.format(str((int(number)+1)).zfill(3)),'w') as f:
                        f.write(f'''#!/bin/bash

#SBATCH --job-name=run{str((int(number)+1)).zfill(3)}
#SBATCH --partition=c-64-1
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH --output=run{str((int(number)+1)).zfill(3)}.out
#SBATCH --error=run{str((int(number)+1)).zfill(3)}.err

mpirun -np 64 pmemd.MPI -i ti{str((int(number)+1)).zfill(3)}.in -c ti{number.zfill(3)}.rst7 -p ti.parm7 \
-O -o ti{str((int(number)+1)).zfill(3)}.out -inf ti{str((int(number)+1)).zfill(3)}.info -e ti{str((int(number)+1)).zfill(3)}.en -r ti{str((int(number)+1)).zfill(3)}.rst7 -x ti{str((int(number)+1)).zfill(3)}.nc \
-l ti{str((int(number)+1)).zfill(3)}.log''')
                elif run_type == 'cuda':
                    with open('ti{}.slurm'.format(str((int(number)+1)).zfill(3)),'w') as f:
                        f.write(f'''#!/bin/bash

#SBATCH --job-name=run{str((int(number)+1)).zfill(3)}
#SBATCH --partition=g-v100-1
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH --output=run{str((int(number)+1)).zfill(3)}.out
#SBATCH --error=run{str((int(number)+1)).zfill(3)}.err

pmemd.cuda -i ti{str((int(number)+1)).zfill(3)}.in -c ti{number.zfill(3)}.rst7 -p ti.parm7 \
-O -o ti{str((int(number)+1)).zfill(3)}.out -inf ti{str((int(number)+1)).zfill(3)}.info -e ti{str((int(number)+1)).zfill(3)}.en -r ti{str((int(number)+1)).zfill(3)}.rst7 -x ti{str((int(number)+1)).zfill(3)}.nc \
-l ti{str((int(number)+1)).zfill(3)}.log''')
                os.system('sbatch ti{}.slurm'.format(str((int(number)+1)).zfill(3)))
                print('Submitted job for {} in {} {}'.format(i1,fn_in,i2))
            else:
                print('Already finished {}'.format('%s/%s/%s' % (fn_in,i1,i2)))
        else:
            print('Still running {}'.format('%s/%s/%s' % (fn_in,i1,i2)))

                
