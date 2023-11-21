import re

pattern = re.compile(
    r'(?P<a>\(\w+\))(?P<direction>(?:->)|(?:<-)|(?:--))(?P<b>\(\w+\))')


class Sommet():

    index_incr = 0

    def __init__(self, data):
        self.data = data
        self.voisins = []
        self.index = self.index_incr
        self.index_incr += 1

    def add_voisin(self, sommet):
        self.voisins.append(sommet)

    def remove_voisin(self, sommet):
        self.voisins.remove(sommet)

    def __str__(self):
        return f"{self.data}"

    def __repr__(self):
        return f"{self.data}"


class Graph():
    def __init__(self, filename):
        self.filename = filename
        self.sommets = []
        self.arcs = []
        self.read_file()

    def __str__(self):
        string = ""
        for sommet in self.sommets:
            string += f"{sommet.data} -> {sommet.voisins}\n"

        return string

    def add_arc(self, a, b):
        self.arcs.append((a, b))
        a.add_voisin(b)

    def read_file(self):
        with open(self.filename) as f:
            for line in f:
                if line[0] == '/':
                    continue

                match = pattern.match(line)
                if match:
                    a = match.group('a')
                    b = match.group('b')

                    a_sommet = Sommet(a)
                    b_sommet = Sommet(b)
                    self.sommets.append(a_sommet)
                    self.sommets.append(b_sommet)

                    direction = match.group('direction')
                    if direction == '->':
                        self.add_arc(a_sommet, b_sommet)
                    elif direction == '<-':
                        self.add_arc(b_sommet, a_sommet)
                    elif direction == '--':
                        self.add_arc(a_sommet, b_sommet)
                        self.add_arc(b_sommet, a_sommet)
                else:
                    print("syntax error in line", line)
                    exit(1)

    def get_nb_sommets(self):
        return len(self.sommets)

    def get_nb_arcs(self):
        return len(self.arcs)

    def get_sommets(self):
        return self.sommets
