import networkx as nx


class ParsedGraph():
    css_granularity = 10

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
                g.node[node_id]["nodes"] = str([x for x in nodes])
                g.node[node_id]["size"] = len(nodes)
                rel_size = float(g.node[node_id]["size"])/len(self.graph)
                node_type_number = int(self.css_granularity * rel_size)
                g.node[node_id]["rel_size"] = int(100*rel_size)
                g.node[node_id]["type"] = "size_" + str(node_type_number)

            for n in cutpoints:
                g.add_node(n)
                g.node[n]["type"] = "cutpoint"  # TODO put a number here too
                for neigh in self.graph[n].keys():
                    if neigh in cutpoints:
                        g.add_edge(n, neigh, {'weight': 1})  # TODO weight
                    else:
                        for k, v in component_dict.items():
                            if neigh in v:
                                g.add_edge(n, k, {'weight': 1})  # TODO weight

        self.condensed_graph = g
