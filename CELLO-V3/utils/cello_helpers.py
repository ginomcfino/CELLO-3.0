import json


class Gate:
    def __init__(self, gate_id, gate_type, inputs, output):
        self.gate_id = gate_id
        self.gate_type = gate_type
        self.inputs = inputs
        self.output = output

    def __str__(self):
        return f'{self.gate_type} gate {self.gate_id} w/ inputs {self.inputs}, output {self.output}'

class Graph:
    def __init__(self, inputs, outputs, gates):
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates

    def load_gates(self, gates_data):
        for gate_id, gate_info in gates_data.items():
            gate = Gate(
                gate_id,
                gate_info["type"],
                gate_info["inputs"],
                gate_info["output"]
            )
            self.gates.append(gate)

    def __str__(self):
        gates_str = "\n".join(str(gate) for gate in self.gates)
        return f"Inputs: {self.inputs}, \nOutputs: {self.outputs}\nGates:\n{gates_str}"


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
