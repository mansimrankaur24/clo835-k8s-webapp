from flask import Flask
from flask import render_template
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

try:
    mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
    image_url = json_data["success_url"] if json_data else "Not Available"
except:
    image_url = json_data["failed_url"] if json_data else "Not Available"

#download the s3 image locally using aws cli command
cmd = "aws s3 cp " + image_url + " static/img/image.jpg"
process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
print("Background image url from S3: ", image_url)

@app.route("/")
def main():
    db_connect_result = False
    err_message = ""
    try:
        mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#39b54b'
        db_connect_result = True
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)
    
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color, group_name=group_name, image_url=image_url)

@app.route("/debug")
def debug():
    color = '#2196f3'
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set"), color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)