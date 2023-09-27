#!/bin/bash
#SBATCH --account=rrg-cbright
#SBATCH --time=0-12:00

for ((i=300; i<=900; i+=30)); do ./runbenchmarks.sh p 150-$i > p-150-$i.log; done
