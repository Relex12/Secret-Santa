
# Serveur école :
# serveur = smtplib.SMTP('smtps.esisar.grenoble-inp.com:465')

#################
# Zone exécutée #
#################

import smtplib
from random import choice

if __name__ == '__main__':
    print ("Bienvenue dans l'outil Secret-Santa")
    try:
        # connexion au serveur SMTP
        serveur = smtplib.SMTP(hostname)
        serveur.starttls()
        serveur.login(username, password)

        # attribution des rôles
        name_list = [x["name"] for x in receivers]
        for person in receivers:
            cible = person["name"]
            while cible in person["blacklist"]:
                cible = choice(name_list)
            # print ("{} doit donner un cadeau à {}".format(person["name"], cible))
            serveur.sendmail(sender, person["email"], message.format(sender, person["email"], person["name"], cible).encode('utf-8'))
            # print (message.format(sender, person["email"], person["name"], cible))
            name_list.remove(cible)

        serveur.close()
        print ("Secret-Santa a fini son travail")
    except Exception as e:
        print ("Erreur :"+str(e))
