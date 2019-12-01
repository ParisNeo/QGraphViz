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
import enum
from QGraphViz.DotParser import DotParser, Node, Edge, Graph


class QGraphVizManipulationMode(enum.Enum):
    Nodes_Move_Mode=0
    Edges_Conect_Mode=1

class QGraphViz(QWidget):
    """
    Main graphviz widget to draw and interact with graphs
    """
    def __init__(
                    self, 
                    parent=None, 
                    engine=None, 
                    manipulation_mode=QGraphVizManipulationMode.Nodes_Move_Mode,
                    new_edge_created_callback=None # A callbakc called when a new connection is created between two nodes using the GUI
                ):
        QWidget.__init__(self,parent)
        self.parser = DotParser()
        self.engine=engine
        self.qnodes=[]
        self.qedges=[]
        # Nodes manipulation
        self.manipulation_mode = manipulation_mode
        self.selected_Node = None  
        self.current_pos = [0,0]
        self.mouse_down=False
        self.new_edge_created_callback = new_edge_created_callback

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

        if( self.manipulation_mode==QGraphVizManipulationMode.Edges_Conect_Mode and 
            self.mouse_down and 
            self.selected_Node is not None):
            painter.drawLine(self.selected_Node.pos[0], self.selected_Node.pos[1],
                             self.current_pos[0],self.current_pos[1])
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

    def findNode(self, x, y):
        for n in self.engine.graph.nodes:
            if(
                n.pos[0]-n.size[0]/2<x and n.pos[0]+n.size[0]/2>x and
                n.pos[1]-n.size[1]/2<y and n.pos[1]+n.size[1]/2>y
            ):
                return n
        return None

    def load_file(self, filename):
        self.main_graph = self.parser.parseFile(filename)

    def save(self, filename):
        self.parser.save(filename, self.engine.graph)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            n = self.findNode(x,y)
            self.selected_Node = n                
            self.current_pos = [x,y]
            self.mouse_down=True

    def mouseMoveEvent(self, event):
        if self.selected_Node is not None and self.mouse_down:
            x = event.x()
            y = event.y()
            if(self.manipulation_mode==QGraphVizManipulationMode.Nodes_Move_Mode):
                self.selected_Node.pos[0] += x-self.current_pos[0]
                self.selected_Node.pos[1] += y-self.current_pos[1]

            self.current_pos = [x,y]
            self.repaint()
    def mouseReleaseEvent(self, event):
        if(self.manipulation_mode==QGraphVizManipulationMode.Edges_Conect_Mode):
            x = event.x()
            y = event.y()
            if self.selected_Node is not None and self.mouse_down:
                n = self.findNode(x,y)
                if(n!=self.selected_Node):
                    self.addEdge(self.selected_Node, n)
                    self.build()
                    self.repaint()
                    if(self.new_edge_created_callback is not None):
                        self.new_edge_created_callback(self.selected_Node,n)
                self.selected_Node=None

        self.mouse_down=False
