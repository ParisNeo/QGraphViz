#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""
from dot_parser.graph import Graph
from dot_parser.node import Node
from dot_parser.edge import Edge

class DotParser():
    """
    The dot language parser
    """
    def __init__(self):
        pass
    
    def parseFile(self, filename):
        with open(filename, "r"):
            pass # TODO implement file loading