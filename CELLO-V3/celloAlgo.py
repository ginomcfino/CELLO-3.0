import json
from logic_synthesis import *
from netlist_class import Netlist
from ucf_class import UCF
import sys
sys.path.insert(0, 'utils/')  # links the utils folder to the search path
from cello_helpers import *

# first, run Yosys to produce RG
# second, check that the RG netlist is supported (only NOR + NOT gates, for now)
# map gates from ucf to netlist using algorithm
# use Eugene to help produce final SBOL output

# CELLO arguments:
# 1. verilog name
# 2. ucf name (could be not included)
# 3. path-to-verilog-and-ucf
# 4. path-for-output
# 5. options (optional)


class CELLO3:
    def __init__(self, vname, ucfname, inpath, outpath, options=None):
        self.inpath = inpath
        self.outpath = outpath
        self.vrlgname = vname
        self.ucfname = ucfname
        print_centered(['CELLO V3', self.vrlgname + ' + ' + self.ucfname], padding=True)
        try:
            call_YOSYS(inpath, outpath, vname, 1)
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
        return netlist
    
    def check_conditions(self, verbose=True):
        if verbose: print()
        if verbose: print_centered('condition checks for valid input')
        
        num_ucf_input_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'input_sensors'))
        num_ucf_input_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'structures'))
        num_ucf_input_models = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'models'))
        num_ucf_input_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'parts'))
        if verbose: print('\nINPUTS:')
        if verbose: print(f'num IN-SENSORS in {ucfname} in-UCF: {num_ucf_input_sensors}')
        if verbose: print(f'num IN-STRUCTURES in {ucfname} in-UCF: {num_ucf_input_structures}')
        if verbose: print(f'num IN-MODELS in {ucfname} in-UCF: {num_ucf_input_models}')
        if verbose: print(f'num IN-PARTS in {ucfname} in-UCF: {num_ucf_input_parts}')
        if verbose: print(f'num IN-NODES in {vname} netlist: {len(self.rnl.inputs)}')
        inputs_match = (num_ucf_input_sensors == num_ucf_input_models == num_ucf_input_structures == num_ucf_input_parts) and (num_ucf_input_parts >= len(self.rnl.inputs))
        if verbose: print(('Valid' if inputs_match else 'NOT valid') + ' input match!')
        
        num_ucf_output_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'output_devices'))
        num_ucf_output_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'structures'))
        num_ucf_output_models = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'models'))
        num_ucf_output_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'parts'))
        if verbose: print('\nOUTPUTS:')
        if verbose: print(f'num OUT-SENSORS in {ucfname} out-UCF: {num_ucf_output_sensors}')
        if verbose: print(f'num OUT-STRUCTURES in {ucfname} out-UCF: {num_ucf_output_structures}')
        if verbose: print(f'num OUT-MODELS in {ucfname} out-UCF: {num_ucf_output_models}')
        if verbose: print(f'num OUT-PARTS in {ucfname} out-UCF: {num_ucf_output_parts}')
        if verbose: print(f'num OUT-NODES in {vname} netlist: {len(self.rnl.outputs)}')
        outputs_match = (num_ucf_output_sensors == num_ucf_output_models == num_ucf_output_parts == num_ucf_output_structures) and (num_ucf_output_parts >= len(self.rnl.outputs))
        if verbose: print(('Valid' if outputs_match else 'NOT valid') + ' output match!')
        
        numStructs = self.ucf.collection_count['structures']
        numModels = self.ucf.collection_count['gates']
        numGates = self.ucf.collection_count['gates']
        if verbose: print('\nGATES:')
        if verbose: print(f'num STRUCTURES in {ucfname} UCF: {numStructs}')
        if verbose: print(f'num MODELS in {ucfname} UCF: {numModels}')
        if verbose: print(f'num GATES in {ucfname} UCF: {numGates}')
        if verbose: print(f'num GATES in {vname} netlist: {len(self.rnl.gates)}')
        gates_match = (numStructs == numModels == numGates) and (numGates >= len(self.rnl.gates))
        if verbose: print(('Valid' if gates_match else 'NOT valid') + ' intermediate match!\n')
        
        if verbose: print('NETLIST:')
        netlist_valid = self.rnl.is_valid_netlist()
        if verbose: print(f'isvalid: {netlist_valid}\n')
        
        return netlist_valid and inputs_match and outputs_match and gates_match
                
    # NOTE: execution of the CELLO gate assignment simulation & optimization algorithm
    def evaluate(self):
        graph = Graph(self.rnl.inputs, self.rnl.outputs, [])
        graph.load_gates(self.rnl.gates)
        print(graph)
        return 0

if __name__ == '__main__':
    vname = 'priorityDetector'
    ucfname = 'SC1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    Cello3Process = CELLO3(vname, ucfname, inpath, outpath)
    pass_check = Cello3Process.check_conditions()
    print(f'Condition check passed? {pass_check}\n')
    if pass_check:
        Cello3Process.evaluate()