#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFontMetrics, QFont
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
        self.font = QFont("Arial", 12)
        self.fm = QFontMetrics(self.font)
        self.margins=20

    def process(self, n, index=0, nb_brothers=0):
        n.processed+=1
        width = 0
        height = 0
        if("label" in n.kwargs.keys()):
            if(n.kwargs["label"]!=""):
                rect = self.fm.boundingRect(n.kwargs["label"])
                width=rect.width()+self.margins
                height=rect.height()+self.margins

        if width==0 or height==0:
            width=self.default_node_width
            height=self.default_node_height
            
        n.size[0]=width
        n.size[1]=height

        if len(n.in_edges)==0:
            n.pos[0]=self.current_x
            n.pos[1]=self.default_node_height/2

            self.current_x += width + self.default_min_nodes_dist
            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, i,len(n.out_edges))
        else:
            x=(width + self.default_min_nodes_dist)*(-(nb_brothers-1)/2+index)
            y=0
            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, i,len(n.out_edges))

            for edg in n.in_edges:
                if (edg.source.processed==0):
                    self.process(edg.source)
                x += edg.source.pos[0]
                if(y<edg.source.pos[1]+width/2+self.default_min_nodes_dist):
                    y = edg.source.pos[1]+width/2+self.default_min_nodes_dist
            x/=len(n.in_edges)

            n.pos[0]=x
            n.pos[1]=y
                    
            for i,oe in enumerate(n.out_edges):
                if oe.dest.processed<20:
                    self.process(oe.dest, i,len(n.out_edges))

    def build(self):
        self.current_x=self.default_node_width/2
        self.current_y =self.default_node_height/2
        for n in self.graph.nodes:
            n.processed=0

        for i,n in enumerate(self.graph.nodes):
            if(n.processed==0):
                self.process(n)
            # TODO : implement painting graph using DOT engine
        for n in self.graph.nodes: 

            if(n.pos[0]<n.size[0]/2):
                for node in self.graph.nodes:
                    node.pos[0]+=(n.size[0]/2)-n.pos[0]

