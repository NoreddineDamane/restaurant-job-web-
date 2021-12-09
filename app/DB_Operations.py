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
myconn= mysql.connector.connect(host="172.19.0.3",user="root",password="root",database="projet_etr")
cursor = myconn.cursor(dictionary=True)

# acces to mysql via cmd: 
#docker exec -it app-web-flask-mysql_db_1 bash -l
#mysql -u root -proot

#Create table into db if not exists
#cursor.execute("CREATE DATABASE projet_ia")
#cursor.execute("CREATE TABLE IF NOT EXISTS Condidat (id VARCHAR(30) UNIQUE PRIMARY KEY,Nom VARCHAR(30), Prenom VARCHAR(30),Age VARCHAR(30), Experience VARCHAR(30), Adresse VARCHAR(30),profil VARCHAR(30), contrat VARCHAR(30), url_image VARCHAR(30) )")

#Update data if already exists in db
def add_text(text_value1, text_value2,text_value3, text_value4, text_value5 , text_value6, text_value7, text_value8, text_value9):
  query = "SELECT id from Condidat"
  cursor.execute(query)
  id_list = [id for (id) in cursor]
  for n in range(len(id_list)):
    if id_list[n]["id"] == w["ID"]:
      query_update = "UPDATE IGNORE Condidat SET Nom=%s, Prenom=%s, Age=%s, Experience=%s, Adresse=%s ,profil=%s, contrat=%s, url_image=%s WHERE id=%s"
      values_update = (text_value1, text_value2,text_value3, text_value4, text_value5 , text_value6, text_value7, text_value8, text_value9, id_list[n]["id"])
      cursor.execute(query_update,values_update)
      myconn.commit()
      #Insert data if not exists in db
  query_insert = "INSERT IGNORE INTO Condidat (id, Nom, Prenom, Age, Experience, Adresse, profil, contrat, url_image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  values_insert = (text_value1, text_value2,text_value3, text_value4, text_value5 , text_value6, text_value7, text_value8, text_value9)
  cursor.execute(query_insert,values_insert)