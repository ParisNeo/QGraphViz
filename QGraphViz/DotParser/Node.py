#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""
from PyQt5.QtGui import QFontMetrics, QFont
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

        self.font = QFont("Arial", 12)
        self.fm = QFontMetrics(self.font)


    @property
    def global_pos(self):
        if(self.parent_graph is not None):
            return [
                self.pos[0]+self.parent_graph.pos[0]-self.parent_graph.size[0]/2, 
                self.pos[1]+self.parent_graph.pos[1]-self.parent_graph.size[1]/2
                ]
        else:
            return self.pos

    def toDICT(self):
        node_dic = {}
        node_dic["name"]=self.name
        node_dic["kwargs"]=self.kwargs
        return node_dic