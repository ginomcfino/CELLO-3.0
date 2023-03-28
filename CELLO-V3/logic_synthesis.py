# Python default libraries
import subprocess
import os
import datetime


def call_YOSYS(in_path=None, out_path=None, vname=None, choice=0):
    print(in_path)
    print(out_path)
    print(vname)
    print(choice)
    print('---')
    try:
        new_out = os.path.join(out_path, vname)
        os.makedirs(new_out)
    except Exception as e:
        print("Error\n" + str(e))
        return
    print(new_out) # new out_path
    if '/' in vname:
        new_in = os.path.join(in_path, '/'.join(vname.split('/')[:-1]))
        vname = vname.split('/')[-1]
        print(new_in)
    else:
        new_in = in_path
    verilog = vname + '.v'
    print(verilog)
    print()
    # User Settings
    # if in_path is None or out_path is None or vname is None:
    #     in_path = input("ex: ../../IO/inputs\n")
    #     out_path = input("ex: ../../IO/temp_folder\n")
    #     vname = input("ex: ____.v?")
    # # timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # # new_folder_name = f"{verilog}_{timestamp}"
    # new_folder_path = os.path.join(out_path, vname)
    # os.makedirs(new_folder_path)
    # out_path = new_folder_path

    # verilog = vname + '.v'
    v_loc = os.path.join(new_in, verilog)
    if not os.path.isfile(v_loc):
        print(f"ERROR finding {verilog}, please check verilog input.")
        return

    # try:
    #     v_path = vname.split('/')
    #     if len(v_path) > 1:
    #         vname = vname[-1]
    #         in_path += '/' + v_path[0]
    # except Exception as e:
    #     print('Error\n' + str(e))

    command_start = ["read_verilog {}/{};".format(new_in, verilog)]

    command_end = [
        "show -format pdf -prefix {}/{}_yosys".format(new_out, vname),
        "write_verilog -noexpr {}/{}".format(new_out, 'struct_'+vname),
        "write_edif {}/{}.edif;".format(new_out, vname),
        "write_json {}/{}.json;".format(new_out, vname),
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
            'hierarchy -auto-top',
            'flatten',
            'proc',
            'opt -full',
            'memory',
            'opt -full',
            'fsm',
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
            # general application Yosys commands
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


# Example Yosys formatting
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
