# coding=utf-8

import sys
from pycosat import solve as solveSAT
from pysat.card import *
from classes import graph
from itertools import combinations


def solve3Coloring(g, verbose):
    """
    Solves the 3-Coloring problem.
    :param g: graph G
    :return: True if the graph is 3-colorable, False otherwise.
    """

    if verbose:
        print("Input Graph")
        print(g)

    n = g.get_nb_sommets()

    # Variables for coloring vertices with 3 colors
    variables = [i for i in range(1, n + 1)]

    # List to store constraints
    cnf = []

    # Add constraints for each vertex
    for u in range(1, n + 1):
        # Each vertex must be assigned one of three colors
        cnf.append([variables[u-1] * 3 - i for i in range(0, 3)])
    print(cnf)

    # Add constraints for each edge
    for u, v in combinations(range(1, n + 1), 2):
        if str(v) in g.get_voisin(str(u)):
            # Ensure that adjacent vertices have different colors
            for i in range(0, 3):
                cnf.append([-(variables[u-1] * 3 - i), -
                           (variables[v-1] * 3 - i)])

    if verbose:
        print("Input for the SAT solver")
        print(cnf)

    solutionSAT = solveSAT(cnf)
    if verbose:
        print("Solution for SAT")
        print(solutionSAT)

    if solutionSAT != "UNSAT":
        return True
    else:
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : python3 solveClique.py <filename> <size_clique> [-v]")
        exit(1)
    filename = sys.argv[1]
    if len(sys.argv) > 2 and (sys.argv[2] == "-v"
                              or sys.argv[2] == "--verbose"):
        verbose = True
    else:
        verbose = False

    g = graph.Graph(filename)

    is_3_colorable = solve3Coloring(g, verbose)

    if is_3_colorable:
        print("The graph is 3-colorable.")
    else:
        print("The graph is not 3-colorable.")
