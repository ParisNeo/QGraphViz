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
        self.update()
        self.show()
    def update(self):
        w=abs(self.edge.dest.pos[0]-self.edge.source.pos[0])
        h=abs(self.edge.dest.pos[1] - self.edge.source.pos[1])
        if w==0:
            w=5
        if h==0:
            h=5

        self.setGeometry(self.edge.source.pos[0],self.edge.source.pos[1],
                         w,h)
    
    def paintEvent(self, event):
        painter = QPainter(self) 
        painter.drawLine(0,0,
        self.edge.dest.pos[0] - self.edge.source.pos[0],
        self.edge.dest.pos[1] - self.edge.source.pos[1])
         # TODO : implement painting graph using DOT engine
