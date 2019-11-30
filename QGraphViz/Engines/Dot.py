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

    def process(self, n, index=0, nb_brothers=0):
        n.processed=True
        if len(n.in_edges)==0:
            n.pos[0]=self.current_x
            n.pos[1]=self.default_node_height/2
            n.size[0]=self.default_node_width
            n.size[1]=self.default_node_height
            self.current_x += self.default_node_width + self.default_min_nodes_dist
            for i,oe in enumerate(n.out_edges):
                self.process(oe.dest, i,len(n.out_edges))
        else:
            x=(self.default_node_width + self.default_min_nodes_dist)*(-(nb_brothers-1)/2+index)
            y=0
            for i,oe in enumerate(n.out_edges):
                self.process(oe.dest, i,len(n.out_edges))

            for edg in n.in_edges:
                if not(edg.source.processed):
                    self.process(edg.source)
                x += edg.source.pos[0]
                if(y<edg.source.pos[1]+self.default_node_height/2+self.default_min_nodes_dist):
                    y = edg.source.pos[1]+self.default_node_height/2+self.default_min_nodes_dist
            x/=len(n.in_edges)

            n.pos[0]=x
            n.pos[1]=y
            n.size[0]=self.default_node_width
            n.size[1]=self.default_node_height
            for i,oe in enumerate(n.out_edges):
                self.process(oe.dest, i,len(n.out_edges))

    def build(self):
        self.current_x=self.default_node_width/2
        self.current_y =self.default_node_height/2
        for n in self.graph.nodes:
            n.processed=False

        for i,n in enumerate(self.graph.nodes):
            if(n.processed==False):
                self.process(n)
            # TODO : implement painting graph using DOT engine
