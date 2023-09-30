#!/usr/bin/env python

import sys, random
import time
import settings
from collections import Counter
from collections import defaultdict

random.seed(42) 

def choose_literal(formula, heuristic="v"):  
    counter_dicts = get_counter_all(formula)
    counter_two_clause = get_counter(formula, True) if heuristic in ['v', 'p', 't'] else {}
    counter = get_counter(formula)
    counter_weighted, counter_absolute, counter_weighted_absolute = counter_dicts[0], counter_dicts[1], counter_dicts[2]

    if heuristic == "r":
        selected_literal = random.choice(list(counter.keys()))
    elif heuristic == "t":
        selected_literal = get_max(counter_two_clause) if counter_two_clause else random.choice(list(counter.keys()))
    elif heuristic in ["v", "p"]:
        selected_literal_0 = get_max(counter_weighted) #Jeroslow-Wang Heuristic
        selected_literal_1 = get_max(counter_weighted_absolute) #Jeroslow-Wang Heuristic (2-sides)
        selected_literal_2 = get_max(counter_absolute) #DLCS: Dynamic Largest Individual Sum
        selected_literal_3 = get_max(counter_two_clause) if counter_two_clause else random.choice(list(counter.keys()))
        list_of_literals = [selected_literal_0, selected_literal_1, selected_literal_2, selected_literal_3 ]
        selected_literal = majority_voting(list_of_literals) if heuristic == "v" else output_based_on_prob(list_of_literals)
    else:
        print("invalid option, using 2-clause by default")
        selected_literal = get_max(counter_two_clause) if counter_two_clause else random.choice(list(counter.keys()))

    settings.split_counter += 1
    return selected_literal

def majority_voting(int_list):
    count_dict = Counter(int_list)
    max_count = max(count_dict.values())
    majority_elements = [k for k, v in count_dict.items() if v == max_count]
    return random.choice(majority_elements)

def output_based_on_prob(int_list):
    counts = Counter(int_list)
    total = len(int_list)
    prob = [counts[key]/total for key in counts]
    return random.choices(list(counts.keys()), prob)[0]

def get_max(counter):
    return max(counter, key=counter.get)

def get_counter(formula, two_clause = False):
    counter = {}
    for clause in formula:
        if two_clause:
            if len(clause) == 2:
                for literal in clause:
                    if literal in counter:
                        counter[literal] += 1
                    else:
                        counter[literal] = 1
        else:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
    return counter

def get_counter_all(formula):
    counter_weighted = defaultdict(float)
    counter_absolute = defaultdict(int)
    counter_weighted_absolute = defaultdict(float)
    
    for clause in formula:
        for literal in clause:
            abs_literal = abs(literal)
            counter_weighted[literal] += 2 ** -len(clause)
            counter_absolute[abs_literal] += 1
            counter_weighted_absolute[abs_literal] += 2 ** -len(clause)

    return counter_weighted, counter_absolute, counter_weighted_absolute
