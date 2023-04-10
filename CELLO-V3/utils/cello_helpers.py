import json
import networkx as nx
import matplotlib.pyplot as plt

class Gate:
    def __init__(self, gate_id, gate_type, inputs, output):
        self.gate_id = gate_id
        self.gate_type = gate_type
        self.inputs = list(inputs.values()) # each gate can have up to 2 inputs
        self.output = list(output.values())[0] # each gate can have only 1 output
    
    def __str__(self):
        return f'{self.gate_type} gate {self.gate_id} w/ inputs {self.inputs} and output {self.output}'

class Graph:
    def __init__(self, inputs, outputs, gates):
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates

    def load_gates(self, gates_data):
        for gate_id, gate_info in gates_data.items():
            gate = Gate(gate_id, gate_info["type"], gate_info["inputs"], gate_info["output"])
            self.gates.append(gate)
            
    def assign_inputs(self):
        # return the different input combo permutations
        pass
    
    def assign_outputs(self):
        # return the different output combo permutations
        pass            
            
    def traverse_graph(self, start_node):
        # traverse the graph and assign gates to each node
        return 0 #return 0 exit code
    
    def to_networkx(self):
        G = nx.DiGraph()

        # Add input and output nodes to the graph
        for (input_node, no) in self.inputs:
            G.add_node(no, type='input')

        # Add gate nodes and edges to the graph
        for gate in self.gates:
            gate_name = f'{gate.gate_type}{gate.gate_id}'
            G.add_node(gate_name, type=gate.gate_type)
            for input_node in gate.inputs:
                G.add_edge(input_node, gate_name)
            G.add_node(gate.output, type='output')
            G.add_edge(gate_name, gate.output)
            

        return G
            
    def __str__(self):
        gates_str = "\n".join(str(gate) for gate in self.gates)
        return f"Inputs: {self.inputs}, \nOutputs: {self.outputs}\nGates:\n{gates_str}"

# def draw_logic_circuit(G):
#     pos = nx.spring_layout(G, seed=42)  # Compute a layout for the nodes

#     for (n, d) in G.nodes(data=True):
#         print(n, d)
#     # Draw the different node types with different colors and shapes
#     input_nodes = [n for (n, d) in G.nodes(data=True) if d is not None and d['type'] == "input"]
#     output_nodes = [n for (n, d) in G.nodes(data=True) if d['type'] == "output"]
#     gate_nodes = [n for (n, d) in G.nodes(data=True) if d['type'] not in ["input", "output"]]

#     nx.draw_networkx_nodes(G, pos, nodelist=input_nodes, node_color="green", node_shape="s", node_size=1000)
#     nx.draw_networkx_nodes(G, pos, nodelist=output_nodes, node_color="red", node_shape="o", node_size=1000)
#     nx.draw_networkx_nodes(G, pos, nodelist=gate_nodes, node_color="blue", node_shape="h", node_size=1000)

#     # Draw edges and labels
#     nx.draw_networkx_edges(G, pos)
#     nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

#     plt.axis("off")
#     plt.show()

# def draw_logic_circuit(G):
#     # Compute the distances from input nodes
#     distances = {input_node: 0 for input_node, data in G.nodes(data=True) if data["type"] == "input"}

#     for input_node in list(distances.keys()):
#         for node, distance in nx.single_source_shortest_path_length(G, input_node).items():
#             distances[node] = max(distances.get(node, 0), distance)

#     # Create a custom layout that distributes nodes across layers
#     pos = {}
#     layer_counts = {}
#     for node, distance in distances.items():
#         layer_counts[distance] = layer_counts.get(distance, 0) + 1
#         pos[node] = (distance, -layer_counts[distance])

#     # Draw the different node types with different colors and shapes
#     input_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "input"]
#     output_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "output"]
#     gate_nodes = [n for n, d in G.nodes(data=True) if d["type"] not in ["input", "output"]]

#     nx.draw_networkx_nodes(G, pos, nodelist=input_nodes, node_color="green", node_shape="s", node_size=1000)
#     nx.draw_networkx_nodes(G, pos, nodelist=output_nodes, node_color="red", node_shape="o", node_size=1000)
#     nx.draw_networkx_nodes(G, pos, nodelist=gate_nodes, node_color="blue", node_shape="h", node_size=1000)

#     # Draw edges and labels
#     nx.draw_networkx_edges(G, pos, arrows=True)
#     nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

#     plt.axis("off")
#     plt.show()

def visualize_logic_circuit(G, preview=True, outfile=None):
    if not preview: plt.figure()
    # Compute the distances from input nodes
    distances = {input_node: 0 for input_node, data in G.nodes(data=True) if data["type"] == "input"}

    for input_node in list(distances.keys()):
        for node, distance in nx.single_source_shortest_path_length(G, input_node).items():
            distances[node] = max(distances.get(node, 0), distance)

    # Create a custom layout that distributes nodes across layers
    pos = {}
    layer_counts = {}
    for node, distance in distances.items():
        layer_counts[distance] = layer_counts.get(distance, 0) + 1
        pos[node] = (distance, -layer_counts[distance])

    # Draw the different node types with different colors and shapes
    input_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "input"]
    output_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "output"]
    gate_nodes = [n for n, d in G.nodes(data=True) if d["type"] not in ["input", "output"]]

    nx.draw_networkx_nodes(G, pos, nodelist=input_nodes, node_color="green", node_shape="o")
    nx.draw_networkx_nodes(G, pos, nodelist=output_nodes, node_color="red", node_shape="o")
    nx.draw_networkx_nodes(G, pos, nodelist=gate_nodes, node_shape="s")

    # Draw edges with arrows and labels
    edge_opts = {
        "arrowsize": 20,      # Set the size of the arrowhead
        "arrowstyle": "-|>",  # Set the style of the arrowhead
    }
    nx.draw_networkx_edges(G, pos, arrows=True)  # Add 'arrows=True' to draw arrows for the edges
    nx.draw_networkx_labels(G, pos)

    plt.axis("off")
    if preview: 
        plt.show()
    else:
        plt.savefig(outfile)
        plt.close()

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
