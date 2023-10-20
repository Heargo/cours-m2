from collections import deque
from classes import graph, coloration
from random import randint

###############################################
#               SolvBacktracking              #
###############################################


def solve_backtracking_rec(graph, coloriage, node):
    choices = {}
    # pick a random color for the node that is not in choices and is not in the neighbors
    picked = pick_valid_color(graph, coloriage, choices, node)
    # if no color is possible, remove color and return false
    if not picked:
        coloriage.remove_color(node)
        # print(f"<{node}> can't choose a color, sending backtring signal")
        return False

    nb_colored = 0
    while picked and nb_colored < len(graph.get_voisin(node)):
        for neighbor in graph.get_voisin(node):
            # skip neighbors that are already colored
            if (coloriage.is_colored(neighbor)):
                nb_colored += 1
            else:
                res = solve_backtracking_rec(
                    graph, coloriage, neighbor)
                if res == False:
                    # print(f"<{node}> {neighbor} said he's stuck, picking another color")
                    picked = pick_valid_color(graph, coloriage, choices, node)
                else:
                    coloriage = res

    return coloriage


def solve_backtracking(graph):
    coloriage = coloration.Coloration(graph)
    node = list(graph.get_graph().keys())[3]
    return solve_backtracking_rec(graph, coloriage, node), len(coloriage.couleurs) == len(graph.get_graph())

###############################################
#                 SolvRandom                  #
###############################################


def impossible(choices):
    res = True
    for node in choices:
        if len(choices[node]) < len(coloration.Coloration.COLORS):
            return False
    return res


def solve_random(graph):
    coloriage = coloration.Coloration(graph)
    coloriage.couleurs = coloriage.random_coloration()
    incorrect_nodes = coloriage.verify()
    choices = {}
    # get all the colors that are already used
    for node in coloriage.couleurs:
        choices[node] = [coloriage.couleurs[node]]

    while len(incorrect_nodes) > 0 and not impossible(choices):
        rand_node = incorrect_nodes[randint(0, len(incorrect_nodes)-1)]
        new_color = coloriage.change_color(rand_node)
        choices[rand_node].append(new_color)
        incorrect_nodes = coloriage.verify()

    return coloriage, len(incorrect_nodes) == 0


def pick_valid_color(graph, coloriage, choices, node):
    # get neighbors colors
    neighbors_colors = []
    for neighbor in graph.get_voisin(node):
        if (neighbor in coloriage.couleurs):
            neighbors_colors.append(coloriage.couleurs[neighbor])

    for color in coloration.Coloration.COLORS:
        if color not in choices and color not in neighbors_colors:
            choices[node] = color
            coloriage.change_color(node, color)
            # print(f"<{node}> is now {color}")
            return True

    return False

###############################################
#                 SolvLawler                  #
###############################################


def is_independent(graph, subset):
    # Fonction pour vérifier si le sous-ensemble est indépendant
    for vertex in subset:
        neighbors = graph[vertex]
        if any(neighbor in subset for neighbor in neighbors):
            return False
    return True


def is_bipartite(graph):
    if not graph:
        return True  # Un graphe vide est biparti par définition.
    # Dictionnaire pour suivre l'état de chaque sommet : -1 pour non visité, 0 pour couleur 0, 1 pour couleur 1.
    visited = {}
    queue = deque()
    colors = {}
    for vertex in graph:
        colors[vertex] = -1

    for vertex in graph:
        if vertex not in visited:
            queue.append(vertex)
            visited[vertex] = 0  # Colorier le premier sommet en 0.

            while queue:
                current = queue.popleft()
                current_color = visited[current]

                for neighbor in graph[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        # Alterner les couleurs 0 et 1.
                        visited[neighbor] = 1 - current_color
                    elif visited[neighbor] == current_color:
                        # Deux sommets adjacents ont la même couleur, le graphe n'est pas biparti.
                        return False

    return True


def get_all_subsets(nodes, size):
    # Fonction pour générer tous les sous-ensembles de taille donnée
    if size == 0:
        return [[]]

    subsets = []
    for i in range(len(nodes)):
        node = nodes[i]
        # Génère tous les sous-ensembles de taille size-1 à partir du noeud actuel
        for subset in get_all_subsets(nodes[i + 1:], size - 1):
            subsets.append([node] + subset)

    return subsets


def SolvLawler(graph):
    vertices = list(graph.keys())
    for i in range(1, len(vertices) + 1):
        subsets = get_all_subsets(vertices, i)
        for subset in subsets:
            complement = set(vertices) - set(subset)
            if is_independent(graph, subset) and is_bipartite(complement):
                return True
    return False

###############################################
#                    Main                     #
###############################################


if __name__ == "__main__":
    graph = graph.Graph("../instances/test_nok_2.txt")

    # backtracking
    coloriage, colorable = solve_backtracking(graph)
    print("BACKTRACKING Colorable :", colorable,
          "coloriage:", coloriage.couleurs)

    # random
    coloriage, colorable = solve_random(graph)
    print("RANDOM Colorable :", colorable, "coloriage:", coloriage.couleurs)

    # lawler
    # colorable = SolvLawler(graph.get_graph())
    # print("LAWLER Colorable :", colorable)

    # tests
    # graph1 = {
    #     'A': ['B', 'C'],
    #     'B': ['A', 'C'],
    #     'C': ['A', 'B'],
    # }
    # subset1 = {'A', 'B'}

    # graph2 = {
    #     'A': ['B'],
    #     'B': ['A'],
    #     'C': [],
    # }
    # subset2 = {'A', 'B'}

    # # Testez la fonction avec les cas de test
    # result1 = is_bipartite(graph1, subset1)
    # result2 = is_bipartite(graph2, subset2)

    # # Vérifiez les résultats
    # if result1:
    #     print("Le complément du sous-ensemble est biparti.")
    # else:
    #     print("Le complément du sous-ensemble n'est pas biparti.")

    # if not result2:
    #     print("Le complément du sous-ensemble n'est pas biparti.")
    # else:
    #     print("Le complément du sous-ensemble est biparti.")
