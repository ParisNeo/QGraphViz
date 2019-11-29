#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from QGraphViz.Engines.LayoutEngine import LayoutEngine
from PyQt5.QtGui import QPainter 

class QEdge(QWidget):
    """
    The dot graphviz engine
    """
    def __init__(self, edge, parent):
        super().__init__(parent)
        self.edge=edge
        self.setGeometry(self.edge.source.pos[0],self.edge.source.pos[1],
                         self.edge.dest.pos[0]-self.edge.dest.pos[0],self.edge.source.pos[1] - self.edge.source.pos[1])
    def update(self):
        self.setGeometry(self.edge.source.pos[0],self.edge.source.pos[1],
                         abs(self.edge.dest.pos[0]-self.edge.dest.pos[0]),abs(self.edge.source.pos[1] - self.edge.source.pos[1]))
    
    def paintEvent(self, event):
        painter = QPainter(self) 
        painter.drawRect(0,0,self.edge.dest.pos[0]-self.edge.dest.pos[0],self.edge.source.pos[1] - self.edge.source.pos[1])
         # TODO : implement painting graph using DOT engine
