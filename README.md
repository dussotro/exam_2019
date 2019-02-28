Ce projet s'inscrit dans le cadre d'un projet réalisé durant notre dernière année d'école d'ingénieur à L'ENSTA Bretagne.

Dans ce Github vous trouverez:
* un dossier server ou les code originels sont disponible.
* un dossier client ou le code client est disponible.
* Les fichiers déjà compiler à télécharger et à copier sur votre RaspberryPI *projet_cross_compiler*.

Notre système se compose de 4 fichiers importants:

* servo_server.py (RaspberryPI)
* v4l2grab        (RaspberryPI)
* server_camera   (RaspberryPI)
* client.py       (Ordinateur)




=========Installations requises======
* Docker      *https://doc.ubuntu-fr.org/docker* suivre les indication
* Pygame      *sudo pip install pygame*
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
* _cd exam_2019/server/v4l2grab/_
* _./autogen.sh_, puis
* _ac_cv_func_malloc_0_nonnull=yes ac_cv_func_realloc_0_nonnull=yes ./configure --host=arm-buildroot-linux-uclibcgnueabihf CC=/root/buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc_
* _make_,pour cross compilé
* _cd /root/exam_2019/servers/_
* _/root/buildroot-precompiled-2017.08/output/host/bin/arm-linux-gcc -Wall -o server_camera.o server_camera.c_


le Fichier cross compiler pour votre RaspberryPi est **v4l2grab**

### Flashage de la raspberry

On copie l'image, qui sera flasher sur la carte, sur notre machine hôte depuis le docker.
Ouvrez un autre terminal ou vous serez en dehors du docker et executez la commande suivante:

**$ sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .**

Vous trouvez le contener id en executant la commande **sudo docker ps -a**

Puis on Flash l'image sur la carte SD grâce à la commande _dd_

**$ sudo dd if=sdcard.img of=/dev/sdX bs=4096 status=progress**

_sdX_ étant le port sur lequel la carte SD est branché. On peut le récupérer a l'aide de _dmesg_.

Si des fois vous voulez modifier l'image, par exemple rajouter des librairie, cela est possible mais il faudra recompiler l'image grâce à l'outil Buildroot.

# Buildroot

Voici comment on utilise builroot.
Vous savez déjà cross-compiler avec buildroot! Voir au dessus,, mais si vous voulez avoir plus d'info !

Si vous voulez avoir des informations sur l'image en question, le kernel et plus encore, executez la commande **make menuconfig** dans le docker dans buildroot-precompiled-2017.08 .

Pour d'autres informations, voici le lien vers la documentation officiel: https://buildroot.org/downloads/manual/manual.html pour savoir comment utiliser ce fabuleux outil. 


## Copier Fichier dans la RaspberryPi
Mettez vous dans le terminal ou vous n'êtes pas dans le Docker.
Copier les fichiers sur votre ordinateur, depuis le docker, dans un dossier:

**sudo docker cp <container_id>:/root/exam_2019/servers/servo_server.py .**

**sudo docker cp <container_id>:/root/exam_2019/servers/v4l2grab/v4l2grab .**

**sudo docker cp <container_id>:/root/exam_2019/servers/server_camera.o .**

**sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot/start_x.elf .**

**sudo docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/build/rpi-firmware-685b3ceb0a6d6d6da7b028ee409850e83fb7ede7/boot/fixup_x.dat .**


Monter la carte SD pour faciliter la copie des fichiers. Ces fichiers sont disponibles dans le dossier *almost_plug_and_play*

Mettre les fichiers dans le répertoire _/home/user_,créez un dossier server qui aura les fichiers:
* servo_server.py
* server_camera.o (fichier cross compilé)
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

Pour cela, brancher la Raspberry en liaison série avec votre ordinateur. Aller sur votre ordinateur, ouvrez _gtkterm_ et configurer le sur le bon port série *ttyUSB0* par exemple (check on _dmesg | grep tty_).
Mettre de Baud_rate à 115200
Si rien ne s'affiche, débrancher et rebrancher l'alimentation de la RaspberryPi.

Vous devez ensuite entrer l'identifiant : _root_ et le mot de passe: _*root1*_

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
Si ce n'est pas la cas, vous pouvez executer la commande suivant dans le terminal *gtkterm*:
**ifconfig eth0 172.20.21.164**
Cette commande fixera l'addresse Ip de la RaspberryPi.

### Il faut ensuite faire correspondre Adresse IP fixe de l'ordinateur :
Pour l'ordinateur il faut effectuer la commande,

en général l'éthernet peut s'appeler *ethX* ou *enpXXXXX*: on peut utiliser *ifconfig* pour trouver le nom de l'interface.

*ifconfig XXXXXXX 172.20.11.72*

## Servo Moteur

On a choisit de brancher le servo moteur sur le port **GPIO4**.
[Pour trouver les pins de votre raspberry](https://www.framboise314.fr/wp-content/uploads/2018/02/kit_composants_GPIO_01.png)
Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degrés.

## Lancement du code

Sur la RaspberryPI, aller dans _/home/user/_, là où se trouve les fichiers à exécuter et exécutez les commande suivantes à l'aide de _gtkterm_:
* **python server_servo.py 172.20.21.164 &**
* **./server_camera.o**

Sur votre ordinateur, aller dans le dossier client et lancer la commande, **python3 client.py**. A cette instant vous entrez dans la peau du client qui peut communiquer avec le server de la RaspberryPi.

## Règles du jeu ! Commandes chez le client

* Pour changer l'angle de la caméra il vous faudra appuyer sur les touches flèches *droite* et *gauche*. L'angle s'affiche sur l'écran pour savoir ou vous en êtes.

* Pour prendre une photo il faut appuyer sur la touche *s* de votre clavier (essayer de rester appuyé), pour sauvegarder l'image sur votre ordinateur et l'afficher. L'image est écrasée d'un appui à l'autre sur la touche *s*.

* Si vous rester appuyer dessus, vous aurez une vidéo en 1fps ! Trop rapide.

## Problèmes éventuels
Si vous rencontrez des soucis lors de l'exécution des commandes lançant les codes, vérifiez bien les addresses Ip de votre ordinateur et de la RaspberryPi.

Pour toutes autres questions ou demandes, n'hésitez pas à nous contacter.

L'équipe vous remercie de la confiance accordée à leur travail.

Amusez-vous bien !


Elias & Evann & Romain & Victor.
