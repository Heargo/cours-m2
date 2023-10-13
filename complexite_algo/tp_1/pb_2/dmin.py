#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# On définit une classe pour les points

class Point:
    x = 0
    y = 0

    def __init__(self, u, v):
        self.x = u
        self.y = v

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __str__(self):
        return "Point"

    def distance(self, autre):
        diff_x = self.x-autre.x
        diff_y = self.y-autre.y
        return sqrt(diff_x**2+diff_y**2)

    def cmp_x(self, autre):
        return (self.x < autre.x)

    def cmp_y(self, autre):
        return (self.y < autre.y)


# Fonctions de recherche de distance minimale.
# Le deuxième algorithme est à implémenter

#      Algorithme naïf quadratique
def distance_min_naive(L):
    if len(L) < 2:
        print("Il doit y avoir au moins deux points.")
        return 0
    else:
        daux = L[0].distance(L[1])
        for indA, a in enumerate(L):
            for indB, b in enumerate(L):
                if indA < indB:
                    if a.distance(b) < daux:
                        daux = a.distance(b)
        return daux

#      Algorithme amélioré vu en cours


def distance_min_dpr(points):
    '''
    Trouve la distance minimale entre deux points dans une liste de points.
    Complexité : O(n log n)
    '''
    n = len(points)

    # Cas de base
    if n < 3:
        return distance_min_naive(points)

    # Trier les points par coordonnée x
    points.sort(key=lambda point: point.x)

    # Diviser les points en deux moitiés
    mid = n // 2
    left_half = points[:mid]
    right_half = points[mid:]

    # Diviser pour régner récursivement sur les deux moitiés
    min_left = distance_min_dpr(left_half)
    min_right = distance_min_dpr(right_half)

    # Trouver la distance minimale entre les deux moitiés
    min_dist = min(min_left, min_right)

    # Trouver les points de la bande centrale
    strip = [point for point in points if abs(
        point.x - points[mid].x) < min_dist]

    # Trier les points de la bande centrale par coordonnée y
    strip.sort(key=lambda point: point.y)

    # Parcourir la bande centrale pour trouver des distances plus courtes
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j].y - strip[i].y >= min_dist:
                break
            dist = strip[i].distance(strip[j])
            min_dist = min(min_dist, dist)

    return min_dist


# Fonction mère (normalement il n'y a pas à modifier la suite)

#  Aide indiquant comment utiliser notre fonction
def usage(nom):
    print("Usage : " + nom + " METHODE file")
    print("  Importe un fichier file listant un ensemble de points dans")
    print("  le plan puis détermine la distance minimum entre deux de")
    print("  ces points.")
    print("  Valeurs valides pour METHODE :")
    print("  - naive -          Double boucle en O(n^2)")
    print("  - dpr -            Méthode diviser-pour-régner ")
    print("                       (algorithme à implémenter))")
    print("  - naive_muette -   comme naive mais sans sortie")
    print("  - dpr_muette -     comme dpr mais sans sortie")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Ce programme nécessite une méthode et un fichier en arguments.")
        usage(sys.argv[0])
        exit(1)

    mute = 0

    if sys.argv[1] == "naive":
        print("# [Méthode naïve]")
        fctDistMin = distance_min_naive
    elif sys.argv[1] == "naive_muette":
        fctDistMin = distance_min_naive
        mute = 1
    elif sys.argv[1] == "dpr":
        print("# [Méthode diviser-pour-régner]")
        fctDistMin = distance_min_dpr
    elif sys.argv[1] == "dpr_muette":
        fctDistMin = distance_min_dpr
        mute = 1
    else:
        print("Cette méthode n'existe pas.")
        usage(sys.argv[0])
        exit(1)

    filename = sys.argv[2]
    tab = []
    file = open(filename, "r")
    try:
        next(file)
        for line in file:
            CoupPoints = line.split()
            tab.append(Point(int(CoupPoints[0]), int(CoupPoints[1])))
    finally:
        file.close()
    if mute == 0:
        print("input : ", end="")
        print(tab)

    # Si besoin, on peut augmenter le nombre de récursions possible pour les méthodes récursives
        # sys.setrecursionlimit(10 ** 6)
        # resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
    val = fctDistMin(tab)
    if mute == 0:
        print(val)
