from Graph import Graph
import numpy as np


g = Graph("./tp_1_oriente.txt")
g_non_oriente = Graph("./tp_1_non_oriente.txt")


# Question 1
print("\n\nQUESTION 1\n")
print("graph is", g)
print("matrice adjacence is\n", g.get_matrice_adjacence())

print("graph non oriente is", g_non_oriente)
print("matrice adjacence non oriente is\n",
      g_non_oriente.get_matrice_adjacence())


# Question 2
print("\n\nQUESTION 2\n")
print("liste sommets oriente est", g.sommets)
for sommet in g.sommets:
    print(
        f"degree entrant de {sommet} : {g.get_degre_entrant(sommet)} et sortant : {g.get_degre_sortant(sommet)}")

print("liste sommets non oriente est", g_non_oriente.sommets)
for sommet in g_non_oriente.sommets:
    # degree entrant = degree sortant for non oriented graph
    print(f"degree de {sommet} : {g_non_oriente.get_degre_sortant(sommet)}")


# Question 3
print("\n\nQUESTION 3\n")
print(f" il y a {g.nb_sommet_at_distance(2,2)} sommets à 2 de  distance 2")

# Question 4
print("\n\nQUESTION 4\n")
a = 2
b = 6
print(
    f"la distance minimal pour le graph oriente entre {a} et {b} est de {g.distance_minimal(a,b)} ")
print(
    f"la distance minimal pour le graph  non oriente entre {a} et {b} est de {g_non_oriente.distance_minimal(a,b)} ")


# Question 5
print("\n\nQUESTION 5\n")
print("nb composante connexe oriente\n", g.nb_composantes_connexes())
print("nb composante connexe non oriente\n",
      g_non_oriente.nb_composantes_connexes())


g_test = Graph("./test.txt")
print("test connex", g_test.nb_composantes_connexes())
