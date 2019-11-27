#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from QGraphViz.Engines.LayoutEngine import LayoutEngine

class Dot(LayoutEngine):
    """
    The dot graphviz engine
    """
    def __init__(self):
        pass
    
    def paint(self, painter, graph):
        pass # TODO : implement painting graph using DOT engine
