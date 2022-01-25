from tkinter import *
import mysql.connector
import execution

root = Tk()

db = execution.db_connect()

mycursor = db.cursor()


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

scrollbar_showitems = Scrollbar(root)
scrollbar_showitems.grid(row=1, column=1, ipady=60)
listbox_emails = Listbox(root, selectmode="multiple", selectbackground="green")
for i in range(1, len(emails)):
    listbox_emails.insert(i, emails[i])


listbox_emails.grid(row=1, column=0, ipadx=60)
listbox_emails.config(yscrollcommand=scrollbar_showitems.set)
scrollbar_showitems.config(command=listbox_emails.yview)

root.mainloop()
