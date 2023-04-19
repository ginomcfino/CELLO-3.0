import json
from logic_synthesis import *
from netlist_class import Netlist
from ucf_class import UCF
import sys
sys.path.insert(0, 'utils/')  # links the utils folder to the search path
from cello_helpers import *
from gate_assignment import *

# first, run Yosys to produce RG
# second, check that the RG netlist is supported (only NOR + NOT gates, for now)
# map gates from ucf to netlist using algorithm
# use Eugene to help produce final SBOL output

# CELLO arguments:
# 1. verilog name
# 2. ucf name (could be optional)
# 3. path-to-verilog-and-ucf
# 4. path-for-output
# 5. options (optional)

# NOTE: if verilog has multiple outputs, SC1C1G1T1 is the only UCF with 2 output devices, 
# therefore so far it is the only one that will work for 2-output circuits
# TODO: need MORE UCFs
# NOTE: To fully utilize the algorithm of Cello v3, built to support multi-output circuits, make more UCFs


class CELLO3:
    def __init__(self, vname, ucfname, inpath, outpath, options=None):
        if options is not None:
            yosys_cmd_choice = options['yosys_choice']
        else:
            yosys_cmd_choice = 1
        self.inpath = inpath
        self.outpath = outpath
        self.vrlgname = vname
        self.ucfname = ucfname
        print_centered(['CELLO V3', self.vrlgname + ' + ' + self.ucfname], padding=True)
        try:
            call_YOSYS(inpath, outpath, vname, yosys_cmd_choice) # yosys command set 1 seems to work best after trial & error
        except Exception as e:
            debug_print(f'YOSYS output for {vname} already exists... skipping')
            print(e)
        # initialize UCF from file
        self.ucf = UCF(inpath, ucfname)
        # initialize RG from netlist JSON output from Yosys
        self.rnl = self.__load_netlist()
        
    def __load_netlist(self):
        netpath = self.outpath + '/' + self.vrlgname + '/' + self.vrlgname + '.json'
        netfile = open(netpath, 'r')
        netjson = json.load(netfile)
        netlist = Netlist(netjson)
        if not netlist.is_valid_netlist():
            return None
        return netlist
    
    def check_conditions(self, verbose=True):
        if verbose: print()
        if verbose: print_centered('condition checks for valid input')
        
        if verbose: print('\nNETLIST:')
        netlist_valid = False
        if self.rnl is not None:
            netlist_valid = self.rnl.is_valid_netlist()
        if verbose: print(f'isvalid: {netlist_valid}')

        num_ucf_input_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'input_sensors'))
        num_ucf_input_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'structures'))
        num_ucf_input_models = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'models'))
        num_ucf_input_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'parts'))
        num_netlist_inputs = len(self.rnl.inputs) if netlist_valid else 99999
        if verbose: print('\nINPUTS:')
        if verbose: print(f'num IN-SENSORS in {ucfname} in-UCF: {num_ucf_input_sensors}')
        if verbose: print(f'num IN-STRUCTURES in {ucfname} in-UCF: {num_ucf_input_structures}')
        if verbose: print(f'num IN-MODELS in {ucfname} in-UCF: {num_ucf_input_models}')
        if verbose: print(f'num IN-PARTS in {ucfname} in-UCF: {num_ucf_input_parts}')
        if verbose: print(f'num IN-NODES in {vname} netlist: {num_netlist_inputs}')
        inputs_match = (num_ucf_input_sensors == num_ucf_input_models == num_ucf_input_structures == num_ucf_input_parts) and (num_ucf_input_parts >= num_netlist_inputs)
        if verbose: print(('Valid' if inputs_match else 'NOT valid') + ' input match!')
        
        num_ucf_output_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'output_devices'))
        num_ucf_output_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'structures'))
        num_ucf_output_models = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'models'))
        num_ucf_output_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'parts'))
        num_netlist_outputs = len(self.rnl.outputs) if netlist_valid else 99999
        if verbose: print('\nOUTPUTS:')
        if verbose: print(f'num OUT-SENSORS in {ucfname} out-UCF: {num_ucf_output_sensors}')
        if verbose: print(f'num OUT-STRUCTURES in {ucfname} out-UCF: {num_ucf_output_structures}')
        if verbose: print(f'num OUT-MODELS in {ucfname} out-UCF: {num_ucf_output_models}')
        if verbose: print(f'num OUT-PARTS in {ucfname} out-UCF: {num_ucf_output_parts}')
        if verbose: print(f'num OUT-NODES in {vname} netlist: {num_netlist_outputs}')
        outputs_match = (num_ucf_output_sensors == num_ucf_output_models == num_ucf_output_parts == num_ucf_output_structures) and (num_ucf_output_parts >= num_netlist_outputs)
        if verbose: print(('Valid' if outputs_match else 'NOT valid') + ' output match!')
        
        numStructs = self.ucf.collection_count['structures']
        numModels = self.ucf.collection_count['models']
        numGates = self.ucf.collection_count['gates']
        # numParts = self.ucf.collection_count['parts']
        # numFunctions = len(self.ucf.query_top_level_collection(self.ucf.UCFmain, 'functions'))
        if verbose: print('\nGATES:')
        # if verbose: print(f'num PARTS in {ucfname} UCF: {numParts}')
        # if verbose: print(f'(ref only) num FUNCTIONS in {ucfname} UCF: {numFunctions}')
        if verbose: print(f'num STRUCTURES in {ucfname} UCF: {numStructs}')
        if verbose: print(f'num MODELS in {ucfname} UCF: {numModels}')
        if verbose: print(f'num GATES in {ucfname} UCF: {numGates}')
        
        num_gates_availabe = []
        logic_constraints = self.ucf.query_top_level_collection(self.ucf.UCFmain, 'logic_constraints')
        for l in logic_constraints:
            for g in l['available_gates']:
                num_gates_availabe.append(g['max_instances'])
        if verbose: print(f'num GATE USES: {num_gates_availabe}')
        num_netlist_gates = len(self.rnl.gates) if netlist_valid else 99999
        if verbose: print(f'num GATES in {vname} netlist: {num_netlist_gates}')
        gates_match = (numStructs == numModels == numGates) and (numGates >= num_netlist_gates)
        if verbose: print(('Valid' if gates_match else 'NOT valid') + ' intermediate match!\n')
        
        return netlist_valid and inputs_match and outputs_match and gates_match
                
    # NOTE: execution of the CELLO gate assignment simulation & optimization algorithm
    def evaluate(self):
        print_centered('Beginning GATE ASSIGNMENT', padding=True)
        # print(json.dumps(self.rnl.gates, indent=4))
        
        circuit = Graph(self.rnl.inputs, self.rnl.outputs, [])
        
        print()
        print(self.rnl.inputs)
        print(self.rnl.outputs)
        print(self.rnl.gates)
        print()
        
        circuit.load_gates(self.rnl.gates)
        
        debug_print('netlist de-construction')
        print(circuit)
        # print()
        G = circuit.to_networkx()
        visualize_logic_circuit(G, preview=False, outfile=f'{self.outpath}/{self.vrlgname}/techmap_preview.png')
        # save_circuit_graph(G, f'{self.outpath}/{self.vrlgname}/techmap_preview.png')
        print()
        
        # TODO: under development - assign gates and optimized
        debug_print('listing all input_sensor permutations')
        input_sensor_assignments = circuit.assign_inputs(self.ucf) # 
        for g in input_sensor_assignments:
            print(g)
            
        debug_print('listing all gate permutations')
        new_gate_assignments = circuit.assign_gates(self.ucf) # 
        for g in new_gate_assignments:
            print(str(g))
            
        debug_print('listing all output_devicce permutations')
        output_device_permutations = circuit.assign_outputs(self.ucf) # 
        for g in output_device_permutations:
            print(g)
            
        # TODO: now try the permutations of gates and try to predict circuit score from assignments 
        best_score = self.gate_assignment_algorithm(input_sensor_assignments, output_device_permutations, new_gate_assignments)
            
        print_centered('End of GATE ASSIGNMENT', padding=True)
        return 0
    
    def gate_assignment_algorithm(self, I, O, G):
        # (I know, why so convuluted?)
        # TODO: refactor redundant code
        # print(I, O, G)
        print()
        print(self.__IO_permu_sorter(I))
        print(self.__IO_permu_sorter(O))
        print()
        return -1
    
    def __IO_permu_sorter(self, IO_list):
        ids = list(set([g[1] for g in IO_list]))
        IO_dict = {id: [] for id in ids}
        for g in IO_list:
            IO_dict[g[1]].append(g[0])
        return IO_dict
            

if __name__ == '__main__':
    # vname = 'priorityDetector'
    vname = 'chat_3x2'
    ucfname = 'SC1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    
    Cello3Process = CELLO3(vname, ucfname, inpath, outpath, options={'yosys_choice': 1})
    
    pass_check = Cello3Process.check_conditions(verbose=True)
    print(f'Condition check passed? {pass_check}\n')
    
    if pass_check:
        Cello3Process.evaluate()