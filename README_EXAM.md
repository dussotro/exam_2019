Linux Embarqué : Mini Projet.

=========Installations requises======
* docker
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

Dans le docker commencer par faire un _autogen_, puis un _configure_ et enfin cross compilé.

Pour ce faire, il existe la méthode brute qui consiste à modifier les gcc par le gcc du processeur **ARM** dans le Makefile.

# Servo Moteur

On a choisit de brancher le servo moteur sur le port **GPIO4**.

Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degres.

# Modification de l'adresse Ip de la Raspb pour la rendre statique

Afin de modifier l'adresse ip de la Raspberry
il faut effectuer les commandes suivantes :

**$ sudo nano /etc/network/interfaces**

Il faut ensuite remplacer la ligne

*iface eth0 inet dhcp*

par

*iface eth0 inet static

address 172.20.21.164
netmask 255.255.0.0*

Adresse ip fixe de la raspberry : _172.20.21.164_

## Il faut ensuite faire correspondre
Adresse ip fixe de l'ordinateur :

Pour l'orinateur il faut effectuer la commande

*ifconfig XXXXXXX 172.20.11.72*

Pour moi XXXXXX c'est enp4s0f1, c'est le nom de l'ethernet du pc.

/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot
(C'est l'endroit ou trouverl le fichier start_x et fixup_x)

_172.20.11.72_

../../buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc
