# TP2 - Documentation du projet de stéganographie, signature, etc.

Cette interface en ligne de commande (CLI) est conçue pour les opérations cryptographiques sur les images.

## Utilisation

```bash
python main.py [options]
```

## Options

- `-h, --help`: Affiche ce message d'aide et quitte.
- `-i IMAGE, --image IMAGE`: Fichier image d'entrée au format PNG ou PPM.
- `-m MESSAGE, --message MESSAGE`: Message à encoder ou décoder.
- `-a ALGORITHM, --algorithm ALGORITHM`: Algorithme à utiliser pour le chiffrement ou le déchiffrement.
- `-d DECRYPT, --decrypt DECRYPT`: Si spécifié, le message sera déchiffré.
- `-n NAME, --name NAME`: Nom associé à l'opération.
- `-da DATE, --date DATE`: Date associée à l'opération.
- `-me MENTION, --mention MENTION`: Mention associée à l'opération.
- `-o OUTPUT, --output OUTPUT`: Fichier de sortie pour le résultat.
- `-f FUNCTION, --function FUNCTION`: Fonction à exécuter sur l'image ou le message.
- - `-vu VERIFICATION_URL, --verification-url VERIFICATION_URL`: URL pour vérifier le certificat, exemple : https://some-university.com/diplome/verify (par défaut : https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Exemples

1. Chiffrer un message dans une image :

   ```bash
   python .\main.py -f stenography -i image.png -a basic -m "Hello world"
   ```

2. Déchiffrer un message à partir d'une image :

   ```bash
   python .\main.py -f stenography -i output.png -a basic -d true
   ```

3. Génération d'un diplome :

   ```bash
   python .\main.py -f generate -n "Dupond Dupont" -da "25/01/2024" -me "Avec la mention Bien" -o "diplome.png" -p "https://some-university.com" -vu "https://some-university.com/diplome/verify"
   ```

## Remarque

- Assurez-vous que les bibliothèques requises pour les algorithmes spécifiés sont installées.
- L'image d'entrée doit être au format PNG ou PPM.

## Questions

### Q1

encrypt :

```bash
python .\main.py -i image.png -a basic -m "Hello world"
```

descrypt :

```bash
python .\main.py -i output.png -a basic -d true
```

## Choix d'implémentation

### Stéganographie

- on cache les infos dans les premiers pixels (poid faible du rouge des pixels)
- on signe et on cache les infos du diplome afin que un diplome modifié par photoshop ou autre ne soit pas valide

### QRCode

Nous avons ajouter le QR code qui permet de renvoyer vers un liens du provider du diplome. La base du lien est fournis par l'attribut `-vu` ou `--verification-url` et on y ajouter l'uuid du diplome. En production la génération de l'uuid se fera en lien avec la base de donnée.

L'idée est de pouvoir vérifier l'authenticité du diplome en scannant le QR code. Le lien renvoie donc vers une page qui fournira une clé publique unique pour vérifier la signature additionnelle du diplome. En effet, en plus de la signature du message par la clé privé du provider. Un paire de clé doit être généré pour chaque étudiant et permettre de signer un deuxième message, identique au premier, mais signé par la clé privé unique à l'étudiant. Ainsi, même si la clé privé du provider est compromise, la signature additionnelle permet de vérifier l'authenticité du diplome. La clé privée unique par étudiant est supprimé après la signature du diplome.
