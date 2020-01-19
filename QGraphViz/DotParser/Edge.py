#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""

class Edge():
    """
    Describes edges that connect nodes
    """
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.kwargs={}

        source.out_edges.append(self)
        dest.in_edges.append(self)

    def toDICT(self):
        edge_dic = {}
        edge_dic["source"]=self.source.name
        edge_dic["dest"]=self.dest.name
        edge_dic["kwargs"]=self.kwargs
        return edge_dic
    
