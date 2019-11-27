#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""
from QGraphViz.DotParser import Graph
from QGraphViz.DotParser import Node
from QGraphViz.DotParser import Edge

class DotParser():
    """
    The dot language parser
    """
    def __init__(self):
        pass
    
    def parseFile(self, filename):
        with open(filename, "r"):
            pass # TODO implement file loading