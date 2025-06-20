
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def load_graph_from_json(path):
    f = open(path, "r")
    data = json.load(f)
    graph = nx.node_link_graph(data)
    return graph

# def score_normalize(dictvalues):
#     dictvalues_arr = np.array([x for x in dictvalues])
#     values_total = np.sum(np.abs(dictvalues_arr))
#     return dictvalues_arr/values_total

def draw_spring(graph, seed=123, node_color="tab:blue", figsize=(8,8), node_alpha = 0.7, edge_alpha=0.7):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figsize))
    pos = nx.spring_layout(graph, seed = seed)
    nx.draw_networkx_nodes(graph, pos=pos, node_color=node_color, ax=ax, alpha=node_alpha)
    nx.draw_networkx_edges(graph, pos=pos, ax=ax, alpha = edge_alpha)
    nx.draw_networkx_labels(graph, pos=pos, ax=ax);

def dataframe_from_results(graph, results_dict, name):
    nodes = list(graph.nodes)
    df = pd.DataFrame({"nodes":nodes, f"{name}":results_dict.values()})
    df.set_index("nodes", inplace=True)
    return df

def score_normalize(input, from_dictionary=True):
    if from_dictionary == True:
        scores = np.array(list(input.values()))
        sum_scores = np.sum(scores)
        return scores/sum_scores
    else:
        scores = list(input)
        scores = np.array(input.to_list())
        sum_scores = np.sum(scores)
        return scores/sum_scores

# this function does not import for some reason. Error is not explicit
# def compare_centrality(graph, title):
#     results = []
#     for i in [nx.degree_centrality, nx.closeness_centrality, nx.eigenvector_centrality, nx.betweenness_centrality]:
#         res = i(graph)
#         results.append(res)

#     comparision_df = pd.DataFrame({"stations":results[0].keys(), "degree_c":results[0].values(), "closeness_c":results[1].values(),\
#                                    "eig_c":results[2].values(), "between_c":results[3].values()})
#     comparision_df.set_index("stations", inplace=True)

#     fig, ax = plt.subplots(1,2, figsize=[16,8])
#     plt.suptitle(f"Correlation for {title}")
#     sns.heatmap(comparision_df.corr(), annot=True, vmin=-1, vmax=1, ax=ax[0])
#     means = comparision_df.corr().mean()
#     sns.barplot(x = means.values, y= means.index, ax = ax[1])


## Save for later

# level0_nodes = [x for x in g_drones if x != "2021R0664" or "2019R0945"]
# level1_nodes = ["2021R0664", "2019R0945"]
# edges_for_2001R0664 = [(x,y) for x, y in g_drones.edges() if x == "2021R0664"]
# edges_for_2019R0945 = [(x,y) for x, y in g_drones.edges() if x == "2019R0945"]
#
# g_drones_bipartite = nx.Graph()
# g_drones_bipartite.add_nodes_from(level0_nodes, bipartite=0)
# g_drones_bipartite.add_nodes_from(level1_nodes, bipartite=1)
#
# g_drones_bipartite.add_edges_from(edges_for_2001R0664)
# g_drones_bipartite.add_edges_from(edges_for_2019R0945)
#
# nodeset1 = [y for x,y in edges_for_2019R0945]+["2019R0945"]
# nodeset2 = [y for x,y in edges_for_2001R0664]+["2021R0664"]
#
# print(nodeset2)
#
# plt.figure(figsize=(6, 6))
# pos = nx.bipartite_layout(g_drones_bipartite, nodes=level1_nodes)
#
# nx.draw_networkx_nodes(g_drones_bipartite, nodelist=nodeset1, node_color="tab:blue", pos = pos, alpha=0.5)
# nx.draw_networkx_edges(g_drones_bipartite, edgelist= edges_for_2019R0945, pos = pos, alpha=0.5)
# nx.draw_networkx_nodes(g_drones_bipartite, nodelist=nodeset2, node_color="tab:orange", pos = pos, alpha=0.5)
# nx.draw_networkx_edges(g_drones_bipartite, edgelist=edges_for_2001R0664, pos = pos, alpha=0.5)
# nx.draw_networkx_labels(g_drones_bipartite, pos=pos, labels={"2019R0945":"2019R0945", "2021R0664":"2021R0664"}, font_size=10);
