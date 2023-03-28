import sys
sys.path.insert(0, '../')  # Add parent directory to Python path
from logic_synthesis import *

# define path to folder containing verilogs
verilog_path = '../../../IO/inputs'
# define path to store YOSYS outputs for Restricted Graph & netlist
out_path = '../../../IO/temp_folder'

# find all verilogs in input folder
def find_verilogs(v_path):
    verilogs = []
    for root, dirs, files in os.walk(v_path):
        print(root)
        print(dirs)
        print()
        prefix = ''
        if root != v_path:
            prefix = root.split('/')[-1] + '/'
        for file in files:
            if file.endswith('.v'):
                verilogs.append(prefix+file)
    return verilogs

verilogs_to_test = find_verilogs(verilog_path)
print(verilogs_to_test)

for verilog in verilogs_to_test:
    try:
        make_RG(verilog_path, out_path, verilog, 2)
    except Exception as e:
        print('ERROR:\n' + str(e))