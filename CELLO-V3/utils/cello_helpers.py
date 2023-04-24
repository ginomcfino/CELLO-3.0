import json
import math
import itertools

'''
cello gate_assignment algorithm pseudo code:

def assign_hash_table_for_every_gate_permu():
    hash_table = {} #(may reach up to 100mb in memory)
    max_score = 0
    best_design = None
    for each possibility in (I)P(i) * (O)P(o) * (G)P(g) permutations: (recursion?)
        design = new Circuit(possibility)
        hash_table[hash(design)] = (False, None) (new init, not yet evaluated)
        circuit_score = evaluate(design)
        hash_table[hash(design)] = (True, circuit_score)
        if circuit_sccore > max_score:
            max_score = circuit_score
            best_design = design
    confirm len(hash_table) = (I)P(i) * (O)P(o) * (G)P(g)
    return max(hash_table), best_design
    
(decided to scrap the hash table)
'''

def permute_count_helper(i_netlist, o_netlist, g_netlist, i_ucf, o_ucf, g_ucf):
    factorial = lambda n: 1 if n == 0 else n * factorial(n - 1)
    partial_factorial = lambda n, k: 1 if n <= k else n * partial_factorial(n - 1, k)
    # check it thrice
    total_permutations = partial_factorial(i_ucf, i_ucf-i_netlist) * partial_factorial(g_ucf, g_ucf-g_netlist) * partial_factorial(o_ucf, o_ucf-o_netlist)
    confirm_permutations = (factorial(i_ucf) / factorial(i_ucf - i_netlist)) * (factorial(o_ucf) / factorial(o_ucf - o_netlist)) * (factorial(g_ucf) / factorial(g_ucf - g_netlist))
    confirm_permuattions2 = math.perm(i_ucf, i_netlist) * math.perm(o_ucf, o_netlist) * math.perm(g_ucf, g_netlist)
    return total_permutations, (confirm_permutations + confirm_permuattions2) / 2

def print_centered(text, padding=False):
    length = 88  # Length of the string of slashes
    if padding:
        print()
    print("/" * length)
    if type(text) == list:
        for t in text:
            print(t.center(length))
    else:
        print(text.center(length))
    print("/" * length)
    if padding:
        print()


def debug_print(msg, padding=True):
    out_msg = f'DEBUG: {msg}'
    if padding:
        out_msg = '\n' + out_msg + '\n'
    print(out_msg)


def print_json(chunk):
    print(json.dumps(chunk, indent=4))
