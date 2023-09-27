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
                settings.split_counter += 1
                return "flag", []
            index = 0  # reset the index when unit is found and assigned
        else:
            index += 1
    return formula, assignment

def find_literal(formula):
    assignment = [] 
    counter = get_counter(formula)
    pure_literals = {literal for literal, times in counter.items() if -literal not in counter}

    new_formula = []
    for clause in formula:
        new_clause = []
        for literal in clause:
            if abs(literal) in pure_literals:
                if literal > 0:
                    assignment.append(literal)
                continue
            new_clause.append(literal)
        if new_clause:
            new_formula.append(new_clause)

    return new_formula, assignment

def assign(formula, unit):
    """if a clause has only one unassigned literal, that literal must be assigned the value that satisfies the clause"""
    new_formula = []
    for clause in formula:
        if unit in clause:
            continue
        new_clause = [x for x in clause if x != -unit]
        if not new_clause:
            return "flag"
        new_formula.append(new_clause)
    return new_formula

def solve(formula, assignment, arg=None):
    formula, pure_assignment = find_literal(formula)
    formula, unit_assignment = unit_propagation(formula)

    assignment += pure_assignment + unit_assignment

    if not formula:
        return assignment
    elif formula == "flag":
        return []

    variable = choose_literal(formula, arg) if arg else choose_literal(formula)

    for var in [variable, -variable]:
        solution = solve(assign(formula, var), assignment + [var], arg)
        if solution:
            return solution
    return []

def print_results(solution, var_num, elapsed_time):
    print('c total solving time:', elapsed_time)
    print('c number of splits:', settings.split_counter)
    if solution:
        solution += [x for x in range(1, var_num + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print('s SATISFIABLE')
        print('v', ' '.join(map(str, solution)), '0')
    else:
        print('s UNSATISFIABLE')

def main():
    clauses, var_num = parse_dimacs_file(sys.argv[1])
    start_time = time.time()
    if len(sys.argv) > 2:
        solution = solve(clauses, [], sys.argv[2])
    else:
        solution = solve(clauses, [])
    elapsed_time = time.time() - start_time
    print_results(solution, var_num, elapsed_time)

if __name__ == '__main__':
    main()