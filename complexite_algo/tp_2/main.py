from classes import graph, coloration
from random import randint


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


if __name__ == "__main__":
    graph = graph.Graph("./test_nok.txt")

    # backtracking
    coloriage, colorable = solve_backtracking(graph)
    print("BACKTRACKING Colorable :", colorable,
          "coloriage:", coloriage.couleurs)

    # random
    coloriage, colorable = solve_random(graph)
    print("RANDOM Colorable :", colorable, "coloriage:", coloriage.couleurs)
