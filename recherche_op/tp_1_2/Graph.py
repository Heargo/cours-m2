import re
import numpy as np
from Sommet import Sommet

pattern = re.compile(
    r'(?P<a>\w+)(?P<direction>(?:-(-|[0-9]*)->)|(?:<-(-|[0-9]*)-)|(?:-(-|[0-9]*)-))(?P<b>\w+)')


class Graph():
    def __init__(self, filename, first=1):
        self.filename = filename
        self.sommets = []
        self.arcs = []
        self.read_file()
        self.first = first

    def copy(self):
        g = Graph(self.filename)
        g.sommets = self.sommets.copy()
        g.arcs = self.arcs.copy()
        return g

    def __str__(self):
        string = ""
        for sommet in self.sommets:
            string += f"{sommet.label} -> {sommet.voisins}\n"
        return string

    def add_sommet(self, label):
        for s in self.sommets:
            if s.label == label:
                return s

        print(f"add sommet {label}")
        s = Sommet(label)
        self.sommets.append(s)
        return s

    def add_arc(self, a, b, w, both=False):
        self.arcs.append((a, b, w))
        # print(f"add arc {a} -> {b} | {type(a)} -> {type(b)}")
        a.add_voisin(b)
        if both:
            self.add_arc(b, a)

    def remove_arc(self, a, b, both=False):
        for arc in self.arcs:
            if (arc[0] == a and arc[1] == b) or (both and arc[0].label == b and arc[1].label == a):
                self.arcs.remove(arc)
                a.remove_voisin(b)
                if both:
                    self.remove_arc(b, a)
                return

    def get_matrice_adjacence(self):
        matrice_adjacence = []
        for i in range(len(self.sommets)):
            matrice_adjacence.append([0]*len(self.sommets))

        for arc in self.arcs:
            matrice_adjacence[arc[0].index -
                              self.first][arc[1].index-self.first] = 1

        return np.array(matrice_adjacence)

    def get_matrice_adjacence_pondere(self):
        matrice_adjacence = []
        for i in range(len(self.sommets)):
            matrice_adjacence.append([0]*len(self.sommets))

        for arc in self.arcs:
            matrice_adjacence[arc[0].index-self.first][arc[1].index -
                                                       self.first] = arc[2]

        return np.array(matrice_adjacence, dtype=np.float64)

    def dijkstra(self, start):
        matrice_adjacence = self.get_matrice_adjacence_pondere()
        matrice_adjacence[matrice_adjacence == 0] = np.inf
        d = matrice_adjacence.copy()
        # put 0 in diagonal of d
        np.fill_diagonal(d, 0)
        # calculer le chemin le plus court entre start et tous les autres sommets
        for k in range(len(matrice_adjacence)):
            for i in range(len(matrice_adjacence)):
                for j in range(len(matrice_adjacence)):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]

        return d[start-self.first]

    def dijkstra_with_path(self, start, end):
        matrice_adjacence = self.get_matrice_adjacence_pondere()
        matrice_adjacence[matrice_adjacence == 0] = np.inf
        d = matrice_adjacence.copy()
        # put 0 in diagonal of d
        np.fill_diagonal(d, 0)
        path = d.copy()
        # calculer le chemin le plus court entre start et tous les autres sommets
        for k in range(len(matrice_adjacence)):
            for i in range(len(matrice_adjacence)):
                for j in range(len(matrice_adjacence)):
                    if d[i][j] > d[i][k] + d[k][j]:
                        # store weight and where we come from
                        d[i][j] = d[i][k] + d[k][j]
                        path[i][j] = k

        path_final = []
        current = end
        while current != start:
            path_final.append(current)
            current = path[start-self.first][current-self.first]
        print("path final", path)
        return path_final

    def floyd(self):
        w = self.get_matrice_adjacence_pondere()
        p = w.copy()
        w[w == 0] = float('inf')
        np.fill_diagonal(w, 0)
        for i in range(len(p)):
            for j in range(len(p[i])):
                if (p[i, j] != 0):
                    p[i, j] = j

        for k in range(len(w)):
            for i in range(len(w)):
                for j in range(len(w)):
                    if w[i][j] > w[i][k] + w[k][j]:
                        w[i][j] = w[i][k] + w[k][j]
                        p[i][j] = k

        return w, p

    # Fait comme floyd mais avec les chemins
    def floyd_path(p, start, end):
        if (p[start, end] == end):
            return [start, end]
        else:
            return floyd_path(p, start, p[start, end]) + floyd_path(p, p[start, end], end)[1:]

    def get_degre_entrant(self, sommet):
        matrice_adjacence = self.get_matrice_adjacence()
        degre_entrant = 0
        for i in range(len(matrice_adjacence)):
            degre_entrant += matrice_adjacence[i][sommet.index-self.first]
        return degre_entrant

    def get_degre_sortant(self, sommet):
        matrice_adjacence = self.get_matrice_adjacence()
        return sum(matrice_adjacence[sommet.index-self.first])

    def get_nb_sommets(self):
        return len(self.sommets)

    def get_nb_arcs(self):
        return len(self.arcs)

    def get_sommets(self):
        return self.sommets

    def get_sommet(self, label):
        for s in self.sommets:
            if s.label == str(label):
                return s
        raise Exception(f"Sommet with label {label} not found")

    def nb_sommet_at_distance(self, sommet, distance):
        matrice_adjacence = self.get_matrice_adjacence()
        matrice_distance = matrice_adjacence.copy()

        for i in range(distance-1):
            matrice_distance = matrice_distance.dot(matrice_adjacence)

        return matrice_distance[self.get_sommet(str(sommet)).index-self.first].sum()

    def distance_minimal(self, a, b):
        sommet_a = self.get_sommet(a)
        sommet_b = self.get_sommet(b)

        matrice_adjacence = self.get_matrice_adjacence()
        matrice_distance = matrice_adjacence.copy()

        # max distance is the number of sommets
        for i in range(len(self.sommets)):
            if (matrice_distance[a-self.first][b-self.first] == 1):
                return i + 1
            matrice_distance = matrice_distance.dot(matrice_adjacence)

        return -1

    def nb_composantes_connexes_not_optimized(self):
        matrice_adjacence = self.get_matrice_adjacence()
        matrice_distance = matrice_adjacence.copy()
        matrice_distance = matrice_distance + np.identity(len(self.sommets))

        for i in range(len(self.sommets)):
            matrice_distance = matrice_distance.dot(matrice_distance)
            matrice_distance[matrice_distance > 1] = 1

        print("connexes\n", matrice_distance)
        # find the number of biggest square full of 1 in the matrix
        connexes = []
        diag_used_in_connexes = []
        for i in range(len(self.sommets)):
            if (i in diag_used_in_connexes):
                continue

            current_diag = matrice_distance[i, i]
            # while there is ones in the square starting at i,i (top,left corner), increase the size of the square
            size = 0
            valid = True
            while valid and i+size <= len(self.sommets):
                square = matrice_distance[i:i+size, i:i+size]
                # if 0 in square valid = False
                if 0 in square:
                    valid = False
                    square = matrice_distance[i:i+size-1, i:i+size-1]
                else:
                    size += 1

            # add the diag used in the square to the list of diag used
            for j in range(size):
                diag_used_in_connexes.append(i+j-1)
            connexes.append(square)

        return len(connexes)

    def nb_composantes_connexes(graph):
        """
        This code does the same as the methods before but suppose that dist will never have paterns like the following matrice
        [[1. 1. 1. 1.]
        [0. 1. 1. 0. ]
        [0. 1. 1. 1. ]
        [0. 0. 1. 1. ]]
        I don't understand why it's the case and can't find a counter example. It piss me off.
        """
        dist = graph.get_matrice_adjacence()
        dist = dist + np.identity(len(graph.sommets))
        for i in range(len(dist)):
            dist = dist.dot(dist)
            dist[dist > 1] = 1
        cc_count = 1
        for i in range(len(dist)):
            if dist[i][cc_count-1] == 0:
                cc_count += 1
        return cc_count

    def get_rangs(self):
        matrice_adjacence = self.get_matrice_adjacence()
        rangs = {}
        for i in range(1, len(matrice_adjacence)):
            if (self.get_degre_entrant(self.get_sommet(i)) == 0):
                rangs[i] = 0
            else:
                rangs[i] = None
        for x in range(0, len(matrice_adjacence)-self.first):
            for k in range(0, len(matrice_adjacence)-self.first):
                if (rangs[k] == None):
                    pred = np.argwhere(matrice_adjacence[:, k-1] > 0)
                    tous_def = True
                    predecesseur = pred.reshape(-1)
                    for c in predecesseur:
                        if (rangs[c-self.first] == None):
                            tous_def = False
                            break
                    if (tous_def):
                        rangs[k] = rangs[max(predecesseur+1)] + 1
        return rangs

    def read_file(self):
        with open(self.filename) as f:
            for line in f:
                if line[0] == '/':
                    continue

                match = pattern.match(line)
                if match:
                    a = match.group('a')
                    b = match.group('b')

                    a_sommet = self.add_sommet(a)
                    b_sommet = self.add_sommet(b)

                    direction = match.group('direction')
                    weight = direction[1:-1].replace('-', '')
                    weight = 1 if weight == '' else int(weight)
                    if '>' in direction:
                        self.add_arc(a_sommet, b_sommet, weight)
                    elif '<' in direction:
                        self.add_arc(b_sommet, a_sommet, weight)
                    else:
                        self.add_arc(a_sommet, b_sommet, weight)
                        self.add_arc(b_sommet, a_sommet, weight)
                else:
                    print("syntax error in line", line)
                    exit(1)
