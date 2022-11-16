#!/bin/sh
#
# Setup for the free energy simulations: creates and links to the input file as
# necessary.  Two alternative for the de- and recharging step can be used.
#

# partial removal/addition of charges: softcore atoms only
decharge_crg=":2@H6"
vdw_crg=":1@H6 | :2@O1,H6"
recharge_crg=":1@O1,H6"

# complete removal/addition of charges
#decharge_crg=":2"
#vdw_crg=":1,2"
#recharge_crg=":1"

decharge=" ifsc = 0, crgmask = '$decharge_crg',"
vdw_bonded=" ifsc=1, scmask1=':1@H6', scmask2=':2@O1,H6', crgmask='$vdw_crg'"
recharge=" ifsc = 0, crgmask = '$recharge_crg',"

basedir=.
top=$(pwd)
setup_dir=$(cd "$basedir"; pwd)

for system in ligands complex; do
  if [ \! -d $system ]; then
    mkdir $system
  fi

  cd $system

  for step in decharge vdw_bonded recharge; do
    if [ \! -d $step ]; then
      mkdir $step
    fi

    cd $step

    for w in 0.00922  0.04794  0.11505  0.20634  0.31608  0.43738  0.56262  0.68392  0.79366  0.88495  0.95206  0.99078  0.995  0.999; do
      if [ \! -d $w ]; then
        mkdir $w
      fi

      FE=$(eval "echo \${$step}")
      sed -e "s/%L%/$w/" -e "s/%FE%/$FE/" $top/heat.tmpl > $w/heat.in
      sed -e "s/%L%/$w/" -e "s/%FE%/$FE/" $top/prod.tmpl > $w/ti.in
      sed -e "s/%L%/$w/" -e "s/%FE%/$FE/" $top/run.tmpl > $w/run.slurm

      (
        cd $w
        ln -sf $setup_dir/${system}_$step.parm7 ti.parm7
        ln -sf $setup_dir/${system}_$step.rst7  ti.rst7
      )
    done

    cd ..
  done

  cd $top
done

