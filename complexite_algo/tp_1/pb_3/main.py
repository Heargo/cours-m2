#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys


# -----------------------   Votre algorithme   ------------------------------

def sommeMin(t, i):
    if i == 0:
        return 0

    opt = float('inf')

    for x in [1, 3, 5]:
        if x <= i:
            tmp = t[i] + sommeMin(t, i - x)
            if tmp < opt:
                opt = tmp

    return opt


mem = {0: 0}


def sommeMinMemo(t, n):
    if n not in mem:
        for i in range(1, n + 1):
            opt = float('inf')
            for x in [1, 3, 5]:
                if x <= i:
                    tmp = t[i] + sommeMinMemo(t, i-x)
                    if tmp < opt:
                        opt = tmp
            mem[i] = opt
    return mem[n]

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

    val = sommeMinMemo(tab, len(tab) - 1)

    if verbose:
        print("Output: ")
        print(val)
