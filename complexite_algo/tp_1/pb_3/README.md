Pour tester le programme, il suffit de lancer la commande suivante:

```bash
python3 graphChronoGenerator.py testData
```

Pour la méthode non optimisé utiliser ces paramètres:

```json
{
  "executable": "python3 main.py",
  "generator": "python3 genererPartie.py --tempFile",
  "temp_file": "calculAux.tmp",
  "arg_executable": "calculAux.tmp",
  "valeurInitiale": 1,
  "borneSup": 40,
  "increment": "x+1",
  "attenteMax": 25,
  "logScale": false,
  "courbesSup": ["log(x)", "x", "x*log(x)", "x**2", "2**x"],
  "outputImageNamePrefix": "graph",
  "outputImageSize": "1000,700"
}
```
