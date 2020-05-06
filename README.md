# ecoLinky
Simulation d'un EcoDevice pour interfacer un ESP8266 (connecter au port TIC d'un Linky) avec Domoticz

Projet: Intégrer mes données de consommation d'énergie provenant du Linky à Domoticz

Problème #1: Le Linky se trouve à l'extérieur de la maison dans un garage situé à une 20aine de mètres.
Il n'est donc pas possible d'y accèder directement en série avec ma box domotique (RPI 3+) qui se trouve elle dans la maison.

Solution: Accéder à distance en Wifi
Utilisation d'un module ESP8266 avec la pile ESPEasy pour s'interfacer avec le TIC du Linky
Configuration de l'ESPEasy pour accèder au port du Teleinfo via un serveur TCP

Jusque là pas de gros problème, il est maintenant possible d'accèder au port TIC du compteur Linky via le Wifi
info: l'alimentation mise à disposition par le Linky (port I1 A), n'est pas assez puissante pour l'ESP8266, il faut une alimentation externe.


Problème #2: Connecter l'ESP avec Domoticz.
Domoticz intégre bien un plugin pour s'interfacer avec une interface TIC, mais uniquement en série.

Solution #1: utiliser socat pour emuler un port série virtuel et le relier au serveur tcp de l'ESP.
Malheureusement, le plugin de Domoticz ne semble pas bien gérer ce type de port série.

Solution #2: utiliser le matériel EcoDevice présent dans Domoticz, il utilise les mêmes fonctions de base que le pluging Teleinfo

Il me faut soit modifier le code de l'ESP pour y intégrer l'API de l'EcoDevice, soit créer une interface logiciel pour créer le pont entre Domoticz et l'ESP.
J'ai préféré la seconde solution, par plus rapide et plus flexible.

Il s'agit donc ici, de l'interface logiciel simulant l'API d'un module EcoDevice

sources:
http://sarakha63-domotique.fr/nodemcu-teleinformation-wifi/
https://www.domoticz.com/wiki/Eco_Devices_Via_LAN_Interface
http://www.touteladomotique.com/index.php?option=com_content&id=985:premiers-pas-avec-leco-devices-sur-la-route-de-la-maitrise-de-lenergie&Itemid=89#.WKcK0zi3ik5
https://github.com/domoticz/domoticz/blob/master/hardware/EcoDevices.cpp
