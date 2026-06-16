import argparse
from cpuElems import CPU
from parser import ParseCode
import pandas as pd

def main():

    parser = argparse.ArgumentParser(description='CPU Emulator')
    parser.add_argument('--code', action="store", dest='input_code')
    parser.add_argument('--const', action="store", dest='input_constants')
    parser.add_argument('--instr', action="store", dest='input_data_stream')
    parser.add_argument('--output', action="store", dest='output_data_stream')
    args = parser.parse_args()
    print(args.input_code)

    constants = [1024, 3072, 5120, 7168, 7168, 5120, 3072, 1024]
    constants += [0 for i in range(24)]
    #print(constants)
    vals = [0 for i in range(32)]
    cpu = CPU(constants, vals)

    history = []

    code = ParseCode(args.input_code)

    for tick in range(10):
        vals = [0 for i in range(32)]
        if(tick == 1):
            vals[0] = 32768
        print(vals)
        cpu.inputValues(vals)
        for i in code:
            cpu.step(i)


    history = cpu.Dump()

    #print(history)

    if history:
        column_names = [f"REG_{i}" for i in range(32)]
        df = pd.DataFrame(history, columns=column_names)
        df.index.name = 'Tick'
        output_filename = "register_dump.csv"   
        df.to_csv(output_filename, sep=';')
    
      

if __name__ == "__main__":
    main()
        
