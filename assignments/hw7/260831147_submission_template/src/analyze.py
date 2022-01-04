import os
import argparse
import pandas as pd
import json

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input file', required=True)
parser.add_argument('-o', help='Output file', required=False)
args = parser.parse_args()

def main():

    if(args.o):
        out_file = args.o
        print_flag = False
        out_dir, file_name = os.path.split(args.o)
        # if directory does not exist, create it
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    else:
        print_flag = True

    path = os.getcwd()
    # input = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), args.i)
    input = args.i
    df = pd.read_csv(input, sep='\t')
    data = count(df)

    if print_flag:
        print(data)
    else:
        with open(out_file, 'w') as f:
            json.dump(data, f)

    return

def count(df):
    count_c = 0
    count_f = 0
    count_r = 0
    count_o = 0

    data = {}

    for _, row in df.iterrows():
        if row['coding'] == 'c':
            count_c += 1
        elif row['coding'] == 'f':
            count_f += 1
        elif row['coding'] == 'r':
            count_r += 1
        elif row['coding'] == 'o':
            count_o += 1

    data['course-related'] = count_c
    data['food_related'] = count_f
    data['residence-related'] = count_r
    data['other'] = count_o

    return data

if __name__ == "__main__":
    main()