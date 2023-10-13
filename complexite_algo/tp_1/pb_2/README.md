Pour tester le programme, il suffit de lancer la commande suivante:

```bash
python3 graphChronoGenerator.py testData
```

Pour la méthode naive utiliser ces paramètres:

```json
{
  "executable": "python3 dmin.py naive",
  "generator": "python3 genererPoints.py --tempFile",
  "temp_file": "calculAux.tmp",
  "arg_executable": "calculAux.tmp",
  "valeurInitiale": 10,
  "borneSup": 5000,
  "increment": "floor(3*x/2)+1",
  "attenteMax": 25,
  "logScale": false,
  "courbesSup": ["log(x)", "x", "x*log(x)", "x**2", "2**x"],
  "outputImageNamePrefix": "graph",
  "outputImageSize": "1000,700"
}
```

Pour la méthode diviser pour regner

```json
{
  "executable": "python3 dmin.py dpr",
  "generator": "python3 genererPoints.py --tempFile",
  "temp_file": "calculAux.tmp",
  "arg_executable": "calculAux.tmp",
  "valeurInitiale": 10,
  "borneSup": 10000,
  "increment": "floor(3*x/2)+1",
  "attenteMax": 25,
  "logScale": false,
  "courbesSup": ["log(x)", "x", "x*log(x)", "x**2", "2**x"],
  "outputImageNamePrefix": "graph",
  "outputImageSize": "1000,700"
}
```
