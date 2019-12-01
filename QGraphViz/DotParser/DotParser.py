#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""
from QGraphViz.DotParser.Graph import Graph, GraphType
from QGraphViz.DotParser import Node
from QGraphViz.DotParser import Edge

class DotParser():
    """
    The dot language parser
    """
    def __init__(self):
        pass
    
    def parseFile(self, filename):
        with open(filename, "r"):
            pass # TODO implement file loading
        
    def save(self, filename, graph):
        with open(filename,"w") as fi:
            if graph.graph_type == GraphType.SimpleGraph:
                fi.write("graph {\n")
                for node in graph.nodes:
                    fi.write("    {} [{}]\n".format(node.name, " ".join(["{}={}".format(k,v) for k,v in node.kwargs.items()])))
                for edge in graph.edges:
                    fi.write("    {} -- {}\n".format(edge.source.name, edge.dest.name))
                fi.write("}")
            if graph.graph_type == GraphType.DirectedGraph:
                fi.write("graph {\n")
                for node in graph.nodes:
                    fi.write("    {} [{}]\n".format(node.name, " ".join(["{}={}".format(k,v) for k,v in node.kwargs.items()])))
                for edge in graph.edges:
                    fi.write("    {} -> {}\n".format(edge.source.name, edge.dest.name))
                fi.write("}")
