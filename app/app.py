from threading import local
from flask import Flask, request, render_template
from flask import current_app, flash, jsonify, make_response, redirect, url_for
import mysql.connector
import json
import os
import base64
import cv2 as cv
import numpy as np

APP_FOLDER = "/app/"
os.chdir(APP_FOLDER)

# get ip container adress
# docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" app-web-flask-mysql_db_1

#Connect to db
myconn= mysql.connector.connect(host="172.22.0.2",user="root",password="root",database="projet_etr")
cursor = myconn.cursor(dictionary=True)

# acces to mysql via cmd: 
#docker exec -it app-web-flask-mysql_db_1 bash -l
#mysql -u root -proot

#Create table into db if not exists
#cursor.execute("CREATE DATABASE projet_ia")
cursor.execute("CREATE TABLE IF NOT EXISTS Condidat (id VARCHAR(30) UNIQUE PRIMARY KEY,Nom VARCHAR(30), Prenom VARCHAR(30),Age VARCHAR(30), Experience VARCHAR(30), Adresse VARCHAR(30),profil VARCHAR(30), contrat VARCHAR(30), url_image VARCHAR(30) )")
app = Flask(__name__)
# 1)####################################################################
#decode function returns url of saved files

def decode(idd, img, f):
    image_64_decode = base64.b64decode(img)
    url = "static/assets/" + "images/" + idd + f
    image_result = open(url, 'wb')
    image_result.write(image_64_decode)
    return url

#Retour flux json
def retour(code, attributs):
	elts=""
	flux_positif = { "code" : code, "Description":"Les données que vous avez envoyées ont été traitées avec succès"}
	if len(attributs)>0:
		for n in range(len(attributs)):
			elts += attributs[n] + " "
	flux_négatif = { "code" : code, "Description" : "Les données que vous avez envoyés ne sont pas au bon format, vérifiez : "+ elts}
	if code == "419":
		return flux_négatif
	if code == "200":
		return flux_positif
##############################################################
new_dict = {}
list_dict = []
@app.route('/addProject', methods=['POST'])
def add_data():
    code = "200"
    attributs = []
    #Reception json file 
    request_data = request.json
    #Implement list
    for v,w in request_data.items():
        if w["ID"]=="" :
            code="419"
            attributs.append("id")
            retour(code, attributs)
            
        # attributs nécessaires
        if w["ID"] !="":
            code = "200"
            img = decode(w["ID"], w["image"],".jpg")
            
            #Update data if already exists in db
            query = "SELECT id from Condidat"
            cursor.execute(query)
            id_list = [id for (id) in cursor]
            for n in range(len(id_list)):
                if id_list[n]["id"] == w["ID"]:
                    query_update = "UPDATE IGNORE Condidat SET Nom=%s, Prenom=%s, Age=%s, Experience=%s, Adresse=%s ,profil=%s, contrat=%s, url_image=%s WHERE id=%s"
                    values_update = (w["Nom"],w["Prenom"],w["Age"],w["Experience"],w["Adresse"],w["profile"], w["contrat"], img, id_list[n]["id"])
                    cursor.execute(query_update,values_update)
                    myconn.commit()
            #Insert data if not exists in db
            query_insert = "INSERT IGNORE INTO Condidat (id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values_insert = (w["ID"], w["Nom"],w["Prenom"],w["Age"],w["Experience"],w["Adresse"],w["profile"], w["contrat"], img )
            cursor.execute(query_insert,values_insert)
            myconn.commit()

 # POST response method for mutiple json 
        list_dict.append(retour(code, attributs))
    for d in list_dict:
        for key in d:
            if key not in new_dict:
                new_dict[key] = []
            new_dict[key].append(d[key])
    return jsonify(new_dict)

@app.route('/ListProfil/<row>/<value>/',methods=['GET'])
def list_data_modele(row, value):
    if row == "profil":
        query = "SELECT Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat WHERE profil = %s"
        val = (str(value),)
        cursor.execute(query, val)
        myresult = cursor.fetchall()
        res = jsonify(myresult)
    return res
@app.route('/GetCondidat')
def GetCondidat():
    query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat FROM Condidat"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('GetCondidat.html', data=data)

@app.route('/profils')
def home1():
    query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('profils.html', data=data)

@app.route('/profil-1')
def home2():
  query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat"
  cursor.execute(query)
  data = cursor.fetchall()
  return render_template('profil-1.html', data=data)

@app.route("/add_text", methods=["POST", "GET"])
def AddText():
    if request.method == "POST":
        text_value = request.form["textv"]
        return render_template('data.html', add_new  = text_value)
    else:
        query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat"
        cursor.execute(query)
        data = cursor.fetchall() 
        return render_template('form.html', data = data)

@app.route('/index')
def home5():
  return render_template('index.html')

@app.route('/employé_employeur')
def employe():
  return render_template('employé_employeur.html')

@app.route('/inscription_employeur')
def inscription_employeur():
  return render_template('inscription_employeur.html')

@app.route('/inscription')
def inscription():
  return render_template('inscription.html')

# @app.route('/data.html')
# def home2():
#   text_value = request.form["textv"]
#   return render_template('data.html', add_new  = text_value)

  #return render_template('profil-1.html', add_new  = text_value)


# @app.route('/profil-1.html',methods=['GET', 'POST'])
# def home3():
#   if request.method == 'POST':
#     # Then get the data from the form
#     tag = request.div['tag']
#     Prenom = tag_lookup(tag)
#     return render_template('profil-1.html', Prenom=Prenom)
#   else:
#     return render_template('profil-1.html')

# # @app.route('/profil-1.html',methods=['GET', 'POST'])
# def home3():
#   # Then get the data from the form
#   tag = request.args["myvar"]
#   Prenom = tag_lookup(tag)
#   return render_template('profil-1.html', Prenom=Prenom)

# @app.route('/form')
# def form():
#   query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat"
#   cursor.execute(query)
#   data = cursor.fetchall()
#   return render_template('form.html', data = data)



# @app.context_processor
# def context_processor():
#   query = "SELECT id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image FROM Condidat"
#   cursor.execute(query)
#   data = cursor.fetchall()
#   return dict(data = data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')