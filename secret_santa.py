import smtplib
from random import choice
from yaml import safe_load
from sys import argv
from getpass import getpass

class ImpossibleToDrawError(Exception):
    """
    This error is raised when `nb_err` exceeds `LIMIT_ERR_MAX`.
    """
    def __init__(self):
        pass

LIMIT_ERR_MAX = 50
"""
When too many errors occur during the drawing, it is considered impossible.
"""

if __name__ == '__main__':
    print ("Bienvenue dans l'outil Secret-Santa")

#############################
# Importation des variables #
#############################

tirage = safe_load (open('tirage.yaml', 'r'))

# Connexion au serveur mail
hostname = tirage['hostname']
sender = tirage['sender']

if len(argv) > 1:
    username = argv[1]
elif 'username' in tirage.keys():
    username = tirage['username']
else:
    username = input("nom d'utilisateur : ")

if len(argv) > 2:
    password = argv[2]
elif 'password' in tirage.keys():
    password = tirage['password']
else:
    password = getpass("mot de passe : ")

# Liste des personnes
receivers = tirage['receivers']

#####################
# Message à envoyer #
#####################

message = """From: From Secret-Santa <{0}>
To: To {2} <{1}>
MIME-Version: 1.0
Content-type: text/html; charset=utf-8
Subject: Secret-Santa - distribution des r=?utf-8?B?w7Q=?=les

<h1>Bonjour {2}</h1>

La personne qui t'a été attribuée lors du tirage est <b>{3}</b>.<br><br><br>

Bon courage pour lui trouver un cadeau,<br><br>

Et n'oublie que moins les gens savent, plus c'est fun.<br><br>

<hr>
Secret-Santa est un bot créé par Adrian Bonnet.<br>
"""

message = """From: From Secret-Santa <{0}>
To: To {2} <{1}>
MIME-Version: 1.0
Content-type: text/html; charset=utf-8
Subject: Secret-Santa - test des adresses mails

<h1>Bonjour {2}</h1>

Ce message est un test pour vérifier que toutes les adresses mails sont correctes.<br><br>

La personne qui t'a été attribuée lors de ce test est <b>{3}</b>.<br><br><br>

Merci de ne pas tenir compte de ce message pour l'instant.<br><br>

Le vrai message arrive dans la soirée.<br><br>

<hr>
Secret-Santa est un bot créé par Adrian Bonnet.<br>
"""

#################
# Zone exécutée #
#################

if __name__ == '__main__':

    # tri des participants par longueur de blacklist décroissante
    receivers = sorted(receivers, key=lambda person: len(person["blacklist"]), reverse=True)

    # attribution des rôles
    error_while_exec = True
    nb_err = 0

    # si le tirage en cours n'est pas soluble, on recommence
    while error_while_exec:
        error_while_exec = False
        name_list = [x["name"] for x in receivers]

        # pour chaque personne, on tire sa cible parmi les personnes possibles
        for person in receivers:
            # [name_list] - [person["blacklist"]]
            drawable = [x for x in name_list if not x in person["blacklist"]]
            if drawable == []:  # on recommence
                error_while_exec = True
                nb_err += 1
            else:
                target = choice(drawable)
                person["target"] = target
                name_list.remove(target)
        if nb_err > LIMIT_ERR_MAX:
            raise ImpossibleToDrawError

    try:
        # connexion au serveur SMTP
        serveur = smtplib.SMTP(hostname)
        serveur.starttls()
        serveur.login(username, password)
        for person in receivers:
            # print ("{} doit donner un cadeau à {}".format(person["name"], person["target"]))
            serveur.sendmail(sender, person["email"], message.format(sender, person["email"], person["name"], person["target"]).encode('utf-8'))
            # print (message.format(sender, person["email"], person["name"], target))

        serveur.close()
        print ("Secret-Santa a fini son travail")
    except Exception as e:
        print ("Erreur : "+str(e))
