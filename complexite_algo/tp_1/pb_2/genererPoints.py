#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import argparse
import sys
from random import randrange

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generates points in the plane.')
    parser.add_argument('size', metavar='S', type=int,
                   help='number of points')
    parser.add_argument('--range', type=int, metavar= 'R', dest = 'range', default=-1, \
        help='range of the coordinates (default R=S^2)')
    parser.add_argument('--tempFile', type=str, metavar= 'F', dest = 'tfile', default="", \
        help='name of the temporary file (default F="pointsListe_S")')
    args = parser.parse_args()
    S = args.size
    if args.tfile == "":
        F = "pointsListe_"+str(S)
    else:
        F = args.tfile
    if args.range >=0:
        R = args.range
    else:
        R = S*S

    f = open(F,"w+")
    try:
        f.write('Liste de '+str(S)+' points :\n')
        for i in range(S):
            f.write(str(randrange(R))+' '+str(randrange(R))+'\n')
    finally:
        f.close()

