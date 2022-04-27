"""

    validation script for SeqGen Runner
    version 1.0
    Auteur : Salix Boulet
    Date   : Hiver 2022

    Ce script accompagne le programme SeqGen Runner version 1.0
    Permet l'exécution de SeqGen en validant les paramètres avant


"""

import os
import re


# validations des paramètres de la ligne de commande selon l'usage de SeqGen
def val_params(line_in, params, files):
    if len(files) == 1:
        if len(line_in) - len(params) > 1:
            return False
    if len(files) == 2:
        if len(line_in) - len(params) > 2:
            return False
    if len(params) > 1 and '-h' in params:
        return False
    if '-h' in params and len(line_in) != 1:
        return False
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
    return True


#valide la présence du fichier output, si oui offre de le remplacer
def val_outfile(outfile):
    if os.path.exists('./seqgen_SB' + "/" + str(outfile)):
        choice_ok = False
        while not choice_ok:
            replace = input("Un fichier "+str(outfile)+" existe déjà, voulez-vous le remplacer(Y/N)? ")
            if replace in ("Y", "y", "N", "n"):
                choice_ok = True
        if replace in ("Y", "y"):
            return True
        else:
            return False
    else:
        return True
