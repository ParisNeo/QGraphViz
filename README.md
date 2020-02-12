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
2. Simple gv files read/write
3. Graph nodes can hold custom parameters that can be used by the application
4. Graph nodes are now manipulable and we can add nodes and link them using the QWidget gui, wa can also delete nodes.
5. The application can accept or refuse edges creation and even add custom parameters to the edges
6. The nodes can be double clicked and an event is sent to the application allowing it to do custom
7. User application is informed wen a new connection is created between two nodes, when a node is selected or when it is double clicked.
8. User application is informed when a edge is selected or double clicked.
9. Only two supported node shapes (box or oval)
10. Advanced nodes shapes are not yet implemented
11. Subgraphs are not supported yet
12. Only the dot layout is implemented


## Example code
You can find an example code for manipulating graphs in examples/QGraphViewer.py.

## Changelog
### V 0.0.19 :
Bugfix in opening files with clusters
Cluster paramters syntax is still incompatible with Standard GraphViz syntax:
    subgraph [parameters]{
        put nodes here
    }
### V 0.0.20 :
Better compatibility with Graphviz.
Clusters can now have graphviz style parameters
Semicolumn at the end of each line is no more needed

### V 0.0.21 :
Fixed subgraph loading code

### V 0.0.24 :
Added save and load json format graphs

### V 0.0.25 :
Added the possibility to add multiple edges between the same nodes two nodes
The cycles are still forbidden as they break the Dot engine

### V 0.0.26 :
Edge selection when more than a single edge is used between two nodes

### V 0.0.27 :
Added edge event. Now adding edge results in two events:
 - The first event is new_edge_beingAdded_callback which asks the application to validate the edge adding. 
 - The second event is new_edge_created_callback whicj informs the application that the edge is created
### V 0.0.28 :
Added node removed and edge removed events.