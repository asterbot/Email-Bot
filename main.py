from logging import raiseExceptions
from tkinter import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from tkinter import messagebox

# ----------------------------------------------------------------------------------------------------------------------
# Database and table setup


def db_connect():

    try:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="password", database="email_bot"
        )

    # create database if it doesn't exist
    except:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="password")

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

def getcontacts():
    mycursor.execute("select * from contacts;")
    names=[]
    emails=[]
    for i in mycursor:
        names.append(i[0]+" "+i[1])
        emails.append(i[2])                                                                     
    return names,emails
names=getcontacts()[0]
emails=getcontacts()[1]

def getmessages():
    mycursor.execute("select * from emails;")
    messages=[]
    for i in mycursor:
        i=list(i)
        if "\n" in i[2]:
            i[2]=i[2].replace("\n","<br>")
        messages.append(tuple(i))
    return messages

messages=getmessages()

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

    try:
        db.cursor(buffered=True).execute(
            f"INSERT INTO CONTACTS (fname, lname, email) VALUES ('{fname}', '{lname}', '{email}');"
        )
    except mysql.connector.errors.IntegrityError:

        messagebox.showerror(
            "Duplicate Entry", "A contact already exists with this email address. Please try again. Click the Delete Contact button to remove the contact.")

    db.commit()

    # clear entry boxes
    fname_entry.delete(0, END)
    lname_entry.delete(0, END)
    email_entry.delete(0, END)


def delete_contact(email):
    """Deletes contact from database."""

    try:
        if email == "":
            messagebox.showerror("No Contact Selected",
                                 "Please select a contact to delete.")
            return

        db.cursor(buffered=True).execute(
            f"DELETE FROM CONTACTS WHERE email = '{email}';")

        messagebox.showinfo("Contact Deleted", "Contact has been deleted.")
        email.delete(0, END)

    except:
        messagebox.showerror("Error", "Contact could not be deleted.")


def contact_mang():
    """Contact management window."""
    removeall()

    global fname_entry, lname_entry, email_entry

    title = Label(root, text="Contact Management")
    title.grid(row=0, column=0)

    fname_label = Label(root, text="Enter First Name:")
    fname_label.grid(row=1, column=0)
    fname_entry = Entry(root, exportselection=0, fg="blue")
    fname_entry.grid(row=1, column=1)

    lname_label = Label(root, text="Enter Last Name:")
    lname_label.grid(row=2, column=0)
    lname_entry = Entry(root, exportselection=0, fg="blue")
    lname_entry.grid(row=2, column=1)

    email_label = Label(root, text="Enter Email*:")
    email_label.grid(row=3, column=0)
    email_entry = Entry(root, exportselection=0, fg="blue")
    email_entry.grid(row=3, column=1)

    add_contact_button = Button(root, text="Add Contact", command=lambda: add_manual_contact(
        fname_entry.get(), lname_entry.get(), email_entry.get()))
    add_contact_button.grid(row=4, column=0)

    delete_contact_button = Button(
        root, text="Delete Contact", command=lambda: delete_contact(email_entry.get()))
    delete_contact_button.grid(row=4, column=1)

    info_label = Label(root, text="*Enter only the email to delete a contact.")
    info_label.grid(row=5, column=0)

    back_button = Button(root, text="Back", command=mainscreen)
    back_button.grid(row=6, column=0)


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
contact_mang_button = Button(
    root, text="Contact management", command=contact_mang)
email_mang_button = Button(root, text="Email management", command=email_mang)


def mainscreen():
    """Main screen window."""
    removeall()

    options_title.grid(row=0, column=1)
    contact_mang_button.grid(row=1, column=0)
    email_mang_button.grid(row=1, column=2)


def login():
    """Login to email"""

    global sender
    global password
    global options_title
    global contact_mang_button
    global email_mang_button
    sender = username_entry.get()
    password = password_entry.get()

    mainscreen()


root.mainloop()
