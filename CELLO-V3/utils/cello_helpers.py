import json

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
