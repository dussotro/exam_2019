Linux Embarqué : Mini Projet.
==============Matériel===============
* RaspberryPI 3
* Alimentation RaspberryPI
* Carte SD 512Mo (Minimum)
* Servo moteur 0-180°
* Adaptateur usb liaison série
* Caméra RaspberryPI
* Câbles de branchement



=========Installations requises======
* Docker      *sudo apt install docker*
* MatplotLib  *sudo pip install matplotlib*
* Pygame      *sudo pip install pygame*
* PIL         *sudo pip install Pillow*
* GTKterm     *sudo apt-get install gtkterm*
* librairies libv4l & libjpeg *sudo apt install libjpeg-dev libv4l-dev autoconf automake libtool*
=====================================

# Flashage de la Raspberry

On récupère le docker :

**$ docker pull pblottiere/embsys-rpi3-buildroot-video

$ docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash

$ docker# cd /root

$ docker# tar zxvf buildroot-precompiled-2017.08.tar.gz**

On copie l'image, qui sera flasher sur la carte, sur notre machine hôte depuis le docker.

**$ docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .**

Puis on Flash l'image sur la carte SD grâce à la commande _dd_

**$ sudo dd if=sdcard.img of=/dev/sdX**

_sdX_ étant le port sur lequel la carte SD est branché. On peut le récupérer a l'aide de _dmesg_.

Dans le docker commencer par faire:
* _./autogen_, puis
* _./configure --host=arm-buildroot-linux-uclibcgnueabihf cc=../buildroot-precompiled-2017.08/output/host/usr/bin/arm_linux_gcc_
* et enfin cross compilé.

Pour ce faire, il existe la méthode brute qui consiste à modifier les gcc par le gcc du processeur **ARM** dans le Makefile.

#Cross Compilation (Dans le docker)

Commande à réaliser pour cross compiler votre fichier si vous voulez modifier le fichier C ou en créer un nouveau.

*../../buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc -Wall nom_du_fichier.c -o nom_du_fichier.o*

#Copier Fichier dans la RaspberryPi

Il faut copier votre binaire dans la Raspberry Pi.
Pour cela aller sur votre ordinateur, ouvrez gtkterm et configurer le sur le bon port série *ttyUSB0* par exemple (check on _dmesg | grep tty_). Mettre de Baud rate à 155200.

Si non prendre la carte sd et la mettre sur l'ordinateur et déplacer les fichier a la main.

Mettre les fichier dans le répertoire /home/user



# Modification de l'adresse Ip de la RaspberryPi pour rendre l'IP statique

Afin de modifier l'adresse ip de la Raspberry
Connecter vous en liaison série avec votre RaspberryPi
il faut effectuer les commandes suivantes :

**$ sudo nano /etc/network/interfaces**

Il faut ensuite remplacer la ligne

*iface eth0 inet dhcp*

par

*iface eth0 inet static

address 172.20.21.164
netmask 255.255.0.0*

Si vous voulez changer aussi l'adresse wifi de votre carte et la mettre en static rajouter les ligne suivantes a la suite des autre, Mettez une adresse Ip libre de votre réseau wifi :

*iface wlan0 inet static

address XXX.XXX.XXX.XXX
netmask 255.255.0.0*


Adresse ip fixe de la RaspberryPi : _172.20.21.164_
Redémarré votre RaaspberryPi.


## Il faut ensuite faire correspondre Adresse IP fixe de l'ordinateur :
Pour l'ordinateur il faut effectuer la commande, avec XXXXXXX, le nom de l'ethernet de votre pc

*ifconfig XXXXXXX 172.20.11.72*

# Servo Moteur

On a choisit de brancher le servo moteur sur le port **GPIO4**.

Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degrés.

#Lancer le code grâce au Makefile !


Aller dans /home/user, là où se trouve le Makefile et exécutez la commande *makerun*. A cette instant vous entrez dans la peau du client qui peut communiquer avec le server de la RaspberryPi. Reste plus qu'à jouer !


# Règles du jeu ! Commandes chez le client

* Pour changer l'angle de la caméra il vous faudra appuyer sur les touches flèches *droite* et *gauche*. L'angle s'affiche sur l'écran pour savoir ou vous en êtes.

* Pour prendre une photo il faut appuyer sur la touche *s* de votre clavier pour sauvegarder l'image sur votre ordinateur et l'afficher. L'image est écrasée d'un appui à l'autre sur la touche *s*.


<<<<<<< HEAD:TUTO.md



Pour tout autre questions ou évolutions possibles du code, veuillez vous adressez à l'adresser au personnes en question sur le Github.



Pour tout autre questions ou évolutions possibles du code, veuillez vous adressez à l'adresser au personnes en question sur le Github.

/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot
(C'est l'endroit ou trouverl le fichier start_x et fixup_x)

_172.20.11.72_

L'équipe vous remercie de la confiance accordée à leur travail.
