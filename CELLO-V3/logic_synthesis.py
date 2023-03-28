# Python default libraries
import subprocess
import os
import datetime


def make_RG(in_path=None, out_path=None, verilog=None, choice=0):
    # User Settings
    if in_path is None or out_path is None or verilog is None:
        in_path = input("ex: ../../IO/inputs\n")
        out_path = input("ex: ../../IO/temp_folder\n")
        verilog = input("ex: example.v\n")
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    new_folder_name = f"{verilog}_{timestamp}"
    new_folder_path = os.path.join(out_path, new_folder_name)
    os.makedirs(new_folder_path)
    out_path = new_folder_path

    vpath = os.path.join(in_path, verilog)
    if not os.path.isfile(vpath):
        print(f"ERROR finding {verilog}, please check verilog input.")
        return

    try:
        verilog_location = verilog.split('/')
        if len(verilog_location) > 1:
            verilog = verilog_location[-1]
            in_path += '/' + verilog_location[0]
    except Exception as e:
        print('Error\n' + str(e))

    # Run YOSYS to produce Restricted Graph
    # command = f'yosys -p "read_verilog {in_path}/{verilog}; \
    #         flatten; \
    #         splitnets -ports; \
    #         hierarchy -auto-top; \
    #         proc; \
    #         techmap; \
    #         opt; \
    #         abc -g NOR; \
    #         opt; \
    #         hierarchy -auto-top; \
    #         opt_clean -purge; \
    #         show -format pdf -prefix {out_path}/{verilog}_yosys; \
    #         write_edif {out_path}/{verilog}.edif; \
    #         write_json {out_path}/{verilog}.json"'

    command_start = ["read_verilog {}/{};".format(in_path, verilog)]

    command_end = [
        "show -format pdf -prefix {}/{}_yosys;".format(out_path, verilog),
        "write_edif {}/{}.edif;".format(out_path, verilog),
        "write_json {}/{}.json;".format(out_path, verilog)
    ]

    core_commands = [
        [
            # Old Cello Yosys commands
            "flatten",
            "splitnets -ports",
            "hierarchy -auto-top",
            "proc",
            "techmap",
            "opt",
            "abc -g NOR",
            "opt",
            "hierarchy -auto-top",
            "opt_clean -purge",
        ],
        [
            # JAI's MD5 Yosys commands
            'splitnets',
            'hierarchy -top',
            'flatten',
            'proc',
            'opt -full',
            'memory',
            'opt -full',
            'fsm'
            'opt -full',
            'techmap',
            'opt -full',
            'abc -g NOR',
            'splitnets -ports',
            'opt -full',
            'opt_clean',
            'clean -purge',
            'flatten'
        ],
        [
            # slightly optimized Yosys commands
            'hierarchy -check',
            'proc',
            'techmap',
            'opt',
            'abc -g NOR',
            'opt',
            'clean',
        ]
    ]
    
    try:
        commands = command_start + core_commands[choice] + command_end
        command = f"yosys -p \"{'; '.join(commands)}\""
        subprocess.call(command, shell=True)
    except Exception as e:
        print("Error\n" + str(e))
