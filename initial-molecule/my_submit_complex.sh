#!/bin/sh
#
# Run all ligand simulations.  This is mostly a template for the LSF job
# scheduler.
#


cd complex

for step in decharge vdw_bonded recharge; do
  cd $step

  for w in 0.00 0.05 0.10 0.15 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.85 0.90 0.95 1.00; do
    cd $w
    
    pmemd.cuda -i heat.in -c ti.rst7 -ref ti.rst7 -p ti.parm7 \
  -O -o heat.out -inf heat.info -e heat.en -r heat.rst7 -x heat.nc -l heat.log && pmemd.cuda -i ti.in -c heat.rst7 -p ti.parm7 \
  -O -o ti001.out -inf ti001.info -e ti001.en -r ti001.rst7 -x ti001.nc \
     -l ti001.log
     
    # adapt above for your job scheduler

    cd ..
  done

  cd ..
done

