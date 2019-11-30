#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Main Class to QGraphViz tool
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt 
import sys
from QGraphViz.DotParser import DotParser, Node, Edge, Graph
from QGraphViz.QWidgets import QNode, QEdge
class QGraphViz(QWidget):
    """
    Main graphviz widget to draw and interact with graphs
    """
    def __init__(self, parent=None, engine=None):
        QWidget.__init__(self,parent)
        self.parser = DotParser()
        self.engine=engine
        self.qnodes=[]
        self.qedges=[]

    def build(self):
        self.engine.build()
        """
        for node in self.engine.graph.nodes:
            qnode = QNode(node, self)
            qnode.setParent(self)
            self.qnodes.append(qnode)
        for edge in self.engine.graph.edges:
            qedge = QEdge(edge, self)
            qedge.setParent(self)
            self.qedges.append(qedge)
        """
    def paintEvent(self, event):
        painter = QPainter(self) 
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.white)
        painter.setBrush(brush)
        for edge in self.engine.graph.edges:
            painter.drawLine(edge.source.pos[0],edge.source.pos[1],
            edge.dest.pos[0],
            edge.dest.pos[1])
         # TODO : implement painting graph using DOT engine
        for node in self.engine.graph.nodes:
            painter.drawEllipse(
                        node.pos[0]-node.size[0]/2,
                        node.pos[1]-node.size[1]/2,
                        node.size[0], node.size[1])
            if("label" in node.kwargs.keys()):
                painter.drawText(
                    node.pos[0]-node.size[0]/2,
                    node.pos[1]-node.size[1]/2,
                    node.size[0], node.size[1],
                    Qt.AlignCenter|Qt.AlignTop,node.kwargs["label"])

    def new(self, engine):
        """
        Creates a new engine
        :param engine: An engine object (for example a Dot engine)
        """
        self.engine=engine

    def addNode(self, node_name, **kwargs):
        node = Node(node_name, **kwargs)
        self.engine.graph.nodes.append(node)
        return node

    def addEdge(self, source, dest):
        edge = Edge(source, dest)
        self.engine.graph.edges.append(edge)

    def load_file(self, filename):
        self.main_graph = self.parser.parseFile(filename)
    
