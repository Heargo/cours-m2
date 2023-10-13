#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------

#  L'argument l contient une liste d'entiers de taille n

def fctAlgo(l):
    '''
       Cet algorithme calcule la somme des éléments de la liste l.
       Complexité : O(n)
    '''
    somme = 0
    for i in range(len(l)):
        somme += l[i]

    return somme


def fctAlgo2(l):
    '''
       Cet algorithme creer une liste de taille n avec comme valeur la somme des éléments de la liste l.
       Complexité : O(n²)
    '''
    new_list = []
    for i in l:
        somme = 0
        for j in l:
            somme += j
        new_list.append(somme)

    return new_list


def fctAlgo3(l):
    '''
       Compte le nombre de boucles effectuées.
       Complexité : O(n^3)
    '''
    nb_boucles = 0
    for i in range(len(l)):
        for j in range(len(l)):
            for k in range(len(l)):
                nb_boucles += 1

    return nb_boucles


def fctAlgo4(l):
    '''
    Merge sort
    Complexité : O(n log(n))
    '''
    if len(l) <= 1:
        return l
    else:
        pivot = l[0]
        l1 = [x for x in l if x < pivot]
        l2 = [x for x in l if x > pivot]
        return fctAlgo4(l1) + [pivot] + fctAlgo4(l2)


def fctAlgo5(l):
    '''
    Compte le nombre de boucles effectuées.
    Complexité : O(exp(n))
    '''
    nb_boucles = 0
    for i in range(2**len(l)):
        nb_boucles += 1

    return nb_boucles


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
            tab.append(int(line))
    finally:
        file.close()
    if verbose:
        print("Input: ")
        print(tab)

    val = fctAlgo(tab)

    if verbose:
        print("Output: ")
        print(val)
