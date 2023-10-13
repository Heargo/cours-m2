#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import math
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------

def distance(point1, point2):
    """
    Calcule la distance euclidienne entre deux points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def fctAlgo(points):
    """
    Trouve la distance minimale parmi toutes les paires de points en utilisant une approche naïve.
    """
    n = len(points)
    # Initialisation a la distance entre les deux premiers points
    min_distance = distance(points[0], points[1])

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            min_distance = min(min_distance, dist)

    return min_distance


def fctAlgo2(points):
    """
    Trouve la distance minimale parmi toutes les paires de points en utilisant l'approche Diviser pour Régner.
    :param points: Une liste de points, chaque point étant une paire (x, y).
    :return: La distance minimale entre deux points.
    """
    n = len(points)

    # Trier les points par coordonnée x
    points.sort(key=lambda x: x[0])

    # Diviser les points en deux moitiés
    mid = n // 2
    left_half = points[:mid]
    right_half = points[mid:]

    # Diviser pour régner récursivement sur les deux moitiés
    min_left = fctAlgo2(left_half)
    min_right = fctAlgo2(right_half)

    # Trouver la distance minimale entre les deux moitiés
    min_dist = min(min_left, min_right)

    # Trouver les points de la bande centrale
    strip = [point for point in points if abs(
        point[0] - points[mid][0]) < min_dist]

    # Trier les points de la bande centrale par coordonnée y
    strip.sort(key=lambda x: x[1])

    # Parcourir la bande centrale pour trouver des distances plus courtes
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] >= min_dist:
                break
            dist = distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)

    return min_dist


# -----  Fonction mère (normalement il n'y a pas à modifier la suite)  ------

#  Aide indiquant comment utiliser notre fonction
def usage(nom):
    print("Usage : " + nom + " file")
    print("  Importe un fichier file listant un ensemble d'entiers et")
    print("  applique votre algorithme sur cette liste d'entiers.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ce programme nécessite un fichier en argument.")
        usage(sys.argv[0])
        exit(1)

    verbose = True
    if len(sys.argv) >= 3 and sys.argv[1] == "--mute":
        verbose = False
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]

    tab = []
    file = open(filename, "r")
    try:
        next(file)
        for line in file:
            tab.append(int(line))  # TODO CHANGE TO POINTS
    finally:
        file.close()
    if verbose:
        print("Input: ")
        print(tab)

    val = fctAlgo(tab)

    if verbose:
        print("Output: ")
        print(val)
