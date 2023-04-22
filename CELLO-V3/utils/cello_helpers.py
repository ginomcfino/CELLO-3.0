import json

# def next_input(inputs, index, current, result):
#     if index == len(inputs):
#         result.append(current[:])
#         return

#     for i in range(len(inputs)):
#         if inputs[i] not in current:
#             current.append(inputs[i])
#             next_input(inputs, index + 1, current, result)
#             current.pop()

# def generate_permutations(inputs):
#     result = []
#     next_input(inputs, 0, [], result)
#     return result

# def iterate_graph(input_sensors, gates, output_devices):
#     input_permutations = generate_permutations(input_sensors)
#     gate_permutations = generate_permutations(gates)
#     output_permutations = generate_permutations(output_devices)

#     iterations = 0
#     for input_combination in input_permutations:
#         for gate_combination in gate_permutations:
#             for output_combination in output_permutations:
#                 #unique_names = set(x[0] for x in input_combination + gate_combination + output_combination)
#                 #if len(unique_names) == len(input_combination) + len(gate_combination) + len(output_combination):
#                     iterations += 1
#                     # Perform your desired operation with the current iteration
#                     print(input_combination, gate_combination, output_combination)
#     return iterations

# def is_valid(current_combination):
#     seen = set()
#     for node in current_combination:
#         if node[0] in seen:
#             return False
#         seen.add(node[0])
#     return True

# def backtrack(index, nodes, current_combination, all_combinations):
#     if index == len(nodes):
#         if is_valid(current_combination):
#             all_combinations.append(current_combination[:])
#         return

#     for node in nodes[index]:
#         current_combination.append(node)
#         backtrack(index + 1, nodes, current_combination, all_combinations)
#         current_combination.pop()

# def generate_combinations(input_sensors, gates, output_devices):
#     all_nodes = [input_sensors, gates, output_devices]
#     all_combinations = []
#     backtrack(0, all_nodes, [], all_combinations)
#     return all_combinations

def is_valid(combination):
    names = [node[0] for node in combination]
    return len(names) == len(set(names))

def generate_combinations(inputs, gates, outputs):
    all_combinations = []

    for input1 in inputs:
        for input2 in inputs:
            if input1[0] == input2[0]:
                continue
            for gate1 in gates:
                for gate2 in gates:
                    if gate1[0] == gate2[0]:
                        continue
                    for output in outputs:
                        combination = [input1, input2, gate1, gate2, output]
                        if is_valid(combination):
                            all_combinations.append(combination)

    return all_combinations

def permute_count_helper(i_netlist, o_netlist, g_netlist, i_ucf, o_ucf, g_ucf):
    factorial = lambda n: 1 if n == 0 else n * factorial(n - 1)
    partial_factorial = lambda n, k: 1 if n <= k else n * partial_factorial(n - 1, k)
    total_permutations = partial_factorial(i_ucf, i_ucf-i_netlist) * partial_factorial(g_ucf, g_ucf-g_netlist) * partial_factorial(o_ucf, o_ucf-o_netlist)
    confirm_permutations = (factorial(i_ucf) / factorial(i_ucf - i_netlist)) * (factorial(o_ucf) / factorial(o_ucf - o_netlist)) * (factorial(g_ucf) / factorial(g_ucf - g_netlist))
    return total_permutations, confirm_permutations

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
