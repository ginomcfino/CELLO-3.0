# import networkx as nx
# import matplotlib.pyplot as plt
from ucf_class import *
    
class IO:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __lt__(self, other):
        if isinstance(other, IO):
            return self.id < other.id
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, IO):
            return self.id == other.id
        return NotImplemented

    def __repr__(self):
        return f'{self.name}'

class Input(IO):
    def __init__(self, name, id, function=None, function_parameters=[{}]):
        super().__init__(name, id)
        # TODO: implementation-in-progress
        if function is not None:
            self.func = function
            self.fun_params = function_parameters
    
    def __str__(self):
        return f'{self.name} input {self.id}'

class Output(IO):
    def __str__(self):
        return f'{self.name} output {self.id}'
    
    
class Gate:
    # NOTE: used to represent a gate in a netlist
    def __init__(self, gate_id, gate_type, inputs, output):
        self.gate_id = gate_id
        self.gate_type = gate_type
        self.inputs = inputs if type(inputs) == list else list(inputs.values()) # each gate can have up to 2 inputs
        self.output = output if type(output) == int else list(output.values())[0] # each gate can have only 1 output
        self.uid = ','.join(str(i) for i in self.inputs) + '-' + str(self.output)
    
    def __str__(self):
        return f'{self.gate_type} gate {self.gate_id} w/ inputs {self.inputs} and output {self.output}'
    
    def __repr__(self):
        return f'{self.gate_id}'
    
    def __lt__(self, other):
        if isinstance(other, Gate):
            return self.gate_id < other.gate_id
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Gate):
            return (self.inputs == other.inputs) and (self.output == other.output)
        return NotImplemented
    
    def __hash__(self):
        return hash((tuple(self.inputs), self.output))

class AssignGraph:
    def __init__(self, inputs=[], outputs=[], gates=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        
    def add_input(self, input):
        self.inputs.append(input)
        
    def add_output(self, output):
        self.outputs.append(output)
        
    def add_gate(self, gate):
        self.gates.append(gate)
        
    def remove_gate(self, gate):
        self.gates.remove(gate)
        
    def remove_input(self, input):
        self.inputs.remove(input)
        
    def remove_output(self, output):
        self.outputs.remove(output)
        
    def __repr__(self):
        return f"Inputs: {self.inputs}, Outputs: {self.outputs}, Gates: {self.gates}"

# NOTE: used to initialize all permuations of gate assignments from UCF to netlist
class GraphParser:
    def __init__(self, inputs, outputs, gates):
        self.inputs = self.load_inputs(inputs)
        self.outputs = self.load_outputs(outputs)
        self.gates = self.load_gates(gates)
        
    def load_inputs(self, in_data):
        inputs = []
        for (name, id) in in_data:
            inputs.append(Input(name, id))
        return inputs
    
    def load_outputs(self, out_data):
        outputs = []
        for (name, id) in out_data:
            outputs.append(Output(name, id))
        return outputs

    def load_gates(self, gates_data):
        gates = []
        for gate_id, gate_info in gates_data.items():
            gate = Gate(gate_id, gate_info["type"], gate_info["inputs"], gate_info["output"])
            gates.append(gate)
        return gates
            
    def permute_inputs(self, UCFobj: UCF):
        # return the different input combo permutations
        input_sensors = UCFobj.query_top_level_collection(UCFobj.UCFin, 'input_sensors')
        new_inputs = []
        for (_, edge_no) in self.inputs:
            for sensor in input_sensors:
                sensor_name = sensor['name']
                new_inputs.append((sensor_name, edge_no))
        return new_inputs
    
    def permute_outputs(self, UCFobj: UCF):
        # return the different input combo permutations
        output_devices = UCFobj.query_top_level_collection(UCFobj.UCFout, 'output_devices')
        new_outputs = []
        for (_, edge_no) in self.outputs:
            for device in output_devices:
                device_name = device['name']
                new_outputs.append((device_name, edge_no))
        return new_outputs        
    
    def permute_gates(self, UCFobj: UCF):
        ucf_gates = UCFobj.query_top_level_collection(UCFobj.UCFmain, 'gates')
        new_gates = []
        for g in self.gates:
            for ug in ucf_gates:
                new_gates.append(Gate(ug['name'], ug['gate_type'], g.inputs, g.output))
        uids = list(set([g.uid for g in new_gates]))
        # print(uids)
        gate_dict = {id: [] for id in uids}
        for g in new_gates:
            gate_dict[g.uid].append(g)
        return new_gates, gate_dict
    
    def traverse_graph(self, start_node):
        # traverse the graph and assign gates to each node
        return 0 #return 0 exit code
    
    # NOTE: Scrapped for weight-reduction
    # def to_networkx(self):
    #     G = nx.DiGraph()

    #     # Add input and output nodes to the graph
    #     for (input_node, no) in self.inputs:
    #         G.add_node(no, type='input')

    #     # Add gate nodes and edges to the graph
    #     for gate in self.gates:
    #         gate_name = f'{gate.gate_type}{gate.gate_id}'
    #         G.add_node(gate_name, type=gate.gate_type)
    #         for input_node in gate.inputs:
    #             G.add_edge(input_node, gate_name)
    #         G.add_node(gate.output, type='output')
    #         G.add_edge(gate_name, gate.output)
            

        return G
            
    def __str__(self):
        gates_str = "\n".join(str(gate) for gate in self.gates)
        return f"Inputs: {self.inputs},\n\nOutputs: {self.outputs}\n\nGates:\n{gates_str}"
    
# NOTE: Scrapped for weight reduction
# def visualize_logic_circuit(G, preview=True, outfile=None):
#     if not preview: plt.figure()
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

#     nx.draw_networkx_nodes(G, pos, nodelist=input_nodes, node_color="green", node_shape="o")
#     nx.draw_networkx_nodes(G, pos, nodelist=output_nodes, node_color="red", node_shape="o")
#     nx.draw_networkx_nodes(G, pos, nodelist=gate_nodes, node_shape="s")

#     # Draw edges with arrows and labels
#     edge_opts = {
#         "arrowsize": 20,      # Set the size of the arrowhead
#         "arrowstyle": "-|>",  # Set the style of the arrowhead
#     }
#     nx.draw_networkx_edges(G, pos, arrows=True)  # Add 'arrows=True' to draw arrows for the edges
#     nx.draw_networkx_labels(G, pos)

#     plt.axis("off")
#     if preview: 
#         plt.show()
#     else:
#         plt.savefig(outfile)
#         plt.close()