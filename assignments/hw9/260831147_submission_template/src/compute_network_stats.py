import argparse
import json
import networkx as nx
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input json', required=True)
parser.add_argument('-o', help='Output json', required=True)
args = parser.parse_args()

def main():
    with open(args.i, 'r') as f:
        data = json.load(f)

    out_dir, file_name = os.path.split(args.o)
    # if directory does not exist, create it
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    top_num_edges = get_top_num_edges(data)
    top_total_weight = get_top_total_weight(data)
    top_betweenness = get_top_betweenness(data)

    out_dict = {}
    out_dict["most_connected_by_num"] = top_num_edges
    out_dict["most_connected_by_weight"] = top_total_weight
    out_dict["most_central_by_betweenness"] = top_betweenness
    # print(out_dict)

    with open(args.o, 'w') as f:
        json.dump(out_dict, f, indent=4)

    return 0

def get_top_betweenness(data):
    G = build_graph(data)
    bet_list = list(nx.betweenness_centrality(G).items())
    bet_list.sort(key=lambda x: -x[1])
    top_betweenness = []
    for i in range(3):
        top_betweenness.append(bet_list[i][0])

    return top_betweenness

def build_graph(data):
    G = nx.Graph()
    for u, sub_dict in data.items():

        for v, weight in sub_dict.items():
            # print(f'w: {weight}')
            if not G.has_edge(u,v):
                G.add_edge(u,v,weight=weight)
    return G

# def extract_info(G):
#     info = {}
#     for n, nbrs in G.adj.items():
#         nested_info = {}
#         for nbr, eattr in nbrs.items():
#             wt = eattr['weight']
#             nested_info[nbr] = wt
#         info[n] = nested_info
#
#     return info

def get_top_total_weight(data):
    info_dict = {}
    for key, sub_dict in data.items():
        sum = 0
        for _,weight in sub_dict.items():
            sum += weight
        info_dict[key] = sum
    sorted_list = list(info_dict.items())
    sorted_list.sort(key=lambda x: -x[1])
    top_total_weight = []
    for i in range(3):
        top_total_weight.append(sorted_list[i][0])
    return top_total_weight

def get_top_num_edges(data):
    info_dict = {}
    for key, sub_dict in data.items():
        num_edges = len(sub_dict)
        info_dict[key] = num_edges
    sorted_list = list(info_dict.items())
    sorted_list.sort(key= lambda x: -x[1])
    top_num_edges = []
    for i in range(3):
        top_num_edges.append(sorted_list[i][0])
    return top_num_edges

if __name__ == '__main__':
    main()