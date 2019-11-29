#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from QGraphViz.Engines.LayoutEngine import LayoutEngine

class Dot(LayoutEngine):
    """
    The dot graphviz engine
    """
    def __init__(self, graph):
        self.graph = graph
        self.default_node_width=100
        self.default_node_height=100
        self.default_min_nodes_dist=self.default_node_height

    def process(self, n):
        if len(n.in_edges)==0:
            n.pos[0]=self.current_x
            n.pos[1]=self.default_node_height/2
            n.size[0]=self.default_node_width
            n.size[1]=self.default_node_height
            self.current_x += self.default_node_width + self.default_min_nodes_dist
        else:
            x=0
            y=0
            for edg in n.in_edges:
                if(edg.source.processed):
                    x += edg.source.pos[0]
                    if(y<edg.source.pos[1]+self.default_node_height/2+self.default_min_nodes_dist):
                        y = edg.source.pos[1]+self.default_node_height/2+self.default_min_nodes_dist
                else:
                    self.process(edg.source)
                x/=len(n.in_edges)
            n.pos[0]=x
            n.pos[1]=y
            n.size[0]=self.default_node_width
            n.size[1]=self.default_node_height
        n.processed=True
    def build(self):
        self.current_x=self.default_node_width/2
        self.current_y =self.default_node_height/2
        for n in self.graph.nodes:
            n.processed=False

        for i,n in enumerate(self.graph.nodes):
            if(n.processed==False):
                self.process(n)
            # TODO : implement painting graph using DOT engine
