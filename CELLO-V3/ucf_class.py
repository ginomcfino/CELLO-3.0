import os
import json

# Work in progress

class UCF:

    def __init__(self, filepath, name):
        (U, I, O) = self.__parse_helper(filepath, name)
        self.UCFmain = U
        self.UCFin = I
        self.UCFout = O
        self.numGates = self.__count_gates(self.UCFmain)
        
    def __count_gates(self, mainucf):
        internal_nodes = 0
        for c in mainucf:
            if c['collection'] == 'gates':
                internal_nodes += 1
        return internal_nodes

    def __parse_helper(self, filepath, name):
        U = os.path.join(filepath, name + '.UCF.json')
        I = os.path.join(filepath, name + '.input.json')
        O = os.path.join(filepath, name + '.output.json')
        paths = [U, I, O]
        out = []
        for f in paths:
            with open(f, 'r') as ucf:
                ucf = json.load(ucf)
                out.append(ucf)
        return tuple(out)

    def __str__(self):
        return json.dumps(self.UCFmain[0], indent=4) + '\n\n'+ \
            json.dumps(self.UCFin[0], indent=4) + '\n\n' + \
            json.dumps(self.UCFout[0], indent=4)

    def list_collection_prarmeters(self, cName):
        params = []
        for c in self.UCFmain:
            if c['collection'] == cName:
                params.append(list(c.keys()))
        params_set = set(tuple(x) for x in params)
        params = [list(x) for x in params_set]
        return params

    def query_top_level_collection(self, ucf, cName):
        matches = []
        for c in ucf:
            if c['collection'] == cName:
                matches.append(c)
        return matches

# testing the class
# ucf_path = '../../IO/inputs'
# test_ucf = 'Eco1C1G1T1'
# ucf = UCF(ucf_path, test_ucf)
# print(ucf)
