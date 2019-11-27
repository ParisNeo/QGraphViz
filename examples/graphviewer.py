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
sys.path.insert(1,os.path.dirname(__file__)+"/../src")
print(sys.path)
from qgraphviz import QGraphViz

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qgv = QGraphViz()
    w = QMainWindow()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.setCentralWidget(qgv)

    w.show()
    
    sys.exit(app.exec_())