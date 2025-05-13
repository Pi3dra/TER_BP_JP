# TER_BP_JP

## Commandes utilisées frequemment

Copier des fichiers qui sont dans le raspberry:
scp pi@your_raspberry_ip:/path/to/remote/file /path/to/local/destination

Lancer les scripts pythons en arriere-plan:
nohup python3 script.py > output.log 2>&1 &

Arreter le script precedent:
kill $(pgrep -f script.py)

Verifier le fonctionnement de systemd-networkd:
sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd
sudo systemctl status systemd-networkd

Activer un environement python:
source myenv/bin/activate

Creation environement python et installation de librairies
python3.11 -m venv myenv
sourche myenv/bin/activate
pip install -r requirements.txt


Username@Hostname des Raspberrys:
capteur@kpteur
pi@controlleur

## Demarrage

- tout brancher et connecter les Raspberrys, et votre ordinateur au même reseaux wifi

- Ensuite se connecter par ssh aux deux Raspberrys
avec ssh username@hosntame.local 

- lancer la commande ifconfig pour noter l'adresse IP du capteur 

- Sur le capteur, lancer le script ./LaunchServer <IP_Capteur> <Q_table>(Optionnel)
    En utilisant l'environement python myenv
    ceci lance  le script server.py en arriere arriere-plan
    et le script capteur.py pour transmettre les données au serveur 
    qui les transmet ensuite au controlleur

- Sur le controlleur lancer ./LaunchClient -ip IP du capteur
    En utilisant l'environement python myenv ceci lance le script
    

Si les scripts ne marchent pas il est possible de tout lancer manuellement avec les commandes
données en haut.

cela devrait donc demarrer la voiture.

Si ce n'est pas le cas verifier que tout marche et est bien branché avec les scripts dans le dossier tests:

le script gpio.py doit faire avancer la voiture avec des intervalles de vitesse croissants.

Pour verifier le capteur il faut brancher une manette a l'endroit ou est branché le controlleur, lancer le script
ensuite faire avancer la voiture et verifier que les mesures sont coherents (valeur comprises ente -0.5 et 14.7)



## Autre

Dans le git vous trouverez aussi des schemas expliquant comment brancher les differents composants, et les fiches techniques des differents composants.
