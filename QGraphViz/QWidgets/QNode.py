#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QSizePolicy
from QGraphViz.Engines.LayoutEngine import LayoutEngine
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class QNode(QWidget):
    """
    The dot graphviz engine
    """
    def __init__(self, node, parent):
        super().__init__(parent)
        self.node=node
        self.setGeometry(self.node.pos[0], self.node.pos[1], self.node.size[0], self.node.size[1])
        self.node.obj=self
        self.setLayout(QHBoxLayout())
        if("label" in self.node.kwargs.keys()):
            self.label=QLabel(self.node.kwargs["label"])
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.layout().addWidget(self.label, Qt.AlignCenter)

    def update(self):
        self.setGeometry(self.node.pos[0]+self.node.size[0]/2, self.node.pos[1]+self.node.size[1]/2, self.node.size[0], self.node.size[1])
    
    def paintEvent(self, event):
        painter = QPainter(self) 
        painter.drawRect(0,0,self.node.size[0]-1, self.node.size[1]-1)
         # TODO : implement painting graph using DOT engine
