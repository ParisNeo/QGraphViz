#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""
from QGraphViz.DotParser.Graph import Graph, GraphType
from QGraphViz.DotParser.Node import Node
from QGraphViz.DotParser.Edge import Edge

class DotParser():
    """
    The dot language parser
    """
    def __init__(self):
        pass
    def split(self, s):
        parts = []
        dquotes_level = 0
        quotes_level = 0
        bracket_level = 0
        braces_level = 0
        current = []
        # trick to remove special-case of trailing chars
        for c in (s + ","):
            if c == "," and braces_level == 0 and bracket_level == 0 and quotes_level == 0 and dquotes_level == 0:
                parts.append("".join(current))
                current = []
            else:
                if c == "\"":
                    if dquotes_level==0:
                        dquotes_level += 1
                    else:
                        dquotes_level = 0
                if c == "'":
                    if quotes_level==0:
                        quotes_level += 1
                    else:
                        quotes_level = 0
                if c == "{":
                    bracket_level += 1
                elif c == "}":
                    bracket_level -= 1

                if c == "[":
                    braces_level += 1
                elif c == "]":
                    braces_level -= 1
                current.append(c)
        return parts

    def find_params(self, data):
        try:
            start_idx=data.index("[")
            end_index=data.rindex("]")

            strparams = self.split(data[start_idx+1:end_index])#.split(",")
            params={}
            for param in strparams:
                vals = param.split("=")
                params[vals[0].strip()] = "=".join(vals[1:]).strip()
            return params, start_idx, end_index
        except:
            return None, 0, 0

    def parse_subdata(self, data, graph, connection_sign="--"):
        try:
            end_index=data.index(";")
            sub_data = data[:end_index]
            # Try to find a subgraph
            # Try to find an edge connection
            try:
                link_idx=sub_data.index(connection_sign)
                # find parameters
                source_node_name = sub_data[:link_idx].strip()
                params, params_start_idx, params_end_index =self.find_params(sub_data)
                
                if(params is not None):
                    dest_node_name = sub_data[link_idx+3:params_start_idx].strip()
                else:
                    dest_node_name = sub_data[link_idx+3:end_index].strip()

                source_node  = graph.getNodeByName(source_node_name)
                dest_node  = graph.getNodeByName(dest_node_name)
                if(source_node is not None and dest_node is not None):
                    edge = Edge(source_node, dest_node)
                    if(params is None):
                        edge.kwargs={}
                    else:
                        edge.kwargs=params
                    graph.edges.append(edge)
            except:
                try:
                    params, params_start_idx, params_end_index =self.find_params(sub_data)
                    if(params is not None):
                        subname = data[0:params_start_idx].strip()
                    else:
                        subname = data[0:end_index].strip()

                    node = Node(subname)
                    node.kwargs = params
                    graph.nodes.append(node)


                except:
                    pass
            if(end_index<len(data)):
                self.parse_subdata(data[end_index+1:], graph, connection_sign)
        except:
            pass

    def parseFile(self, filename):
        graph=Graph("main_graph")
        with open(filename,"r") as fi:
            data=fi.read()
            try:
                graph_idx= data.index("dgraph")
                connection_sign = "->"
                print("found dgraph at {}".format(graph_idx))
                graph=Graph("main_graph",GraphType.DirectedGraph)
            except:
                try:
                    graph_idx= data.index("graph")
                    connection_sign = "--"
                    print("found dgraph at {}".format(graph_idx))
                    graph=Graph("main_graph")
                except:
                    raise Exception("Syntax error")
            data=data[graph_idx+5:]
            start_id=data.index("{")
            end_id=data.rindex("}")
            self.parse_subdata(data[start_id+1:end_id], graph, connection_sign)
        return graph

    def populate_file(self, graph, connection_sign, fi):
        for node in graph.nodes:
            if(type(node)==Graph):
                fi.write("    subgraph cluster_{}".format(node.name))
                fi.write("{\n")
                self.populate_file(node, connection_sign, fi)
                fi.write("    };\n")
            else:
                fi.write("    {} [{}];\n".format(node.name, ",".join(["{}={}".format(k,v) for k,v in node.kwargs.items()])))
        for edge in graph.edges:
            if(not edge.kwargs):
                fi.write("    {} {} {};\n".format(edge.source.name, connection_sign, edge.dest.name))
            else:
                fi.write("    {} {} {} [{}];\n".format(edge.source.name, connection_sign, edge.dest.name, ",".join(["{}={}".format(k,v) for k,v in edge.kwargs.items()])))

    def save(self, filename, graph):
        with open(filename,"w") as fi:
            if graph.graph_type == GraphType.SimpleGraph:
                fi.write("graph {\n")
                self.populate_file(graph, "--", fi)
                fi.write("}")
            if graph.graph_type == GraphType.DirectedGraph:
                fi.write("dgraph {\n")
                self.populate_file(graph, "->", fi)
                fi.write("}")
