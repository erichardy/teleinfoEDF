.. Téléinformation EDF documentation master file, created by
   sphinx-quickstart on Wed Oct 26 18:31:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. include:: links.rst


Téléinformation EDF
===================

.. toctree::
   :maxdepth: 2
   :caption: Table des matières:

	Introduction <intro>
	Les tergiversations <tergiversations>
	L'électronique <electronique>
	Le code d'acquisition <acquisition>


Résumé
======

Les compteurs EDF de nouvelle génération, à savoir les compteurs électroniques et, plus récemment, les
compteurs Linky(TM) ont une fonctionnalité très intéressante : il fournissent en continu et en temps réel
les informations électriques. Par exemple :

* la consommation instantanée (par phase si compteur tri-phasé)
* le mode Heures pleines vs Heures creuses
* le type d'abonnement
* etc...

Ces informations sont à la disposition des usagers (pas EDF) via une liaison constituée de 2 fils
sur les bornes I1 et I2 du compteur.

	.. note:: Ne pas confondre ces informations qui sont la disposition des usagers et les informations collectées
	  par EDF via une communication par CPL (il me semble) à l'extérieur du foyer.


Ces informations peuvent être utilisées par des modules qui peuvent, eux-mêmes, piloter des équipements par exemple.

Me concernant, ayant un **compteur tri-phasé** et un **abonnement tempo**, je souhaitais avoir une vue assez précise, en temps
réel et en différé, de ma consommation. La première étape a donc été de réaliser le circuit électronique d'acquisition
des données puis de mettre en oeuvre une architecture de traitement de ces données :

* affichage
* stockage
* visualisation diverses

Autre élément du contexte : depuis quelques petites années, je m'intéresse et me forme à l'électronique, celle
des amateurs... La réalisation d'un projet comme celui-ci est pour moi très intéressante sur le plan de l'apprentissage
de cette discipline, la partie scritement électonique étant vraiment accessible à un amateur même relativement
débutant.

La partie informatique qui est associée à ce projet est celle qui me passionne le moins, ayant excercé ce métier pendant
près de 25 ans. j'y ai tout de même pris du plaisir car c'est cette partie là qui met en valeur l'électronique
d'acquisition des données.

**A tout lecteur** : disposez librement de toutes les informations présentées dans ce projet. Si vous rendez publique
une partie de ce projet ré-arangée à votre sauce, merci d'en citer la provenance.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
