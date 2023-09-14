#!/usr/bin/env python

import sys, random
import time
import settings
from collections import Counter

def choose_literal(formula, heuristic = "v"):
    """add heuristic on how the literals are chosen"""
    #reference: https://baldur.iti.kit.edu/sat/files/2018/l05.pdf
    #https://en.wikipedia.org/wiki/Boolean_satisfiability_algorithm_heuristics
    counter_dicts = get_counter_all(formula)
    counter_weighted, counter_absolute, counter_weighted_absolute = counter_dicts[0], counter_dicts[1], counter_dicts[2]
    #random.choice(literals)
    #two_clause(formula, literals)

    #Jeroslow-Wang Heuristic
    selected_literal_0 = max(counter_weighted, key=counter_weighted.get)
    #Jeroslow-Wang Heuristic (2 sided)
    selected_literal_1 = max(counter_weighted_absolute, key=counter_weighted_absolute.get)
    #searches for the shortest clause with all literals positive.
    selected_literal_2 = shortest_positive_clause(formula)
    #DLCS
    selected_literal_3 = max(counter_absolute, key=counter_absolute.get)

    selected_literal = selected_literal_3

    if heuristic == "v":
        #perform relative majority voting
        selected_literal = majority_voting([selected_literal_0, selected_literal_1, selected_literal_2, selected_literal_3])
    elif heuristic == "p":
        #output based on probability
        selected_literal = output_based_on_prob([selected_literal_0, selected_literal_1, selected_literal_2, selected_literal_3])
    else:
        print ("invalid option, using relative majority voting by default")
        selected_literal = majority_voting([selected_literal_0, selected_literal_1, selected_literal_2, selected_literal_3])

    #to test random heuristic, run this
    #literals = list(counter.keys())
    #selected_literal = random.choice(literals)

    #to test 2-clause heuristic, run this
    #literals = list(counter.keys())
    #selected_literal = two_clause(formula, literals)

    #print ("literal chosen by different heuristics:", selected_literal_0, selected_literal_1, selected_literal_2, selected_literal_3)
    #print ("choosing", selected_literal)
    return selected_literal

def majority_voting(int_list):
    count_dict = {}

    for num in int_list:
        if num not in list(count_dict.keys()):
            count_dict[num] = 0
        else:
            count_dict[num] += 1

    max_count = max(count_dict.values())

    majority_elements = [k for k, v in count_dict.items() if v == max_count]

    return random.choice(majority_elements)

def output_based_on_prob(int_list):
    counts = Counter(int_list)
    total = len(int_list)
    prob = [counts[key]/total for key in counts]
    return random.choices(list(counts.keys()), prob)[0]

def two_clause(formula, literals):
    clause_filter = [form for form in formula if len(formula)==2]
    literal_count_dict = {}
    for literal in literals:
        literal_count = sum(clause.count(literal) for clause in clause_filter)
        literal_count_dict[literal] = literal_count
    max_value = max(literal_count_dict.values())
    literals = [key for key, value in literal_count_dict.items() if value == max_value]
    return random.choice(literals)

def get_counter_all(formula):
    counter_weighted = {}
    counter_absolute = {}
    counter_weighted_absolute = {}
    for clause in formula:
        for literal in clause:
            abs_literal = abs(literal)
            if literal in counter_weighted:
                counter_weighted[literal] += 2 ** -len(clause)
            else:
                counter_weighted[literal] = 1
            if abs_literal in counter_absolute:
                counter_absolute[abs_literal] += 1
            else:
                counter_absolute[abs_literal] = 1
            if abs_literal in counter_weighted_absolute:
                counter_weighted_absolute[abs_literal] += 2 ** -len(clause)
            else:
                counter_weighted_absolute[abs_literal] = 1
    return counter_weighted, counter_absolute, counter_weighted_absolute

def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

def shortest_positive_clause(formula):
    min_len = sys.maxsize
    best_literal = None
    for clause in formula:
        negatives = sum(1 for literal in clause if literal < 0)
        if not negatives and len(clause) < min_len: 
            best_literal = clause[0]
            min_len = len(clause)
    if not best_literal:
        return formula[0][0]
    return best_literal