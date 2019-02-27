Ce projet s'inscrit dans le cadre d'un projet réalisé durant notre dernière année d'école d'ingénieur à L'ENSTA Bretagne.

Dans ce Github vous trouverez:
* Un fichier _TUTO.md_ montrant comment nous avons réalisé notre projet (docker, flashage, ,cross compilation, IP, ...)
* Les fichiers à télécharger et à copier sur votre RaspberryPI.

Notre système se compose de 5 fichiers importants:

* servo_server.py (RaspberryPI)
* v4l2grab        (RaspberryPI)
* Makefile        (RaspberryPI)
* client.py       (Ordinateur)
* Makefile        (Ordianteur)

## CAS D'UNE RAPSBERRYPI AVEC OS

Si vous avez déja une carte micro SD avec un OS, il vous suffit :
* de copier le dossier _server_ sur votre RaspberryPi contenant:
* _servo_server.py_
* _v4l2grab_
* Makefile

Et de copier le dossier  sur votre ordinateur personnel, contenant:
* _client.py_
* Makefile

Il faut aussi les fichier du dossier config dans la premiere partition de votre raspberry.

Et enfin modifier le fichier *config.txt* de la 1ère partition en ajoutant ces lignes:
**start_x=1
gpu_mem=128**

## CAS D'UNE RAPSBERRYPI SANS OS

Si vous voulez flasher votre carte par vos propre moyen, un tuto vous est mis à disposition (*suivre depuis le début "[TUTO.md](TUTO.md)"*).

## MATERIEL 

Il faut brancher le servomoteur sur le port GPIO4 de votre raspberry. 
[Pour trouver les pins de votre raspberry](https://www.framboise314.fr/wp-content/uploads/2018/02/kit_composants_GPIO_01.png)

Il faut aussi vous connecter en ethernet a votre raspberry.

## Lancement du code

Sur la RaspberryPI, aller dans _/home/user/server_, là où se trouve le Makefile et exécutez la commande *make*, cette commande vas exécuter les commandes nécessaires.
Et ensuite *make run* pour lancer les servers.
A cette instant les serveurs sont lancés.

Sur votre ordinateur, aller dans le dossier client et lancer la commande, *make*. A cette instant vous entrez dans la peau du client qui peut communiquer avec le server de la RaspberryPi.

## Règles du jeu ! Commandes chez le client

* Pour changer l'angle de la caméra il vous faudra appuyer sur les touches flèches *droite* et *gauche*. L'angle s'affiche sur l'écran pour savoir ou vous en êtes.

* Pour prendre une photo il faut appuyer sur la touche *s* de votre clavier pour sauvegarder l'image sur votre ordinateur et l'afficher. L'image est écrasée d'un appui à l'autre sur la touche *s*.

L'équipe vous remercie de la confiance accordée à leur travail.


Pour toutes autres questions ou demandes, n'hésitez pas à nous contacter.

Amusez-vous bien !


Elias & Evann & Romain & Victor.
