#!/bin/bash

#SBATCH --job-name=prep
#SBATCH --partition=g-v100-1
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH --output=prep.out
#SBATCH --error=prep.err

echo "lig minimization"
pmemd.cuda -i min_lig.in -p ligands_vdw_bonded.parm7 -c ligands_vdw_bonded.rst7  -ref ligands_vdw_bonded.rst7 -O -o min_lig.out -e min_lig.en -inf min_lig.info -r min_lig.rst7 -l min_lig.log
echo "lig heating"
pmemd.cuda -i heat_lig.in -p ligands_vdw_bonded.parm7 -c min_lig.rst7 -ref ligands_vdw_bonded.rst7 -O -o heat_lig.out -e heat_lig.en -inf heat_lig.info -r heat_lig.rst7 -x heat_lig.nc -l heat_lig.log
echo "lig press"
pmemd.cuda -i press_lig.in -p ligands_vdw_bonded.parm7 -c heat_lig.rst7 -ref heat_lig.rst7 -O -o press_lig.out -e press_lig.en -inf press_lig.info -r press_lig.rst7 -x press_lig.nc     -l press_lig.log
echo "com minimization"
pmemd.cuda   -i min_com.in -p complex_vdw_bonded.parm7 -c complex_vdw_bonded.rst7  -ref complex_vdw_bonded.rst7   -O -o min_com.out -e min_com.en -inf min_com.info -r min_com.rst7 -l min_com.log
echo "com heating"
pmemd.cuda   -i heat_com.in -p complex_vdw_bonded.parm7 -c min_com.rst7 -ref complex_vdw_bonded.rst7   -O -o heat_com.out -e heat_com.en -inf heat_com.info -r heat_com.rst7 -x heat_com.nc -l heat_com.log
echo "com press"
pmemd.cuda  -i press_com.in -p complex_vdw_bonded.parm7 -c heat_com.rst7 -ref heat_com.rst7   -O -o press_com.out -e press_com.en -inf press_com.info -r press_com.rst7 -x press_com.nc  -l press_com.log

