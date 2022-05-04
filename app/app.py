#!/usr/bin/python

#=============================
#== Serveur Flask
#== Validation
#=============================
__auteur__ = "Alix Boc"

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, send_file
import bd, os
from datetime import datetime
#from flask_session import Session
#from validation import Validation
from validation_Field import Validation
import seqgen_commands_web_field
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
params_dict = {}
infile = ""
R1 = ""
upload=False

@app.route('/')
def default():
    return render_template('seqgen_home.html', upload=upload)
#a chaque fois que tu fais un render tempplate pour seqgen-home, on renvoit status

@app.route('/results', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def results(req_path):
    BASE_DIR = './tmp'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)
     # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
     # Show directory contents
    files = os.listdir(abs_path)
    return render_template('results.html', files=files)


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

# @app.route ('/params-load', methods=['POST'])
# def importerParamsFichier ():
#     file = request.files["file"]
#     file.save(os.path.join(app.config['tmp'], file.filename))  # sauver le fichier dans le répertoire
#     filename = app.config['tmp'] + "/" + file.filename  # faire un chemin
#     file_in = open(filename, "r")
#     for ligne in file_in:
#         if not ligne.strip():
#             continue
#         else:
#             params_list.append(ligne.strip("\n"))
#             print("params",params_list)
#     return default()


@app.route ('/submitTree', methods=['POST'])
def submitTree ():
    global infile
    global upload
    if request.form["optionTree"] == "pasted": #écrire un fichier à partir du champ
        tree =request.form["treeEntry"]
        infile ="tmp/entry.tree"
        file_in=open("tmp/entry.tree", "w")
        for lines in tree:
            file_in.write(lines)
        file_in.close()
    elif request.form["optionTree"] == "file": #sauver le fichier dans tmp
        infile = []
        file = request.files["userfile"]
        file.save(os.path.join(app.config['tmp'], file.filename))  # sauver le fichier dans le répertoire tmp
        filename = app.config['tmp'] + "/" + file.filename  # faire un chemin
        file_in = open(filename, "r")
        for ligne in file_in:
            if not ligne.strip():
                continue
            else:
                infile.append(ligne.strip("\n"))
        infile = filename
        file_in.close()
    if len(infile) != 0:
        upload=True
    return render_template('seqgen_home.html', upload = upload)


@app.route ('/paramsField', methods=['POST']) # Fini pour les paramètres de base :)
def paramsField():
    temp_list = {}
    temp_list["m"] = str(request.form["model"])
    temp_list["l"] = str(request.form["length"])
    temp_list["n"] = str(request.form["datasets"])
    #params_list["ds"] = str(request.form["i_range"]) ça marche pantoute ici
    temp_list["k"] = str(request.form["k_ancestral"])
    temp_list["a"] = str(request.form["shape"])
    #temp_list["g"] = str(request.form["g_range"])
    temp_list["c1"] = str(request.form["codon_het2"])
    temp_list["c2"] = str(request.form["codon_het2"])
    temp_list["c3"] = str(request.form["codon_het2"])
    temp_list["r1"] = str(request.form["nt_rate1"])
    temp_list["r2"] = str(request.form["nt_rate2"])
    temp_list["r3"] = str(request.form["nt_rate3"])
    temp_list["r4"] = str(request.form["nt_rate4"])
    temp_list["r5"] = str(request.form["nt_rate5"])
    temp_list["f1"] = str(request.form["nt_rate6"])
    temp_list["f2"] = str(request.form["nt_freq1"])
    temp_list["f2"] = str(request.form["nt_freq2"])
    temp_list["f3"] = str(request.form["nt_freq3"])
    temp_list["f4"] = str(request.form["nt_freq4"])  ###ici les paramètres acides aminés devraient commencer
    temp_list["f3"] = str(request.form["nt_freq3"])
    temp_list["o"] = str(request.form["output"])
    #temp_list["outputFile"] = str(request.form["outputFile"])      ## on utilise pas ce champs pour l'instant

    global params_dict
    for k, v in temp_list.items():
        if v != "":
            params_dict[k] = v
    # global infile
    # if request.form["optionTree"] == "pasted":
    #     infile = request.form["treeEntry"]
    # else:
    #     file = request.form["userfile"]
    #     infile = app.config['tmp'] + "/" + file  # faire un chemin
    #     print(infile)

    params_list = []
    for cle, valeur in params_dict.items():
       params_list.append("-" + cle + valeur)
    valide = validerParametres(params_list)
    print (valide)
    print (params_list)
    if valide:
        return render_template("seqgen_home.html", success="Les paramètres sont valides, procédez", isValid=True)
    else:
        return render_template('seqgen_home.html', erreur="Paramètres non valides, revoyez l'utilisation")

    # if params_dict["l"].isdigit() == False or params_dict["m"] == "" or infile == "":
    #     return render_template('seqgen_home.html', erreur="Paramètres non valides, revoyez l'utilisation")
    # else:
    #     return render_template("seqgen_home.html", success="Les paramètres sont valides, procédez", isValid=True)


def validerParametres(params_list):
    V1 = Validation(params_list)
    print(V1.valide)
    return V1.valide

@app.route ('/runprog',methods=['POST'])
def runprog():
    outfile = './tmp/'+datetime.now().strftime("%H%M%S") + '_output_seqgen.txt'
    global R1, infile, upload
    R1 = RunProg(params_dict, infile, outfile, './tmp')
    R1.run()
    # for f in os.listdir('./tmp'):
    #     if os.path.isfile(str('./tmp' + f)):
    #         print("the file:", f)
    #         os.remove(f)
    infile = ""
    upload = False
    return render_template('running.html', status=R1.execution)

@app.route ('/getStatus', methods=['GET'])
def getStatus():
    global R1
    return render_template('running.html', status=R1.execution)

@app.route ('/clearRun', methods=['POST'])
def clearRun():
    message=R1.reset
    return render_template("seqgen_home.html", erreur=message)

@app.route('/<path:path>')
def all_files(path):
    if os.path.exists("static/" + path):
        return app.send_static_file(path)
    else:
        return default()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=4999)
