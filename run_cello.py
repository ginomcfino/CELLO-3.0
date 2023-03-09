from celloapi2 import CelloQuery, CelloResult

in_dir = "/home/weiqiji/Desktop/CIDARlab/CELLO/IO/inputs"
out_dir = "/home/weiqiji/Desktop/CIDARlab/CELLO/IO/single_outputs"

verilog = input("whats the verilog you want to test? ")
# verilog = "g5_boolean_modified.v"
if len(verilog) < 1:
    raise Exception
chasse = ["Eco1C1G1T1", "Eco1C2G2T2", "Eco2C1g3T1", "Eco2C1g5T1", "Bth1C1G1T1", 'SC1C1G1T1']
print(chasse)
chassis_name = input("which UCF to use? ")
if not chassis_name in chasse:
    chassis_name = "Eco1C1G1T1"
options = "options.csv"

in_ucf = f"{chassis_name}.UCF.json"
in_sensor_file = f"{chassis_name}.input.json"
out_device_file = f"{chassis_name}.output.json" 

query = CelloQuery(
    input_directory=in_dir, 
    output_directory=out_dir, 
    verilog_file=verilog, 
    compiler_options=options, 
    input_ucf=in_ucf, 
    input_sensors=in_sensor_file, 
    output_device=out_device_file,
    logging=True,
)

query.get_results()
result = CelloResult(results_dir=out_dir)
print(f"{verilog} circuit score: {result.circuit_score}\n")

# TODO: this part needs to be automated (or is it even necessary?)
# signals = query.set_input_signals(['LacI', 'TetR', 'AraC', 'LuxR'])
# print(signals)

def archive_lastrun_results(verilog_name, chassis_name):
    # empty_query = CelloQuery(None, None, None, None, None, None, None, False, True, False)
    verilog_name = verilog_name.split('.')[0]
    query.archive_prior_results(verilog_name, chassis_name)

archive_lastrun_results(verilog, chassis_name)

print('ALL-DONE!')