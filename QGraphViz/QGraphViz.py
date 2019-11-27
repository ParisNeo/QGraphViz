#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Main Class to QGraphViz tool
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter 
import sys
from QGraphViz.DotParser import DotParser
class QGraphViz(QWidget):
    """
    Main graphviz widget to draw and interact with graphs
    """
    def __init__(self, parent=None, engine=None):
        QWidget.__init__(self,parent)
        self.parser = DotParser()
        self.engine=engine
        self.graph=None

    def paintEvent(self, event):
        painter = QPainter(self)
        self.engine.paint(painter,self.graph)

    def new(self, engine):
        """
        Creates a new engine
        :param engine: An engine object (for example a Dot engine)
        """
        self.engine=engine

    def load_file(self, filename):
        self.main_graph = self.parser.parseFile(filename)
    
