# TP2_SB_ME
TP finale INF8214
Setup pour git:
  1) Créer un compte github 
  2) Setup une clé ssh : 
      - En ligne de commande sur l'ordinateur personnel taper la commande: ssh-keygen -t rsa 
      - - Se connecter sur son compte github, aller dans settings, puis dans SSH and GPG key. 
      - Ajouter un nouvelle cle, puis copier coller le contenu du fichier id_rsa.pub 
  3) Créer un repertoire local:  
  4) En ligne de commande, sur son desktop taper la commande: git clone git@github.com:mennajimi/TP2_SB_ME.git


COMMANDE IMPORTANTE POUR GIT (dans le terminal)

*********
Super important: Toujours toujours toujours (si tu veux pas de conflits de version) faire un "git pull" avant de commencer à travailler
*********

- git pull = Mise à jour du répertoire (quand tu commences à travailler)

Si tu veux rajouter des modifications:
  1- git add= ajout de modifications local (sur ta machine)
  2-git commit= commit et ajout de commentaires (avec nano)
  3-git push = soumettre les changements au répertoire distant
  
Commande pratiques
* git status = Vérifier le status du projet
* git diff= Montrer les changements
* git checkout -b NomDeLaBranche = Changer ou créer une branche
* git log = Voir l'historique des changements
