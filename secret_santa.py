import smtplib
from random import choice
from yaml import safe_load
from sys import argv
from getpass import getpass

if __name__ == '__main__':
    print ("Bienvenue dans l'outil Secret-Santa")

#############################
# Importation des variables #
#############################

tirage = safe_load (open('my_tirage.yaml', 'r'))

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

#################
# Zone exécutée #
#################

if __name__ == '__main__':
    try:
        # connexion au serveur SMTP
        serveur = smtplib.SMTP(hostname)
        serveur.starttls()
        serveur.login(username, password)

        # attribution des rôles
        name_list = [x["name"] for x in receivers]
        for person in receivers:
            target = person["name"]
            while target in person["blacklist"]:
                target = choice(name_list)
            # print ("{} doit donner un cadeau à {}".format(person["name"], target))
            serveur.sendmail(sender, person["email"], message.format(sender, person["email"], person["name"], target).encode('utf-8'))
            # print (message.format(sender, person["email"], person["name"], target))
            name_list.remove(target)

        serveur.close()
        print ("Secret-Santa a fini son travail")
    except Exception as e:
        print ("Erreur :"+str(e))
