from tkinter import *
import mysql.connector
import execution

root = Tk()

db = execution.db_connect()

mycursor = db.cursor(buffered=True)

contact_mang_title = Label(root, text="Manage contacts")
contact_mang_title.grid(row=0, column=0)

# select contacts from list
mycursor.execute("select * from contacts;")
names = [0]
emails = [0]
for i in mycursor:
    names.append(i[0] + " " + i[1])
    emails.append(i[2])

print(names)
print(emails)

mycursor.execute("select * from emails;")
messages = []
for i in mycursor:
    messages.append(i)
print(messages)


def send_emails():
    message = msg.get("1.0", END)
    to_send = listbox_emails.curselection()


# Emails
contact_mang_title = Label(root, text="Select contacts", font=("Arial", 25))
contact_mang_title.grid(row=0, column=0)
scrollbar_contacts = Scrollbar(root)
scrollbar_contacts.grid(row=1, column=1, ipady=60)
listbox_emails = Listbox(root, selectmode="multiple", selectbackground="#00DE1B")
for i in range(1, len(emails)):
    listbox_emails.insert(i, names[i] + "(" + emails[i] + ")")


listbox_emails.grid(row=1, column=0, ipadx=100, ipady=110)
listbox_emails.config(yscrollcommand=scrollbar_contacts.set)
scrollbar_contacts.config(command=listbox_emails.yview)

# Message
msg_title = Label(root, text="Write message", font=("Arial", 25))
msg_title.grid(row=0, column=1)

msg = Text(root)
msg.grid(row=1, column=1, padx=20)

send_button = Button(
    root, text="Send emails", width=20, height=2, bg="cyan", command=send_emails
)
send_button.grid(row=2, column=1)

# Past messages
pastmsgs = Label(root, text="Past messages", font=("Arial", 25))
pastmsgs.grid(row=0, column=2)

listbox_messages = Listbox(root, selectbackground="#00DE1B")
listbox_messages.grid(row=1, column=2, ipadx=100, ipady=110)


scrollbar_showitems = Scrollbar(root)
scrollbar_showitems.grid(row=1, column=1, ipady=60)
listbox_emails = Listbox(root, selectmode="multiple", selectbackground="green")
for i in range(1, len(emails)):
    listbox_emails.insert(i, emails[i])


listbox_emails.grid(row=1, column=0, ipadx=60)
listbox_emails.config(yscrollcommand=scrollbar_showitems.set)
scrollbar_showitems.config(command=listbox_emails.yview)

root.mainloop()
