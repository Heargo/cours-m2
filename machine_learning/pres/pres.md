---
title: SwinIR Image Restoration Using Swin Transformer
---

# SwinIR: Image Restoration Using Swin Transformer

Liang, J., Cao, J., Sun, G., Zhang, K., Van Gool, L., & Timofte, R. (2021). [SwinIR: Image restoration using swin transformer](https://openaccess.thecvf.com/content/ICCV2021W/AIM/papers/Liang_SwinIR_Image_Restoration_Using_Swin_Transformer_ICCVW_2021_paper.pdf). In Proceedings of the IEEE/CVF international conference on computer vision (pp. 1833-1844).

[TOC]

# Image Restoration

La restauration d'image fait référence au processus d'amélioration de la qualité d'une image en éliminant ou en réduisant divers types de dégradations, telles que le bruit, le flou ou d'autres distorsions. L'objectif est de reconstruire une version de meilleure qualité à partir d'une entrée dégradée ou imparfaite.

|                                  Image de référence                                  |                                        SwinIR                                        |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
| ![](https://codimd.math.cnrs.fr/uploads/upload_9745ae00cb64173006a5391a8080f5a8.png) | ![](https://codimd.math.cnrs.fr/uploads/upload_819d8deb818d76ceb5af1fd119597741.png) |
| ![](https://codimd.math.cnrs.fr/uploads/upload_0da5a7334cbcdd6407b639f911b2718f.png) | ![](https://codimd.math.cnrs.fr/uploads/upload_b6186bcf341a5392bf265806e6ea613f.png) |

Quelques cas d'utilisation :

1. **Imagerie Médicale :** Amélioration des images médicales pour un meilleur diagnostic.
2. **Surveillance :** Amélioration de la clarté des images de surveillance.
3. **Photographie :** Élimination du bruit et des artefacts sur les photos.
4. **Imagerie Satellite :** Amélioration des images satellite pour une meilleure analyse.
5. **Criminalistique :** Restauration des détails dans les images pour l'analyse médico-légale.

## CNN vs Transformer :

| **Aspect**        | **CNN**                                          | **Transformer**                           |
| ----------------- | ------------------------------------------------ | ----------------------------------------- |
| **Avantages**     | Hiérarchies Spatiales, Invariance de Translation | Contexte Global, Parallélisation Efficace |
| **Inconvénients** | Contexte Global Limité, Parallélisation Limitée  | Nature Séquentielle                       |

**Hiérarchies Spatiales**
Capables de reconnaître des motifs complexes à différentes échelles dans une image.

**Invariance de Translation**
Robustes aux variations dans la position des objets à l'intérieur d'une image.

**Contexte Global**
Permet de capturer un contexte global étendu dans une image et une relation entre les pixels au niveau de l'image globale et pas uniquement de la zone observée.

**Nature Séquentielle**
Examinent l'information un élément à la fois, en suivant une séquence prédéfinie.

## Swin Transformer :

Le Swin Transformer est un type d'architecture transformer qui adresse les limitations des transformers traditionnels dans le traitement des hiérarchies spatiales des images. Il divise l'image en morceaux non chevauchants et les traite de manière hiérarchique, permettant la capture d'informations locales et globales.

![swin_transformer](https://user-images.githubusercontent.com/24825165/121768619-038e6d80-cb9a-11eb-8cb7-daa827e7772b.png)

# SwinIR :

SwinIR applique l'architecture Swin Transformer à la tâche de **restauration d'image**. En exploitant les points forts du Swin Transformer, SwinIR vise à atteindre des performances de pointe dans des tâches telles que le débruitage, le défloutage et la super-résolution.

![performances](https://codimd.math.cnrs.fr/uploads/upload_6b26713a4a227a8462204e78ac172e6f.png)

:::info
Comparé à d'autres modèles, SwinIR est plus performant, tout en ayant moins de paramètres (ce qui diminue la taille du modèle)
:::

![swinIR_global_architecture](https://codimd.math.cnrs.fr/uploads/upload_bbbfd6b022be07a8d8d855050af26cde.png)

L'architecture globale de SwinIR est découpée en trois parties

- Shallow feature extraction
- Deep feature extraction
- HQ image reconstruction

## Shallow feature extraction

Cette partie est assez basique, il s'agit uniquement d'une couche de convolution avec un filtre 3x3.

Elle permet de faire un premier filtre qui garantie une stabilité dans les résultats et la performance.

## Deep feature extraction

### Residual Swin Transformer Block (RSTB)

![rstb](https://codimd.math.cnrs.fr/uploads/upload_bcc60b2b49bc237b20efc09ed7c904f2.png)

### Swin Transformer layer (ou STL)

![stl](https://codimd.math.cnrs.fr/uploads/upload_4fe29687fd65bf30f6ae0e66fb133611.png)

Le but de la couche STL est de combiner plusieurs techniques (MSA et MLP) tout en garda

#### LayerNorm

L'idée de cette couche est de normaliser les valeurs d'une matrice. C'est également combiné avec des paramètres d'apprentissage.

#### Multi-head self attention (MSA)

Ici, X est la fenêtre locale (local window feature) et $P_Q$, $P_K$ et $P_V$ sont des matrices de projection partagées entre différentes fenêtres.

$$Q = XP_Q, \space K = XP_K,\space V = XP_V $$

On utilise ensuite donc les matrices $Q$, $K$ et $V$ pour calculer l'attention.

$$Attention(Q, K, V ) = SoftMax\Big(\frac{QK^T}{\sqrt{d}} + B\Big)V$$

:::info
**Détaillons la formule**

- $Q$ (Query), $K$ (Key), et $V$ (Value) sont des matrices calculées à partir des caractéristiques d'une fenêtre locale.
- $d$ est la dimension de l'état caché du modèle.
- $B$ est un encodage positionnel relatif (matrice).
  :::
  Pour mieux comprendre tout ça, imaginez que vous travaillez sur un projet de groupe avec vos amis, et vous devez décider qui contribue à quoi dans le projet. Chaque ami a ses compétences uniques, et vous voulez vous assurer que la contribution de chacun est prise en compte de manière appropriée.

**$Q$ (Query), $K$ (Key), et $V$ (Value)**
Chaque ami a ses compétences uniques. La Query représente ce qu'ils peuvent apporter, la Key est leur expertise spécifique, et la Value est la contribution réelle qu'ils peuvent faire.

**Mécanisme d'attention :**
Maintenant, pour décider de la quantité d'attention à accorder à chaque ami, vous voulez voir à quel point leurs compétences correspondent aux besoins globaux du projet. C'est un peu comme évaluer à quel point leur Key correspond aux Queries des autres amis.

La fonction SoftMax est comme attribuer des scores en fonction de cette correspondance. Elle s'assure que les scores d'attention s'additionnent à 1, un peu comme dire : _"D'accord, assurons-nous que nous prenons en compte tout le monde, et l'attention totale est de 100%."_

**Mise à l'échelle $d$ :**
La division par $\sqrt{d}$ ajuste les scores pour garantir qu'ils conviennent à la dimension de l'état caché. C'est une façon de dire : _"Assurons-nous que notre attention n'est pas trop grande ou trop petite ; ajustons-la correctement."_

**Encodage Positionnel Relatif $B$**
L'encodage positionnel relatif apprenable $B$ revient à considérer les relations ou positions uniques entre chaque ami. C'est dire : _"Hé, n'oublions pas que la façon dont chaque ami est lié aux autres peut influencer notre attention."_

**En pratique :**

Après ce processus, vous avez des scores d'attention pour chaque ami (donc une matrice d'attention). Plus le score est élevé, plus ils reçoivent d'attention. Maintenant, vous pouvez combiner les contributions réelles de chacun (la matrice $V$) en fonction de ces scores d'attention. Cela vous donne donc la matrice finale qui contient la contribution de chacun pondéré par son importance. Cependant, dans le cas de MSA, au lieux de donner le projet à un seul groupe d'amis, vous le donnez au plusieurs groupes d'amis qui travaillent dessus en parallèle et à la fin vous combinez le résultat de tout les groupes !

Cela permet d'avoir un projet bien meilleur. Dans le cas du modèle SwinIR cela permet une meilleure "description" de la fenêtre locale.

la couche MSA ressemble donc à ça :
![](https://codimd.math.cnrs.fr/uploads/upload_befe335d32af10520d51d1559b4d817c.png)

### MLP

C'est un réseau de neurones à deux couches densément connectés. Le réseau utilise la fonction d'activation GELU

![gelu_vs_relu](https://miro.medium.com/v2/resize:fit:491/1*kwHcbpKUNLda8tvCiwudqQ.png)

## Sub-pixel Convolution Neural Network

![](https://codimd.math.cnrs.fr/uploads/upload_f186fd7493bbe83fc024c3bd519d8150.png)
