# -*- coding: utf-8 -*-

import requests
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_msg(msg, name):
    """Setup smtp"""
    msg = MIMEMultipart()
    msg['From'] = 'email_from'
    msg['To'] = 'email_to'
    msg['Subject'] = 'Status of backup: {0} {1}s'.format(name, msg)
    message = 'Status of backup: {0} - {1}'.format(msg, name)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('HOST', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('login', 'password')
    mailserver.sendmail('from@email', 'to@email', msg.as_string())
    mailserver.quit()


def Status_Connect():
    """Check status code"""
    try:
        db_zip = requests.post(url, params=values)
        r = db_zip.status_code
        return r
    except:
        print("server is down")

#Time setup
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

#Connexion Odoo/Flectra server
url = 'http://URL_of_instance/web/database/backup'
backup_dir = 'Path to the backup files'
values = {'master_pwd': 'master password',
          'name': 'DB name',
          'backup_format': 'zip'}

# Message setup
msg_error = ("Problem master password or no DB exist")
msg_ok = ("Backup is OK the name of backup file is : ")
msg_code_error = ("Code requests is not 200 probably the server is down")

if Status_Connect() == 200:
    db_zip = requests.post(url, params=values)
    if db_zip.headers["Content-type"] != 'application/octet-stream; charset=binary':
        send_msg(msg_error, "")
        print(msg_error)
    else:
        name_db = (values.get("name")+st+".zip")
        with open(backup_dir+name_db, 'wb') as output:
            output.write(db_zip.content)
        send_msg(msg_ok, name_db)
        print(msg_ok + name_db)
else:
    send_msg(msg_code_error, "")
    print(msg_code_error)
