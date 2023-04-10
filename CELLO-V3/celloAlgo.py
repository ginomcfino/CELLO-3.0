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
        try:
            call_YOSYS(inpath, outpath, vname, 1)
        except Exception as e:
            print(f'YOSYS output for {vname} already exists... skipping')
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
    
    def __check_conditions(self):
        netlist_valid = self.rnl.is_valid_netlist()


    # helps you see what's going on
    def print_initialization(self):
        print_centered(['CELLO V3', self.vrlgname + ' + ' + self.ucfname], padding=True)
        print('\nINPUTS:')
        num_ucf_input_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'input_sensors'))
        num_ucf_input_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'structures'))
        num_ucf_input_models = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'models'))
        num_ucf_input_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFin, 'parts'))
        print(f'num IN-SENSORS in {ucfname} in-UCF: {num_ucf_input_sensors}')
        print(f'num IN-STRUCTURES in {ucfname} in-UCF: {num_ucf_input_structures}')
        print(f'num IN-MODELS in {ucfname} in-UCF: {num_ucf_input_models}')
        print(f'num IN-PARTS in {ucfname} in-UCF: {num_ucf_input_parts}')
        print(f'num IN-NODES in {vname} netlist: {len(self.rnl.inputs)}')
        # print(self.rnl.inputs)
        print(('Valid' if len(self.rnl.inputs) <=
              num_ucf_input_sensors else 'NOT valid') + ' input match!')
        print('\nOUTPUTS:')
        num_ucf_output_sensors = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'output_devices'))
        num_ucf_output_structures = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'structures'))
        num_ucf_output_models = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'models'))
        num_ucf_output_parts = len(self.ucf.query_top_level_collection(self.ucf.UCFout, 'parts'))
        print(f'num OUT-SENSORS in {ucfname} out-UCF: {num_ucf_output_sensors}')
        print(f'num OUT-STRUCTURES in {ucfname} out-UCF: {num_ucf_output_structures}')
        print(f'num OUT-MODELS in {ucfname} out-UCF: {num_ucf_output_models}')
        print(f'num OUT-PARTS in {ucfname} out-UCF: {num_ucf_output_parts}')
        print(f'num OUT-NODES in {vname} netlist: {len(self.rnl.outputs)}')
        # print(self.rnl.outputs)
        print(('Valid' if len(self.rnl.outputs) <=
              num_ucf_output_sensors else 'NOT valid') + ' output match!')
        print('\nGATES:')
        numStructs = self.ucf.collection_count['structures']
        print(f'num STRUCTURES in {ucfname} UCF: {numStructs}')
        numModels = self.ucf.collection_count['gates']
        print(f'num MODELS in {ucfname} UCF: {numModels}')
        numGates = self.ucf.collection_count['gates']
        print(f'num GATES in {ucfname} UCF: {numGates}')
        print(f'num GATES in {vname} netlist: {len(self.rnl.gates)}')
        print(('Valid' if len(self.rnl.gates) <=
              numGates else 'NOT valid') + ' intermediate match!')
        print('\nNetlist Check:')
        netlist_valid = self.rnl.is_valid_netlist()
        # netlist_gates = self.rnl.gates
        # print(json.dumps(netlist_gates, indent=4))
        # (GinOk, GoutOk) = self.rnl.check_gates_valid()
        print(netlist_valid)
        # print(('NO' if (GinOk and GoutOk) else 'CONTAINS') + ' multi-bit gates!')
        print()


if __name__ == '__main__':
    vname = 'g77_boolean'
    ucfname = 'SC1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    Cello3Process = CELLO3(vname, ucfname, inpath, outpath)
    Cello3Process.print_initialization()
