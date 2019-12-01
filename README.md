# QGraphViz
A PyQT based GraphViz builder/renderer (100% opensource)

## Introduction

I was searching for a handy tool to code graphs using python then visualize them within my software. I found about graphviz which is a great tool to build graphs.

The problem is that you need to install the graphviz software in order to compile your file and render it.
There is a graphviz package on PYPI that allows creating dot code that can then be processed by graphviz, but in practice, you need to install graphviz and somehow add it to your path in order to execute the render command.

PyGraphviz is another package that can be used. But as you can read in their documentation, you still need to install Graphviz.

I also found this visualizer based on pyQt4. It is a simple Qt based visualizer that tracks the updates on the .gv file and redraws it in realtime:
DDorch/GraphVizLiveUpdateViewer

So since I didn't find any package out there that satifies my needs, I decided to create a pyQT5 based Graphviz tool that can visualize Graphviz code without the need to install Graphviz and provide it with MIT licence, so that other people can simply use it in their software.

## Objective

Build python pyQT5 based QWidget that can visualize graphs and allow realtime interaction with graphs add edges and nodes, change attributes ...
## Requirements

As its name suggests, this module needs you to install pyqt5 package first.
```bash
pip install pyqt5
```

## Installation
```bash
pip install QGraphViz
```

## Actual status
1. Simple graphs visualization (nodes + edges)
2. Siple graphs writing to file
3. Graph nodes are now manipulable and we can add nodes and link them using the QWidget gui, wa can also delete nodes.
4. User application is informed wen a new connection is created between two nodes, when a node is selected or when it is double clicked.
5. Only two supported node shapes (box or oval)
6. File parsing is not implemented yet
7. Advanced nodes coloring and shapes are not yet implemented
8. Subgraphs are not supported yet
9. Only the dot layout is partially implemented