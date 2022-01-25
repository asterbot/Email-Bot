import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import mysql.connector

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="arjun2004",
    database="email_bot"
)

mycursor=db.cursor()

mycursor.execute("select * from emails;")
data=[]
for i in mycursor:
    data.append(i)
print(data)

mycursor.execute("select * from contacts;")
emails=[]
for i in mycursor:
    emails.append(i)
print(emails)

    
# login
sender = "cproject290@gmail.com"
password = "thisiscsproject"
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.login(sender, password)

# stats
count = 1
total = len(data)

for row in data:
    #print(row)
    name = str(emails[0][0])+" "+str(emails[0][1])
    receiver = emails[0][2]
    
    # message details
    message = MIMEMultipart("alternative")
    message["Subject"] = row[1]
    message["From"] = sender
    message["To"] = receiver
    print(message)
    
    #print(receiver)
    html = row[2]

    # plaintext = MIMEText(text, "plain")
    html = MIMEText(html, "html")
    
    # message.attach(plaintext)
    message.attach(html)
    
    '''
    try:
        server.sendmail(sender, receiver, message.as_string())
    except:
        pass
    '''
    count+=1
    