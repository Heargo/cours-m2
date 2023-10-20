# TP 2

## Hugo REY - Simon PICHENOT

### Partie 1

#### Verificateur

Code disponible dans le fichier `verificateur.py`

#### SolvBackTracking

Code disponible dans le fichier `partie_1.py`. Pour tester modifier la ligne 166 `graph = graph.Graph("../instances/file.txt")` en remplacant `file.txt` par le nom du fichier à tester.
`test_ok.txt` est 3 coloriable, `test_nok.txt` ne l'est pas.

#### SolvRandom

Code disponible dans le fichier `partie_1.py`. Pour tester, même chose que pour `SolvBackTracking`.

#### SolvLawler

Code disponible dans le fichier `partie_1.py`. Non terminé, les tests sont donc commentés.

### Partie 2

#### Problème Clique

Code disponible dans le fichier `solveClique.py`. Lancer la commande suivante pour tester:

```bash
python solveClique.py file x
```

où `file` est le nom du fichier à tester et `x` la taille de la clique.

#### Problème 3Coloration

Code disponible dans le fichier `solve3ColorSat.py`. Lancer la commande suivante pour tester:

```bash
python solve3ColorSat.py file
```

#### Problème Couverture par 3 Cliques

Code disponible dans le fichier `solve3Clique.py`. Lancer la commande suivante pour tester:

```bash
python solve3Clique.py file
```

file est le nom du fichier à tester. (`test_clique_ok.txt` et `test_clique_nok.txt` sont disponibles pour tester)

#### 3Col est NP-complet

Non réalisé.
