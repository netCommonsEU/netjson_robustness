import networkx as nx


class ParsedGraph():
    max_node_size = 100.0

    def __init__(self, netJSON):
        self.netJSON = netJSON
        self.graph = self.netJSON.graph
        self.condensed_graph = None

    def condensate_graph(self):
        g = nx.Graph()
        if not len(self.graph):
            pass
        else:
            components = list(nx.biconnected_components(self.graph))
            max_component_size = max([len(x) for x in components])
            component_dict = {}
            cutpoints = set(nx.articulation_points(self.graph))
            i = 0
            for c in sorted(components, key=lambda x: -len(x)):
                nodes = set(c) - cutpoints
                if not nodes:
                    continue
                node_id = "component_" + str(i)
                g.add_node(node_id)
                component_dict[node_id] = nodes
                i += 1
                g.node[node_id]["nodes"] = " ".join([x for x in nodes])
                g.node[node_id]["num_nodes"] = len(nodes)
                g.node[node_id]["radius"] = max(int(self.max_node_size *
                                                float(len(nodes)) /
                                                max_component_size), 1)
                g.node[node_id]["type"] = "block"

            for n in cutpoints:
                g.add_node(n)
                g.node[n]["type"] = "cutpoint"  # TODO put a number here too
                #g.node[n]["radius"] = "10"  # TODO put a number here too
                for neigh in self.graph[n].keys():
                    if neigh in cutpoints:
                        g.add_edge(n, neigh, {'weight': 1})  # TODO weight
                    else:
                        for k, v in component_dict.items():
                            if neigh in v:
                                g.add_edge(n, k, {'weight': 1})  # TODO weight

        # let's merge some leaves
        i = 0
        for n, data in g.nodes(data=True):
            tobemerged = []
            if data["type"] == "cutpoint":
                for (neigh, ndata) in g[n].items():
                    if g.node[neigh]["type"] == "block" and \
                       g.node[neigh]["num_nodes"] == 1:
                        tobemerged.append(neigh)
            if tobemerged:
                nodes = " ".join([g.node[y]["nodes"] for y in tobemerged])
                g.add_node(i, {"nodes": str(x for x in nodes),
                               "num_nodes": len(tobemerged),
                               "radius": int(self.max_node_size *
                                             float(len(tobemerged)) /
                                             max_component_size),
                               "type": "block"})
                g.add_edge(i, n, {"weight": 1})  # TODO need weight here
                i += 1
                for n in tobemerged:
                    g.remove_node(n)

        #FIXME need to check disconnected components

        # then relabel all the blocks
        self.condensed_graph = g
        nx.write_graphml(g, "/tmp/ninux.graphml")
