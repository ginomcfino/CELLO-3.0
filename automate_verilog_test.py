from celloapi2 import CelloQuery, CelloResult
import os
import glob

in_dir = "/Users/jiweiqi/Work/Cello/IO/inputs"
out_dir = "/Users/jiweiqi/Work/Cello/IO/outputs"
log_path = "/home/weiqiji/Desktop/CIDARlab/CELLO/IO/logging"
chasse = ["Eco1C1G1T1", "Eco1C2G2T2", "Eco2C1g3T1", "Eco2C1g5T1", "Bth1C1G1T1", 'SC1C1G1T1']
options = "options.csv"

in_path = os.path.join(f"{in_dir}", '*')
in_contents = glob.glob(in_path)
v_files = list(
    filter(lambda x: x.endswith('.v'), in_contents)
)
for i in range(len(v_files)):
    v = v_files[i]
    v = v.split('/')[-1]
    v_files[i] = v


for verilog in v_files:
    for chassis_name in chasse:
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
        query.archive_prior_results(verilog.split('.')[0], chassis_name)
        # result = CelloResult(results_dir=out_dir)
        # print(f"{v} circuit score: ")
        print(f'{verilog} execution COMPLETE!')

query.archive_prior_results(verilog.split('.')[0])

print()