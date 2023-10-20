# coding=utf-8

import sys
from pycosat import solve as solveSAT
from pysat.card import *
from classes import graph
from itertools import combinations
from solve3ColorSat import solve3Coloring

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : python3 solveClique.py <filename> [-v]")
        exit(1)
    filename = sys.argv[1]
    if len(sys.argv) > 2 and (sys.argv[2] == "-v"
                              or sys.argv[2] == "--verbose"):
        verbose = True
    else:
        verbose = False

    g = graph.Graph(filename)

    g.inverse()

    has_3_clique = solve3Coloring(g, verbose)

    if has_3_clique:
        print("The graph has 3 cliques")
    else:
        print("The graph hasn't 3 cliques.")
