# coding=utf-8

from random import random, randrange
from sys import argv


def generateGraph(s, nb_edges, filename):

    proba = (float(nb_edges) / float(s * (s - 1) // 2)) + 0.05

    edges = []
    while len(edges) < nb_edges:
        edges = []
        for i in range(s):
            for j in range(i + 1, s):
                if random() < proba:
                    edges.append((i, j))
    while len(edges) > nb_edges:
        r = randrange(len(edges))
        edges.pop(r)

    with open(filename,'w') as file:
        file.write("c\n")
        file.write("c Random graph with " + str(size) + " vertices\n")
        file.write("c and " + str(nb_edges) + " edges.\n")
        file.write("c\n")
        file.write("p edge " + str(size) + " " + str(nb_edges) + "\n")
        for e in edges:
            file.write("e " + str(e[0]) + " " + str(e[1]) + "\n")


if __name__ == '__main__':
    if len(argv) <= 3:
        print("Usage: python generatorGraphFixedNumberEdges.py <size_graph> <number_edge> <output_file>")
        exit(1)

    try:
        size = int(argv[1])
        nb_edges = int(argv[2])
    except TypeError:
        print("The first argument is the size of the graph and should be an integer.")
        exit(1)

    if size <= 1:
        print("The size of the graph should be larger than one.")
        exit(1)

    all_edges = size * (size - 1) // 2
    if nb_edges < 0 or nb_edges > all_edges:
        print("The number of edges should be between 0 and " + str(all_edges))
        exit(1)

    file_output = argv[3]

    generateGraph(size, nb_edges, file_output)
