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

================= CAS D'UNE RAPSBERRYPI AVEC OS ============
Si vous avez déja une carte micro SD avec un OS, il vous suffit :
* de copier le dossier _server_ sur votre RaspberryPi contenant:
* _servo_server.py_
* _v4l2grab_
* Makefile

Et de copier le dossier  sur votre ordinateur personnel, contenant:
* _client.py_
* Makefile

Il vous rest plus qu'à lancer la simulation !
(*cf fin du "TUTO.md" pour le lancement et les commande du système*).


================= CAS D'UNE RAPSBERRYPI SANS OS ============

Si vous voulez flasher votre carte par vos propre moyen, un tuto vous est mis à disposition (*cf début "TUTO.md"*).


Pour toutes autres questions ou demandes, n'hésitez pas à nous contacter.

Amusez-vous bien !

Elias & Evann & Romain & Victor.
