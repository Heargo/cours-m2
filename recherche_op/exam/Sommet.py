class Sommet():

    def __init__(self, label, index):
        self.label = label
        self.voisins = []

        self.index = index

    def add_voisin(self, label):
        self.voisins.append(label)

    def remove_voisin(self, sommet):
        if (label in self.voisins):
            self.voisins.remove(label)

    def get_voisins(self):
        return self.voisins

    def get_label(self):
        return self.label

    def has_voisin(self, sommet):
        for voisin in self.voisins:
            if voisin.label == sommet:
                return True
        return False

    def __str__(self):
        return f"{self.label}"

    def __repr__(self):
        return f"{self.label}"
