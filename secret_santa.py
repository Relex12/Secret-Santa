#!/usr/bin/env python3

from smtplib  import SMTP
from random   import choice
from yaml     import safe_load
from sys      import argv
from getpass  import getpass
from argparse import ArgumentParser

# When too many errors occur during the drawing
# it is considered impossible
LIMIT_ERR_MAX = 50

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

Ceci est le véritable tirage, garde précieusement ce mail en cas d'oubli.<br><br>

Bon courage pour lui trouver un cadeau,<br><br>

Et n'oublie que moins les gens savent, plus c'est fun.<br><br>

<hr>
Secret-Santa est un bot créé par Adrian Bonnet.<br>
"""
# TODO: use a specified library for subject encoding instead of doing it manually

test_msg = """From: From Secret-Santa <{0}>
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


def drawing(receivers):
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
            # raise ImpossibleToDrawError
            raise Exception(f"error: draw failed {LIMIT_ERR_MAX} times consecutively, considered impossible")

def print_draw(receivers):
    str = ''
    for person in receivers:
        str+=f"{person['name']} got {person['target']}, "
    print (str)

def check_draw(receivers):
    for person in receivers:
        if not args.self_include and person["target"] == person["name"]:
            raise Exception(f"error: {person['name']} draw himself")

        for other in receivers:
            if person != other and person["target"] == other["target"]:
                raise Exception(f"error: {person['name']} and {other['name']} draw the same person {person['target']}")

if __name__ == '__main__':

    ########################
    # Arguments processing #
    ########################

    parser = ArgumentParser()

    parser.add_argument("-c", "--config"  , type=str, default='tirage.yml', help="config file name, default tirage.yml")
    parser.add_argument("-H", "--hostname", type=str, help="hostname for email server connection")
    parser.add_argument("-u", "--username", type=str, help="username for email server connection")
    parser.add_argument("-p", "--password", type=str, help="password for email server connection")
    parser.add_argument("-s", "--sender"  , type=str, help="sender email for email server connection")

    parser.add_argument("-i", "--self-include", action='store_true', help="receivers can draw themselves")
    parser.add_argument("-t", "--test" , action='store_true', help="send a test mail instead of real draw")
    parser.add_argument("-d", "--debug", action='store_true', help="for debug purposes")
    parser.add_argument("-l", "--log"  , action='store_true', help="for debug purposes")

    args = parser.parse_args()

    print ("Bienvenue dans l'outil Secret-Santa")

    ####################
    # Import variables #
    ####################

    draw = safe_load (open(args.config, 'r'))
    # TODO: rename draw as draw

    hostname = args.hostname if args.hostname is not None else draw['hostname'] if 'hostname' in draw.keys() else None
    if hostname is None:
        raise Exception("error: hostname unspecified")

    sender = args.sender if args.sender is not None else draw['sender'] if 'sender' in draw.keys() else None
    if sender is None:
        raise Exception("error: sender unspecified")

    username = args.username if args.username is not None else draw['username'] if 'username' in draw.keys() else None
    if username is None:
        username = input("nom d'utilisateur : ")

    password = args.password if args.password is not None else draw['password'] if 'password' in draw.keys() else None
    if password is None:
        password = input("mot de passe : ")
    if args.password is not None:
        print("Warning: giving password as argument is not unsafe, consider using config file or input text")

    receivers = draw['receivers'] if 'receivers' in draw.keys() else None
    if receivers is None:
        raise Exception("error: receivers unspecified")


    # Include receivers in their own blacklist
    if not args.self_include:
        for person in receivers:
            if not person["name"] in person["blacklist"]:
                person["blacklist"].append(person["name"])

    # Proceed drawing
    drawing(receivers)
    if args.log:
        print_draw(receivers)
    check_draw(receivers)

    # Send emails
    if not args.debug:
        msg_to_send = message if not args.test else test_msg
        try:
            # Connexion au serveur SMTP
            serveur = SMTP(hostname)
            serveur.starttls()
            serveur.login(username, password)
            for person in receivers:
                serveur.sendmail(sender, person["email"], msg_to_send.format(sender, person["email"], person["name"], person["target"]).encode('utf-8'))

            serveur.close()
            print ("Secret-Santa a fini son travail")
        except Exception as e:
            print ("Erreur : "+str(e))

    # Debug section
    if args.debug:
        for i in range (1, 1000000):
            drawing(receivers)
            if args.log:
                print_draw(receivers)
            check_draw(receivers)
