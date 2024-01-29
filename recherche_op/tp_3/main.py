from Graph import Graph
import numpy as np
from random import randint
from time import time
from parserCities import get_matrice_from_file, get_cities_positions_from_file
"""
# 1) Prendre le fichier defi250.csv
g = Graph("./defi250.csv")


# 2) Construire la matrice de distance euclidienne entre les 250 villes
# (lire avec la librairie csv (à l’aide de csv.reader(open(‘defi250.csv’, ‘’r’’),delimiter=‘’;’’)))ou
# avec panda; mettre inf sur la diagonale).
print("graph is", g)
print(f"matrice distance is\n {g.matrice_distance}")

# 3) Construire le première permutation des villes de 0 à 249 (par exemple dans l’ordre
# Sigma=(0,1,2,3,…,249) et évaluer la fonction distance F(Sigma)
chemin_basic = [i for i in range(250)]
print("distance from 0 tp 249 is", g.get_distance(chemin_basic))

# 4) Construire les 4 transformations locales
chemin_test = [i for i in range(5)]
print("chemin_test is", chemin_test)
# 4.1) Swap: échanger deux villes consécutives dans la permutation
print("swap 3 with next", g.swap_with_next(chemin_test, 3))
# 4.2) Insert: insérer une ville à une position donnée
print("insert 1 at 4", g.move_city_at(chemin_test, 1, 4))
# 4.3) SwapIndex: échanger deux villes à des positions données
print("swap 2 and 4", g.swap_indexes(chemin_test, 2, 4))
# 4.4) 2opt: inversement de l’ordre des villes entre deux positions données
print("2opt between 1 and 3", chemin_test,
      g.voisinage_2_opt(chemin_test, 4, 1))


# 6) Choisir aléatoirement un élément dans le voisinage de Sigma associé à l’une des
# transformations locales.
l = randint(1, 250)
a = randint(0, l)
b = randint(0, l)

chemin = [i for i in range(l)]
voisin = g.voisinage_2_opt(chemin, a, b)
print(f"opt2 on a:{a} b:{b}", voisin)


# fun
# chemin = [i for i in range(250)]
# best_chemin = g.best_chemin_stupid(chemin, max_iter=2000)
# print("best chemin is", best_chemin)
# print("distance best chemin is", g.get_distance(best_chemin))
# 14.073034864155504
# 13.978898672811631
# 13.433352938966683


# 9) On va construire une solution gloutonne, on part de la ville i, on rajoute la ville i dans une
# liste des villes déjà parcourue ensuite on va rajouter à la fin de la liste la ville non encore
# parcourue la plus proche de la ville i puis on part de la dernière ville rajoutée dans la liste et
# on rajoute à nouveau la ville non encore parcourue la plus proche et ainsi de suite pour
# obtenir Sigma
greedy = g.best_start_greedy()
print("distance greedy", g.get_distance(greedy))  # 14.181429278042408
# t = time()
# opti = g.best_chemin_less_stupid(greedy, max_iter=5000)
# print("distance opti", g.get_distance(opti))
# print("time", time() - t, "seconds (", (time() - t)/60, "minutes)")
# save opti chemin to opti.txt
# with open("opti_better.txt", "w") as f:
#     f.write(str(opti))
# g.show_chemin(greedy)

# 10) Recuit simulé

recuit_simule = g.recuit_simule()
print("distance recuit_simule", g.get_distance(recuit_simule))
# g.show_chemin(recuit_simule, step=0.1)

# use ant colony optimization
# aco = g.get_chemin_ant_algorithm(
#     num_ants=10, num_iterations=10, alpha=0.5, beta=0.5, evaporation_rate=0.1)

# print("distance aco", g.get_distance(aco))
"""
# Suite TP3

print("Cas réel")

g_128 = Graph(
    cities_position=get_cities_positions_from_file("./att532.tsp"))
# best_greedy = g_128.best_start_greedy()
# print("distance greedy", g_128.get_distance(best_greedy))
# recuit_simule = g_128.recuit_simule()
# print("distance recuit_simule", g_128.get_distance(recuit_simule))
# g_128.show_chemin(recuit_simule, step=0.01)


paths = g_128.get_n_optimal_paths(9)
print("best paths", paths)
g_128.show_multiples_paths(paths, step=0.001)
