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



=========Installations requises======
* Docker      *sudo apt install docker*
* MatplotLib  *sudo pip install matplotlib*
* Pygame      *sudo pip install pygame*
* PIL         *sudo pip install Pillow*
* GTKterm     *sudo apt-get install gtkterm*
=====================================

# DEROULEMENT
* Préparation du docker
* Flashage de la Raspberry
* Cross compilation
* Copie des dossier sur la Raspberry et votre Ordinateur
* Modification Adresse IP (RAPSBERRYPI et ORDINATEUR)
* Branchement Servo moteur & caméra
* Commande à lancer
* Règle du jeu

## Préparation du docker

On récupère le docker :

**sudo docker pull pblottiere/embsys-rpi3-buildroot-video**

**sudo docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash**

**$ docker# cd /root**

**$ docker# tar zxvf buildroot-precompiled-2017.08.tar.gz** 


## Cross Compilation (Dans le docker)

Commande à réaliser pour cross compiler votre fichier si vous voulez modifier le fichier C ou en créer un nouveau.

Dans le docker commencer par faire:
* _git clone https://github.com/dussotro/exam_2019.git_
* _cd exam_2019/server/camera/v4l2grab-master/
* _./autogen.sh_, puis
* _ac_cv_func_malloc_0_nonnull=yes ac_cv_func_realloc_0_nonnull=yes ./configure --host=arm-buildroot-linux-uclibcgnueabihf CC=/root/buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc_
* _make_,pour cross compilé

le Fichier cross compiler pour votre RaspberryPi est **v4l2grab**

### Flashage de la raspberry

On copie l'image, qui sera flasher sur la carte, sur notre machine hôte depuis le docker.
Ouvrez un autre terminal ou vous serez en dehors du docker et executez la commande suivante:

**$ sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .**

Vous trouvez le contener id en executant la commande **sudo docker ps -a**

Puis on Flash l'image sur la carte SD grâce à la commande _dd_

**$ sudo dd if=sdcard.img of=/dev/sdX bs=4096 status=progress**

_sdX_ étant le port sur lequel la carte SD est branché. On peut le récupérer a l'aide de _dmesg_.

## Copier Fichier dans la RaspberryPi
Mettez vous dans le terminal ou vous n'êtes pas dans le Docker.
Copier les fichiers sur votre ordinateur, depuis le docker, dans un dossier:

**sudo docker cp <container_id>:/root/exam_2019/servers/servo_server.py .**

**sudo docker cp <container_id>:/root/exam_2019/servers/camera/v4l2grab-master/v4l2grab .**

**sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot/start_x.elf .**

**sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot/fixup_x.dat .**


Prendre la carte sd et la mettre sur l'ordinateur et déplacer les fichier à la main.

Mettre les fichiers dans le répertoire _/home/user_,créez un dossier server qui aura les fichiers:
* servo_server.py
* v4l2grab (fichier cross compilé)

Il faut aussi que vous copier les fichier sur la 1ère partition de la carte SD:
* _start_x.elf_
* _fixup_x.dat_
Utilisé la commande _cp_ ou faite le à la main.


Modifier le fichier *config.txt* de la 1ère partition en ajoutant ces lignes:
**start_x=1
gpu_mem=128**

## Modification de l'adresse Ip de la RaspberryPi pour rendre l'IP statique

Connecter votre Raspberry en ethernet a votre ordinateur.
Afin de modifier l'adresse ip de la Raspberry
Connecter vous en liaison série avec votre RaspberryPi

Pour cela, brancher la Raspberry en liaison série avec votre ordinateur. Aller sur votre ordinateur, ouvrez _gtkterm_ et configurer le sur le bon port série *ttyUSB0* par exemple (check on _dmesg | grep tty_).
Mettre de Baud_rate à 115200.

Par la suite il faut effectuer les commandes suivantes sur gtkterm :

**$ sudo nano /etc/network/interfaces**

Il faut ensuite remplacer la ligne

*iface eth0 inet dhcp*

par

*auto eth0<br />
allow-hotplug eth0<br />
iface eth0 inet static<br />
  address 172.20.21.164<br />
  netmask 255.255.0.0<br />
  geteway 172.20.255.255*


Si vous voulez changer aussi l'adresse wifi de votre carte et la mettre en static rajouter les ligne suivantes à la suite des autres. Mettez une adresse Ip libre de votre réseau wifi :

*iface wlan0 inet static*

*address XXX.XXX.XXX.XXX*<br />
*netmask 255.255.0.0*

Adresse ip fixe de la RaspberryPi : _172.20.21.164_<br />
Redémarré votre RaaspberryPi.

Veuillez bien vérifier que votre RaspberryPi est bien la bonne adresse IP. 
Si ce n'est pas la cas

### Il faut ensuite faire correspondre Adresse IP fixe de l'ordinateur :
Pour l'ordinateur il faut effectuer la commande,

*ifconfig XXXXXXX 172.20.11.72*

 avec XXXXXXX, le nom de l'ethernet de votre pc

## Servo Moteur

On a choisit de brancher le servo moteur sur le port **GPIO4**.
[Pour trouver les pins de votre raspberry](https://www.framboise314.fr/wp-content/uploads/2018/02/kit_composants_GPIO_01.png)
Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degrés.

## Lancement du code

Sur la RaspberryPI, aller dans _/home/user/server_, là où se trouve le Makefile et exécutez la commande *make*, cette commande vas exécuter les commandes nécessaires.
Et ensuite *make run* pour lancer les servers.
A cette instant les serveurs sont lancés.

Sur votre ordinateur, aller dans le dossier client et lancer la commande, *make*. A cette instant vous entrez dans la peau du client qui peut communiquer avec le server de la RaspberryPi.

## Règles du jeu ! Commandes chez le client

* Pour changer l'angle de la caméra il vous faudra appuyer sur les touches flèches *droite* et *gauche*. L'angle s'affiche sur l'écran pour savoir ou vous en êtes.

* Pour prendre une photo il faut appuyer sur la touche *s* de votre clavier pour sauvegarder l'image sur votre ordinateur et l'afficher. L'image est écrasée d'un appui à l'autre sur la touche *s*.

L'équipe vous remercie de la confiance accordée à leur travail.


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
