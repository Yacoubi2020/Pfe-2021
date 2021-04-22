# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 09:23:01 2021

@author: simou
"""

from flask import Flask,render_template,request,url_for
from flask_mysqldb import MySQL
 
app = Flask(_name_)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pfe'
app.config['MYSQL_PASSWORD'] = 'pfeclass'
app.config['MYSQL_DB'] = 'pfe_value'
p={}
mysql = MySQL(app)
@app.route('/add',methods=['GET'])
def login():
        if request.method=='GET':
            
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * From pfe_cap ''')
            results=cursor.fetchall()
            print(results[0][3])
            print(results[1][3])
            b=len(results) #nombre de colon
            a=results
            for i in range(b):
            
                    temp_dalas=a[i][1]
                    temp_DHT22=a[i][2]
                    hum_dht22=a[i][3]
                    pluie=a[i][4]
                    mq7=a[i][5]
                    MG811=a[i][6]
                    lpg=a[i][7]
                    co=a[i][8]
                    smoke=a[i][9]
                    flamme=a[i][10]
                               
                    value={'a':temp_dalas,
                       'c':temp_DHT22,
                       'd':hum_dht22,
                       'e':pluie,
                       'f':mq7,
                       'g':MG811,
                       'h':lpg,
                       'i':co,
                       'j':smoke,
                       'k':flamme
                       }
            return render_template("pfe.html",**value)
 
if _name=="main_":
    
    app.run(debug=True,host='0.0.0.0',port=8080)