# QGraphViz
A PyQT based GraphViz builder/renderer

## Introduction

I was searching a handy tool to code graphs using python then visualize them within my software. I found about graphviz which is a great tool to build graphs.
The problem is that you need to install the graphviz software in order to compile your file and render it.
There is a graphviz package on PYPI that allows creating dot code that can then be processed by graphviz, but in practice, you need to install graphviz and somehow add it to your path in order to execute the render command.

PyGraphviz is another package that can be used. But as you can read in their documentation, you still need to install Graphviz.

I also found this visualizer based on pyQt4. It is a simple Qt based visualizer that tracks the updates on the .gv file and redraws it in realtime:
DDorch/GraphVizLiveUpdateViewer

So since I didn't find any package out there that satifies my needs, I decided to create a pyQT5 based Graphviz tool that can visualize Graphviz code without the need to install Graphviz and provide it with MIT licence, so that other people can simply use it in their software.

## Objective

Build python pyQT5 based QWidget that can visualize graphs and allow realtime interaction with graphs add edges and nodes, change attributes ...
## Requirements

As its name suggests, this module needs you to install pyqt5 first.
```bash
pip install pyqt5
```

## Installation
```bash
pip install QGraphViz
```

## Actual status
1. Simple nodes with a very simplified Dot engine is working
2. Graph nodes are not yet manipulable
3. File parsing is not implemented yet