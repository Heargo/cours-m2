# coding=utf-8

import sys
from pycosat import solve as solveSAT
from pysat.card import *
from classes import graph


def solveClique(g, size, verbose):
    """
    Résout le problème Clique
    :param g: graphe G
    :param size: taille de la clique recherchée
    :return: cherche s'il existe une clique de taille
    `size' dans G.
    """

    # La suite est à compléter/modifier
    # (décommentez petit à petit les lignes commençant par #)

    if verbose:
        print("Graphe d'entrée")
        print(g)

    n = g.get_nb_sommets()

    """
    Nos variables seront X1,...,Xn
    On voudrait que Xi soit vraie si la clique contient le sommet (i-1)
    """
    variables = [i for i in range(1, n+1)]

    """
    On veut que la clique soit de taille `size'.
    Donc parmi les n variables X1,...,Xn, exactement `size' doivent
    être vraies.
    Déjà n variables sont utilisées, donc les nouvelles variables
    commenceront à n+1.
    """
    cnf = CardEnc.equals([i for i in range(1, n + 1)],
                         bound=size, top_id=n, encoding=EncType.seqcounter)

    """
    Pour chaque paire de sommets (u,v), si (u,v) n'est pas une arête,
    on rajoute la contrainte qu'une des extrémités ne doit pas appartenir
    à la clique.
    """
    for u in range(1, n+1):
        for v in range(1, u):
            if str(v) not in g.get_voisin(str(u)):
                cnf.append([-u, -v])

    if verbose:
        print("Entrée pour le SAT solveur")
        print(cnf)

    solutionSAT = solveSAT(cnf)
    if verbose:
        print("Solution pour SAT")
        print(solutionSAT)

    """
    Si le SAT-solver n'a pas trouvé de solution, il renvoit "UNSAT".
    Sinon, il renvoit une liste d'entiers [l1, l2, l3, ...]
    Si l1 = 1 alors X1 est True
    Si l1 = -1 alors X1 est False
    Les variables l(n+1), l(n+2), ... ont été créées pour la contrainte de
    cardinalité et ne nous intéressent pas.
    En conclusion, le noeud i-1 est dans la clique si i est dans solutionSAT
    """
    if solutionSAT != "UNSAT":
        solution = [i for i in solutionSAT[:n] if i > 0]
    else:
        solution = []
    return solution


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage : python3 solveClique.py <filename> <size_clique> [-v]")
        exit(1)
    filename = sys.argv[1]
    try:
        size = int(sys.argv[2])
    except:
        print("Le deuxième argument <size_clique> doit être un entier.")
        exit(1)
    if len(sys.argv) > 3 and (sys.argv[3] == "-v"
                              or sys.argv[3] == "--verbose"):
        verbose = True
    else:
        verbose = False

    g = graph.Graph(filename)
    print("g is", g.get_graph())

    solution = solveClique(g, size, verbose)

    print("Solution pour le problème Clique")
    if solution != []:
        print(solution)
    else:
        print("Pas de clique de taille " + str(size) + ".")
