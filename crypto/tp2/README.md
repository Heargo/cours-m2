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

- On signe les infos du diplome (nom, date et mention) afin qu'une modification de l'image soit immédiatement vérifiable. En effet si la signature une fois déchiffré ne correspond pas à ce qui est visible sur l'image alors on sait que l'image a été modifié.

- Pour cacher les infos dans l'image on change le bit de poid faible du rouge des pixels dans les premiers pixels de l'image. On encode de cette manière la signature du message (nom, date et mention) au format hexadécimal.

### QRCode

Nous avons ajouter le QR code qui permet de renvoyer vers un liens du provider du diplome. La base du lien est fournis par l'attribut `-vu` ou `--verification-url` et on y ajouter l'uuid du diplome. En production la génération de l'uuid se fera en lien avec la base de donnée.

L'idée est de pouvoir vérifier l'authenticité du diplome en scannant le QR code. Le lien renvoie donc vers une page qui fournira une clé publique unique pour vérifier la signature additionnelle du diplome. En effet, en plus de la signature du message par la clé privé du provider. Un paire de clé doit être généré pour chaque étudiant et permettre de signer un deuxième message, identique au premier, mais signé par la clé privé unique à l'étudiant. Ainsi, même si la clé privé du provider est compromise, la signature additionnelle permet de vérifier l'authenticité du diplome. La clé privée unique par étudiant est supprimé après la signature du diplome.

### Généricité et abstraction

- On peut ajouter des méthode de sténographie facilement en héritant de la classe `EncodeurDecodeur`
- la gestion des clé et gérée automatiquement par le `Signateur`. Si les fichiers `public.pem` et `private.pem` n'existe pas alors ils sont générés automatiquement.
- les commandes permettent de générer des diplomes ou de cacher une information dans une image.
