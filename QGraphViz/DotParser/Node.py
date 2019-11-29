#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""

class Node():
    """
    The dot graphviz engine
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.pos=[0,0]
        self.size=[1,1]
        self.kwargs=kwargs
        # Nodes
        self.in_edges=[]
        self.out_edges=[]

    
