#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Generic layout engine implementation
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFontMetrics, QFont, QImage

class LayoutEngine():
    """
    An abstract main class for layout engines
    """
    def __init__(self, current_path="", font = QFont("Arial", 12), margins=[20,20]):
        self.current_path = current_path
        self.font = font
        self.fm = QFontMetrics(self.font)
        self.margins=margins


    def paint(self, painter, graph):
        pass 
    
