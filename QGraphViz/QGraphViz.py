#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Main Class to QGraphViz tool
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt 
import sys
import enum
import datetime
from QGraphViz.DotParser import DotParser, Node, Edge, Graph


class QGraphVizManipulationMode(enum.Enum):
    Nodes_Move_Mode=0
    Edges_Conect_Mode=1
    Node_remove_Mode=2

class QGraphViz(QWidget):
    """
    Main graphviz widget to draw and interact with graphs
    """
    def __init__(
                    self, 
                    parent=None, 
                    engine=None, 
                    manipulation_mode=QGraphVizManipulationMode.Nodes_Move_Mode,
                    new_edge_created_callback=None, # A callbakc called when a new connection is created between two nodes using the GUI
                    node_selected_callback=None, # A callback called when a node is clicked
                    node_invoked_callback=None # A callback called when a node is double clicked
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
        self.node_selected_callback = node_selected_callback
        self.node_invoked_callback = node_invoked_callback


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
        painter.setFont(self.engine.font)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.white)
        pen=QPen()
        painter.setBrush(brush)
        for edge in self.engine.graph.edges:
            painter.drawLine(edge.source.pos[0],edge.source.pos[1],
            edge.dest.pos[0],
            edge.dest.pos[1])
         # TODO : implement painting graph using DOT engine
        for node in self.engine.graph.nodes:
            if("shape" in node.kwargs.keys()):
                if(node.kwargs["shape"]=="box"):
                    painter.drawRect(
                                node.pos[0]-node.size[0]/2,
                                node.pos[1]-node.size[1]/2,
                                node.size[0], node.size[1])
                if(node.kwargs["shape"]=="circle"):
                    painter.drawEllipse(
                                node.pos[0]-node.size[0]/2,
                                node.pos[1]-node.size[1]/2,
                                node.size[0], node.size[1])

            else:
                painter.drawEllipse(
                            node.pos[0]-node.size[0]/2,
                            node.pos[1]-node.size[1]/2,
                            node.size[0], node.size[1])
            if("color" in node.kwargs.keys()):
                pen.setColor(QColor(node.kwargs["color"]))
            else:
                pen.setColor(QColor("black"))

            painter.setPen(pen)

            if("label" in node.kwargs.keys()):
                painter.drawText(
                    node.pos[0]-node.size[0]/2,
                    node.pos[1]-node.size[1]/2,
                    node.size[0], node.size[1],
                    Qt.AlignCenter|Qt.AlignTop,node.kwargs["label"])

        if( self.manipulation_mode==QGraphVizManipulationMode.Edges_Conect_Mode and 
            self.mouse_down and 
            self.selected_Node is not None):
            bkp = painter.pen()
            pen=QPen(Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(self.selected_Node.pos[0], self.selected_Node.pos[1],
                             self.current_pos[0],self.current_pos[1])
            painter.setPen(bkp)

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

    def addEdge(self, source, dest, kwargs):
        edge = Edge(source, dest)
        edge.kwargs=kwargs
        self.engine.graph.edges.append(edge)

    def removeNode(self, node):
        if(node in self.engine.graph.nodes):
            idx = self.engine.graph.nodes.index(node)
            node = self.engine.graph.nodes[idx]
            for edge in node.in_edges:
                del edge.source.out_edges[edge.source.out_edges.index(edge)]
                del self.engine.graph.edges[self.engine.graph.edges.index(edge)]
            for edge in node.out_edges:
                del self.engine.graph.edges[self.engine.graph.edges.index(edge)]
                del edge.dest.in_edges[edge.dest.in_edges.index(edge)]
            del self.engine.graph.nodes[idx]
            self.repaint()

    def findNode(self, x, y):
        for n in self.engine.graph.nodes:
            if(
                n.pos[0]-n.size[0]/2<x and n.pos[0]+n.size[0]/2>x and
                n.pos[1]-n.size[1]/2<y and n.pos[1]+n.size[1]/2>y
            ):
                return n
        return None

    def load_file(self, filename):
        self.engine.graph = self.parser.parseFile(filename)
        self.build()
        self.update()

    def save(self, filename):
        self.parser.save(filename, self.engine.graph)


    def mouseDoubleClickEvent(self, event):
        if(self.node_invoked_callback is not None):
            x = event.x()
            y = event.y()
            n = self.findNode(x,y)
            self.node_invoked_callback(n)
        QWidget.mouseDoubleClickEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            n = self.findNode(x,y)
            self.selected_Node = n                
            self.current_pos = [x,y]
            self.mouse_down=True
        QWidget.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        if self.selected_Node is not None and self.mouse_down:
            x = event.x()
            y = event.y()
            if(self.manipulation_mode==QGraphVizManipulationMode.Nodes_Move_Mode):
                self.selected_Node.pos[0] += x-self.current_pos[0]
                self.selected_Node.pos[1] += y-self.current_pos[1]

            self.current_pos = [x,y]
            self.repaint()
        QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        n = self.findNode(x,y)        
        if(self.manipulation_mode==QGraphVizManipulationMode.Edges_Conect_Mode):
            if self.selected_Node is not None and self.mouse_down:
                n = self.findNode(x,y)
                if(n!=self.selected_Node and n is not None):
                    add_the_edge=True
                    if(self.new_edge_created_callback is not None):
                        add_the_edge, kwargs=self.new_edge_created_callback(self.selected_Node, n)
                    if add_the_edge:
                        self.addEdge(self.selected_Node, n, kwargs)
                        self.build()
                self.selected_Node=None

        QWidget.mouseReleaseEvent(self, event)
        if(self.manipulation_mode==QGraphVizManipulationMode.Node_remove_Mode):
            if(n is not None):
                self.removeNode(n)
                self.build()
                self.repaint()

        if(self.node_selected_callback is not None):
            self.node_selected_callback(n)

        self.mouse_down=False
        self.repaint()

        
