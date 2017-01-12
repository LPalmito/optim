#Optimisation - Devoir Maison n°1
###### Par Augustin Courtier & Yannick Morel

###Ce dossier contient :

+ L'implémentation de la classe CSP : `CentraleSupélec.py`
+ Un exemple d'utilisation de cette classe pour le problème n-Reines : `nReines.py`
+ L'implémentation de la classe Tile : `Tile.py`
+ Des fonctions relatives au problème "Infinity Loop" : `connect.py`

###Zoom sur le fichier `Tile.py` :

Celui-ci contient :

+ Une classe 'Tile', pour représenter au mieux les tuiles. 'Tile' contient :
    + 2 attributs :
        + 'connectors', qui contient un tableau de 4 booléens représentant la présence d'un connecteur ou non sur la face concernée
        + 'nb_rots', qui contient l'orientation de la tuile, codée par une nombre entier entre 0 et 3 (0 correspondant aux tuiles 0, 1, 3, 5, 7, f)
    + 1 méthode :
        + 'get_hexa', qui renvoie le nombre hexadécimal correspondant à la tuile
+ 2 méthodes annexes :
    + 'hexa_to_list', qui permet de convertir un hexa en un tableau de booléens pour l'attribut 'connectors'
    + 'hexa_to_nb_rots', qui permet de convertir un hexa en le nombre de rotations associées pour l'attribut 'nb_rots'

###Zoom sur la démarche de résolution du problème :
Nous avons choisi de travailler avec les rotations des différentes tuiles du problème, d'où le fait que notre 'domains' soit un tableau de {0, 1, 2, 3}. Les différentes étapes de la fonction 'solve' dans `connect.py` :

1) Restriction du domaine en prenant en compte les contraintes aux 4 bords
2) Restriction du domaine en prenant en compte les contraintes aux 4 angles
3) Instanciation du problème CSP avec ce domaine défini
4) Ajout des contraintes liées aux liens haut-bas entre les tuiles (en passant par des objets 'Tile')
5) Ajout des contraintes liées aux liens gauche-droite entre les tuiles (en passant par des objets 'Tile')
6) Résolution du problème et affichage des résultats

### Mesures de performance :
Nous avons effectué des mesures de performance pour un échantillon de 50 essais avec solution pour n variant de 1 à 20, voici les résultats que nous obtenons :
![alt tag](https://raw.githubusercontent.com/LPalmito/optim/master/img/min_avg_max.png)
![alt tag](https://raw.githubusercontent.com/LPalmito/optim/master/img/with_or_without_AC.png)
On remarque donc qu'il est plus efficace de maintenir l'arc consistance pour n<12, alors que la tendance s'inverse au-delà de cette valeur.
Il est possible d'effectuer d'autres mesures de performance en runnant `perfs.py`. La méthode 'measure_perf' est alors lancée, elle prend pour arguments:

+ 'n_max': les mesures de performance seront effectuées pour tout n entre 1 et n_max (pour des grilles de taille n*n)
+ 'precision': le nombre de mesures effectuées pour chaque n, plus 'precision' est grand, plus les mesures seront significatives

PS : Pour la solution du cadeau de Noël, c'est par ici !
=> http://www-desir.lip6.fr/~durrc/Iut/optim/images/19412