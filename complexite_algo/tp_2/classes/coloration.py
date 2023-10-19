from random import randint


class Coloration():
    COLORS = ["red", "green", "blue"]

    def __init__(self, graphe):
        self.graphe = graphe
        self.couleurs = {}

    def random_coloration(self):
        couleurs = {}
        graph = self.graphe.get_graph()
        for node in graph:
            couleurs[node] = self.COLORS[randint(0, len(self.COLORS)-1)]
        return couleurs

    def is_color_ok(self, node):
        for voisin in self.graphe.get_voisin(node):
            if self.couleurs[node] == self.couleurs[voisin]:
                return False
        return True

    def verify(self):
        # print("Verification du graph")
        incorrect_node = []
        for node in self.graphe.get_graph().keys():
            if not self.is_color_ok(node):
                # print("le graph n'est pas bon car le noeud", node, "est mal coloré")
                incorrect_node += [node]
        return incorrect_node

    def change_color(self, node, color="random"):
        if color == "random":
            previous_color = self.couleurs[node]
            while self.couleurs[node] == previous_color:
                self.couleurs[node] = self.COLORS[randint(
                    0, len(self.COLORS)-1)]
        else:
            self.couleurs[node] = color
        return self.couleurs[node]

    def is_colored(self, node):
        return node in self.couleurs

    def remove_color(self, node):
        if node in self.couleurs:
            del self.couleurs[node]
