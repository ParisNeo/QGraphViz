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
from QGraphViz.DotParser.Graph import Graph, GraphType
class Dot(LayoutEngine):
    """
    The dot graphviz engine
    """
    def __init__(self, graph, show_subgraphs=True):
        self.graph = graph
        self.default_node_width=100
        self.default_node_height=100
        self.default_min_nodes_dist=self.default_node_height
        self.font = QFont("Arial", 12)
        self.fm = QFontMetrics(self.font)
        self.margins=20
        self.show_subgraphs = show_subgraphs

    def process(self, n, graph, index=0, nb_brothers=0):
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

        if(type(n)==Graph and self.show_subgraphs):
            if len(n.nodes)>0:
                minx=10000
                miny=10000
                maxx=0
                maxy=0
                for i, node in enumerate(n.nodes):
                    if(node.processed<3):
                        self.process(node, n, index)

                    if(node.pos[0]<minx):
                        minx = node.pos[0]-node.size[0]/2
                    if(node.pos[1]<miny):
                        miny = node.pos[1]-node.size[1]/2

                    if(node.pos[0]>maxx):
                        maxx = node.pos[0]+node.size[0]/2
                    if(node.pos[1]>maxy):
                        maxy = node.pos[1]+node.size[1]/2

                w=maxx-minx+2*self.margins
                h=maxy-miny+2*self.margins
                width = w if w>width else width
                height = h if h>height else height
            else:
                graph.size=[width, height]
                

        n.size[0]=width
        n.size[1]=height

        if len(n.in_edges)==0:
            n.pos[0]=graph.current_x
            n.pos[1]=self.default_node_height/2

            graph.current_x += width + self.default_min_nodes_dist
            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, graph, i,len(n.out_edges))
        else:
            x=(width + self.default_min_nodes_dist)*(-(nb_brothers-1)/2+index)
            y=0
            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, graph, i,len(n.out_edges))

            for edg in n.in_edges:
                if (edg.source.processed==0):
                    self.process(edg.source, graph)
                if(n.parent_graph == edg.source.parent_graph):
                    x += edg.source.pos[0]
                    if(y<edg.source.pos[1]+width/2+self.default_min_nodes_dist):
                        y = edg.source.pos[1]+width/2+self.default_min_nodes_dist
            x/=len(n.in_edges)

            n.pos[0]=x
            n.pos[1]=y
                    
            for i,oe in enumerate(n.out_edges):
                if oe.dest.processed<20:
                    self.process(oe.dest, graph, i,len(n.out_edges))

    def build_graph(self, graph):
        for n in graph.nodes:
            n.processed=0
         
        for i,n in enumerate(graph.nodes):
            if(n.processed<3):
                self.process(n, graph)

        for n in graph.nodes: 
            if(n.pos[0]<n.size[0]/2):
                for node in self.graph.nodes:
                    node.pos[0]+=(n.size[0]/2)-n.pos[0]
        



    def build(self):
        self.graph.current_x=self.default_node_width/2
        self.graph.current_y =self.default_node_height/2

        self.build_graph(self.graph)
