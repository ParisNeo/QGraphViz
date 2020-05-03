#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFontMetrics, QFont, QImage
from QGraphViz.Engines.LayoutEngine import LayoutEngine
from QGraphViz.DotParser.Graph import Graph, GraphType

# Import os is needed for locating image files
import os
class Dot(LayoutEngine):
    """
    The dot graphviz engine
    """
    def __init__(self, graph, show_subgraphs=True, current_path= "", font = QFont("Arial", 12), margins=[20, 20]):
        """
        Builds a Dot graphviz engine
        """
        self.graph = graph
        self.default_node_width=100
        self.default_node_height=100
        self.default_min_nodes_dist=self.default_node_height
        self.show_subgraphs = show_subgraphs
        self.graph.depth_x_pos = [0]
        self.margins = margins
        LayoutEngine.__init__(self, current_path, font)

    def process_size(self,n):
        # If this node is a subgraph, then process children 
        if type(n)==Graph:
            for nn in n.nodes:
                self.process_size(nn)
        
        if("label" in n.kwargs.keys()):
            if(n.kwargs["label"]!=""):
                rect = self.fm.boundingRect(n.kwargs["label"])
                width=rect.width()+self.margins[0]
                height=rect.height()+self.margins[1]
        # If there is a special shape, then process it
        if("shape" in n.kwargs.keys()):
            w=0
            h=0
            image = None
            if("," in n.kwargs["shape"]): # if there is a , in the shape, the first part is the path, then width, then height
                img_params = n.kwargs["shape"].split(",")
                if len(img_params)==3:# img:width:height
                    img_path = img_params[0]
                    w =  int(img_params[1])
                    h =  int(img_params[2])
                    img_path2 = os.path.join(os.path.dirname(self.current_path),img_path)
                    if(os.path.isfile(img_path)):
                        image = QImage(img_path)
                    elif(os.path.isfile(img_path2)):
                        image = QImage(img_path2)
            else:
                img_path = n.kwargs["shape"]
                img_path2 = os.path.join(os.path.dirname(self.current_path),img_path)
                if(os.path.isfile(img_path)):
                    image = QImage(img_path)
                    w =  image.size().width()
                    h =  image.size().height()
                elif(os.path.isfile(img_path2)):
                    image = QImage(img_path2)
                    w =  image.size().width()
                    h =  image.size().height()
            if image is not None:
                width = w if w>width else width
                height = h if h>height else height

        if width==0 or height==0:
            width=self.default_node_width
            height=self.default_node_height

        if(type(n)==Graph and self.show_subgraphs):
            n.depth_x_pos=[0]
            for nn in n.nodes:
                self.process(nn, n, 0, len(n.nodes), depth=0)
            _,_,w_,h_=n.getRect()
            #w_+=2*self.default_min_nodes_dist
            width = w_ if w_>width else width
            height = h_ if h_>height else height
            width += 2*self.margins[0]
            height += 2*self.margins[1]
            
        

        n.size[0]=width
        n.size[1]=height        

    def process(self, n, graph, index=0, nb_brothers=0, depth=0, stage=0):
        n.processed+=1
        if("pos" in n.kwargs):
            n.pos[0]=n.kwargs["pos"][0]
            n.pos[1]=n.kwargs["pos"][1]
            n.size[0]=n.kwargs["size"][0]
            n.size[1]=n.kwargs["size"][1]

            if len(graph.depth_x_pos)>depth:
                graph.depth_x_pos[depth] += n.size[0] + self.default_min_nodes_dist
            else:
                graph.depth_x_pos.append(n.size[0] + self.default_min_nodes_dist)

            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, graph, i,len(n.out_edges), depth=depth+1)

            return
        width = n.size[0]
        height = n.size[1]



        if len(n.in_edges)==0:
            n.pos[0]=graph.depth_x_pos[depth]+self.margins[0]+width/2
            n.pos[1]=self.default_node_height/2+self.margins[1]+height/2
            if len(graph.depth_x_pos)>depth:
                graph.depth_x_pos[depth] += width/2 + self.default_min_nodes_dist
            else:
                graph.depth_x_pos.append(width/2 + self.default_min_nodes_dist)
        else:
            x=(width/2 + self.default_min_nodes_dist)*(-(nb_brothers-1)/2+index)
            y=0
            for i,oe in enumerate(n.out_edges):
                if (oe.dest.processed<20):
                    self.process(oe.dest, graph, i,len(n.out_edges),depth=depth+1)

            for edg in n.in_edges:
                if (edg.source.processed==0):
                    self.process(edg.source, graph)
                if(n.parent_graph == edg.source.parent_graph):
                    x += edg.source.pos[0]
                    if(y<edg.source.pos[1]+edg.source.size[1]/2+height/2+self.default_min_nodes_dist):
                        y = edg.source.pos[1]+edg.source.size[1]/2+height/2+self.default_min_nodes_dist
            x/=len(n.in_edges)

            n.pos[0]=x
            n.pos[1]=y
                    
        for i,oe in enumerate(n.out_edges):
            if oe.dest.processed<20:
                self.process(oe.dest, graph, i,len(n.out_edges))

        if(type(n)==Graph and self.show_subgraphs):
            n.depth_x_pos=[0]
            for nn in n.nodes:
                self.process(nn, n, 0, len(n.nodes), depth=depth)
            

    def build_graph(self, graph):
        for n in graph.nodes:
            n.processed=0
         
        for i,n in enumerate(graph.nodes):
            self.process_size(n)

        for i,n in enumerate(graph.nodes):
            if(n.processed<3):
                self.process(n, graph)
        """
        for n in graph.nodes: 
            if(n.pos[0]<n.size[0]/2):
                for node in graph.nodes:
                    node.pos[0]+=(n.size[0]/2)-n.pos[0]
        """
        _,_,graph.size[0], graph.size[1] = graph.getRect()
        graph.pos[0] = graph.size[0] /2
        graph.pos[1] = graph.size[1] /2


    def build(self):
        self.graph.depth_x_pos = [0]

        self.build_graph(self.graph)
