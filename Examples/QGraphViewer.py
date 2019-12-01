#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
A simple graphviz graphs viewer that enables creating graphs visually, 
manipulate them and save them

"""
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QLineEdit
import sys
import os
sys.path.insert(1,os.path.dirname(__file__)+"/..")
print(sys.path)
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph
from QGraphViz.Engines import Dot

if __name__ == "__main__":
    # Create QT application
    app = QApplication(sys.argv)
    # Create QGraphViz widget
    qgv = QGraphViz()
    # Create A new Graph using Dot layout engine
    qgv.new(Dot(Graph()))
    # Define sone graph
    n1 = qgv.addNode("Node1", label="N1")
    n2 = qgv.addNode("Node2", label="N2")
    n3 = qgv.addNode("Node3", label="N3")
    n4 = qgv.addNode("Node4", label="N4")
    n5 = qgv.addNode("Node5", label="N5")
    n6 = qgv.addNode("Node6", label="N6")
    qgv.addEdge(n1, n2)
    qgv.addEdge(n3, n2)
    qgv.addEdge(n2, n4)
    qgv.addEdge(n4, n5)
    qgv.addEdge(n4, n6)
    qgv.addEdge(n3, n6)
    # Build the graph (the layout engine organizes where the nodes and connections are)
    qgv.build()
    # Save it to a file to be loaded by Graphviz if needed
    qgv.save("test.gv")
    # Create a Main window
    w = QMainWindow()
    w.setWindowTitle('Simple')
    # Create a central widget to handle the QGraphViz object
    wi=QWidget()
    wi.setLayout(QVBoxLayout())
    w.setCentralWidget(wi)
    # Add the QGraphViz object to the layout
    wi.layout().addWidget(qgv)
    # Add a horizontal layout (a pannel to select what to do)
    hpanel=QHBoxLayout()
    wi.layout().addLayout(hpanel)
    # Add few buttons to the panel
    def manipulate():
        qgv.manipulation_mode=QGraphVizManipulationMode.Nodes_Move_Mode
    def save():
        qgv.save("test.gv")
    def add_node():
        node_name, okPressed = QInputDialog.getText(wi, "Node name","Node name:", QLineEdit.Normal, "")
        if okPressed and node_name != '':
            node_label, okPressed = QInputDialog.getText(wi, "Node label","Node label:", QLineEdit.Normal, "")
            if okPressed and node_label != '':
                qgv.addNode(node_name, label=node_label)
                qgv.build()
    def add_edge():
        qgv.manipulation_mode=QGraphVizManipulationMode.Edges_Conect_Mode

    btnManip = QPushButton("Manipulate")    
    btnManip.clicked.connect(manipulate)
    hpanel.addWidget(btnManip)
    btnSave = QPushButton("Save")    
    btnSave.clicked.connect(save)
    hpanel.addWidget(btnSave)
    btnAddNode = QPushButton("Add Node")    
    btnAddNode.clicked.connect(add_node)
    hpanel.addWidget(btnAddNode)
    btnAddEdge = QPushButton("Add Edge")    
    btnAddEdge.clicked.connect(add_edge)
    hpanel.addWidget(btnAddEdge)
    w.showMaximized()
    
    sys.exit(app.exec_())