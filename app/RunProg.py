"""

    SeqGen Runner
    version 1.0
    Auteur : Salix Boulet
    Date   : Hiver 2022

    Ce programme permet l'exécution de SeqGen à partir d'un fichier d'entré de paramètres.
    Dépendences: validation.py version 1


"""

import re
import os
import shutil
import subprocess
from datetime import datetime


class RunProg:

    def __init__(self, paramsFile, infile, outfile, directory):
        print("prog inti")
        self.__directory = directory
        self.__params = paramsFile   #__params: de __input, les éléments qui sont des paramètres seqgen
        self.__infile, self.__outfile = infile, outfile
        self.__valide = True # valide _valide: Boolean qui indique si les paramètres entrés sont valides pour Seqgen
        self.__process = ""  #__process: permet de lancer le processus d'exécution de programme
        self.__logfile = ""  #__logfile: sauvegarde le log de Seqgen pour consultation au besoin

    def run(self):         # initie l'exécution, à l'aide de la fonction run_popen ci-bas
        cmd = shutil.which("./seq-gen")
        if (self.__valide == True and '-h' in self.__params):
            cmd = "./seq-gen -h"
        elif self.__valide != 0:

            # on crée la commande
            for cle, valeur in self.__params.items():
                cmd += " -" + cle + valeur + " "
            cmd += " < " + self.__infile + " > " + self.__outfile

        RunProg.run_popen(self, cmd)
        print("Process SeqGen initié")

    def run_popen(self, cmd):     # créer une instance de popen (self.__process) pour gérer l'exécution
        self.__logfile = str(self.__directory) + "/" + str(RunProg.__now) + "_log.txt"
        if (len(self.__infile)+len(self.__outfile)) != 0 and self.__valide:
            with open(self.__logfile, "w") as f:
                self.__process = subprocess.Popen(cmd, shell=True, stderr=f)
        else:
            self.__process = "help"
            subprocess.run(cmd, shell=True, stdout=None)

    def status(self):   #utilisé pour vérifier le status d'exécution du process seqgen
        if self.__process == "":
            print("\nStatut d'exécution: non commencé 0 ")
        elif self.__process == "help" or self.__process.poll() == 0:
            print("\nStatut d'exécution: terminé avec succès 2")
        elif self.__process.poll() is None:
            print("\nStatut d'exécution: en cours 1")
        else:
            print("\nStatut d'exécution: terminé avec échec 3, voir: " + str(self.__logfile))
        #IL FAUT RETOURNER STATUS

    def reset(self):   #permet d'effacer les documents et d'annuler la requête (kill)
        print("\nVotre requête est annulée")
        if not self.__process == "":
            self.__process.kill()
            if os.path.isfile(str(self.__directory) + "/" + str(self.__outfile)):
                os.remove(str(self.__directory) + "/" + str(self.__outfile))
            if os.path.isfile(str(self.__logfile)):
                os.remove(str(self.__logfile))
        else:
            print("\nVotre exécution n'est pas lancée")

    def view(self):   #permet de voir les fichiers dans le dossier de travail seqgen
        my_files = []
        if os.path.exists(self.__directory):
            for f in os.listdir(self.__directory):
                if os.path.isfile(str(self.__directory) + "/" + f):
                    my_files.append(f)
            if len(my_files) != 0:
                print("\nFichier(s) dans" + " " + str(self.__directory) + ":")
                for f in my_files:
                    print(f)
            else:
                print("Aucun ficher dans: ", self.__directory)
        else:
            print("Il n'y a pas de résultats pour cette requête")

    def read(self, file=None):  #permet de lire le contenu du document du process seqgen
        if os.path.exists(str(self.__directory) + "/" + str(file)):
            print("\nVoici le contenu de:" + str(self.__directory) + "/" + str(file) + ":")
            file_in = open(str(self.__directory) + "/" + str(file), "r")
            for ligne in file_in:
                print(ligne)
            file_in.close()
        elif os.path.exists(str(self.__directory) + "/" + str(self.__outfile)):
            print("\nFichier non-spécifié ou n'existe pas, voici le contenu de exécution SeqGen en cours:"
                  + str(self.__directory) + "/" + str(self.__outfile) + ":")
            file_in = open(str(self.__directory) + "/" + str(self.__outfile), "r")
            for ligne in file_in:
                print(ligne)
            file_in.close()
        else:
            print("Aucun fichier",str(file),"dans votre dossier")


    """
ci-bas, ensemble de méthode privée de la classe qui permettent la gestion des informations internes de la classe
    """

    def __new_dir(self): # afin de créer un dossier de travail
        directory = './seqgen_SB'
        if not os.path.exists(directory):
            os.mkdir(directory)
        return (directory)


    # variable de classe __now qui permet de créer des fichiers avec identifiant unique
    __now = datetime.now().strftime("%H%M%S")

    # ci-bas, La variable de classe  __options contient toutes les expressions régulières
    # qui peuvent définir les options d'utilisation
    # de SeqGen
    __options = ['(-m)((F84)|(HKY)|(GTR)|(JTT)|(WAG)|(PAM)|(BLOSUM)|(MTREV)|(CPREV)|(GENERAL))$',
                 '(-l)([1-9][0-9]*)',
                 '(-n)([1-9][0-9]*)',
                 '(-p)([1-9][0-9]*)',
                 '((-s)(?=.*[1-9])\d*(?:\.\d*)?)',
                 '((-d)(?=.*[1-9])\d*(?:\.\d*)?)',
                 '((-t)(?=.*[1-9])\d*(?:\.\d*)?)',
                 '((-a)(?=.*[1-9])\d*(?:\.\d*)?)',
                 '(-g)(([2-9]|[12][0-9]|3[0-2]))',
                 '(-k)([1-9][0-9]*)',
                 '-o(p|r|n|f)$',
                 '-w(a|r)$',
                 '-z-?\d',
                 '-x^[\w,\s-]+\.[A-Za-z]{3}$',
                 '-h$',
                 '-q$',
                 '(-i)(0(\.\d+))?',
                 '(-c)(((?=.*[1-9])\d*(?:\.\d*)?)[,\s]){2}((?=.*[1-9])\d*(?:\.\d*)?)$',
                 '((-r)(((?=.*[1-9])\d*(?:\.\d*)?)[,\s]){5}((?=.*[1-9])\d*(?:\.\d*)?)$)|((-f)(((?=.*[1-9])\d*(?:\.\d*)?)[,\s]){189}((?=.*[1-9])\d*(?:\.\d*)?)$)',
                 '((-f)(((?=.*[1-9])\d*(?:\.\d*)?)[,\s]){3}((?=.*[1-9])\d*(?:\.\d*)?)$)|((-f)(((?=.*[1-9])\d*(?:\.\d*)?)[,\s]){19}((?=.*[1-9])\d*(?:\.\d*)?)$)',
                 '-fe$'
                 ]
