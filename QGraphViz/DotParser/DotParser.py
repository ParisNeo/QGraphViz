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

from itertools import groupby

import json

class DotParser():
    """
    The dot language parser
    """
    def __init__(self):
        pass

    def isParam_line(self, data):
        """
        Detect if the following is a parameters line
        """
        l=len(data)
        for (i,c) in enumerate(data):
            if c=="=":
                return True
            if c=="[":
                return False
            if i < l-1:
                if data[i:i+2]=="--":
                    return False
                if data[i:i+2]=="->":
                    return False
        return False  

    def isNode_line(self, data):  
        """
        Detects if this is a node line
        """
        l=len(data)
        for (i,c) in enumerate(data):
            if c=="[":
                return True
            if c=="}":
                return False
            if i < l-1:
                if data[i:i+2]=="--":
                    return False
                if data[i:i+2]=="->":
                    return False
        return True

    def isEdge_line(self, data, connection_sign="--"): 
        """
        Detects if this is an edge line
        """ 
        l=len(data)
        for (i,_) in enumerate(data):
            if i < l-1:
                if data[i:i+2]==connection_sign:
                    return True
        return False

    def has_params(self, data):
        """
        Detects if a node or cluster has parameters
        """
        for c in data:
            if c=="[":
                return True
            if c=="{":
                return False
        return False

    def find_end_brackets(self, data):
        """
        Suppose data starts after a bracket, find the index of the closing bracket
        """
        dquotes_level = 0
        quotes_level = 0
        bracket_level = 0
        braces_level = 0
        for i, c in enumerate(data):
            if c == "}" and braces_level == 0 and bracket_level == 0 and quotes_level == 0 and dquotes_level == 0:
                return i
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
        return None

    def split(self, s):
        """
        Splits a string while respecting ponctuation
        """
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
        """
        Finds parameters
        """
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


    def parse_Graph(self, data, graph, connection_sign="--"):
        """
        Parses a graph (or a subgraph)
        """
        while len(data)>0:
            lines = data.split("\n",1)
            line = lines[0].strip()
            if(len(lines)>=2):
                data=lines[1]
            else:
                data=""
            if len(line)==0:
                continue
            if "subgraph" in line:
                single_line=False
                if "{" in line:
                    start_brackets_pos = line.index("{")
                    name = line[9:start_brackets_pos]
                    if "cluster_" in name:
                        name = name.replace("cluster_","")
                    end_brackets_pos = self.find_end_brackets(line[start_brackets_pos+1:])
                    if (end_brackets_pos is not None):
                        single_line=True
                    else:
                        end_brackets_pos = self.find_end_brackets(data)

                else:
                    name = line[9:].strip()
                subgraph = Graph(name, graph.graph_type, graph)
                graph.nodes.append(subgraph)
                if single_line:
                    self.parse_Graph(lines[0][start_brackets_pos+1:end_brackets_pos], subgraph, connection_sign)
                else:
                    end_brackets_pos = self.find_end_brackets(lines[1])
                    self.parse_Graph(lines[1][:end_brackets_pos], subgraph, connection_sign)
                    data = lines[1][end_brackets_pos:]
            else:
                if self.isParam_line(lines[0]):
                    title,val = lines[0].split("=",1)
                    graph.kwargs[title.strip()]=val
                    
                elif self.isNode_line(lines[0]):
                    params, params_start_idx, params_end_index =self.find_params(lines[0])
                    if(params is not None):
                        subname = lines[0][0:params_start_idx].strip()
                    else:
                        subname = lines[0].strip()
                    node = Node(subname, graph)
                    if(params is not None):
                        node.kwargs = params
                    graph.nodes.append(node)
                elif self.isEdge_line(lines[0], connection_sign):
                    link_idx=lines[0].index(connection_sign)
                    # find parameters
                    source_node_name = lines[0][:link_idx].strip()
                    params, params_start_idx, params_end_index =self.find_params(lines[0])
                    
                    if(params is not None):
                        dest_node_name = lines[0][link_idx+3:params_start_idx].strip()
                    else:
                        dest_node_name = lines[0][link_idx+3:].strip()

                    source_node  = graph.getNodeByName(source_node_name)
                    dest_node  = graph.getNodeByName(dest_node_name)
                    if(source_node is not None and dest_node is not None):
                        edge = Edge(source_node, dest_node)
                        if(params is None):
                            edge.kwargs={}
                        else:
                            edge.kwargs=params
                        graph.edges.append(edge)
            


    def parseFile(self, filename):
        """
        Parses a file
        """
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
            self.parse_Graph(data[start_id+1:end_id], graph, connection_sign)
        return graph

    def populate_file(self, graph, connection_sign, fi):
        """
        Fills a gv file with data from the graph
        """
        for node in graph.nodes:
            if(type(node)==Graph):
                fi.write("    subgraph cluster_{}".format(node.name))
                fi.write("{\n")
                fi.write("\n".join(["{}={}".format(k,v) for k,v in node.kwargs.items()]))
                fi.write("\n")
                self.populate_file(node, connection_sign, fi)
                fi.write("    }\n")
            else:
                fi.write("    {} [{}]\n".format(node.name, ",".join(["{}={}".format(k,v) for k,v in node.kwargs.items()])))
        for edge in graph.edges:
            if(not edge.kwargs):
                fi.write("    {} {} {}\n".format(edge.source.name, connection_sign, edge.dest.name))
            else:
                fi.write("    {} {} {} [{}]\n".format(edge.source.name, connection_sign, edge.dest.name, ",".join(["{}={}".format(k,v) for k,v in edge.kwargs.items()])))

    def save(self, filename, graph):
        """
        Saves a graph to a gv file
        """
        with open(filename,"w") as fi:
            if graph.graph_type == GraphType.SimpleGraph:
                fi.write("graph {\n")
                self.populate_file(graph, "--", fi)
                fi.write("}")
            if graph.graph_type == GraphType.DirectedGraph:
                fi.write("dgraph {\n")
                self.populate_file(graph, "->", fi)
                fi.write("}")

    def toJSON(self, filename, graph):
        graph_dic = graph.toDICT()
        with open(filename, 'w') as fp:
            json.dump(graph_dic, fp, indent=4)

    def fromJSON(self, filename):
        graph = Graph("")
        with open(filename, 'r') as fp:
            graph_dic = json.load(fp)
            graph.fromDICT(graph_dic)
        return graph