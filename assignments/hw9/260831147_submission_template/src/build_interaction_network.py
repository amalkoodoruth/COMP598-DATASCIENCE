import argparse
import pandas as pd
import numpy as np
import networkx as nx
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input csv', required=True)
parser.add_argument('-o', help='Output json', required=True)
args = parser.parse_args()

def main():
    out_dir, file_name = os.path.split(args.o)
    # if directory does not exist, create it
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(args.i, 'r') as f:
        data = pd.read_csv(f)
    data['pony'] = data['pony'].str.lower()
    data = data[['title', 'pony']]

    find_illegal(data)


    G = build_graph(data)

    info = extract_info(G)

    with open(args.o, 'w') as f:
        json.dump(info, f, indent=4)


    return 0

def extract_info(G):
    info = {}
    for n, nbrs in G.adj.items():
        nested_info = {}
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            nested_info[nbr] = wt
        info[n] = nested_info

    return info


def build_graph(data):
    G = nx.Graph()
    most_freq = get_most_freq(data, 101)
    for index, row in data.iterrows():
        pony1 = row['pony']
        # check if pony1 in most frequent and not last
        if pony1 in most_freq and index != data.shape[0] - 1:
        # if yes, check if next is in most frequent and not the same
            pony2 = data.iloc[index + 1]['pony']
            if pony2 in most_freq and pony2 != pony1:
        # if yes, check if episode is the same
                if row['title'] == data.iloc[index+1]['title']:
                    # if edge exists, increment weight, else, create edge
                    if G.has_edge(pony1, pony2):
                        G[pony1][pony2]['weight'] += 1
                    else:
                        G.add_edge(pony1, pony2, weight=1)

    return G
    # for index, row in data.iterrows():

def get_most_freq(data, n):
    col = data['pony']
    val_count = list(col.value_counts().keys())
    # remove "illegal"
    val_count.remove('illegal')
    return val_count[0:n]

def find_illegal(data):
    illegal_names = ['others', 'ponies', 'and', 'all']
    for index, row in data.iterrows():

        for word in row['pony'].split():
            if word in illegal_names:
                row['pony'] = row['pony'].replace(row['pony'], "illegal")

if __name__ == '__main__':
    main()