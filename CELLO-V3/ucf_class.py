import os
import json

# Work in progress

class UCF:

    def __init__(self, filepath, name):
        (U, I, O) = self.__parse_helper(filepath, name)
        self.UCFmain = U
        self.UCFin = I
        self.UCFout = O
        self.collection_count = {cName : self.__count_collection(cName) for cName in self.__collection_names(self.UCFmain)}
        
    def __count_collection(self, cName):
        internal_nodes = 0
        for c in self.UCFmain:
            if c['collection'] == cName:
                internal_nodes += 1
        return internal_nodes

    def __collection_names(self, UCFchoice):
        return list(set([c['collection'] for c in UCFchoice]))

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
        # print only the first indexed enumeration to test seeing
        return json.dumps(self.UCFmain[0], indent=4) + '\n\n'+ \
            json.dumps(self.UCFin[0], indent=4) + '\n\n' + \
            json.dumps(self.UCFout[0], indent=4)

    def list_collection_prarmeters(self, cName):
        # returns the list (set) of parameters found in a collection
        params = []
        for c in self.UCFmain:
            if c['collection'] == cName:
                params.append(list(c.keys()))
        params_set = set(tuple(x) for x in params)
        params = [list(x) for x in params_set]
        return params

    def query_top_level_collection(self, ucf, cName):
        # returns all collections with the of a name from the UCF
        matches = []
        for c in ucf:
            if c['collection'] == cName:
                matches.append(c)
        return matches
