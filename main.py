#! /usr/bin/env python

"""
A simple main documenting how to use thhis python package
"""


from netdiff import NetJsonParser
from netdiff.utils import _netjson_networkgraph as to_netjson
from netjson_robustness.analyser import ParsedGraph
import sys
import json


NetJSON = sys.argv[1]  # a NetJSON graph file

nj = NetJsonParser(NetJSON)
pg = ParsedGraph(nj)
pg.condensate_graph()
js = to_netjson(pg.netJSON.protocol, pg.netJSON.version, pg.netJSON.revision,
                pg.netJSON.metric,
                pg.condensed_graph.nodes(data=True),
                pg.condensed_graph.edges(data=True), dict=True)
print json.dumps(js, indent=4)
