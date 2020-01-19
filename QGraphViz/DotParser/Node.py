#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""

class Node():
    """
    The dot graphviz engine
    """
    def __init__(self, name, parent_graph, **kwargs):
        self.name = name
        self.parent_graph = parent_graph
        self.pos=[0,0]
        self.size=[1,1]
        self.kwargs=kwargs
        # Nodes
        self.in_edges=[]
        self.out_edges=[]
        self.processed = 0
        
    @property
    def global_pos(self):
        if(self.parent_graph is not None):
            return [self.pos[0]+self.parent_graph.pos[0], self.pos[1]+self.parent_graph.pos[1]]
        else:
            return self.pos

    def toDICT(self):
        node_dic = {}
        node_dic["name"]=self.name
        node_dic["kwargs"]=self.kwargs
        return node_dic