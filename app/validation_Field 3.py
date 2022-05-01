"""

    SeqGen Validator
    version 1.0
    Auteur : Salix Boulet
    Date   : Hiver 2022

    Ce programme permet de valider les paramètres de Seqgen
    Dépendences: seqgen_commands.py version 1


"""

import seqgen_commands_web_field
import re
import os
import subprocess
from datetime import datetime


class Validation:

    def __init__(self, paramsList):
        self.__input = paramsList  #__input: l'ensemble des éléments du fichier de paramètres
        self.__valide = Validation.__parametresValides(self)   #__valide: Boolean qui indique si les paramètres entrés sont valides pour Seqgen

    @property
    def valide(self):
        return self.__valide

    @property
    def params(self):
        return self.__input

    def __parametresValides(self): #validation des paramètres Seqgen selon la documentation
        params_ok = seqgen_commands_web_field.val_params(self.__input)
        if params_ok:
            return (True)
        else:
            return (False)

    """
ci-bas, ensemble de méthode privée de la classe qui permettent la gestion des informations internes de la classe
    """

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
