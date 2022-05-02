#!/usr/bin/python

#=============================
#== Serveur Flask
#== Validation
#=============================
__auteur__ = "Alix Boc"

import urllib.request, json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import bd, os
from datetime import datetime
#from flask_session import Session
#from validation import Validation
from validation import Validation
# import seqgen_commands_web_field
from RunProg import RunProg
import re

# Setup Flask app.
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '25eb4d5558b3a957'
if not os.path.exists("./tmp"):
    os.mkdir("./tmp")
app.config['tmp'] = './tmp'
#app.config["SESSION_PERMANENT"] = False  ## si jamais besoin de login et user
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
bd.init_db()  #pas d'utilisation de la bd pour l'instant


model_options = ["HKY","F84","GTR","JTT","WAG","PAM","BLOSUM","MTREV","CPREV45","MTART","LG","GENERAL"]
params_list = {}
infile = ""

@app.route('/')
def default():
    print(params_list)
    return render_template('seqgen_home.html', params=params_list)
#a chaque fois que tu fais un render tempplate pour seqgen-home, on renvoit status

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/usage')
def usage():
    return render_template('usage.html')

@app.route ('/returnParams', methods=['POST'])
def returnParams ():
    items = bd.getParams()
    return jsonify(items)

@app.route ('/params-load', methods=['POST'])
def importerParamsFichier ():
    file = request.files["file"]
    file.save(os.path.join(app.config['tmp'], file.filename))  # sauver le fichier dans le répertoire
    filename = app.config['tmp'] + "/" + file.filename  # faire un chemin
    file_in = open(filename, "r")
    for ligne in file_in:
        if not ligne.strip():
            continue
        else:
            params_list.append(ligne.strip("\n"))
            print("params",params_list)
    return default()

# @app.route ('/submitTree', methods=['POST']) #TO DO
# def submitTree ():
    # global infile
    # if request.form["optionTree"] == "pasted":
    #     infile = request.form["treeEntry"]
    # elif request.form["optionTree"] =="file":
    #     infile = []
    #     file = request.files["userfile"]
    #     print(file.filename)
    #     # file.save(os.path.join(app.config['tmp'], file.filename))  # sauver le fichier dans le répertoire tmp
    #     infile = app.config['tmp'] + "/" + file.filename  # faire un chemin
    #     #file_in = open(filename, "r")
    #     #for ligne in file_in:
    #     #    if not ligne.strip():
    #     #        continue
    #     #    else:
    #      #       infile.append(ligne.strip("\n"))
    #     #infile = str(infile)
    #     #file_in.close()
    # print(infile)
    # return render_template('seqgen_home.html', tree=infile)


@app.route ('/paramsField', methods=['POST']) # Fini pour les paramètres de base :)
def paramsField():
    print("coucou")
    # model = "-m"+str(model_options[int(request.form["model"])])
    # length = "-l"+str(request.form["length"])
    # i_range = "-i"+str(request.form["i_range"])

    global params_list
    params_list["m"] = str(request.form["model"])
    params_list["l"] = str(request.form["length"])
    params_list["i"] = str(request.form["i_range"])

    print(params_list)

    global infile
    if request.form["optionTree"] == "pasted":
        infile = request.form["treeEntry"]
    elif request.form["optionTree"] == "file":
        file = request.form["userfile"]
        infile = app.config['tmp'] + "/" + file  # faire un chemin

    print(infile)

    if params_list["l"].isdigit() == False or params_list["m"] == "" or infile == "":
        print("Params non valide")
        return render_template('seqgen_home.html', erreur="Paramètres non valide, revoyez l'utilisation")
    else:
        return render_template("seqgen_home.html", isValid=True)

# @app.route ('/validerParams',methods=['POST'])
# def validerParametres():
#     V1 = Validation(params_list, './tmp')
#     valide = V1.valide
#     print(valide)
#     if valide == False:
#         print("Params non valide")
#         return render_template('seqgen_home.html', erreur="Paramètres non valide, revoyez l'utilisation")
#     else:
#         return default()

@app.route ('/runprog',methods=['POST'])
def runprog():
    # V1 = Validation(params_list, './tmp')
    # valide = V1.valide
    # params = V1.params

    outfile = datetime.now().strftime("%H%M%S") + '_output_seqgen'
    R1 = RunProg(params_list, infile, outfile, './tmp')
    R1.run()
    return default()

@app.route('/<path:path>')
def all_files(path):
    if os.path.exists("static/" + path):
        return app.send_static_file(path)
    else:
        return default()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=4999)
