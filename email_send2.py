from tkinter import *
from execution import db_connect
from tkinter import messagebox

root=Tk()

db=db_connect()

mycursor=db.cursor(buffered=True)

def removeall():
    """Removes all widgets"""
    widgets = root.winfo_children()
    for item in widgets:
        if item.winfo_children():
            widgets.extend(item.winfo_children())
    for item in widgets:
        item.grid_forget()
        


mycursor.execute("select * from contacts;")
names=[]
emails=[]
for i in mycursor:
    names.append(i[0]+" "+i[1])
    emails.append(i[2])                                                                     

#print(names)
#print(emails)

mycursor.execute("select * from emails;")
messages=[]
for i in mycursor:
    messages.append(i)
#print(messages)


'''
def send_emails():
    message=msg.get("1.0",END)
    to_send=listbox_emails.curselection()
'''

#Contacts
def open_contacts():
    removeall()
    contact_mang_title.grid(row=0,column=0)
    scrollbar_contacts.grid(row=1,column=1,ipady=170,sticky='e')
    listbox_contacts.grid(row=1,column=0,ipadx=100,ipady=110)
    continue_button.grid(row=2,column=0)
    select_all_button.grid(row=3,column=0)


contact_mang_title=Label(root,text="Manage contacts")
contact_mang_title.grid(row=0,column=0)

contact_mang_title=Label(root,text="Select contacts",font=("Arial",20))

contact_mang_title.grid_forget()
scrollbar_contacts = Scrollbar(root,orient="vertical")

scrollbar_contacts.grid(row=1,column=1,ipady=170,sticky='e')
listbox_contacts=Listbox(root, selectmode="multiple",selectbackground="#90EE90")

for i in range(len(emails)):
    listbox_contacts.insert(END,names[i]+"("+emails[i]+")")

listbox_contacts.config(yscrollcommand=scrollbar_contacts.set)
listbox_contacts.grid_forget()
scrollbar_contacts.config(command=listbox_contacts.yview)

def contacts_continue():
    receivers=listbox_contacts.curselection()
    if len(receivers)==0:
        messagebox.showerror("Error", "You must select at least one contact")
        return
    open_pastmsgs()
    

def selectall():
    listbox_contacts.select_set(0,END)


continue_button=Button(root,text="Continue",width=20,height=2,bg="cyan",command=contacts_continue)
continue_button.grid_forget()
select_all_button=Button(root,text="Select all",bg="orange",width=20,height=2,command=selectall)
select_all_button.grid_forget()
open_contacts()


'''
#Message
msg_title=Label(root,text="Write message",font=("Arial",25))
msg_title.grid(row=0,column=1)

msg=Text(root)
msg.grid(row=1,column=1,padx=20)

send_button=Button(root,text="Send emails",width=20,height=2,bg="cyan",command=send_emails)
send_button.grid(row=2,column=1)
'''

#Past messages

def open_pastmsgs():
    removeall()
    pastmsgs.grid(row=0,column=1)
    scrollbar_messages.grid(row=1,column=2,ipady=170,sticky='e')
    listbox_messages.grid(row=1,column=1,ipadx=100,ipady=110)
    listbox_messages.grid(row=1,column=1,ipadx=100,ipady=110)
    viewmsgbutton.grid(row=2,column=1)
    addnewmsgbutton.grid(row=3,column=1)
    sendmsgbutton.grid(row=4,column=1)
    backtocontacts.grid(row=5,column=1)

def addnewmsg():
    top=Toplevel(root)
    top.title("Add new message")
    top.geometry("400x400")
    
    top.mainloop()


pastmsgs=Label(root,text="Messages",font=("Arial",25))
pastmsgs.grid_forget()

scrollbar_messages = Scrollbar(root,orient="vertical")
scrollbar_messages.grid_forget()

listbox_messages=Listbox(root,selectbackground="#90EE90")
listbox_messages.grid_forget()

for i in range(len(messages)):
    stuff=messages[i][1]
    listbox_messages.insert(END,stuff)


listbox_messages.grid_forget()
listbox_messages.config(yscrollcommand=scrollbar_messages.set)
scrollbar_contacts.config(command=listbox_messages.yview)

viewmsgbutton=Button(root,text="View/Edit message",bg="cyan",width=20,height=2)
viewmsgbutton.grid_forget()

addnewmsgbutton=Button(root,text="Add new message",bg="orange",width=20,height=2,command=addnewmsg)
addnewmsgbutton.grid_forget()

sendmsgbutton=Button(root,text="Send message",bg="#90EE90",width=20,height=2)
sendmsgbutton.grid_forget()

backtocontacts=Button(root,text="Back to contacts",bg="#DE2247",width=20,height=2,command=open_contacts)
backtocontacts.grid_forget()

root.mainloop() 