"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
file to run the performance test on similarity tool"""
import os
import sys
import time
import lipsum
import pandas as pd
from subprocess_calls import call_subprocess


def create_input():
    """ Function used to generate the input file to do the performance test"""
    row_size = 5  # given row size = 10 will generate around 17,000 rows of data in the excel file generated.
    data = []
    for __ in range(row_size):
        data.extend(lipsum.paras(150, True).split('.'))
    dataf = pd.DataFrame(data, columns=['Steps'])
    dataf.index.name = 'Uniq ID'
    dataf.to_excel(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "input_data.xlsx"))
    print("successfully created the input file")


def validate_perfo(time_val, input_data, t_val):
    """ Function to validate the performance of tool"""
    if not time_val < t_val * int(input_data):
        print("The performance is degraded")
        sys.exit(1)
    print("performance test is COMPLETED & PASSED")


def run_performance_test(time_perf):
    """ Function used to run the test to check how much time similarity tool takes to execute"""
    input_file = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "input_data.xlsx")
    input_count = get_last_line_file(input_file)
    if not os.path.exists(input_file):
        print("input file is not generated")
        sys.exit(1)
    time0 = time.time()
    call_subprocess('python3 -m similarity_processor.similarity_cmd --p "%s" --u 0 --c "1"' % input_file)
    time1 = time.time()
    execution_time = time1 - time0
    out_file = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "input_data_recommendation.csv")
    out_count = get_last_line_file(out_file)
    print("Total time taken to analyse %s input data is %s sec and generated %s combination match " % (input_count,
                                                                                                       execution_time,
                                                                                                       out_count))
    file_out = open(os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))), "perfo.txt"), 'w')
    file_out.write(
        "Total time taken to analyse %s input data is %s sec Vs bench mark %s sec and generated %s combination match "
        % (input_count, execution_time, (time_perf * input_count), out_count))
    file_out.close()
    validate_perfo(execution_time, input_count, time_perf)


def get_last_line_file(file):
    """ Function used to fetch last index from input and out put file to estimate how much time tool could take"""
    function_dict = {
        "XLSX": lambda x: pd.read_excel(file),
        "CSV": lambda x: pd.read_csv(file)
    }
    data_frame = function_dict[file.split('.')[-1].upper()](file)
    if data_frame.empty:
        print("DataFrame is empty!/ input file is not generated")
    return data_frame.index[-1]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("input argument is missing for the performance test. please provide input in seconds as a float value")
        sys.exit(1)
    try:
        COMP_PERF = float(sys.argv[1])
        print("Input is a float  number. Number = ", COMP_PERF)
    except ValueError:
        print("No.. input is not a number. It's a string")
        sys.exit(1)
    print("checking the tool performance ref: single comparison threshold is set to %s sec" % COMP_PERF)
    create_input()
    run_performance_test(COMP_PERF)
