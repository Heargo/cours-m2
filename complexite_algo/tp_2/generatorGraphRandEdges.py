# coding=utf-8

from random import random
from sys import argv


def generateGraph(s, p, filename):

    edges = []
    for i in range(s):
        for j in range(i+1,s):
            if random() < p:
                edges.append((i,j))
    nb_edges = len(edges)

    with open(filename,'w') as file:
        file.write("c\n")
        file.write("c Random graph with " + str(size) + " vertices.\n")
        file.write("c Each edge appears with probability " + str(p) + ".\n")
        file.write("c\n")
        file.write("p edge " + str(size) + " " + str(nb_edges) + "\n")
        for e in edges:
            file.write("e " + str(e[0]) + " " + str(e[1]) + "\n")



if __name__ == '__main__':
    if len(argv) <= 3:
        print("Usage: python generatorGraphRandEdges.py <size_graph> <probability_edge> <output_file>")
        exit(1)

    try:
        size = int(argv[1])
    except TypeError:
        print("The first argument is the size of the graph and should be an integer.")
        exit(1)

    if size <= 1:
        print("The size of the graph should be larger than one.")
        exit(1)

    try:
        proba = float(argv[2])
    except TypeError:
        print("The second argument is the probability of an edge and should be a float.")
        exit(1)

    file_output = argv[3]

    generateGraph(size, proba, file_output)
