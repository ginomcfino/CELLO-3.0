'''
NETLIST class
input: netlist JSON from YOSYS output
(under development)
'''

class Netlist:
    def __init__(self, netlistJSON):
        net_main = netlistJSON['modules']
        self.name = list(net_main.keys())[0]
        ports = net_main[self.name]['ports']
        cells = net_main[self.name]['cells']
        edges = net_main[self.name]['netnames']
        i, o = self.__sort_nodes(ports)
        self.inputs = i
        self.outputs = o
        self.gates = self.__sort_gates(cells)
        self.edges = self.__check_edges(edges)
        
    def __sort_nodes(self, ports):
        in_nodes = []
        out_nodes = []
        for p in ports.keys():
            node_name = p
            direction = ports[p]['direction']
            bits = ports[p]['bits']
            node = (node_name, bits)
            if direction == 'input':
                in_nodes.append(node)
            elif direction == 'output':
                out_nodes.append(node)
            else:
                raise ValueError('Invalid [in/out]put node') 
        return (in_nodes, out_nodes)
    
    def __sort_gates(self, cells):
        gates = {}
        for c in cells.keys():
            partition = list(c.split('$'))
            gate_id = partition[-1]
            gate_type = cells[c]['type']
            gate = {gate_id : 
                    {
                     'type' : gate_type,
                     'inputs' : {},
                     'output' : {},
                    }
                   }
            dirns = cells[c]['port_directions']
            ctns = cells[c]['connections']
            inputs = []
            outputs = []
            for d in dirns.keys():
                inout = dirns[d]
                if inout == 'input':
                    inputs.append(d)
                else:
                    outputs.append(d)
            gate_inputs = []
            gate_outputs = []
            for c in ctns.keys():
                c_nodes = ctns[c]
                if c in inputs:
                    gate_inputs.append((c, c_nodes))
                else:
                    gate_outputs.append((c, c_nodes))
            for tup in gate_inputs:
                (node_name, edge_nos) = tup
                try:
                    gate[gate_id]['inputs'][node_name] += edge_nos
                except Exception as e:
                    gate[gate_id]['inputs'][node_name] = edge_nos
            for tup in gate_outputs:
                (node_name, edge_nos) = tup
                try:
                    gate[gate_id]['output'][node_name] += edge_nos
                except Exception as e:
                    gate[gate_id]['output'][node_name] = edge_nos
            #print(json.dumps(gate, indent=4))
            gates.update(gate)
        return gates
    
    def __str__(self):
        return (f"{self.name}: with \n"
                f"{len(self.inputs)} inputs,\n"
                f"{len(self.outputs)} ouputs.")
    
    def __check_edges(self, edges):
        for n in edges:
            pass
        return 9