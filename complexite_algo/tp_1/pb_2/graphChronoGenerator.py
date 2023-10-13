#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Utilise les libraries : python-numpy et gnuplot.
# sudo apt-get install python-numpy gnuplot

from json import load
from time import time
from math import log, sqrt, floor
from decimal import Decimal
from sys import float_info
import subprocess
import os

CONST_MIN_RUNTIME = 0.25
CONST_EPSILON = 1e-18


def getRunTime(execfile, genefile, tempfile, input):
    """
    Retourne le temps d'execution du programme ``execfile`` avec, en entree, le
    nombre ``input``.
    """
    nbIter = 0
    tps_generator = 0.0
    avant = time()
    while time() - avant < CONST_MIN_RUNTIME:
        debut_generator = time()
        subprocess.check_output("{} {} {}".format(
            genefile, tempfile, input), shell=True)
        tps_generator += time()-debut_generator
        subprocess.check_output("{} {}".format(execfile, tempfile), shell=True)
        nbIter += 1
    temps = (time() - avant-tps_generator)/nbIter
    return temps


def makeRuntimes(data):
    """
    Calcule les temps d'executions.
    """
    timings = []
    x = data['valeurInitiale']
    temps = 0
    wastedTimePerIteration = getRunTime(
        data['executable'], data['generator'], data['temp_file'], x)
    while x < data['borneSup'] and temps < data['attenteMax']:
        temps = getRunTime(data['executable'], data['generator'],
                           data['temp_file'], int(x)) - wastedTimePerIteration
        if temps < 1e-3:
            print("# Input {} is too small, insignificant timing.".format(x))
        else:
            print('# Input {}, {} millisecondes'.format(x, 1000*temps))
            timings.append((x, 1000*temps))
        x = eval(data['increment'])
    data['timings'] = timings


def optimizeCoeff(pts, func, logScale):
    """
    Calcule le coefficient multiplicatif qui permet d'aligner la fonction
    ``func`` aux donnees ``pts``. Il est important de noter que le coefficient
    calcule ne fait "fitter" qu'une seule valeur. Le choix de la valeur depend
    de l'utilisation, ou non, d'une echelle logarithmique lors de l'affichage
    des courbes."
    """
    f = eval("lambda x : " + func)
    minX = min(map(lambda xy: xy[0], pts))
    maxX = max(map(lambda xy: xy[0], pts))
    # print "minX is {} and maxX is {}.".format( minX, maxX)
    # if logScale :
    objectif = (sqrt(maxX * minX))
    # else :
    #  objectif = minX + ( (maxX - minX) / 2 )
    #     objectif = minX + ( sqrt(maxX - minX) / 10 )

    # definition de la fonction erreur
    midValues = pts[0]
    for x, y in pts:
        if abs(x - objectif) < abs(midValues[0] - objectif):
            midValues = (x, y)

    def erreur(coeff): return abs(coeff*f(midValues[0]) - midValues[1])

    try:
        # borne inf
        a = CONST_EPSILON
        err_a = erreur(a)

        # borne sup
        b = 1.0
        err_b = erreur(2*b)
        err_2b = erreur(2*b)
        while err_b > err_2b:
            b *= 2
            err_b = err_2b
            err_2b = erreur(2*b)

        # dichotomie
        l = []
        while b-a >= CONST_EPSILON:
            m = (a+b)/2
            if m == a or m == b:  # limit of float's precision
                return m
            if err_a < err_b:
                b = m
                err_b = erreur(b)
            else:
                a = m
                err_a = erreur(a)
        if err_a < err_b:
            return a
        else:
            return b
    except OverflowError:
        return 0


def findCoeff(data):
    """
    Calcule les coefficients multiplicatifs a ajouter a chacune des fonctions
    decrites dans l'entree "courbesSup".
    """
    data['coeff'] = []
    for f in data['courbesSup']:
        data['coeff'].append(optimizeCoeff(
            data['timings'], f, data['logScale']))


def buildGnuplotCommands(data):
    """
    Construit la liste des commandes pour configurer l'outil gnuplot....
    """
    commands = ''
    commands = 'set term pngcairo size {}\n'.format(data['outputImageSize'])
    if data['logScale']:
        commands += 'set logscale xy\n'
    commands += 'set output "{}"\n'.format(data['outputImageName'])
    commands += 'set xlabel "Input size"\n'
    commands += 'set ylabel "Runtime (millisec)"\n'
    xmin = min(map(lambda x: x[0], data['timings']))
    xmax = max(map(lambda x: x[0], data['timings']))
    ymin = min(map(lambda x: x[1], data['timings']))
    ymax = max(map(lambda x: x[1], data['timings']))
    commands += 'set xrange [{}:{}]\n'.format(xmin, xmax)
    commands += 'set yrange [{}:{}]\n'.format(ymin, ymax)
    commands += 'set key on left\n'.format(ymin, ymax)
    commands += 'set style func linespoints\n'
    commands += 'plot '
    i = 1
    for coeff, extraCurve in zip(data['coeff'], data['courbesSup']):
        curveName = "{:.2E}*{}".format(Decimal(coeff), extraCurve)
        commands += '{}*({}) ls {} title "{}", '.format(
            coeff, extraCurve, i, curveName)
        i += 1
    commands += '"-" using 1:2 with lines lw 2 lt rgb "black" title "Execution time"\n'
    commands += '\n'.join("{} {}".format(x, y) for x, y in data['timings'])
    commands += '\nreplot\n'
    data['gnuplotCommands'] = commands


def buildImageName(data):
    """
    Determine le nom a donner au fichier contenant l'image produite. Ce nom est
    determine en fonction de l'entree "outputImageNamePrefix" et des fichiers
    deja presents dans le dossier.

    Si python2.? au lieu de python3.? est installe sur votre ordinateur, commentez ces 
    lignes et modifier le nom directement dans testData.json. 
    """
    prefix = data['outputImageNamePrefix']
    s, o = subprocess.getstatusoutput("ls {}*.png".format(prefix))
    if s != 0:
        name = '{}-1.png'.format(prefix)
    else:
        o = o.split('\n')
        o = map(lambda x: x.split('-')[1], o)
        o = map(lambda x: x.split('.')[0], o)
        o = map(int, o)
        name = '{}-{}.png'.format(prefix, max(o)+1)
    data['outputImageName'] = name


if __name__ == '__main__':
    fichier = open('testData.json')
    data = load(fichier)
    fichier.close()
    makeRuntimes(data)
    findCoeff(data)
    buildImageName(data)
    buildGnuplotCommands(data)
    pipe = os.popen('gnuplot', 'w')
    pipe.write(data['gnuplotCommands'])
    pipe.close()
    print("Done, see {} for ouput.".format(data['outputImageName']))
