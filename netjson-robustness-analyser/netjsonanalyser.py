import networkx as nx


class ParsedGraph():
    max_node_size = 100.0
    min_node_size = 2
    cutpoint_size = {0: 2, 1: 5, 2: 7, 3: 10, 4: 12,
                     5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 14}

    def __init__(self, netJSON):
        self.netJSON = netJSON
        self.graph = self.netJSON.graph
        self.condensed_graph = nx.Graph()

    def condensate_graph(self):
        graphs = []
        connected_components = list(nx.connected_component_subgraphs(
                                    self.graph))

        counter = 0
        if not len(connected_components):
            self.condensed_graph = nx.Graph()
            return

        for comp in connected_components:
            if len(comp) == 1:
                g = nx.Graph()
                n = comp.nodes()[0]
                g.add_node(n, {"type": "cutpoint"})
                graphs.append(g)
                continue

            g = nx.Graph()
            if not len(comp):
                pass
            else:
                components = list(nx.biconnected_components(comp))
                max_component_size = max([len(x) for x in components if x])
                component_dict = {}
                cutpoints = set(nx.articulation_points(comp))
                i = 0

                for c in sorted(components, key=lambda x: -len(x)):
                    nodes = set(c) - cutpoints
                    if not nodes:
                        continue
                    node_id = "Block " + str(i)
                    g.add_node(node_id)
                    component_dict[node_id] = nodes
                    i += 1
                    g.node[node_id]["nodes"] = " ".join([x for x in nodes])
                    g.node[node_id]["nodes in block"] = len(nodes)
                    g.node[node_id]["radius"] = max(int(self.max_node_size *
                                                    float(len(nodes)) /
                                                    max_component_size),
                                                    self.min_node_size)
                    g.node[node_id]["type"] = "block"

                for n in cutpoints:
                    temp_g = comp.copy()
                    temp_g.remove_node(n)
                    main_c = sorted([x for x in
                                     nx.connected_components(temp_g)],
                                     key=lambda x: len(x))
                    robustness = len(main_c[-1])
                    g.add_node(n)
                    g.node[n]["type"] = "cutpoint"
                    g.node[n]["Potential disconnected nodes"] = len(comp) - robustness - 1
                    for neigh in comp[n].keys():
                        if neigh in cutpoints:
                            g.add_edge(n, neigh, {'weight': 1})  # TODO weight
                        else:
                            for k, v in component_dict.items():
                                if neigh in v:
                                    g.add_edge(n, k, {'weight': 1})  # TODO weight
                    g.node[n]["robustness"] = 10 - int(10*float(robustness) /
                                                       len(comp))
                    g.node[n]["style"] = "cutpoint_" +\
                                          str(10 - int(10*float(robustness) /
                                                       len(comp)))
                    g.node[n]["radius"] = self.cutpoint_size[g.node[n]
                                                        ["robustness"]]

            # let's merge some leaves
            i = 0
            for n, data in g.nodes(data=True):
                tobemerged = []
                mergesize = 0
                if data["type"] == "cutpoint":
                    for (neigh, ndata) in g[n].items():
                        if g.node[neigh]["type"] == "block" and \
                           len(g[neigh]) == 1:
                            tobemerged.append(neigh)
                            mergesize += g.node[neigh]["nodes in block"]
                if len(tobemerged) > 1:
                    nodes = " ".join([g.node[y]["nodes"] for y in tobemerged])
                    g.add_node(i, {"nodes": nodes,
                                   "nodes in block": mergesize,
                                   "radius": max(int(self.max_node_size *
                                                 float(len(tobemerged)) /
                                                 max_component_size),
                                                 self.min_node_size),
                                   "type": "block"})
                    g.add_edge(i, n, {"weight": 1})  # TODO need weight here
                    i += 1
                    for n in tobemerged:
                        g.remove_node(n)

        # then relabel all the blocks
            blocks = {}
            for n, data in g.nodes(data=True):
                if data["type"] == "block":
                    blocks[n] = data["nodes in block"]
            labels = {}
            for n in sorted(blocks.items(), key=lambda x: -x[1]):
                labels[n[0]] = "Block %d" % counter
                counter += 1
            r_g = nx.relabel_nodes(g, labels, copy=True)
            graphs.append(r_g)
        self.condensed_graph = nx.union_all(graphs)
