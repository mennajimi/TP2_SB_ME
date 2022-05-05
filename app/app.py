#!/usr/bin/python
"""

    App
    version 2.0
    Auteur : Salix Boulet et Myriam Ennajimi
    Date   : Hiver 2022

    Serveur Flask pour Seq-gen


"""

from flask import Flask, render_template, request, jsonify, abort, send_file
import os, shutil
from datetime import datetime
from validation_Field import Validation
from RunProg import RunProg

# Setup Flask app.
app = Flask(__name__)
app.debug = True
if not os.path.exists("./tmp"):
    os.mkdir("./tmp")
app.config['tmp'] = './tmp'


params_dict = {}
infile = ""
R1 = ""
upload=False

@app.route('/')
def default():
    return render_template('seqgen_home.html', upload=upload)


@app.route('/results', defaults={'req_path': ''})  ##from https://stackoverflow.com/questions/23718236/python-flask-browsing-through-directory-with-files
@app.route('/<path:req_path>')
def results(req_path):
    BASE_DIR = './tmp'
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    files = os.listdir(abs_path)
    return render_template('results.html', files=files)


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/usage')
def usage():
    return render_template('usage.html')


@app.route ('/submitTree', methods=['POST']) #prend l'arbre soumis et le sauvegarde dans un fichier
def submitTree ():
    eraseDocs()
    global infile, upload
    if request.form["optionTree"] == "pasted": #écrire un fichier à partir du champ
        tree = request.form["treeEntry"]
        infile = "tmp/entry.tree"
        file_in = open("tmp/entry.tree", "w")
        for lines in tree:
            file_in.write(lines)
        file_in.close()
    elif request.form["optionTree"] == "file": #sauver le fichier soumis par l'utilisateur dans tmp
        infile = []
        file = request.files["userfile"]
        file.save(os.path.join(app.config['tmp'], "tree_"+file.filename))  # sauver le fichier dans le répertoire tmp
        filename = app.config['tmp'] + "/" + "tree_"+file.filename  # faire un chemin
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


@app.route ('/paramsField', methods=['POST']) #importer et valider les paramètres
def paramsField():
    temp_dict = fetchParams()
    global params_dict, infile
    for k, v in temp_dict.items():
        if v != "":
            params_dict[k] = v
    params_list = []
    for cle, valeur in params_dict.items():
       params_list.append("-" + cle + valeur)
    print(params_list)
    valide = validerParametres(params_list)
    if valide:
        return render_template("seqgen_home.html", success="Les paramètres sont valides, procédez", isValid=True)
    else:
        eraseDocs()
        return render_template('seqgen_home.html', erreur="Paramètres non valides, revoyez l'utilisation", upload = False, isValid=False)


@app.route ('/runprog',methods=['POST'])  #lancer l'exécution de seq-gen par la classe RunProg
def runprog():
    global R1, infile, upload
    outfile = './tmp/'+datetime.now().strftime("%H%M%S") + '_output_seqgen.txt'
    R1 = RunProg(params_dict, infile, outfile, './tmp')
    R1.run()
    infile = ""
    upload = False
    return render_template('running.html', status=R1.execution)

@app.route ('/getStatus', methods=['GET'])  #obtenir le statut du programme par la classe RunProg
def getStatus():
    global R1
    return render_template('running.html', status=R1.execution)

@app.route ('/clearRun', methods=['POST'])  #effacer les données pour recommencer
def clearRun():
    global infile
    message=R1.reset
    eraseDocs()
    infile = ""
    return render_template("seqgen_home.html", erreur=message, upload = False, isValid=False)

@app.route('/<path:path>')
def all_files(path):
    if os.path.exists("static/" + path):
        return app.send_static_file(path)
    else:
        return default()

def validerParametres(params_list):  #valider les paramètres par la classe Validation
    V1 = Validation(params_list)
    print(V1.valide)
    return V1.valide

def eraseDocs():  # efface les documents dans tmp. fonction trouvée sur https://stackoverflow.com/questions/185936
    global params_dict, infile
    params_dict = {}
    folder = './tmp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if ((os.path.isfile(file_path) or os.path.islink(file_path))): # and re.match("tree", filename):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def fetchParams():  ###va chercher les paramètres dans le doc et
    temp_dict = {}
    temp_dict["m"] = str(request.form["model"])
    temp_dict["l"] = str(request.form["length"])
    temp_dict["n"] = str(request.form["datasets"])
    temp_dict["p"] = str(request.form["partitions"])
    temp_dict["i"] = str(request.form["i_range"])

    temp_dict["scaling"] = str(request.form["scaling"])
    if temp_dict.get("scaling") == "s":
        temp_dict["s"] = str(request.form["text_scaling"])
    if temp_dict.get("scaling") == "d":
        temp_dict["d"] = str(request.form["text_scaling"])
    del temp_dict["scaling"]

    temp_dict["k"] = str(request.form["k_ancestral"])
    temp_dict["a"] = str(request.form["shape"])
    temp_dict["g"] = str(request.form["g_range"])

    temp_dict["c1"] = str(request.form["codon_het2"])
    temp_dict["c2"] = str(request.form["codon_het2"])
    temp_dict["c3"] = str(request.form["codon_het2"])
    if temp_dict.get("c1") != "" and temp_dict.get("c2") != "" and temp_dict.get("c3") != "":
        merged_c = temp_dict.get("c1")+" "+temp_dict.get("c2")+" "+temp_dict.get("c3")
        temp_dict["c"] = merged_c
        del temp_dict["c1"]
        del temp_dict["c2"]
        del temp_dict["c3"]

    temp_dict["r1"] = str(request.form["nt_rate1"])
    temp_dict["r2"] = str(request.form["nt_rate2"])
    temp_dict["r3"] = str(request.form["nt_rate3"])
    temp_dict["r4"] = str(request.form["nt_rate4"])
    temp_dict["r5"] = str(request.form["nt_rate5"])
    temp_dict["r6"] = str(request.form["nt_rate6"])
    if temp_dict.get("r1") != "" and \
            temp_dict.get("r2") != "" and \
            temp_dict.get("r3") != "" and \
            temp_dict.get("r4") != "" and \
            temp_dict.get("r5") != "" and \
            temp_dict.get("r6") != "":
        merged_r = temp_dict.get("r1") + " " + temp_dict.get("r2") + " " + temp_dict.get("r3") + " " + temp_dict.get("r4") + " " + temp_dict.get("r5") + " " + temp_dict.get("r6")
        temp_dict["r"] = merged_r
        del temp_dict["r1"]
        del temp_dict["r2"]
        del temp_dict["r3"]
        del temp_dict["r4"]
        del temp_dict["r5"]
        del temp_dict["r6"]

    temp_dict["f1"] = str(request.form["nt_freq1"])
    temp_dict["f2"] = str(request.form["nt_freq2"])
    temp_dict["f3"] = str(request.form["nt_freq3"])
    temp_dict["f4"] = str(request.form["nt_freq4"])

    if temp_dict.get("f1") != "" and \
            temp_dict.get("f2") != "" and \
            temp_dict.get("f3") != "" and \
            temp_dict.get("f4") != "":

        merged_f = temp_dict.get("f1") + " " + temp_dict.get("f2") + " " + temp_dict.get("f3") + " " + temp_dict.get("f4")
        temp_dict["f"] = merged_f
        del temp_dict["f1"]
        del temp_dict["f2"]
        del temp_dict["f3"]
        del temp_dict["f4"]

    temp_dict["t"] = str(request.form["transition"])
    temp_dict["o"] = str(request.form["output"])
    temp_dict["z"] = str(request.form["seed"])
    return temp_dict


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=4999)
