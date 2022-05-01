"""

    SeqGen Validator
    version 1.0
    Auteur : Salix Boulet
    Date   : Hiver 2022

    Ce programme permet de valider les paramètres de Seqgen
    Dépendences: seqgen_commands.py version 1


"""

import seqgen_commands
import re
import os
import subprocess
from datetime import datetime


class Validation:

    def __init__(self, paramsList, directory):
        print("init")
        self.__directory = directory
        self.__input = paramsList  #__input: l'ensemble des éléments du fichier de paramètres
        self.__params = Validation.__find_params(self)    #__params: de __input, les éléments qui sont des paramètres seqgen
        self.__files = Validation.__find_files(self)        #__file: de __input, les fichiers d'entré et de sortie
        self.__infile, self.__outfile = Validation.__find_in_out(self) #de __files: ID du fichier d'entré vs sortie
        self.__valide = Validation.__parametresValides(self)   #__valide: Boolean qui indique si les paramètres entrés sont valides pour Seqgen

    @property
    def valide(self):
        return self.__valide

    @property
    def params(self):
        return self.__params

    @property
    def infile(self):
        return self.__infile

    @property
    def outfile(self):
        return self.__outfile

    def __find_params(self):  # de la liste input, sert à trouver les paramètres d'exécution pour la ligne de commande
        found_params = []
        for i in range(0, len(Validation.__options)):
            for j in range(0, len(self.__input)):
                if re.match(Validation.__options[i], self.__input[j]):
                    found_params.append(self.__input[j])
        return (found_params)

    def __find_files(self): # de la liste input, sert à trouver les fichiers (in et out) pour la ligne de commande
        found_files = []
        for i in range(0, len(self.__input)):
            if os.path.isfile(str(os.getcwd()) + "/tmp/" + str(self.__input[i])):
                found_files.append(self.__input[i])
            elif self.__input[i] not in self.__params and not re.match('-', str(self.__input[i])):
                found_files.append(self.__input[i])
        return (found_files)

    def __find_in_out(self): # de la liste de fichier, distingue le IN du OUTFILE
        input_file = []
        output_file = []
        for i in range(0, len(self.__files)):
            if os.path.exists(str(self.__files[i])):
                input_file = self.__files[i]
            else:
                output_file = self.__files[i]
        if output_file == []:
            output_file = Validation.__create_file(self)
        return (input_file, output_file)


    def __create_file(self):   #au besoin, créé le nom du fichier output, s'il n'est pas spécifié
        new_file = str(Validation.__now) + '_output_seqgen'
        print("Un nouveau fichier sera créé: ", str(new_file))
        return (new_file)

    def __parametresValides(self): #validation des paramètres Seqgen selon la documentation
        params_ok = seqgen_commands.val_params(self.__input, self.__params, self.__files)
        if params_ok:
            return (True)
        else:
            return (False)

    """
ci-bas, ensemble de méthode privée de la classe qui permettent la gestion des informations internes de la classe
    """



    def __help_menu(self): #si les paramètres ne sont pas valides, offre la possibilité de consulter le -h de Seqgen
        choice_ok = False
        while not choice_ok:
            help_menu = input("Paramètres invalides, revoir l'utilisation de SeqGen(Y/N)? ")
            if help_menu in ("Y", "y", "N", "n"):
                choice_ok = True
            return (help_menu)

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
