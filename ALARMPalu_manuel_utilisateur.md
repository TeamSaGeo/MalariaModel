<a name="br1"></a> 

Manuel d’utilisation

ALARM Palu

MODELISATION DE LA DYNAMIQUE DE POPULATION DES

MOUSTIQUES ET DU RISQUE DE TRANSMISSION DU

PALUDISME,

ANNEE 2023

Par :

Fanjasoa RAKOTOMANANA

Anthonio RAKOTOARISON

Sarah FAMENONTSOA



<a name="br2"></a> 

Sommaire

[**1.**](#br2)[** ](#br2)[A**](#br2)[** ](#br2)[propos**](#br2)[** ](#br2)[...................................................................................................................](#br2)[ ](#br2)[1](#br2)

[**2.**](#br2)[** ](#br2)[Etapes**](#br2)[** ](#br2)[du**](#br2)[** ](#br2)[lancement**](#br2)[** ](#br2)[du**](#br2)[** ](#br2)[modèle**](#br2)[.............................................................................](#br2)[ ](#br2)[1](#br2)

[Etape](#br3)[ ](#br3)[1](#br3)[ ](#br3)[:](#br3)[ ](#br3)[Paramètres](#br3)[ ](#br3)[d’entrée](#br3)[ ](#br3)[.......................................................................................](#br3)[ ](#br3)[2](#br3)

[Etape](#br4)[ ](#br4)[2](#br4)[ ](#br4)[:](#br4)[ ](#br4)[Paramètres](#br4)[ ](#br4)[de](#br4)[ ](#br4)[sortie.......................................................................................](#br4)[ ](#br4)[3](#br4)

[Etape](#br5)[ ](#br5)[3](#br5)[ ](#br5)[:](#br5)[ ](#br5)[Simulation.......................................................................................................](#br5)[ ](#br5)[4](#br5)

[**3.**](#br6)[** ](#br6)[Résultat**](#br6)[** ](#br6)[de**](#br6)[** ](#br6)[la**](#br6)[** ](#br6)[simulation**](#br6)[** ](#br6)[.........................................................................................](#br6)[ ](#br6)[5](#br6)

**1. A propos**

L’outil de Modélisation de la dynamique de population des moustiques et du risque de

transmission du paludisme (ALARM Palu) permet d’évaluer la population des moustiques et

du risque de paludisme sur une zone donnée.

Cette version exécutable sous le système d’exploitation Windows.

Le présent manuel illustre un traitement complet de l’outil.

**2. Etapes du lancement du modèle**

Pour lancer l’outil, cliquer sur le fichier d’exécution “ALARM Palu”.

L’outil se compose de 3 étapes divisées en 3 onglets :

1\. **Les paramètres d’entrée** permettant d’importer les données environnementales et

les données de précipitations et de températures

2\. **Les paramètres de sortie** permettant de choisir les résultats à exporter ainsi que le

format du fichier à exporter

3\. **La simulation** permettant de lancer le modèle

Page 1 sur 6



<a name="br3"></a> 

Etape 1 : Paramètres d’entrée

Sous l’onglet paramètres d’entrée, l’utilisateur devrait choisir les 3 fichiers suivants :

•

•

•

**Fichier environnemental** contenant les données d’occupation du sol ou gite larvaire

(lieu, surface des plans d’eau, surface des rizières, etc.)

**Précipitations** contenant les données de précipitations des zones d’étude dans une

période données

**Températures** contenant les données de températures des zones d’étude dans une

période données

**NB :** les données d’entrée devraient suivre les conditions ci-dessous

**Fichier**

**Format Minimum des champs (colonnes) requises**

Fichier

environnemental

shp

Code Commune (champ de jointure avec le tableau à droite)

Surface des plans d’eau (m2)

Surface des rivières (m2)

Surface des cultures agricoles (m2)

Surface des rizières (m2)

Surface totale (m2)

Préfixe du nombre de population (hab) par année

Précipitations

Températures

csv

Commune

Année

Mois (ou Semaine si données hebdomadaires)

Jour (si données journalières)

Valeur (en mm si précipitation, en °C si température)

Page 2 sur 6



<a name="br4"></a> 

Après avoir chargé les fichiers d’entrée, l’utilisateur devrait choisir les colonnes

correspondantes à chaque ligne du tableau du dessous.

Si les valeurs des colonnes choisis sont valides (c’est-à-dire de type numérique sauf les codes

des Communes et le préfixe du nombre de population), alors l’utilisateur peut passer à l’étape

suivante « Paramètres de sortie ». Sinon, un message d’erreur s’affiche.

Etape 2 : Paramètres de sortie

Sous l’onglet paramètres de sortie, l’utilisateur devrait choisir les éléments suivants :

•

**Le répertoire de sortie :** Le nom du fichier de sortie est comme-suit :

[Nom\_fichier\_environnemental]\_[date\_debut\_sortie]\_[date\_fin\_sortie]

**Les dates de sortie :** soit pour une seule date soit pour une période donnée

o Si pour une date, alors l’utilisateur devrait choisir la date de la fin de sortie. La

date du début des sorties est définie 7 avant la date de fin des sorties

o Si pour une période, l’utilisateur devrait choisir la date du début et celle de fin

ainsi que la fréquence des sorties (tous les n jours ou tous les n mois)

**Le format de sortie :** sous format shapefile et/ou csv et/ou kml

•

•

•

**La date et le nombre de personnes initialement infectées :** entre 0 et le nombre

maximal de population de l’année du début de la simulation

•

**Les valeurs à exporter :** l’utilisateur devrait choisir au moins un des valeurs à

exportés listés en bas de l’onglet (moustiques, humain, capacité de charge)

Page 3 sur 6



<a name="br5"></a> 

Si les valeurs choisis sont valides, alors l’utilisateur peut passer à l’onglet suivant

« Simulation ». Sinon, un message d’erreur s’affiche.

Etape 3 : Simulation

Sous l’onglet « Simulation », l’outil résume les paramètres d’entrée et les paramètres de sortie

choisis par l’utilisateur.

Pour lancer le modèle, l’utilisateur devrait cliquer sur le bouton « Exécuter » en bas. Une boîte

de dialogue apparaît ensuite pour confirmer la réponse de l’utilisateur.

Une fois la simulation lancée, l’outil calcule les valeurs à exportées puis exporte les résultats

selon les formats de fichier et la fréquence de sortie choisis par l’utilisateur.

Si les paramètres KL ou les données de température ou de précipitation sont de valeurs nulles,

alors les valeurs des résultats correspondantes seront nulles.

Page 4 sur 6



<a name="br6"></a> 

L’utilisateur peut annuler la simulation en cliquant sur le bouton « Annuler ». Sinon, une boîte

de dialogue s’affiche lorsque la simulation est terminée.

**3. Résultat de la simulation**

Les résultats de la simulation sont sauvegardés dans le répertoire de sortie choisit par

l’utilisateur dans l’onglet « Paramètres de sortie ». L’historique du paramétrage et de la

simulation y sont stocké également au format texte (.txt).

Page 5 sur 6



<a name="br7"></a> 

Toutes les valeurs numériques exportés sont arrondies à des valeurs en entiers.

Page 6 sur 6

