#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
A simple graphviz graphs viewer that enables creating graphs visually, 
manipulate them and save them

"""
from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, QLabel
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
    # Events
    def node_selected(node):
        if(qgv.manipulation_mode==QGraphVizManipulationMode.Node_remove_Mode):
            print("Node {} removed".format(node))
        else:
            print("Node selected {}".format(node))

    def edge_selected(edge):
        if(qgv.manipulation_mode==QGraphVizManipulationMode.Edge_remove_Mode):
            print("Edge {} removed".format(edge))
        else:
            print("Edge selected {}".format(edge))

    def node_invoked(node):
        print("Node double clicked")
    def edge_invoked(node):
        print("Edge double clicked")
    # Create QGraphViz widget
    qgv = QGraphViz(
        node_selected_callback=node_selected,
        edge_selected_callback=edge_selected,
        node_invoked_callback=node_invoked,
        edge_invoked_callback=edge_invoked,
        )
    # Create A new Graph using Dot layout engine
    qgv.new(Dot(Graph()))
    # Define sone graph
    n1 = qgv.addNode("Node1", label="N1")
    n2 = qgv.addNode("Node2", label="N2")
    n3 = qgv.addNode("Node3", label="N3")
    n4 = qgv.addNode("Node4", label="N4")
    n5 = qgv.addNode("Node5", label="N5")
    n6 = qgv.addNode("Node6", label="N6")

    qgv.addEdge(n1, n2, {})
    qgv.addEdge(n3, n2, {})
    qgv.addEdge(n2, n4, {"width":2})
    qgv.addEdge(n4, n5, {"width":4})
    qgv.addEdge(n4, n6, {"width":5,"color":"red"})
    qgv.addEdge(n3, n6, {"width":2})

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
        fname = QFileDialog.getSaveFileName(qgv, "Save", "", "*.gv")
        if(fname[0]!=""):
            qgv.save(fname[0])
        
    def load():
        fname = QFileDialog.getOpenFileName(qgv, "Open", "", "*.gv")
        if(fname[0]!=""):
            qgv.load_file(fname[0])

    def add_node():
        dlg = QDialog()
        dlg.ok=False
        dlg.node_name=""
        dlg.node_label=""
        dlg.node_type="None"
        # Layouts
        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()

        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)

        leNodeName = QLineEdit()
        leNodeLabel = QLineEdit()
        cbxNodeType = QComboBox()

        pbOK = QPushButton()
        pbCancel = QPushButton()

        cbxNodeType.addItems(["None","circle","box"])
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")

        l.setWidget(0, QFormLayout.LabelRole, QLabel("Node Name"))
        l.setWidget(0, QFormLayout.FieldRole, leNodeName)
        l.setWidget(1, QFormLayout.LabelRole, QLabel("Node Label"))
        l.setWidget(1, QFormLayout.FieldRole, leNodeLabel)
        l.setWidget(2, QFormLayout.LabelRole, QLabel("Node Type"))
        l.setWidget(2, QFormLayout.FieldRole, cbxNodeType)

        def ok():
            dlg.OK=True
            dlg.node_name = leNodeName.text()
            dlg.node_label = leNodeLabel.text()
            dlg.node_type = cbxNodeType.currentText()
            dlg.close()

        def cancel():
            dlg.OK=False
            dlg.close()

        pbOK.clicked.connect(ok)
        pbCancel.clicked.connect(cancel)

        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)
        dlg.exec_()

        #node_name, okPressed = QInputDialog.getText(wi, "Node name","Node name:", QLineEdit.Normal, "")
        if dlg.OK and dlg.node_name != '':
                qgv.addNode(dlg.node_name, label=dlg.node_label, shape=dlg.node_type)
                qgv.build()

    def rem_node():
        qgv.manipulation_mode=QGraphVizManipulationMode.Node_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemNode.setChecked(True)

    def rem_edge():
        qgv.manipulation_mode=QGraphVizManipulationMode.Edge_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemEdge.setChecked(True)

    def add_edge():
        qgv.manipulation_mode=QGraphVizManipulationMode.Edges_Connect_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnAddEdge.setChecked(True)

    
    btnOpen = QPushButton("Open")    
    btnOpen.clicked.connect(load)
    btnSave = QPushButton("Save")    
    btnSave.clicked.connect(save)
    hpanel.addWidget(btnOpen)
    hpanel.addWidget(btnSave)

    buttons_list=[]
    btnManip = QPushButton("Manipulate")    
    btnManip.setCheckable(True)
    btnManip.setChecked(True)
    btnManip.clicked.connect(manipulate)
    hpanel.addWidget(btnManip)
    buttons_list.append(btnManip)

    btnAddNode = QPushButton("Add Node")    
    btnAddNode.setCheckable(True)
    btnAddNode.clicked.connect(add_node)
    hpanel.addWidget(btnAddNode)
    buttons_list.append(btnManip)

    btnRemNode = QPushButton("Rem Node")    
    btnRemNode.setCheckable(True)
    btnRemNode.clicked.connect(rem_node)
    hpanel.addWidget(btnRemNode)
    buttons_list.append(btnRemNode)

    btnAddEdge = QPushButton("Add Edge")    
    btnAddEdge.setCheckable(True)
    btnAddEdge.clicked.connect(add_edge)
    hpanel.addWidget(btnAddEdge)
    buttons_list.append(btnAddEdge)

    btnRemEdge = QPushButton("Rem Edge")    
    btnRemEdge.setCheckable(True)
    btnRemEdge.clicked.connect(rem_edge)
    hpanel.addWidget(btnRemEdge)
    buttons_list.append(btnRemEdge)

    w.showMaximized()
    
    sys.exit(app.exec_())