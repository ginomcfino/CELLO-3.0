# Python default libraries
import subprocess
import os

# User Settings
in_path = "../../IO/inputs"
out_path = "../../IO/temp_folder"
verilog = input("_____.v? ")

v_backup = 'g77_boolean_modified_out81'
vpath = os.path.join(in_path, (verilog + '.v'))
if not os.path.isfile(vpath):
    verilog = v_backup
    

# Run YOSYS to produce Restricted Graph
command = f'yosys -p "read_verilog {in_path}/{verilog}.v; \
        flatten; \
        splitnets -ports; \
        hierarchy -auto-top; \
        proc; \
        techmap; \
        opt; \
        abc -g NOR; \
        opt; \
        hierarchy -auto-top; \
        opt_clean -purge; \
        show -format pdf -prefix {out_path}/{verilog}_yosys; \
        write_edif {out_path}/{verilog}.edif; \
        write_json {out_path}/{verilog}.json"'

subprocess.call(command, shell=True)