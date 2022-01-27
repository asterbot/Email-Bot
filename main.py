from tkinter import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector


# ----------------------------------------------------------------------------------------------------------------------
# Database and table setup


def db_connect():

    try:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="password", database="email_bot"
        )

    # create database if it doesn't exist
    except:
        db = mysql.connector.connect(host="localhost", user="root", passwd="password")

        db.cursor(buffered=True).execute("create database email_bot")

    return db


db = db_connect()
mycursor = db.cursor(buffered=True)

# create tables if they don't exist


def checktab(tab):
    """Check if table exists in database."""
    mycursor.execute("show tables like '" + tab + "'")
    if mycursor.fetchone():
        return True
    else:
        return False


def createtab(tab, cols):
    """Creates table if it doesn't exist."""
    if checktab(tab) is False:
        mycursor.execute("create table " + tab + "(" + cols + ");")


createtab(
    "emails",
    "msgid int primary key, sent boolean, timestamp datetime, subjcet varchar(200), content mediumtext",
)


createtab(
    "contacts", "fname varchar(50), lname varchar(50), email varchar(50) primary key"
)

root = Tk()


def removeall():
    """Removes all widgets"""
    widgets = root.winfo_children()
    for item in widgets:
        if item.winfo_children():
            widgets.extend(item.winfo_children())
    for item in widgets:
        item.grid_forget()


# ----------------------------------------------------------------------------------------------------------------------


def login():

    global sender
    global password
    global options_title
    global contact_mang_button
    global email_mang_button
    sender = username_entry.get()
    password = password_entry.get()

    removeall()

    options_title.grid(row=0, column=1)
    contact_mang_button.grid(row=1, column=0)
    email_mang_button.grid(row=1, column=2)


# ----------------------------------------------------------------------------------------------------------------------
# Email sending


def email_login(sender, password):
    """Login to email"""
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(sender, password)


def create_email_format():
    """Window to create a new email template."""


def send_email():
    """Send email to contacts."""
    email_login()

    # select saved emails from database
    mycursor.execute("select * from emails;")
    data = [i for i in mycursor]

    # select contacts from database
    mycursor.execute("select * from contacts;")
    emails = [i for i in mycursor]
    print(emails)

    count = 1
    total = len(data)

    for row in data:
        name = str(emails[0][0]) + " " + str(emails[0][1])
        receiver = emails[0][2]

        # message details
        message = MIMEMultipart("alternative")
        message["Subject"] = row[1]
        message["From"] = sender
        message["To"] = receiver
        print(message)

        # print(receiver)
        html = row[2]

        # plaintext = MIMEText(text, "plain")
        html = MIMEText(html, "html")

        # message.attach(plaintext)
        message.attach(html)

        """
        try:
            server.sendmail(sender, receiver, message.as_string())
        except:
            pass
        """
        count += 1


def email_mang():
    removeall()


# ----------------------------------------------------------------------------------------------------------------------
# Contact management


def add_manual_contact(fname, lname, email):
    """Adds contact to database manually."""

    db.cursor(buffered=True).execute(
        f"INSERT INTO CONTACTS (fname, lname, email) VALUES ('{fname}', '{lname}', '{email}');"
    )


def delete_contact(email):
    """Deletes contact from database."""

    db.cursor(buffered=True).execute(f"DELETE FROM CONTACTS WHERE email = '{email}';")


def contact_mang():
    removeall()


removeall()

# ----------------------------------------------------------------------------------------------------------------------

# Login window
title = Label(root, text="Email Bot")
title.grid(row=0, column=0)
username_label = Label(root, text="Enter Email")
username_label.grid(row=1, column=0)
username_entry = Entry(root, exportselection=0, fg="blue")
username_entry.grid(row=1, column=1)
password_label = Label(root, text="Enter Password")
password_label.grid(row=2, column=0)
password_entry = Entry(root, exportselection=0, fg="blue", show="●")
password_entry.grid(row=2, column=1)
login_button = Button(root, text="Login", command=login)
login_button.grid(row=3, column=0)


# Options menu
options_title = Label(root, text="Menu")
contact_mang_button = Button(root, text="Contact management", command=contact_mang)
email_mang_button = Button(root, text="Email management", command=email_mang)


def login():
    """Login to email"""
    global sender
    global password
    global options_title
    global contact_mang_button
    global email_mang_button
    sender = username_entry.get()
    password = password_entry.get()

    removeall()

    options_title.grid(row=0, column=1)
    contact_mang_button.grid(row=1, column=0)
    email_mang_button.grid(row=1, column=2)


root.mainloop()
