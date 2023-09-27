#!/bin/bash
#SBATCH --account=rrg-cbright
#SBATCH --time=0-12:00

for ((i=300; i<=600; i+=20)); do ./runbenchmarks.sh t 100-$i > t-100-$i.log; done
