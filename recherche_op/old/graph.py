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
        if (sommet in self.voisins):
            self.voisins.remove(sommet)

    def get_voisins(self):
        return self.voisins

    def get_data(self):
        return self.data

    def has_voisin(self, sommet):
        for voisin in self.voisins:
            if voisin.data == sommet:
                return True
        return False

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

    def copy(self):
        g = Graph(self.filename)
        g.sommets = self.sommets.copy()
        g.arcs = self.arcs.copy()
        return g

    def __str__(self):
        string = ""
        printed_sommets = []
        for sommet in self.sommets:
            if (sommet.index in printed_sommets):
                continue
            string += f"{sommet.data} -> {sommet.voisins}\n"
            printed_sommets.append(sommet.index)

        return string

    def add_sommet(self, data):
        self.sommets.append(Sommet(data))

    def add_arc(self, a, b, both=False):
        self.arcs.append((a, b))
        print(f"add arc {a} -> {b} | {type(a)} -> {type(b)}")
        a.add_voisin(b)
        if both:
            self.add_arc(b, a)

    def remove_arc(self, a, b, both=False):
        for arc in self.arcs:
            if (arc[0] == a and arc[1] == b) or (arc[0].data == b and arc[1].data == a):
                self.arcs.remove(arc)
                a.remove_voisin(b)
                if both:
                    self.remove_arc(b, a)
                return

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

    def get_sommet(self, data):
        for s in self.sommets:
            if s.data == data:
                return s

        raise Exception(f"Sommet with data {data} not found")
