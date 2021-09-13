This file aims to explain very fast what the xxx.py are supposed to be.

    - arc-graphs.py:                wanted to draw some arc-graphs. There is a custom plot available (using matplotlib) and a support for igraph module.
    - gallai.py:                    illustration of Gallai's result on interval graphs: max disjoint set and coloration.
    - IG_edgeCol_square_graph.py:   Attempt at using the "super graph coloring" to find an edge coloration. It is not finished as you told me it was unecessary. 
    - intersection_graph.py:        generates box-like elements and plot the associated intersection graph using igraph. It was the first xxx.py written, so it introduces a lot of functions widely used in the others, for instance: intersection(); fill_edges(), etc.
    - k-regular.py:                 randomly generates 3-reg graphs of size 8. 
    - LF_3-reg.py:                  finds all 3-reg graphs of size 8.
    - library_debugg & library.py:  file used to prove the result of the library problem. Of course I did not realized at the time the property about tree graphs and their number of edges
    - peterson_graph/py:            file used to plot a box-realization of peterson graph. I think it may be useful for you to take a glance at it as you mentionned it last time we met.
    -SU_om2_ksip4.py:               generate US graph by drawing the squares in the first place, then post treatment involving: removing bridges, vertices of degree 1 & vertices of d2 that have neighbours of d2. 
    
The files should contain enough comments about technical details. If you have any question, feel free to mail me, even if the internship is over !