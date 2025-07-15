#%%
import json
import networkx as nx
from pdfminer.high_level import extract_text
import os
import re
import networkx as nx
import textdistance
import seaborn as sns

#%%
texts = []
for i in os.listdir("data/extraterritorial_cases"):
    t = extract_text(os.path.join("data/extraterritorial_cases", i))
    texts.append(t)
#%%
def get_name(astring):
    try:
        res = re.search(r"CASE OF.+\n", astring)
        res = res.group(0)
        return res.strip("\n")
    except:
        return "Unkown"

def get_appno(astring):
    try:
        res = re.search(r"\d{5}\/\d{2}|\d{4}\/\d{2}", astring)
        return res.group(0)
    except:
        return "Unkown"

def get_year(astring):
    try:
        res = re.search(r"\d{4}\n", astring)
        return res.group(0).strip("\n")
    except:
        return "Unkown"

#%%
storage = []
for i in texts:
    results = dict()
    results["name"] = get_name(i)
    results["appno"] = get_appno(i)
    results["year"] = get_year(i)
    results["text"] = i
    storage.append(results)

#%%
g = nx.Graph()
#%%
for i in storage:
    g.add_node(i["appno"], name = i["name"], year = i["year"], text = i["text"])
#%%
edge_storage = []
for i in storage:
    for j in storage:
        if i["appno"] == j["appno"]:
            pass
        else:
            pattern = i['appno']
            counts = re.findall(pattern, j["text"], flags=False)
            ncounts = len(counts)
            distance = textdistance.jaccard(i['text'], j['text'])
            g.add_edge(i["appno"], j["appno"], weight = ncounts, distance = distance)

#%%
dump = nx.node_link_data(g)
with open("data/extraterritorial_cases_3.json", "w") as outfile:
    json.dump(dump, outfile)

#%%
