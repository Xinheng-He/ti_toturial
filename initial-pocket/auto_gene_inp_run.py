
import sys,os
u_num = sys.argv[1]
num_per_ligand = int(sys.argv[2])
mutation = [sys.argv[3]]
mutation_name = sys.argv[4]

w1 = open('min.tmpl','w')
w1.write('''minimisation
 &cntrl
   imin = 1, ntmin = 2, maxcyc = 200,
   ntpr = 20, ntwe = 20,
   dx0 = 1.0D-7,
   ntb = 1,

   icfe = 1, ifsc = 1, clambda = %L%, scalpha = 0.5, scbeta = 12.0,
   logdvdl = 0,
   timask1 = ':{0}&!@{2}', timask2 = ':{1}&!@{2}',
   scmask1 = ':{0}&!@{2}', scmask2 = ':{1}&!@{2}',

   !method 2:
   !scmask1 = '', scmask2 = ':163@HG=',
 /

 &ewald
 /

'''.format(u_num,num_per_ligand+1,",".join(mutation)))

w1.close()
w2 = open('heat.tmpl','w')
w2.write('''heating
 &cntrl
   imin = 0, nstlim = 10000, irest = 0, ntx = 1, dt = 0.002,
   ntt = 1, temp0 = 300.0, tempi = 50.0, tautp = 1.0,
   ntc = 2, ntf = 1,
   ntb = 1,
   ioutfm = 1, iwrap = 1,
   ntwe = 1000, ntwx = 1000, ntpr = 1000, ntwr = 5000,

   !needed for method 2, also set dt=0.001
   !noshakemask = ':99,163',

   nmropt = 1,
   ntr = 1, restraint_wt = 5.00,
   restraintmask='!:WAT & !@H=',

   icfe = 1, ifsc = 1, clambda = %L%, scalpha = 0.5, scbeta = 12.0,
   logdvdl = 0,
   timask1 = ':{0}&!@{2}', timask2 = ':{1}&!@{2}',
   scmask1 = ':{0}&!@{2}', scmask2 = ':{1}&!@{2}',

   !method 2:
   !scmask1 = '', scmask2 = ':163@HG=',
 /

 &ewald
 /

 &wt
   type='TEMP0',
   istep1 = 0, istep2 = 8000,
   value1 = 50.0, value2 = 300.0
 /

 &wt type = 'END'
 /


'''.format(u_num,num_per_ligand+1,",".join(mutation)))
w2.close()

w4 = open('prod1.tmpl','w')
w4.write('''TI simulation
 &cntrl
   imin = 0, nstlim = 2500000, irest = 1, ntx = 5, dt = 0.002,
   ntt = 3, temp0 = 300.0, gamma_ln = 2.0, ig = -1,
   ntc = 2, ntf = 1,
   ntb = 2,
   ntp = 1, pres0 = 1.0, taup = 2.0,
   ioutfm = 1, iwrap = 1,
   ntwe = 10000, ntwx = 10000, ntpr = 10000, ntwr = 10000,

   icfe = 1, ifsc = 1, clambda = %L%, scalpha = 0.5, scbeta = 12.0,
   logdvdl = 1,
   ifmbar = 1, mbar_states = 14,
   mbar_lambda = 0.00922,  0.04794,  0.11505,  0.20634,  0.31608,  0.43738,  0.56262,  0.68392,  0.79366,  0.88495,  0.95206,  0.99078,  0.995,  0.999,
   timask1 = ':{0}&!@{2}', timask2 = ':{1}&!@{2}',
   scmask1 = ':{0}&!@{2}', scmask2 = ':{1}&!@{2}',

   !method 2:
   !scmask1 = '', scmask2 = ':163@HG=',
 /


 &ewald
 / 

'''.format(u_num,num_per_ligand+1,",".join(mutation)))
w4.close()
w5 = open('setup_my_help.sh','w')
w5.write('''#!/bin/sh
#
# Setup for the free energy simulations: creates and links to the input file as
# necessary.  Two alternative for the de- and recharging step can be used.
#

basedir=.
top=$(pwd)
setup_dir=$(cd "$basedir"; pwd)

for system in $1 $2; do
  if [ \! -d $system ]; then
    mkdir $system
  fi

  cd $system

  for w in 0.00922  0.04794  0.11505  0.20634  0.31608  0.43738  0.56262  0.68392  0.79366  0.88495  0.95206  0.99078  0.995  0.999; do
    if [ \! -d $w ]; then
      mkdir $w
    fi

    sed -e "s/%L%/$w/" $top/min.tmpl > $w/min.in
    sed -e "s/%L%/$w/" $top/heat.tmpl > $w/heat.in
    sed -e "s/%L%/$w/" $top/prod1.tmpl > $w/ti1.in
    sed -e "s/%L%/$w/" $top/run.tmpl > $w/run.slurm
    
    (
      cd $w
      ln -sf $setup_dir/merged_${system}.parm7 ti.parm7
      ln -sf $setup_dir/merged_${system}.rst7  ti.rst7
      pwd
      ls
      sbatch run.slurm
    )
  done

  cd $top
done

''')
w5.close()
os.system('chmod +x setup_my_help.sh && ./setup_my_help.sh {0}_protein {0}_complex'.format(mutation_name))