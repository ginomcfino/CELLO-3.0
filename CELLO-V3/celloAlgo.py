from ucf_class import UCF
from netlist_class import Netlist
from logic_synthesis import *
from utils import *
import networkx as nx
import json

# first, run Yosys to produce RG
# second, check that the RG netlist is supported (only NOR + NOT gates, for now)
# map gates from ucf to netlist using algorithm
# use Eugene to help produce final SBOL output

# CELLO arguments:
# 1. verilog name
# 2. ucf name
# 3. path-to-verilog-and-ucf
# 4. path-for-output
# 5. options, optional
class CELLO3:
    def __init__(self, vname, ucfname, inpath, outpath):
        try:
            call_YOSYS(inpath, outpath, vname, 1)
        except Exception as e:
            print(f'YOSYS output for {vname} already exists... skipping')
            print(e)
            
        self.ucf = UCF(inpath, ucfname)
        print(f'GATES in {ucfname} UCF: {self.ucf.numGates}')
        self.rnl = self.__load_netlist(vname, outpath)
        
    def __load_netlist(self, vname, outpath):
        netpath = outpath + '/' + vname + '/' + vname + '.json'
        netfile = open(netpath, 'r')
        netjson = json.load(netfile)
        netlist = Netlist(netjson)
        return netlist
        
        
if __name__ == '__main__':
    vname = 'g92_boolean'
    ucfname = 'Eco1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    newCello3Process = CELLO3(vname, ucfname, inpath, outpath)
    
    
# logger.info("\n");
# logger.info("///////////////////////////////////////////////////////////");
# logger.info("///////////////   Welcome to Cello   //////////////////////");
# logger.info("///////////////////////////////////////////////////////////\n");