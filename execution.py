import mysql.connector
from tkinter import *

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="arjun2004",
    database="email_bot"
)

mycursor=db.cursor(buffered=True)

root=Tk()

def removeall():
    title.grid_forget()
    username_label.grid_forget()
    username_entry.grid_forget()
    password_label.grid_forget()
    password_entry.grid_forget()



#Login page
def login():
    #global title,username_label,username_entry,password_label,password_entry,login_button
    mail=username_entry.get()
    pwd=password_entry.get()
    mycursor.execute("select email_id,password from email_list;")
    for i in mycursor:
        #print(i)
        if i[0]==mail and i[1]==pwd:
            name=mail[0:mail.index("@")]
            print(name)
            print("Logged in!")
            #removeall()
            break   
    else:
        print("Invalid info")

global username_entry,username_label
title=Label(root,text="Email Bot").grid(row=0,column=0)
username_label=Label(root, text="Enter Email").grid(row=1, column=0)
username_entry=Entry(root, exportselection=0, fg="blue").grid(row=1, column=1)
password_label=Label(root, text="Enter Password").grid(row=2, column=0)
password_entry=Entry(root, exportselection=0, fg="blue", show="●").grid(row=2, column=1)
login_button=Button(root,text="Login",command=login).grid(row=3,column=0)

root.mainloop()
