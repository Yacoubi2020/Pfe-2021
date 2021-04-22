# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:01:22 2021

@author: simou
"""

#importer les modules utilisable dans notre programme
from bluetooth import *
import datetime
import time 
import paho.mqtt.client as mqtt
import csv
import mysql.connector
import  blynklib

#Une prise Bluetooth socket  réprésentant un point final d'une connexion bluetooth le protocole  que la socket utilisera c'est RFCOMMM par défaut
server_socket=BluetoothSocket(RFCOMM)
#Adresse mac dela carte esp32
v="9C:9C:1F:EA:A7:16"
#connecté avec la carte esp32 
server_socket.connect((v,1))  #connecter avec raspberry pi via l'adress mac 9C:9C:1F:EA:A7:16
client=mqtt.Client()

#partie thingspeak déclaration des variable 
chanelID_temperateur_humidite="1352141"              #ID de chanelId de thingspeak qui nous créons
writeAPkey_temperateur_humidite="AR2579GYNUBKHLNF"   #Ecrire la clé API
mqttAPIKEY="JNROO970AWY5WZVH"   #Clé API utilisateur

#chanel pour les valeur de gaz 
chanelID_gaz="1352129"              #ID de chanelId de thingspeak qui nous créons
writeAPkey_gaz="NKZ4ZTESLMK5EFU9"   #Ecrire la clé API


#chanel pour les valeur de pluie et flamme
chanelID_pluie_flamme="1352139"              #ID de chanelId de thingspeak qui nous créons
writeAPkey_pluie_flamme="ZOI8YVH0C3PTX5LK"   #Ecrire la clé API

#partie mysql (connecté avec la base de donnée pfe_value )
connexion=mysql.connector.connect(user="pfe",password="pfeclass",host="localhost",database="pfe_value")
l= {}

#partie csv 
#crée un fichier csv nommé par pfe_csv
with open("/home/pi/Desktop/pfe.csv",mode='w') as fie:            
           
               Time=datetime.datetime.now() # Temps actuel 
               wri=csv.writer(fie)          #écrire dans le fichier
               #écrire en chaque ligne
               wri.writerow(["dalastemp","Dht22am2302","HumiditeAm2302","pluie","MQ7","MG811","lpg","co","smoke","Flamme","Time"])


BLYNK_AUTH=" eDR0weOWBv_EzLd30HUMipLjbIdfMQ8-"  #l'authentification entre l'application et notre matériel
blynk=blynklib.Blynk(BLYNK_AUTH)                #connection avec  le compte personnel sur APK  blynk
compte_gmail="pfe.esto2021@gmail.com"       #gmail pour suivi les notifications
envoyé_message_gmail=[compte_gmail]             #déterminer la destination d'un message

@blynk.handle_event("connect")                  #fait la référence  à des objets gérés par le server blynk
def yo():
    operation()
def operation():
    
    while True:
              
        
       
            data=server_socket.recv(1024)     # les données envoyées par esp32 sont sous forme de byte 
            #par exemple si les doonnées sont sous la forme suivante : 'b12:12:12:12:12:12:12:12:12:12'
            e=str(data)           #convertir ces données à une chaine de caractère  (resultat final:"'b12:12:12:12:12:12:12:12:12:12'")
            e=e.replace("\'","")  #remplacer  le caractère '\'' par une chaine vide  (resultat final:"b12:12:12:12:12:12:12:12:12:12")
            e=e.replace("b","")   #remplacer le caractère 'b' par un caractere vide (resultat final:"12:12:12:12:12:12:12:12:12:12"  )
            tr=e.split(":")       #la conversion de la  chaine de caractère final à une liste : [12,12,12,12,12,12,12,12,12,12]
            
            jj=0
            for i in tr :
                l[jj]=float(i)                 #ajouter les valeur de la liste dans un dictionnaire tandis que
                                               #le clé de chaque valeur augmente par 1
                jj+=1
            #Modifier les noms clé de dictionnaire  
            l["dalastemp"]=l.pop(0)   
            l["Dht22am2302"]=l.pop(1)
            l["HumiditeAm2302"]=l.pop(2)
            l["Flamme"]=l.pop(3)
            l["MQ7"]=l.pop(4)
            l["pluie"]=l.pop(5)
            l["MG811"]=l.pop(6)
            l["lpg"]=l.pop(7)
            l["co"]=l.pop(8)
            l["smoke"]=l.pop(9)
            
            print(l) ##afficher le dictionnaire
            moyen=(l["Dht22am2302"]+l["dalastemp"])/2.0
            #afficher la moyenne de température 
            print("la moyen de température :",moyen)
    
            if(l["Dht22am2302"]-1.0>moyen):
        
                m=l["Dht22am2302"]
            elif(l["dalastemp"]-1.0>moyen):
                m=l["dalastemp"]
            Time=datetime.datetime.now() # Temps actuel
            
            #chaque champ contient une valeur 
            payload="field1="+str(moyen)+"&field2="+str(l["HumiditeAm2302"])
            
            payload1="field1="+str(l["MG811"])+"&field2="+str(l["MQ7"])+"&field3="+str(l["lpg"])+"&field4="+str(l["smoke"])+"&field5="+str(l["co"])
            
            payload2="field1="+str(l["Flamme"])+"&field2="+str(l["pluie"])
            
            #connecté  avec thingspeak
            client.connect("mqtt.thingspeak.com",1883)
            #envoie les données sur les trois channels 
            #channel 1  qui spécifier pour recevoir les données de capteur et d'humidité 
            client .publish("channels/" +  chanelID_temperateur_humidite+ "/publish/" + writeAPkey_temperateur_humidite,payload)
            #channel 2  qui spécifier pour recevoir les données de gaz
            client .publish("channels/" + chanelID_gaz + "/publish/" +writeAPkey_gaz ,payload1)
            #channel 3  qui spécifier pour recevoir les données de flamme et pluie
            client .publish("channels/" +  chanelID_pluie_flamme+ "/publish/" + writeAPkey_pluie_flamme,payload2)
            
            
            mycursor=connexion.cursor()
            #crée un tableau (pfe_cap) dans la base de donnée (pfe_value)
            mycursor.execute("CREATE TABLE pfe_cap(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,tempdht22 FLOAT, dalastemp FLOAT, tempdht22AM3202 FLOAT,HumiditeAm2302 FLOAT,HumiditeDht22 FLOAT,pluie FLOAT,MQ7 FLOAT,MG811 FLOAT,lpg FLOAT,co FLOAT,smoke FLOAT,Flamme varchar(20),time DATETIME)")
            #insérez de nouveaux enregistrement (les noms de capteur) dans la table(pfe_cap) 
            sql="INSERT INTO pfe_value.pfe_cap(dalastemp,tempdht22am3202,HumiditeAm2302,pluie,MQ7,MG811,lpg,co,smoke,Flamme,time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
            #la valeur de chaque enregistrement 
            value=(str(l["dalastemp"]),l["Dht22am2302"],l["HumiditeAm2302"],l["pluie"],l["MQ7"],l["MG811"],l["lpg"],l["co"],l["smoke"],l["Flamme"])
            #Executons la requéte
            mycursor.execute(sql,value)
            connexion.commit()
            
            #partie blynk dans le code 
            #envoie  de donnée de moyen températeur (moyen=valeur températeur de capteur dalas +valeur de températeur de capteur DHT22)
            blynk.virtual_write(2,moyen)
            #envoie à l'application blynk dans la porte virtual 3 la valeur de humidité
            blynk.virtual_write(3,l["HumiditeAm2302"])
            #envoie de valeur de co dans la porte virual 4
            blynk.virtual_write(4,l["MQ7"])
            #envoie de valeur de co2 dans la porte virual 5
            blynk.virtual_write(5,l["MG811"])
            
            """si la valeur de capteur de flamme=0 (c'est un dire le feu existe) le serveur blynk va l'envoiyé
               une notification et un message dans la boite de message dans gmail"""
            
            if l["Flamme"]==0.0:
                blynk.notify("Danger")
                blynk.email(compte_gmail,'détection d\'incendie','il y a du feu verifier dans thingspeak dernier mise à jour des données'+"\n"+
                            "https://thingspeak.com/channels/1352139/private_show") #  blynk.gmail(la_destination,objet,message)
            
            #partie de fichier (csv)
            #ajouter dans le fichier pfe_csv
            with open("/home/pi/Desktop/pfe.csv",mode='a') as fie:            
           
               Time=datetime.datetime.now() # Temps actuel 
               #écrire dans le fichier
               wri=csv.writer(fie)          
               #écrire en chaque ligne
               wri.writerow([l["dalastemp"],l["Dht22am2302"],l["HumiditeAm2302"],l["pluie"],l["MQ7"],l["MG811"],l["lpg"],l["co"],l["smoke"],l["Flamme"],Time])
while True:
            
            blynk.run()
            time.sleep(2)