import unittest
import sys
import networkx as nx
from netdiff import NetJsonParser
sys.path.insert(0, "../")
from netjsonanalyser import ParsedGraph

# test division by zero and test the size of the graph is preserved

empty_graph = \
    {
        "type": "NetworkGraph",
        "protocol": "OLSR",
        "version": "0.6.6",
        "revision": "5031a799fcbe17f61d57e387bc3806de",
        "metric": "ETX",
        "nodes":[],
        "links":[]
    }

biconnected_graph = \
    {
        "type": "NetworkGraph",
        "protocol": "OLSR",
        "version": "0.6.6",
        "revision": "5031a799fcbe17f61d57e387bc3806de",
        "metric": "ETX",
        "nodes": [
            {
                "id": "10.150.0.1"
            },
            {
                "id": "10.150.0.2"
            },
            {
                "id": "10.150.0.3"
            },
            {
                "id": "10.150.0.4"
            },
            {
                "id": "10.150.0.5"
            },
            {
                "id": "10.150.0.6"
            },
            {
                "id": "10.150.0.7"
            },
            {
                "id": "10.150.0.8"
            },
            {
                "id": "10.150.0.9"
            },
            {
                "id": "10.150.0.10"
            },
        ],
        "links": [
            {
                "source": "10.150.0.1",
                "target": "10.150.0.2",
                "cost": 1
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.3",
                "cost": 2
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.4",
                "cost": 2.1
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.5",
                "cost": 2.4
            },
            {
                "source": "10.150.0.3",
                "target": "10.150.0.4",
                "cost": 1.9
            },
            {
                "source": "10.150.0.3",
                "target": "10.150.0.5",
                "cost": 2
            },
            {
                "source": "10.150.0.4",
                "target": "10.150.0.5",
                "cost": 1.6
            },
            {
                "source": "10.150.0.5",
                "target": "10.150.0.6",
                "cost": 1.123
            },
            {
                "source": "10.150.0.6",
                "target": "10.150.0.7",
                "cost": 1.12
            },
            {
                "source": "10.150.0.7",
                "target": "10.150.0.8",
                "cost": 1
            },
            {
                "source": "10.150.0.7",
                "target": "10.150.0.9",
                "cost": 1.5
            },
            {
                "source": "10.150.0.8",
                "target": "10.150.0.9",
                "cost": 1.3
            },
            {
                "source": "10.150.0.9",
                "target": "10.150.0.10",
                "cost": 1.1
            },
        ]
    }

disconnected_graph = \
    {
        "type": "NetworkGraph",
        "protocol": "OLSR",
        "version": "0.6.6",
        "revision": "5031a799fcbe17f61d57e387bc3806de",
        "metric": "ETX",
        "nodes": [
            {
                "id": "10.150.0.1"
            },
            {
                "id": "10.150.0.2"
            },
            {
                "id": "10.150.0.3"
            },
            {
                "id": "10.150.0.4"
            },
            {
                "id": "10.150.0.5"
            },
            {
                "id": "10.150.0.6"
            },
            {
                "id": "10.150.0.7"
            },
            {
                "id": "10.150.0.8"
            },
            {
                "id": "10.150.0.9"
            },
            {
                "id": "10.150.0.10"
            },
        ],
        "links": [
            {
                "source": "10.150.0.1",
                "target": "10.150.0.2",
                "cost": 1
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.3",
                "cost": 2
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.4",
                "cost": 2.1
            },
            {
                "source": "10.150.0.2",
                "target": "10.150.0.5",
                "cost": 2.4
            },
            {
                "source": "10.150.0.3",
                "target": "10.150.0.4",
                "cost": 1.9
            },
            {
                "source": "10.150.0.3",
                "target": "10.150.0.5",
                "cost": 2
            },
            {
                "source": "10.150.0.4",
                "target": "10.150.0.5",
                "cost": 1.6
            },
            {
                "source": "10.150.0.5",
                "target": "10.150.0.6",
                "cost": 1.123
            },
            {
                "source": "10.150.0.7",
                "target": "10.150.0.8",
                "cost": 1
            },
            {
                "source": "10.150.0.7",
                "target": "10.150.0.9",
                "cost": 1.5
            },
            {
                "source": "10.150.0.8",
                "target": "10.150.0.9",
                "cost": 1.3
            },
            {
                "source": "10.150.0.9",
                "target": "10.150.0.10",
                "cost": 1.1
            },
        ]
    }


class TestCondensateGraph(unittest.TestCase):

    def setUp(self):
        self.obj = ParsedGraph(NetJsonParser(data=biconnected_graph))

    def test_netjson(self):
        self.assertTrue(self.obj.netJSON)

    def test_graph(self):
        self.assertTrue(self.obj.graph)

    def test_empty(self):
        self.obj = ParsedGraph(NetJsonParser(data=empty_graph))
        self.obj.condensate_graph()
        self.assertEqual(len(self.obj.condensed_graph), 0)

    def test_size(self):
        self.obj = ParsedGraph(NetJsonParser(data=biconnected_graph))
        self.obj.condensate_graph()
        n = 0
        for node, data in self.obj.condensed_graph.nodes(data=True):
            if data["type"] == "cutpoint":
                n += 1
            if data["type"] == "block":
                n += int(data["nodes in block"])
        self.assertEqual(n, len(self.obj.graph))

    def test_connected(self):
        self.obj = ParsedGraph(NetJsonParser(data=biconnected_graph))
        self.obj.condensate_graph()
        self.assertTrue(nx.is_connected(self.obj.graph) ==
                        nx.is_connected(self.obj.condensed_graph))

    def test_type(self):
        self.obj = ParsedGraph(NetJsonParser(data=biconnected_graph))
        self.obj.condensate_graph()
        for node, data in self.obj.condensed_graph.nodes(data=True):
            self.assertTrue(data["type"] in ("cutpoint", "block"))

    def test_radius(self):
        self.obj = ParsedGraph(NetJsonParser(data=biconnected_graph))
        self.obj.condensate_graph()
        for node, data in self.obj.condensed_graph.nodes(data=True):
            self.assertTrue("radius" in data)
            self.assertTrue(data["radius"] <= self.obj.max_node_size)
            self.assertTrue(data["radius"] >= 1)

    def test_disconnected_graph(self):
        self.obj = ParsedGraph(NetJsonParser(data=disconnected_graph))
        self.obj.condensate_graph()
        self.assertFalse(nx.is_connected(self.obj.condensed_graph))

    def test_disconnected_graph_size(self):
        self.obj = ParsedGraph(NetJsonParser(data=disconnected_graph))
        self.obj.condensate_graph()
        n = 0
        for node, data in self.obj.condensed_graph.nodes(data=True):
            if data["type"] == "cutpoint":
                n += 1
            if data["type"] == "block":
                n += int(data["nodes in block"])
        self.assertEqual(n, len(self.obj.graph))


if __name__ == "__main__":
    unittest.main()
