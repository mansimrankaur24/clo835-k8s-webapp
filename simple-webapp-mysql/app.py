from flask import Flask, render_template, request, redirect, url_for
import socket
import mysql.connector
import os
import json
import subprocess
import boto3

app = Flask(__name__)

DB_Host = os.environ.get('DB_Host') or "mysql"
DB_Database = os.environ.get('DB_Database') or "mysql"
DB_User = os.environ.get('DB_User')
DB_Password = os.environ.get('DB_Password')
group_name = os.environ.get('GROUP_NAME')
if os.path.exists('/clo835/config/image_url'):
    s3_url_file = open('/clo835/config/image_url') 
    json_data = json.load(s3_url_file) #convert to json
else: 
    json_data = {}

print("Background image urls from S3: ", json_data)

@app.route("/")
def main():
    db_connect_result = False
    err_message = ""
    try:
        conn = mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#39b54b'
        db_connect_result = True
        image_url = json_data["success_url"] if json_data else "Not Available"
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS clo835 (message VARCHAR(255)) ''')
        cursor.execute("SELECT message FROM clo835")
        items = [i[0] for i in cursor.fetchall()]
        
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)
        image_url = json_data["failed_url"] if json_data else "Not Available"
        cmd = "aws s3 cp " + image_url + f" static/img/image.jpg"
        items = ""
    
    cmd = "aws s3 cp " + image_url + f" static/img/image.jpg"
    process = subprocess.run(cmd, shell=True)
    
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color, group_name=group_name, image_url=image_url, items=items)

@app.route("/", methods = ['POST'])
def insert():
    err_message = ""
    if request.method == 'POST':
        message = request.form['message']
        conn = mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS clo835 (message VARCHAR(255)) ''')
        cursor.execute(''' INSERT INTO clo835 (message) VALUES (%s)''', [(message)])
        conn.commit()
            
    return redirect('/')

@app.route("/debug")
def debug():
    color = '#2196f3'
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set"), color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)