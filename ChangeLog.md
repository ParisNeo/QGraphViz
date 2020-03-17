# ChangeLog

## V 0.0.39

Feature: Added the position to freeze the graph. This can be done either by activating autofreeze, or by calling freeze method of QGraphViz.

## V 0.0.38

Bugfix: Add edge bug due to loss of selected node before finishing the operation  if the event edge being added makes the QGraphViz widget loose focuse. This bug was introduced by Version 0.0.37

Added Node and subgraph color filling with possibility to use basic linear gradient

## V 0.0.37

Bugfix. Added ways to discard selection and hilighting when focus is lost

## V 0.0.33

Added mouse out event handler to reset selection when mouse leaves the qgraphviz widget

## V 0.0.32

Added node and edge hilighting options

## V 0.0.30

Code is reorganized
Added the possibility to set a css stylesheet for the QGraphViz widget

## V 0.0.29

Node shapes from images added by [Ederrod](https://github.com/Ederrod) and merged to the master branch.

## V 0.0.28

Added node removed and edge removed events.

## V 0.0.27

Added edge event. Now adding edge results in two events:

- The first event is new_edge_beingAdded_callback which asks the application to validate the edge adding. 
- The second event is new_edge_created_callback whicj informs the application that the edge is created

## V 0.0.26

Edge selection when more than a single edge is used between two nodes

## V 0.0.25

Added the possibility to add multiple edges between the same nodes two nodes
The cycles are still forbidden as they break the Dot engine

## V 0.0.24

Added save and load json format graphs

## V 0.0.21

Fixed subgraph loading code

## V 0.0.20

Better compatibility with Graphviz.
Clusters can now have graphviz style parameters
Semicolumn at the end of each line is no more needed

## V 0.0.19

Bugfix in opening files with clusters
Cluster paramters syntax is still incompatible with Standard GraphViz syntax:
    subgraph [parameters]{
        put nodes here
    }
