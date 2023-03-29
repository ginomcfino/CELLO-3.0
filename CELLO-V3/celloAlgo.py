from UCFclass import UCF
from netlist import Netlist
from logic_synthesis import *
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
        call_YOSYS(inpath, outpath, vname, 1)
        self.ucf = UCF(inpath, ucfname)
        print(self.ucf.UCFin[0])
        print(self.ucf.UCFmain[0])
        print(self.ucf.UCFout[0])
        self.rgnl = self.__load_netlist(vname, outpath)
        print(self.rgnl.inputs)
        print(self.rgnl.outputs)
        print(self.rgnl.gates)
        print(self.rgnl.edges)
        print(self.rgnl.name)
        
    def __load_netlist(self, vname, outpath):
        netpath = outpath + '/' + vname + '/' + vname + '.json'
        netfile = open(netpath, 'r')
        netjson = json.load(netfile)
        netlist = Netlist(netjson)
        return netlist
        
        
if __name__ == '__main__':
    vname = 'md5Core'
    ucfname = 'Eco1C1G1T1'
    inpath = '../../IO/inputs'
    outpath = '../../IO/celloAlgoTest'
    newCello3Process = CELLO3(vname, ucfname, inpath, outpath)