import json
from logic_synthesis import *
from netlist_class import Netlist
from ucf_class import UCF
import sys
sys.path.insert(0, 'utils/')  # links the utils folder to the search path
from cello_helpers import *
from gate_assignment import *

# CELLO arguments:
# 1. verilog name
# 2. ucf name (could be made optional)
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
                
    # NOTE: POE of the CELLO gate assignment simulation & optimization algorithm
    def evaluate(self):
        print_centered('Beginning GATE ASSIGNMENT', padding=True)
        # print(json.dumps(self.rnl.gates, indent=4))
        
        # print()
        # print(self.rnl.inputs)
        # print(self.rnl.outputs)
        # print(self.rnl.gates)
        # print()
        
        circuit = GraphParser(self.rnl.inputs, self.rnl.outputs, [])
        circuit.load_gates(self.rnl.gates)
        
        debug_print('netlist de-construction')
        print(circuit)
        G = circuit.to_networkx()
        visualize_logic_circuit(G, preview=False, outfile=f'{self.outpath}/{self.vrlgname}/techmap_preview.png')
        print()
        
        in_sensors = self.ucf.query_top_level_collection(self.ucf.UCFin, 'input_sensors')
        I_list = []
        for sensor in in_sensors:
            I_list.append(sensor['name'])
        out_devices = self.ucf.query_top_level_collection(self.ucf.UCFout, 'output_devices')
        O_list = []
        for device in out_devices:
            O_list.append(device['name'])
        gates = self.ucf.query_top_level_collection(self.ucf.UCFmain, 'gates')
        G_list = []
        for gate in gates:
            # G_list.append((gate['name'], gate['gate_type']))
            G_list.append(gate['name'])
        
        print(I_list)
        print(O_list)
        print(G_list)
        i = len(self.rnl.inputs)
        o = len(self.rnl.outputs)
        g = len(self.rnl.gates)
        
        count = 0
        for I_comb in itertools.permutations(I_list, i):
            for O_comb in itertools.permutations(O_list, o):
                for G_comb in itertools.permutations(G_list, g):
                    # Check if inputs, outputs, and gates are unique and the correct number
                    if len(set(I_comb + O_comb + G_comb)) == i+o+g:
                        count += 1
                        # Output the combination
                        # print(f"Inputs: {I_comb}, Outputs: {O_comb}, Gates: {G_comb}")
        print(f'\nCOUNT: {count}')
        
        # TODO: under development - assign gates and optimized
        # debug_print('listing all input_sensor permutations')
        # input_sensor_assignments = circuit.permute_inputs(self.ucf) # 
        # for g in input_sensor_assignments:
        #     print(g)
            
        # debug_print('listing all gate permutations')
        # new_gate_assignments, gate_dict = circuit.permute_gates(self.ucf) # 
        # gates_for_iter = []
        # for g in new_gate_assignments:
        #     gates_for_iter.append((f'{g.gate_type} gate {g.gate_id}', g.inputs, g.output))
        #     print(str(g))
            
        # debug_print('listing all output_device permutations')
        # output_device_permutations = circuit.permute_outputs(self.ucf) # 
        # for g in output_device_permutations:
        #     print(g)
            
        # TODO: now try the permutations of gates and try to predict circuit score from assignments 
        # best_score = self.gate_assignment_algorithm(input_sensor_assignments, output_device_permutations, new_gate_assignments, gate_dict, self.ucf)
        
        # unique_combinations = generate_combinations(input_sensor_assignments, gates_for_iter, output_device_permutations)
        # debug_print(f'NUM ITERS: {len(unique_combinations)}')
        # for c in unique_combinations:
        #     print(c)
        
        print_centered('End of GATE ASSIGNMENT', padding=True)
        return 0
    
    # def evaluate_assignment(self, i, o, gates, ucf):
    #     # examples
    #     # i = ('LacI_sensor', 2)
    #     # o = ('YFP_reporter', 4)
    #     # gates = [Gate(class), ...] 
    #     # ucf = UCF(class)
    #     scores = []
    #     return max(scores)
    
    # def gate_assignment_algorithm(self, I, O, gates, G, ucf):
    #     # TODO: refactor code
    #     I_perm = self.__IO_permu_sorter(I)
    #     O_perm = self.__IO_permu_sorter(O)
    #     G_perm = G
    #     print()
    #     print(I_perm)
    #     print(O_perm)
    #     print(G_perm)
    #     print()
    #     # print(gates)
    #     # print()
    #     print(ucf)
    #     print()
        
    #     # TODO: keep working here
    #     i_inUse = None
    #     o_inUse = None
    #     g_inUse = None
    #     count = 0
    #     cur_assignment = AssignedGraph()
    #     for i_id, i_sensors in I_perm.items():
    #         for i_name in i_sensors:
    #             assign_i = (i_name, i_id)
                
    #             for o_id, o_devices in O_perm.items():
    #                 for o_name in o_devices:
    #                     assign_o = (o_name, o_id)
                        
    #                     # for g in gates:
    #                     count += 1
                        
    #         print(i_id)
            
    #     debug_print(f'GateAssignment Iterations: #{count}')
    #     return -1
    
    # def __IO_permu_sorter(self, IO_list):
    #     ids = list(set([g[1] for g in IO_list]))
    #     IO_dict = {id: [] for id in ids}
    #     for g in IO_list:
    #         IO_dict[g[1]].append(g[0])
    #     return IO_dict
    
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
        if verbose: print(('Valid' if gates_match else 'NOT valid') + ' intermediate match!')
        
        pass_check = netlist_valid and inputs_match and outputs_match and gates_match
        
        (max_iteratons, confirm) = permute_count_helper(num_netlist_inputs, num_netlist_outputs, num_netlist_gates, num_ucf_input_sensors, num_ucf_output_sensors, numGates) if pass_check else (None, None)
        if verbose: debug_print(f'#{max_iteratons} possible permutations for {self.vrlgname}.v+{self.ucfname}')
        if verbose: debug_print(f'#{confirm} PERMS confirmed.', padding=False)

        return pass_check
    
if __name__ == '__main__':
    # vname = 'priorityDetector'
    vname = 'xor'
    # ucflist = ['Bth1C1G1T1', 'Eco1C1G1T1', 'Eco1C2G2T2', 'Eco2C1G3T1', 'Eco2C1G5T1', 'Eco2C1G6T1', 'SC1C1G1T1']
    # problem_ucfs = ['Eco1C2G2T2', 'Eco2C1G6T1']
    ucfname = 'SC1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    
    Cello3Process = CELLO3(vname, ucfname, inpath, outpath, options={'yosys_choice': 1})
    
    pass_check = Cello3Process.check_conditions(verbose=True)
    print(f'\nCondition check passed? {pass_check}\n')
    
    if pass_check:
        Cello3Process.evaluate()