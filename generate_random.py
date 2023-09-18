#!/usr/bin/env python
import sys, random
import os

#The number N of variables, the number K=3 of distinct literals per clause, and the number L of clauses.

def generate_random(N, K, L):
    # Initiate an array for our clauses.
    clauses = []
    
    for i in range(L):
        current_clause = random.sample(range(1, N+1), K)
        current_clause = [prop if random.random() > 0.5 else -prop for prop in current_clause]
        clauses.append(current_clause)
    
    return clauses

if not os.path.exists('3-SAT'):
    os.makedirs('3-SAT')

def main(N, K, L):
    #generate 100 DIMACS files
    for i in range(100):
        clauses = generate_random(N, K, L)
        with open(f'3-SAT/output_{i}.cnf', 'w') as f:
            f.write(f'p cnf {N} {L}\n')
            # Write clauses to the file:
            for clause in clauses:
                f.write(' '.join(map(str, clause)) + ' 0\n')

if __name__ == '__main__':
    N = int(sys.argv[1])
    L = int(sys.argv[2])
    K = 3
    main(N, K, L)