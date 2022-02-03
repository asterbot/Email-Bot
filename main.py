from logging import raiseExceptions
import multiprocessing
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
        db = mysql.connector.connect(host="localhost", user="root", passwd="arjun2004")

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
    "msgid int primary key, subject varchar(200), content mediumtext",
)


createtab(
    "contacts", "fname varchar(50), lname varchar(50), email varchar(50) primary key"
)


def getcontacts():
    mycursor.execute("select * from contacts;")
    names = []
    emails = []
    for i in mycursor:
        names.append(i[0] + " " + i[1])
        emails.append(i[2])
    return names, emails


names = getcontacts()[0]
emails = getcontacts()[1]


def getmessages():
    mycursor.execute("select * from emails;")
    messages = []
    for i in mycursor:
        i = list(i)
        if "\n" in i[2]:
            i[2] = i[2].replace("\n", "<br>")
        messages.append(tuple(i))
    return messages


def updatelistboxcontacts():
    """Updates listbox with contacts."""
    global listbox_contacts
    listbox_contacts.delete(0, END)
    names = getcontacts()[0]
    emails = getcontacts()[1]
    for i in range(len(emails)):
        listbox_contacts.insert(END, names[i] + "(" + emails[i] + ")")


messages = getmessages()

root = Tk()
root.title("Email Bot")


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

    global sender, password, login_button, options_title, contact_mang_button, email_mang_button, send_email_button
    sender = username_entry.get()
    password = password_entry.get()

    removeall()

    options_title.grid(row=0, column=1)
    contact_mang_button.grid(row=1, column=0)
    email_mang_button.grid(row=1, column=2)
    send_email_button.grid(row=2, column=1)


# ----------------------------------------------------------------------------------------------------------------------
# Email sending


def send_email():
    """Send email to contacts."""
    global sender, password

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(sender, password)

    names = getcontacts()[0]
    emails = getcontacts()[1]
    messages = getmessages()
    send_people = [names[i] for i in list(listbox_contacts.curselection())]
    send_mails = [emails[i] for i in list(listbox_contacts.curselection())]

    def send_email_to_one(i):
        """Send email to one contact."""
        message = MIMEMultipart("alternative")
        message["Subject"] = messages[listbox_messages.curselection()[0]][1]
        message["From"] = sender
        message["To"] = send_mails[i]

        fname = send_people[i].split()[0]
        lname = send_people[i].split()[1]

        html = messages[listbox_messages.curselection()[0]][2].format(
            fname=fname, lname=lname, email=send_mails[i]
        )
        html = MIMEText(html, "html")

        # message.attach(plaintext)
        message.attach(html)

        try:
            server.sendmail(sender, send_mails[i], message.as_string())
            print("sent")
        except:
            print("fail")

    for i in range(len(send_mails)):
        send_email_to_one(i)


def viewmsg():
    """View message screen."""
    global listbox_messages

    sel = listbox_messages.curselection()[0]
    subject = messages[sel][1]
    msg = messages[sel][2]

    top = Toplevel(root)
    top.title("View message")
    title_top = Label(top, text="View message", font=("Arial", 15))
    title_top.grid(row=0, column=0, pady=20)
    subject_top_label = Label(
        top, text=subject, width=45, borderwidth=2, bg="white", anchor="w"
    )
    subject_top_label.grid(row=1, column=0, columnspan=2)

    msg_top = Text(top, width=40)
    msg_top.insert(END, msg.replace("<br>", "\n"))
    msg_top.grid(row=2, column=0, columnspan=2, pady=20)
    msg_top.configure(state="disabled")

    top.mainloop()


def send_mail():
    global listbox_contacts, listbox_messages
    removeall()

    title = Label(root, text="Send Email", font=("Arial", 20))
    title.grid(row=0, column=0)
    choose_emails_label = Label(root, text="Choose Email(s)")
    choose_emails_label.grid(row=1, column=0)
    scrollbar_contacts.grid(row=2, column=1, pady=40, ipady=110, sticky="w")
    listbox_contacts.grid(row=2, column=0, ipadx=100, ipady=110)
    listbox_contacts.config(selectmode="multiple")

    choose_messages_label = Label(root, text="Choose Messages")
    choose_messages_label.grid(row=1, column=2)
    scrollbar_messages.grid(row=2, column=3, ipady=170, sticky="e")
    listbox_messages.grid(row=2, column=2, ipadx=100, ipady=110)

    viewmail = Button(root, text="View message", bg="cyan", command=viewmsg)
    viewmail.grid(row=3, column=2)

    sendmailbutton = Button(
        root, text="Send mail", bg="#90EE90", font=("Arial", 10), command=send_email
    )
    sendmailbutton.grid(row=2, column=4, padx=20)


# ----------------------------------------------------------------------------------------------------------------------
# Contact management


def add_manual_contact(fname, lname, email):
    """Adds contact to database manually."""

    try:
        db.cursor(buffered=True).execute(
            f"INSERT INTO CONTACTS (fname, lname, email) VALUES ('{fname}', '{lname}', '{email}');"
        )
        messagebox.showinfo("Info", "Contact added")
        updatelistboxcontacts()
    except mysql.connector.errors.IntegrityError:

        messagebox.showerror(
            "Duplicate Entry",
            "A contact already exists with this email address. Please try again. Click the Delete Contact button to remove the contact.",
        )

    db.commit()

    # clear entry boxes
    fname_entry.delete(0, END)
    lname_entry.delete(0, END)
    email_entry.delete(0, END)


def delete_contact(email):
    global listbox_contacts

    """Deletes contact from database."""

    try:
        if email == "":
            messagebox.showerror(
                "No Contact Selected", "Please select a contact to delete."
            )
            return
        ans = messagebox.askyesno(
            "Delete Contact", f"Are you sure you want to delete {email}?"
        )
        if ans == 1:
            db.cursor(buffered=True).execute(
                f"DELETE FROM CONTACTS WHERE email = '{email}';"
            )

            db.commit()

            messagebox.showinfo("Contact Deleted", "Contact has been deleted.")
            # email.delete(0, END)
            updatelistboxcontacts()
        else:
            return

    except:
        messagebox.showerror("Error", "Contact could not be deleted.")


def contact_mang():
    """Contact management window."""
    removeall()

    global fname_entry, lname_entry, email_entry, emails, names, messages, listbox_contacts

    title = Label(root, text="Contact Management")
    title.grid(row=0, column=0)

    fname_label = Label(root, text="Enter First Name:")
    fname_label.grid(row=1, column=0, sticky=W + E)
    fname_entry = Entry(root, exportselection=0, fg="blue")
    fname_entry.grid(row=1, column=1)

    lname_label = Label(root, text="Enter Last Name:")
    lname_label.grid(row=2, column=0, sticky=W + E)
    lname_entry = Entry(root, exportselection=0, fg="blue")
    lname_entry.grid(row=2, column=1)

    email_label = Label(root, text="Enter Email:")
    email_label.grid(row=3, column=0, sticky=W + E)
    email_entry = Entry(root, exportselection=0, fg="blue")
    email_entry.grid(row=3, column=1)

    add_contact_button = Button(
        root,
        text="Add Contact",
        command=lambda: add_manual_contact(
            fname_entry.get(), lname_entry.get(), email_entry.get()
        ),
    )
    add_contact_button.grid(row=4, column=0)

    # Listbox
    listbox_contacts.config(selectmode="single")
    scrollbar_contacts.grid(row=5, column=1, pady=40, ipady=110, sticky="w")
    listbox_contacts.grid(row=5, column=0, ipadx=100, ipady=50)

    delete_contact_button = Button(
        root,
        text="Delete Contact",
        command=lambda: delete_contact(emails[listbox_contacts.curselection()[0]]),
    )
    delete_contact_button.grid(row=5, column=1)

    back_button = Button(root, text="Back", command=mainscreen)
    back_button.grid(row=6, column=0)


# Contacts listbox
scrollbar_contacts = Scrollbar(root, orient="vertical")
listbox_contacts = Listbox(
    root, selectmode="single", selectbackground="#90EE90", exportselection=0
)

for i in range(len(emails)):
    listbox_contacts.insert(END, names[i] + "(" + emails[i] + ")")

listbox_contacts.config(yscrollcommand=scrollbar_contacts.set)
scrollbar_contacts.config(command=listbox_contacts.yview)

# ----------------------------------------------------------------------------------------------------------------------
# Email management


def vieweditmsg():
    """Edit message window."""
    global messages

    def edit_msg():
        """Edits message in messagelist."""

        global messages

        # get the new subject
        subject = subject_top_entry.get()

        # get the new message
        msg = msg_top.get("1.0", END)

        # get message id
        msgid = messages[listbox_messages.curselection()[0]][0]

        # update content
        db.cursor(buffered=True).execute(
            f"UPDATE EMAILS SET SUBJECT = '{subject}', CONTENT = '{msg}' WHERE MSGID = '{msgid}';"
        )
        db.commit()

        # clear entry boxes
        subject_top_entry.delete(0, END)
        msg_top.delete("1.0", END)
        listbox_messages.delete(0, END)
        messages = getmessages()

        for i in range(len(messages)):
            stuff = messages[i][1]
            listbox_messages.insert(END, stuff)

        # display message
        messagebox.showinfo("Info", "This message has been edited")
        top.withdraw()

    try:
        sel = listbox_messages.curselection()[0]
        subject = messages[sel][1]
        msg = messages[sel][2]
        top = Toplevel(root)

        # view message window
        top.title("View message")
        title_top = Label(top, text="View/Edit message", font=("Arial", 15))
        title_top.grid(row=0, column=0, pady=20)
        subject_top_entry = Entry(top, exportselection=0, width=54)
        subject_top_entry.insert(0, subject)
        subject_top_entry.grid(row=1, column=0, columnspan=2)

        msg_top = Text(top, width=40)
        msg_top.insert(END, msg)
        msg_top.grid(row=2, column=0, columnspan=2, pady=20)

        send_btn_top = Button(
            top, text="Edit message", width=20, height=2, bg="#90EE90", command=edit_msg
        )
        send_btn_top.grid(row=3, column=0)
        top.mainloop()

    except:
        # error if no message was selected
        messagebox.showerror("Error", "Please select a message to edit")


def addnewmsg():
    """Add new message to database."""

    global messages
    top = Toplevel(root)

    def handle_click(event):
        subject_top_entry.delete(0, END)
        subject_top_entry.config(fg="black")

    def handle_click_2(event):
        msg_top.delete("1.0", END)
        msg_top.config(fg="black")

    def add_msg():
        global messages
        """Adds message to messagelist."""
        subject = subject_top_entry.get()
        msg = msg_top.get("1.0", END)
        try:
            if messages == []:
                newmsgid = 1
            else:
                newmsgid = messages[-1][0] + 1
            db.cursor(buffered=True).execute(
                f"INSERT INTO EMAILS VALUES ('{newmsgid}', '{subject}', '{msg}');"
            )
        except mysql.connector.errors.IntegrityError:

            messagebox.showerror(
                "Duplicate Entry",
                "A contact already exists with this email address. Please try again. Click the Delete Contact button to remove the contact.",
            )

        db.commit()

        # clear entry boxes
        subject_top_entry.delete(0, END)
        msg_top.delete("1.0", END)
        listbox_messages.delete(0, END)
        messages = getmessages()

        for i in range(len(messages)):
            stuff = messages[i][1]
            listbox_messages.insert(END, stuff)

        messagebox.showinfo("Info", "This message has been added")

    top.title("Add new message")
    title_top = Label(top, text="Enter new message", font=("Arial", 15))
    title_top.grid(row=0, column=0, pady=20)
    subject_top_entry = Entry(top, exportselection=0, width=54, fg="#696969")
    subject_top_entry.insert(0, "Subject")
    subject_top_entry.grid(row=1, column=0, columnspan=2)
    subject_top_entry.bind("<1>", handle_click)

    msg_top = Text(top, width=40, fg="#696969")
    msg_top.insert(END, "Type your message here...")
    msg_top.grid(row=2, column=0, columnspan=2, pady=20)
    msg_top.bind("<1>", handle_click_2)

    send_btn_top = Button(
        top, text="Add message", width=20, height=2, bg="#90EE90", command=add_msg
    )
    send_btn_top.grid(row=3, column=0)
    top.mainloop()


def email_mang():
    global listbox_messages
    removeall()
    pastmsgs = Label(root, text="Manage Messages", font=("Arial", 20))
    pastmsgs.grid(row=0, column=1)

    # Listbox
    scrollbar_messages.grid(row=1, column=2, ipady=170, sticky="e")
    listbox_messages.grid(row=1, column=1, ipadx=100, ipady=110)

    viewmsgbutton = Button(
        root,
        text="View/Edit message",
        bg="cyan",
        width=20,
        height=2,
        command=vieweditmsg,
    )
    viewmsgbutton.grid(row=2, column=1)

    addnewmsgbutton = Button(
        root, text="Add new message", bg="orange", width=20, height=2, command=addnewmsg
    )
    addnewmsgbutton.grid(row=3, column=1)

    back_button = Button(
        root, text="Back", bg="#DE2247", width=20, height=2, command=mainscreen
    )
    back_button.grid(row=5, column=1)


# Messages listbox
scrollbar_messages = Scrollbar(root, orient="vertical")

listbox_messages = Listbox(root, selectbackground="#90EE90", exportselection=0)
for i in range(len(getmessages())):
    stuff = getmessages()[i][1]
    listbox_messages.insert(END, stuff)

listbox_messages.config(yscrollcommand=scrollbar_messages.set)
scrollbar_messages.config(command=listbox_messages.yview)

# ----------------------------------------------------------------------------------------------------------------------

removeall()
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
send_email_button = Button(root, text="Send Email", command=send_mail)


def mainscreen():
    """Main screen window."""
    global options_title, contact_mang_button, email_mang_button, send_email_button
    removeall()
    options_title.grid(row=0, column=1)
    contact_mang_button.grid(row=1, column=0)
    email_mang_button.grid(row=1, column=2)
    send_email_button.grid(row=2, column=1)


root.mainloop()
