#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import argparse
from random import randrange

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Generates a random game of size S.')
    parser.add_argument('size', metavar='S', type=int,
                        help='size of the game')
    parser.add_argument('--range', type=int, metavar='R', dest='range', default=-1,
                        help='range of the integers (default R=3*S)')
    parser.add_argument('--tempFile', type=str, metavar='F', dest='tfile', default="",
                        help='name of the temporary file (default F="integersList_S")')
    args = parser.parse_args()
    S = args.size
    if args.tfile == "":
        F = "integersList_"+str(S)
    else:
        F = args.tfile
    if args.range >= 0:
        R = args.range
    else:
        R = 3*S

    f = open(F, "w+")
    try:
        f.write("Nouvelle partie !\n")
        f.write(str(0)+'\n')
        for i in range(S):
            f.write(str(randrange(R))+'\n')
        f.write(str(0))
    finally:
        f.close()
