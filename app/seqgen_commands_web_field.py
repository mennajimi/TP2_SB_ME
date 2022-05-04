"""

    validation script for SeqGen Runner
    version 1.0
    Auteur : Salix Boulet
    Date   : Hiver 2022

    Ce script accompagne le programme SeqGen Runner version 1.0
    Permet l'exécution de SeqGen en validant les paramètres avant


"""

import re


# validations des paramètres selon l'usage de SeqGen
def val_params(params):
    found_params = []
    if not re.search('-m', str(params)) and '-h' not in params:
        return False
    if (re.search("-s", str(params))) and (re.search("-d", str(params))):
        return False
    if (re.search("-r", str(params))) and (re.search("-t", str(params))):
        return False
    if len(re.findall("-o", str(params))) > 1:
        return False
    if len(re.findall("-w", str(params))) > 1:
        return False
    if len(re.findall("-m", str(params))) > 1:
        return False
    for i in range(0, len(options)):
        for j in range(0, len(params)):
            if re.match(options[i], params[j]):
                found_params.append(params[j])
    if len(params) != len(found_params):
        return False
    return True


options = ['(-m)((F84)|(HKY)|(GTR)|(JTT)|(WAG)|(PAM)|(BLOSUM)|(MTREV)|(CPREV)|(GENERAL))$',
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







