#!/bin/bash
#SBATCH --account=rrg-cbright
#SBATCH --time=0-12:00

for ((i=300; i<=900; i+=30)); do ./runbenchmarks.sh v 150-$i > v-150-$i.log; done
