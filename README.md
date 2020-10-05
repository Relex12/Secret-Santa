# Secret-Santa
Tirage au sort pour réaliser un Père Noël surprise

![](https://img.shields.io/badge/status-Finished-green) ![](https://img.shields.io/github/v/release/Relex12/Secret-Santa) ![](https://img.shields.io/github/license/Relex12/Secret-Santa) ![](https://img.shields.io/github/repo-size/Relex12/Secret-Santa) ![](https://img.shields.io/github/languages/top/Relex12/Secret-Santa) ![](https://img.shields.io/github/last-commit/Relex12/Secret-Santa) ![](https://img.shields.io/github/stars/Relex12/Secret-Santa?color=red)

---

## Sommaire

* [Qu'est-ce que c'est ?](#Qu'est-ce-que-c'est-)
* [Comment ça marche ?](#Comment-ça-marche-)
* [Comment l'utiliser ?](#Comment-l'utiliser-)
  * [Installation](#Installation)
  * [Compléter les informations](#Compléter-les-informations)
    * [Connexion au serveur mail](#Connexion-au-serveur-mail)
    * [Liste des participants](#Liste-des-participants)
    * [Message du mail](#Message-du-mail)
* [Comment faire le tirage au sort ?](#Comment-faire-le-tirage-au-sort-)
  * [Requis](#Requis)
  * [Erreurs possibles](#Erreurs-possibles)
* [Améliorations possibles](#Améliorations-possibles)
* [Licence](#licence)

## Qu'est-ce que c'est ?

Secret-Santa permet de réaliser un tirage au sort pour le Père Noël surprise.

Le Père Noël surprise est une manière originale de se faire des cadeaux à Noël : vous inscrivez le nom de tous les participants sur des bouts de papier, puis vous les mettez dans une boîte. Ensuite on procède au tirage au sort : chaque participant pioche tour à tour le nom de la personne à laquelle il fera un cadeau. Lorsque tout le monde a pioché un bout de papier, chacun sait à qui il doit faire un cadeau.

Le but est que personne ne soit au courant de qui offre quel cadeau à quelle personne.

**Problèmes** : Comment faire si une personne a pioché son propre nom dans la boîte ? Si plusieurs participants ne se connaissent pas très bien, cela peut être embarrassant de trouver un cadeau adapté. Et si jamais un participant pioche la même personne qu'une année précédente ?

Soit vous refaites un tirage au sort jusqu'à ce que le résultat convienne à tout le monde, soit vous utilisez Secret-Santa.

## Comment ça marche ?

Vous devez préciser à Secret-Santa la liste des participants. Pour chaque participants, vous devez donner un nom d'utilisateur, une adresse mail ainsi que la liste des personnes qu'il ne pourra pas piocher (une blacklist).

**Secret-Santa va alors effectuer le tirage au sort automatique, puis envoyer par mail à chaque participants le nom de la personne à laquelle il doit faire un cadeau.**

De cette manière, personne ne sait qui offre quel cadeau à quelle personne, et **il n'y a besoin d'effectuer qu'un seul tirage**.

## Comment l'utiliser ?

Pour utiliser Secret-Santa, plusieurs étapes sont nécessaires. Il faut que l'un des participants, le Maître du tirage, se dévoue pour réaliser le tirage au sort depuis son ordinateur.

### Installation

Pour utiliser Secret-Santa, le Maître du tirage doit le copier sur son ordinateur, deux possibilités :

* depuis un terminal de commande : `git clone https://github.com/Relex12/Secret-Santa.git`
* en téléchargeant le code source :
  * depuis un navigateur, aller sur `https://github.com/Relex12/Secret-Santa` > bouton `Code` > `Download ZIP`
  * dans vos téléchargements, extraire l'archive téléchargée

### Compléter les informations

Maintenant que le Maître du tirage a le code source de Secret-Santa, il va devoir faire deux choses avant de procéder au tirage :

* modifier le fichier `tirage.yaml` qui contient les information de connexion et la liste des participants

* modifier dans le code source `secret_santa.py` le message envoyé par mail (facultatif)

Le fichier `tirage.yaml` **doit** être dans le même répertoire (dossier) que `secret_santa.py`.

#### Connexion au serveur mail

Pour pouvoir envoyer les résultats par mail, Secret-Santa doit se connecter à un serveur mail correspondant à une adresse mail accessible au Maître du tirage.

Les informations nécessaires à la connexion sont récupérées dans le fichier `tirage.yaml`. Voici le contenu à modifier :

``` yaml
#############################
# Connexion au serveur mail #
#############################

hostname: 	"nom_de_domaine:port"
username: 	"user"				# facultatif
password: 	"p@ssw0rd"			# facultatif
sender: 	"email_address"
```

Pour obtenir le nom de domaine et le numéro de port, vous devez voir ceci dans la configuration du serveur mail que vous utilisez (e.g Yahoo, Orange, Gmail, etc...).  

Le nom d'utilisateur et le mot de passe sont ceux que vous utilisez pour vous connecter à votre boîte mail. L'adresse mail entière (avec nom de domaine) doit être renseignée comme émissaire.

**Sécurité** : pour renseigner votre nom d'utilisateur et votre mot de passe, vous avez plusieurs méthodes :

* plus **pratique** : vous renseignez les identifiants en clair dans le fichier comme ci-dessus, pensez tout de même à supprimer le fichier de manière définitive après le tirage au sort.
* **compromis** : vous renseignez les identifiants comme arguments lors de l'appel `python secret_santa.py username password` (vous pouvez préciser uniquement le nom d'utilisateur pour plus de sécurité)

* plus **sécurisé** : vous renseignez les identifiants lors de l'exécution, ils vous seront demandés si vous ne les avez pas renseigné plus tôt

Vous pouvez vérifier dans le code source que ces informations ne sont jamais stockées ou divulguées avec une autre entité que votre serveur de mail. Secret-Santa ne garde aucune trace de vos identifiants.

**Avec Gmail** (le plus simple) :

* si vous utilisez une adresse Gmail, vous pouvez compléter comme ceci : `hostname='smtp.gmail.com:587'`
* le mot de passe qui vous sera demandé est un mot de passe d'application, voir ici comment générer et se connecter avec un mot de passe d'application : https://support.google.com/accounts/answer/185833

#### Liste des participants

La liste des participants doit être renseignée sous la forme d'une liste de dictionnaires. Chaque dictionnaire représente un participant, il possède les clés :

* `name` : nom du participant sous forme de chaîne de caractères
* `email` : adresse mail du participant sous forme de chaîne de caractères
* `blacklist` : liste des personnes qui ne pourront pas être piochées sous la forme d'une liste de chaînes de caractères

Vous devez modifier le contenu de `tirage.yaml` selon l'exemple ce-dessous pour qu'il corresponde à votre tirage :

```` yaml
#######################
# Liste des personnes #
#######################

receivers:
  - name: "Alice"
  	email: "alice@yahoo.fr"
    blacklist: ["Alice", "Dave"]
  - name: "Bob"
   	email: "bob@gmail.com"
    blacklist: ["Bob"]
  - name: "Carol"
   	email: "carol@orange.fr"
    blacklist: ["Carol"]
  - name: "Dave"
   	email: "dave@hotmail.com"
    blacklist: ["Dave", "Alice"]
  - name: "Eve"
   	email: "eve@aol.com"
    blacklist: ["Eve", "Carol"]
  - name: "Franck"
   	email: "franck@msn.com"
    blacklist: ["Franck", "Bob", "Carol"]
````

**Important** : si vous ne voulez pas qu'un participant puisse piocher son propre nom, il faut que chaque blacklist contienne au minimum le nom du participant (comme ci-dessus).

#### Message du mail

Le message du mail qui est envoyé par Secret-Santa aux participants peut être modifié selon la volonté du Maître du tirage. Le message est écrit selon la syntaxe HTML, avec des balises pour la mise en page.

Le mail par défaut est le suivant (modifier uniquement si vous savez ce que vous faîtes) :

```` python
message = """From: From Secret-Santa <{0}>
To: To {2} <{1}>
MIME-Version: 1.0
Content-type: text/html; charset=utf-8
Subject: Secret-Santa - distribution des r=?utf-8?B?w7Q=?=les

<h1>Bonjour {2}</h1>

La personne qui t'a été attribuée lors du tirage au sort est <b>{3}</b>.<br><br><br>

Bon courage pour lui trouver un cadeau,<br><br>

Et n'oublie que moins les gens savent, plus c'est fun.<br><br>

<hr>
Secret-Santa est un bot créé par Adrian Bonnet.<br>
"""
````

**Pour les entêtes** :  laissez les valeurs de `From:`, `To:`, `MIME-Version:` et `Content-type:` tel quel pour ne pas avoir de mauvaises surprises.

**Pour le sujet du mail** : Si vous voulez utiliser des caractères non ascii dans le sujet du mail, il faut utiliser la représentation décrite dans la RFC 1342, c'est-à-dire dans le format `=?charset?encoding?encoded-text?=`.

Par exemple pour utiliser le caractère `ô`, il faut écrire `=?utf-8?B?w7Q=?=` (`utf-8` est l'ensemble de caractères, `B` est l'encodage base64 et `w7Q=` la représentation de `ô` en base64).

**Pour le formatage du message** :

* `{0}` est remplacé par l'adresse d'émission (`sender`)
* `{1}` est remplacé par l'adresse de réception du participant (`receiver`, clé `email`)
* `{2}` est remplacé par le nom du participant auquel est envoyé le mail (`receiver`, clé `name`)
* `{3}` est remplacé par le nom du participant pioché auquel le destinataire devra offrir un cadeau

**Mention** : merci de laisser la mention en bas de mail comme lien vers le travail de l'auteur.

## Comment faire le tirage au sort ?

Une fois que toutes les modifications ci-dessus ont été effectuées, le Maître du tirage n'a plus qu'à lancer le script depuis un terminal de commande : `python secret_santa.py`.

L'exécution commence lorsque le message `Bienvenue dans l'outil Secret-Santa` s'affiche. Si l'exécution se passe sans erreur ni problèmes, le message `Secret-Santa a fini son travail` s'affiche quelques secondes plus tard. A ce moment-là, les mails ont été envoyés.

### Requis

Pour exécuter Secret-Santa, Python doit être installé sur la machine du Maître du tirage. Comme la fonction `random.choices()` est utilisée, la version 3.6 ou une version supérieure de Python est requise.

### Erreurs possibles

**Connexion au serveur** : Lors de la connexion au serveur, diverses erreurs peuvent se produire. Comme ces erreurs sont propres à la communication avec le serveur mail, il n'est pas possible de faire une liste détaillée des erreurs possibles.

**`ImpossibleToDrawError`** : Cette erreur signifie que le tirage au sort a échoué de trop nombreuses fois et qu'il est considéré comme impossible de le réaliser. Vous devrez alors faire des concessions sur les blacklists de certains participants.

## Améliorations possibles

Secret-Santa laisse sur la boîte mail du Maître du tirage les mails qu'il a envoyé. **Afin de ne pas tricher, le Maître du tirage doit supprimer ces mails de sa boîte mail manuellement.**

Pour remédier à cela, il faut arriver à récupérer les derniers mails envoyés en utilisant le protocole IMAP, puis supprimer ces mails.

## Licence

Ce projet est un petit projet. Le code source est donné librement à la communauté GitHub, sous la seule licence MIT, qui n'est pas trop restrictive.
