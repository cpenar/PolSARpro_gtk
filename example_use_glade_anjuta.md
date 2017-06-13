Exemple de création de la fenêtre 'Environment > Single Data Set (Pol-SAR)'

Avec Glade et Anjuta


# Versions 

+ ubuntu : 14.04
+ python3 : 3.4.3-1ubuntu1~14.04.5
+ glade : 3.16.1-0ubuntu2
+ libgtk-3 : 3.10.8-0ubuntu1.6
+ python3-gi : 3.12.0-1ubuntu1
+ anjuta : 2:3.10.2-0ubuntu2
+ anjuta-extras : 3.10.0-0ubuntu1

# Préalables

###### Configuration de Anjuta pour python 3

En suivant ce lien : [python3-support-in-anjuta](https://stackoverflow.com/questions/12345545/python3-support-in-anjuta)

Le paquet **python3-rope** n'est pas disponible sous ubuntu avant la version 17.10 mais est bien dans les dépots pip3,
dans ce cas précis il a été installé avec la commande : `sudo pip3 install rope`

Suivre le tuto est effectuer les modifs dans le fichier `/usr/lib/anjuta/anjuta-python-autocomplete.py`
+ ajouter en première ligne : `from __future__ import print_function`
+ modifier les `print blahblah` par `print(blahblah)` (ajouter les parenthèses, requises en python3)

# Info non exhaustive de création du fichier ui

Après création d'un nouveau projet dans Anjuta :

### Préalables au fichier ui

Anjuta crée un fichier ui pour la version 3.0 de GTK, or certains widgets de glade ne sont disponibles que pour les versions supérieurs de GTK.
Il faut donc modifier à la main le fichier ui crée par Anjuta et modifier la ligne :

`<requires lib="gtk+" version="3.0"/>`

par

`<requires lib="gtk+" version="3.10"/>`

Sauvegarder et seulement après ouvrir le fichier dans Anjuta en double cliquant dessus.

Le fichier ui se modifie depuis Anjuta par le chemin de projet : `src/ui/blablah.ui`,
double cliquer sur ce fichier ouvre une interface Glade à l'intérieur de Anjuta.

### Création de l'ui

##### Widget Window

+ Général-Astuce : 'Dialog' (pour obtenir une fenêtre centrée non collante)
+ Commun : Cocher 'Visible' (par défaut non coché sauf si créée avec Anjuta)

##### Widget Label

+ Commun-Alignement-Horizontal : 'Start' (pour une justification à gauche)

##### Widget Adjustment

Ce Widget ne s'affiche pas mais servira à la configuration des bornes du SpinButon qui vient juste après.

Le Widjest 'Adjustment' se trouve dans la rubrique 'Miscellanous' de Glade, quand on clique dessus rien n'apparait dans l'interface mais seulement dans l'arborescence des objets.
On peut le configurer en le sélectionnant.
Pour le SpinButton nous avons besoins des bornes (0, 1600) et d'un pas de 100 :
+ Valeur: 934 (valeur de départ)
+ Valeur minimale: 0
+ Valeur maximale: 1600
+ Incrément du pas: 100

##### Widget SpinButton

+ Général-Adjustement : Cliquer sur le crayon et sélectionner l'objet 'Adjustment' qui a été créé précédement.

:mega: **Attention** Il faut créer un objet 'Adjustment' différent pour chaque SpinButton, car s'ils partagent le même il modifieront les même variables internes et auront des valeurs liées et identiques.

##### Widget Label

+ Modifier la font en utilisant [Text Attribute Markup](https://developer.gnome.org/pango/stable/PangoMarkupFormat.html)
   + Général-Use Markup
   + Général-Label : mettre directement du code Markup plutôt que le simple contenu texte.

##### Création d'une fenêtre ColorMap

Comme toutes les fenêtres ColorMap se ressemblent beaucoup et que seulle change la palette de couleur elle-même, nous allons créer une fenêtre qui servira de template pour toutes les fenêtres ColorMap.

Dans Anjuta/Glade : Fichier-New-Fichier d'interface utilisateur.

Nous sauvegarderons ce fichier dans le répertoire `ui` afin d'organiser un peu nos fichiers et nous l'appelerons `colormap_window_template.ui`
En plus des différents Widget classiques, nous créons un widget de type `GtkBox` vide qui servira à héberger les boutons de la colormap lue et nous lui donnons un nom spécifique afin de le désigner simplement dans le code : `boxColorMapBtn`

###### Préparation

Dans le bouton qui correspond à `Supervized ColorMap16` de la fenêtre `single_data_set.ui` :
+ Signaux-GtkButton-Clicked : et nous définissons un gestionnaire `supColorMap16`

Dans le fichier `single_data_set.py` nous définissons cette nouvelle fonction dans la classe `GUI` :

```python
def supColorMap16(self, *args):
   mapFile = os.path.dirname(__file__) + '/ColorMap/Supervised_ColorMap16.pal'
   windowFromFile(mapFile, self)
```

La fonction `windowFromFile` sera créée dans un fichier que nous nommerons `colorMap.py` dans le répertoire `lib`.

Note: afin de pouvoir importer depuis un répertoire [il faut créer un fichier `__init__.py`](https://docs.python.org/3/tutorial/modules.html#packages) (même vide) dans ce répertoire.

Dans le fichier `single_data_set.py` qui utilise cette fonction nous ajoutons donc la ligne :

```Python
from lib.colorMap import windowFromFile
```
 
###### La fonction `windowFromFile`

Elle va :
+ lire un fichier palette passée en argument
+ créer un widget window à partir de `colormap_window_template.ui`
+ créer les widget `ColorButton` à partir de la palette lue
+ et enfin afficher cette nouvelle fenêtre

Cf le code du fichier `colorMap.py` pour plus de détails.
