#!/bin/bash
#SBATCH --account=rrg-cbright
#SBATCH --time=0-24:00

for ((i=600; i<=1200; i+=40)); do ./runbenchmarks.sh t 200-$i > t-200-$i.log; done
