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
            cutpoints = set(nx.articulation_points(self.graph))
            for n in cutpoints:
                g.add_node(n)
                g.node[n]["type"] = "cutpoint"  # TODO put a number here too
                for neigh in g[n].keys():
                    if neigh in cutpoints:
                        g.add_edge(n, neigh, {'weight': 1})  # TODO weight

            i = 0
            for c in sorted(components, key=lambda x: -len(x)):
                c_set = set(c)
                nodes = list(c_set - cutpoints)
                if not nodes:
                    continue
                node_id = "component_" + str(i)
                i += 1
                g.add_node(node_id)
                c_cutpoints = c_set.intersection(cutpoints)
                g.node[node_id]["nodes"] = str(nodes)
                g.node[node_id]["size"] = len(nodes)
                rel_size = float(g.node[node_id]["size"])/len(self.graph)
                node_type_number = int(self.css_granularity * rel_size)
                g.node[node_id]["rel_size"] = int(100*rel_size)
                g.node[node_id]["type"] = "size_" + str(node_type_number)
                for p in c_cutpoints:
                    g.add_edge(p, node_id, {"weight": 1})  # TODO preserve the weight

        self.condensed_graph = g
