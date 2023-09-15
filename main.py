#!/usr/bin/env python

import sys, random
import time
from heuristic import *
import settings

settings.init() 

def parse_dimacs_file(filename):
    clauses = []
    var_num = 0
    with open(filename, 'r') as file:
        for line in file:
            if line[0] in ['c', '%', '0']:
                continue
            if line[0] == 'p':
                _, _, var_num, _ = line.split()
                var_num = int(var_num)
                continue
            clause = list(map(int, line.split()[:-1]))
            if clause:
                clauses.append(clause)
    return clauses, var_num

def unit_propagation(formula):
    assignment = []
    formula = formula[:]  # copy the formula to avoid side-effects

    index = 0
    while index < len(formula):
        clause = formula[index]
        if len(clause) == 1:
            unit = clause[0]
            assignment.append(unit)
            formula = [c for c in formula if unit not in c]
            for i, c in enumerate(formula):
                if -unit in c:
                    formula[i] = [v for v in c if v != -unit]
            if [] in formula:
                return "flag", []
            index = 0  # reset the index when unit is found and assigned
        else:
            index += 1

    return formula, assignment

def find_literal(formula):
    assignment = [] 
    counter = get_counter(formula)
    pure_literals = []
    # check if its negation exist so that we can safely assign to the literal
    for literal, times in counter.items():
        if -literal not in counter:
            pure_literals.append(literal)
    for lit in pure_literals:
        formula = assign(formula, lit)
    assignment += pure_literals
    return formula, assignment

def assign(formula, unit):
    """if a clause has only one unassigned literal, that literal must be assigned the value that satisfies the clause"""
    new_formula = []
    for clause in formula:
        if unit in clause:
            continue
        elif -unit in clause:
            settings.unit_propagations_counter += 1
            updated_clause = [x for x in clause if x != -unit]
            new_formula.append(updated_clause)
            if not updated_clause:
                return "flag"
        else:
            new_formula.append(clause)
    return new_formula

def solve(formula, assignment):
    # Get literal clause
    literal_result = find_literal(formula)
    formula = literal_result[0]
    pure_assignment = literal_result[1]
    # Get unit propagation
    unit_result = unit_propagation(formula)
    formula = unit_result[0]
    unit_assignment = unit_result[1]
    # Update assignment
    assignment.extend(pure_assignment)
    assignment.extend(unit_assignment)
    if formula == "flag":
        return []
    if not formula:
        return assignment
    if len(sys.argv) > 2:
        variable = choose_literal(formula, sys.argv[2])
    else:
        variable = choose_literal(formula)
    settings.split_counter += 1
    solution = solve(assign(formula, variable), assignment + [variable])
    if not solution:
        settings.split_counter += 1
        solution = solve(assign(formula, -variable), assignment + [-variable])
    return solution

def main():
    clauses, var_num = parse_dimacs_file(sys.argv[1])
    st = time.time()
    solution = solve(clauses, [])
    et = time.time()
    elapsed_time = et - st
    print ('c total solving time: ', elapsed_time)
    print ('c number of splits: ', settings.split_counter)
    print ('c number of unit propagations: ', settings.unit_propagations_counter)
    if solution:
        solution += [x for x in range(1, var_num + 1) if x not in solution and -x not in solution]
        solution.sort(key=lambda x: abs(x))
        print ('s SATISFIABLE')
        print ('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print ('s UNSATISFIABLE')

if __name__ == '__main__':
    main()