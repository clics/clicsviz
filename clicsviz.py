"""
Compute colexifications for dedicated wordlists.
"""

from cltoolkit import Wordlist
from pycldf import Dataset
from collections import defaultdict
from itertools import combinations
import json
from lingpy.convert.graph import networkx2igraph
from networkx.readwrite import json_graph
from clldutils.misc import slug
import networkx as nx


def graph2json(graph, filename):
    """
    Compute graph to JSON format.
    """
    # convert to json
    jdata = json_graph.adjacency_data(graph)

    # write to file
    f = open(filename+'.json','w')
    json.dump(jdata,f)
    f.close()


def get_colexifications(language, data):
    """
    Compute colexifications and add them to the data dictionary.
    """
    tmp = defaultdict(list)
    for form in language.forms:
        if form.concept:
            tmp[form.form] += [(form.concept.concepticon_gloss, form)]
    
    for forms, colset in tmp.items():
        concepts = set([f[0] for f in colset])
        for (cA, fA), (cB, fB) in combinations(colset, r=2):
            if cA != cB:
                data[cA, cB][language.name] += [(fA, fB)]    


wl = Wordlist([
    Dataset.from_metadata("cldf-datasets/ids/cldf/cldf-metadata.json"),
    Dataset.from_metadata("cldf-datasets/yuchinese/cldf/cldf-metadata.json")
    ])

cols = defaultdict(lambda : defaultdict(list))
all_languages = []
all_words = {}
for language in wl.languages:
    if language.family and language.glottocode and language.latitude:
        print("[i] analyzing language {0}".format(language.name))
        all_languages += [language]
        get_colexifications(language, cols)
        for form in language.forms:
            all_words[form.id] = [form.form, form.form]

# get all concepts involved in colexifications
G = nx.Graph()
for (nA, nB), data in cols.items():
    if nA != nB:
        if nA not in G.nodes:
            G.add_node( 
                    nA, words=0, languages=0, families=0, frequency=1, 
                    concept=nA, ID=nA)
        if nB not in G.nodes:
            G.add_node(
                    nB, frequency=1, concept=nB, ID=nB, words=0, 
                    languages=0, families=0)
        languages = list(data)
        words, wofam, families = [], [], []
        for lng, forms in data.items():
            words += [forms[0][0].id]
            wofam += ["/".join([
                forms[0][0].id, 
                forms[0][1].id, 
                forms[0][0].form,
                forms[0][0].language.id,
                forms[0][0].language.family])]
            families += [forms[0][0].language.family]
        G.add_edge(
                nA, 
                nB,
                languages=";".join(languages),
                families=";".join(families),
                weight=len(set(families)),
                words="/".join(words),
                wofam=";".join(wofam)
                )

IG = networkx2igraph(G)
concepts = {}
for comm in IG.community_infomap(edge_weights="weight"):
    nodes = [IG.vs[n]["Name"] for n in comm]
    if len(nodes) > 3:
        mynode = slug(nodes[0])
        subgraph = nx.subgraph(G, nodes)
        print('Writing Graph for {0}'.format(mynode))
        graph2json(subgraph, "app/cluster/"+mynode)
        for node in nodes:
            concepts[node] = mynode


# write language geojson file
features = []
for language in all_languages:
    if language.latitude:
        geom = {
                "type": "Point", 
                "coordinates": [
                    float(language.longitude),
                    float(language.latitude)
                    ]
                }
        prop = {
                "language": language.id,
                "lat": float(language.latitude),
                "lon": float(language.longitude),
                "name": language.name,
                "glottocode": language.glottocode,
                "key": language.id,
                "marker-color": "#00ff00",
                "coverage": len(language.forms),
                "family": language.family,
                "source": language.dataset
                }
        features += [{
            "geometry": geom,
            "properties": prop,
            "type": "Feature"
            }]
        
with open("app/user/langsGeo.json", "w") as f:
    json.dump({"features": features}, f, indent=2)
with open("app/user/words.json", "w") as f:
    json.dump(all_words, f, indent=2)
with open("app/user/infomap-names.js", "w") as f:
    f.write("var INFO = "+json.dumps(concepts, indent=2)+";\n")

