
Description du projet
=====================

Récupérer les données du compteur linky(TM) par les bornes de téléinformation I1 et I2
du compteur

L'acquisition : ESP32
Les spécifications de teleinformation du compteur linky :
https://www.capeb.fr/www/capeb/media//vaucluse/document/FicheSeQuelecN17TIC.pdf
Le document ci-dessus contient 2 liens vers les spécifications des données.
Celui à prendre en compte est http://www.enedis.fr/sites/default/files/Enedis-NOI-CPT_54E.pdf
car il traite des données transmises par le linky. L'autre ne concerne que les compteurs électroniques
de la précédente génération.

Il s'avère que le mode de la teleinformation par défaut installé est le mode historique. Celui-ci
est plus lent (1200bps) que le mode "standard" (apparu avec le linky, 9600bps) mais surtout, le nouveau
mode standard contient les informations d'horodatage dans les données transmises. Ceci présente
l'avantage de n'avoir pas besoin de coupler un RTC avec l'acquisition. Les données transmises
pourront donc être plus facilement insérées dans la BDD (openTSDB ?).


traitement des données : ??? ordinateur sous Linux. A ce jour, les choses ne sont pas encore 
déterminées... réception des données par wifi, mise ne base de données (openTSDB ?) et
graphiques avec grafana (?)....

openTSDB : The Scalable Time Series Database : http://opentsdb.net/
grafana : Dashboard anything. Observe everything. https://grafana.com/grafana/

NB: on peut se demander si grafana n'est pas une GROSSE usine à gaz pour juste afficher quelques courbes...???
    Le dashboard de openTSDB serait peut-être suffisant... https://github.com/search?q=opentsdb-dashboard

https://pypi.org/project/potsdb/ : client python de openTSDB (mais dernière version en 2016, 1.0.3)

Des Front-ends : http://opentsdb.net/docs/build/html/resources.html#front-ends




Divers
======

Un exemple de récupération de données TIC avec arduino en C++ :
https://forum.arduino.cc/t/softwareserial-et-deuxieme-uart-pour-arduino-nano/359978/2





