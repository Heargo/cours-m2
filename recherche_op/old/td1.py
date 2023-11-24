from graph import Graph
import random
# Exercice 1 Construire un graphe orienté dont les sommets sont les entiers compris entre 1 et 12 et dont les arcs repré sentent
# la relation « ê tre diviseur de ».


def exo_1():
    g = Graph("./graph.txt")
    print(g)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# (loup) can't have a commun sommet with (chevre) if (fermier) is not in a commun sommet with (loup)


def loup_chevre_ok(g):
    return len(intersection(g.get_sommet("(loup)").get_voisins(), g.get_sommet("(chevre)").get_voisins())) > 0 and len(intersection(g.get_sommet("(fermier)").get_voisins(), g.get_sommet("(loup)").get_voisins())) > 0

# (chevre) can't have a commun sommet with (chou) if (fermier) is not in a commun sommet with (chevre)


def chevre_chou_ok(g):
    return len(g.get_sommet("(chevre)").get_voisins().intersection(g.get_sommet("(chou)").get_voisins())) > 0 and len(g.get_sommet("(fermier)").get_voisins().intersection(g.get_sommet("(chevre)").get_voisins())) > 0


def move_node(g, node):
    current_rive = g.get_sommet("(rive_1)") if g.get_sommet(
        node.data).has_voisin("(rive_1)") else g.get_sommet("(rive_2)")

    next_rive = g.get_sommet(
        "(rive_2)") if current_rive.data == "(rive_1)" else g.get_sommet("(rive_1)")

    g.remove_arc(current_rive, node, both=True)
    g.remove_arc(current_rive, g.get_sommet("(fermier)"), both=True)

    g.add_arc(next_rive, node, both=True)
    g.add_arc(next_rive, g.get_sommet("(fermier)"), both=True)

    print("moved", node)
    return g


def valid_node_to_move(g, node):
    if node.data == "(fermier)" or node.data == "(rive_1)" or node.data == "(rive_2)":
        return False

    print("try to move", node, type(node))
    attemp = g.copy()
    attemp = move_node(attemp, attemp.get_sommet(node.data))

    return loup_chevre_ok(attemp) and chevre_chou_ok(attemp)


def exo_2():
    g = Graph("./fermier.txt")
    print(g)
    # add rive_2
    g.add_sommet("(fermier)")
    g.add_sommet("(rive_2)")

    finished = False
    i = 0
    while not finished and i < 10:
        # check if the game is over
        if len(g.get_sommet("(rive_2)").get_voisins()) == 4:
            print("Game over well done !")
            break

        # select random node to move from rive_1 or rive_2 if rive_1 is empty
        rive = g.get_sommet("(rive_1)").get_voisins()
        if (len(rive) == 0):
            rive = g.get_sommet("(rive_2)").get_voisins()
        random_node = rive[random.randint(
            0, len(rive)-1)]
        print("picked", random_node, type(random_node))
        valid = valid_node_to_move(g, random_node)
        if (valid):
            g = move_node(g, random_node)
            print("moved", random_node)
            print(g)
            continue

        while not valid and i < 10:
            print("can't move", random_node)

            # select random node to move from rive_1 or rive_2 if rive_1 is empty
            rive = g.get_sommet("(rive_1)").get_voisins()
            print("rive I'm trying to take from", rive)
            if (len(rive) == 0):
                print("taking from rive_2")
                rive = g.get_sommet("(rive_2)").get_voisins()

            random_node = rive[random.randint(
                0, len(rive)-1)]
            valid = valid_node_to_move(g, random_node)
            i += 1


exo_2()
