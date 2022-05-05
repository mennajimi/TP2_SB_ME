"""

    SeqGen Runner
    version 2.0
    Auteur : Salix Boulet et Myriam Ennajimi
    Date   : Hiver 2022

    Ce programme permet l'exécution de SeqGen à partir d'un fichier d'entré de paramètres.



"""

import os
import shutil
import subprocess
from datetime import datetime


class RunProg:

    def __init__(self, paramsFile, infile, outfile, directory):
        self.__directory = directory #fichier de travail
        self.__params = paramsFile   #les paramètres seqgen
        self.__infile, self.__outfile = infile, outfile #fichiers: entré et sortie
        self.__process = ""  #__process: permet de lancer le processus d'exécution de programme
        self.__logfile = ""  #__logfile: sauvegarde le log de Seqgen pour consultation au besoin
        self.__execution = "" #pour suivre le statut d'exécution

    def run(self):         # initie l'exécution, à l'aide de la fonction run_popen ci-bas
        cmd = shutil.which("./seq-gen")
        for cle, valeur in self.__params.items():
            cmd += " -" + cle + valeur + " "
        cmd += " < " + self.__infile + " > " + self.__outfile
        RunProg.run_popen(self, cmd)

    def run_popen(self, cmd):     # créer une instance de popen (self.__process) pour gérer l'exécution
        self.__logfile = str(self.__directory) + "/" + str(RunProg.__now) + "_log.txt"
        if (len(self.__infile)+len(self.__outfile)) != 0:# and self.__valide:
            with open(self.__logfile, "w") as f:
                self.__process = subprocess.Popen(cmd, shell=True, stderr=f)
        else:
            self.__process = "help"
            subprocess.run(cmd, shell=True, stdout=None)

    @property
    def execution(self):   ##permet d'obtenir le statut d'exécution du process
        if self.__process == "":
            self.__execution = "Execution: not launched"
        elif self.__process == "help" or self.__process.poll() == 0:
            self.__execution = "Execution: successfully completed"
        elif self.__process.poll() is None:
            self.__execution = "Execution: running"
        else:
            self.__execution = "Execution: failed, see log file"
        return self.__execution

    @property
    def reset(self):   #permet d'effacer les documents et d'annuler la requête (kill)
        if not self.__process == "":
            self.__process.kill()
            folder = './tmp'
            for filename in os.listdir(folder):  ##fonction trouvée sur https://stackoverflow.com/questions/185936
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            return "Run cancelled"
        else:
            return "Program not launched"

    __now = datetime.now().strftime("%H%M%S")
