#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
A simple graphviz graphs viewer
"""
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sys
import os
sys.path.insert(1,os.path.dirname(__file__)+"/..")
print(sys.path)
from QGraphViz.QGraphViz import QGraphViz
from QGraphViz.Engines import Dot
if __name__ == "__main__":
    app = QApplication(sys.argv)
    qgv = QGraphViz()
    qgv.new(Dot())
    w = QMainWindow()
    w.setWindowTitle('Simple')
    w.setCentralWidget(qgv)

    w.showMaximized()
    
    sys.exit(app.exec_())