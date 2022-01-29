from tkinter import *
import mysql.connector
from tkinter import messagebox

root=Tk()

def db_connect():

    try:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="arjun2004", database="email_bot"
        )

    # create database if it doesn't exist
    except:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="password")

        db.cursor(buffered=True).execute("create database email_bot")

    return db

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
    global messages
    top=Toplevel(root)
    def handle_click(event):
        subject_top_entry.delete(0,END)
        subject_top_entry.config(fg="black")
    
    def handle_click_2(event):
        msg_top.delete("1.0",END)
        msg_top.config(fg="black")

    def add_msg():
        global messages
        """Adds message to messagelist."""
        subject=subject_top_entry.get()
        msg=msg_top.get("1.0",END)
        try:
            newmsgid=messages[-1][0]+1
            db.cursor(buffered=True).execute(
                f"INSERT INTO EMAILS VALUES ('{newmsgid}', '{subject}', '{msg}');"
            )
        except mysql.connector.errors.IntegrityError:

            messagebox.showerror(
                "Duplicate Entry", "A contact already exists with this email address. Please try again. Click the Delete Contact button to remove the contact.")

        db.commit()
        # clear entry boxes
        subject_top_entry.delete(0, END)
        msg_top.delete("1.0", END)
        listbox_messages.delete(0,END)
        messages=getmessages()
        for i in range(len(messages)):
            stuff=messages[i][1]
            listbox_messages.insert(END,stuff)
        messagebox.showinfo("Info","This message has been added")


        
    top.title("Add new message")
    title_top=Label(top,text="Enter new message",font=("Arial",15))
    title_top.grid(row=0,column=0,pady=20)
    subject_top_entry=Entry(top,exportselection=0,width=54,fg="#696969")
    subject_top_entry.insert(0,"Subject")
    subject_top_entry.grid(row=1,column=0,columnspan=2)
    subject_top_entry.bind("<1>", handle_click)

    msg_top=Text(top,width=40,fg="#696969")
    msg_top.insert(END,"Type your message here...")
    msg_top.grid(row=2,column=0,columnspan=2,pady=20)
    msg_top.bind("<1>", handle_click_2)

    send_btn_top=Button(top,text="Add message",width=20,height=2,bg="#90EE90",command=add_msg)
    send_btn_top.grid(row=3,column=0)
    top.mainloop()

def vieweditmsg():
    global messages
    def edit_msg():
        global messages
        """Edits message in messagelist."""
        subject=subject_top_entry.get()
        msg=msg_top.get("1.0",END)
        msgid=messages[listbox_messages.curselection()[0]][0]
        db.cursor(buffered=True).execute(
            f"UPDATE EMAILS SET SUBJECT = '{subject}', CONTENT = '{msg}' WHERE MSGID = '{msgid}';"
        )
        db.commit()
        # clear entry boxes
        subject_top_entry.delete(0, END)
        msg_top.delete("1.0", END)
        listbox_messages.delete(0,END)
        messages=getmessages()
        for i in range(len(messages)):
            stuff=messages[i][1]
            listbox_messages.insert(END,stuff)
        messagebox.showinfo("Info","This message has been edited")
        top.withdraw()

    top=Toplevel(root)
    top.title("View message")
    title_top=Label(top,text="View/Edit message",font=("Arial",15))
    title_top.grid(row=0,column=0,pady=20)
    try:
        sel=listbox_messages.curselection()[0]
        subject=messages[sel][1]
        msg=messages[sel][2]
        subject_top_entry=Entry(top,exportselection=0,width=54)
        subject_top_entry.insert(0,subject)
        subject_top_entry.grid(row=1,column=0,columnspan=2)

        msg_top=Text(top,width=40)
        msg_top.insert(END,msg)
        msg_top.grid(row=2,column=0,columnspan=2,pady=20)

        send_btn_top=Button(top,text="Edit message",width=20,height=2,bg="#90EE90",command=edit_msg)
        send_btn_top.grid(row=3,column=0)
        top.mainloop()
    except:
        messagebox.showerror("Error","Please select a message to edit")


pastmsgs=Label(root,text="Messages",font=("Arial",25))
pastmsgs.grid_forget()

scrollbar_messages = Scrollbar(root,orient="vertical")
scrollbar_messages.grid_forget()

listbox_messages=Listbox(root,selectbackground="#90EE90")
listbox_messages.grid_forget()

for i in range(len(getmessages())):
    stuff=getmessages()[i][1]
    listbox_messages.insert(END,stuff)


listbox_messages.grid_forget()
listbox_messages.config(yscrollcommand=scrollbar_messages.set)
scrollbar_contacts.config(command=listbox_messages.yview)

viewmsgbutton=Button(root,text="View/Edit message",bg="cyan",width=20,height=2,command=vieweditmsg)
viewmsgbutton.grid_forget()

addnewmsgbutton=Button(root,text="Add new message",bg="orange",width=20,height=2,command=addnewmsg)
addnewmsgbutton.grid_forget()

sendmsgbutton=Button(root,text="Send message",bg="#90EE90",width=20,height=2)
sendmsgbutton.grid_forget()

backtocontacts=Button(root,text="Back to contacts",bg="#DE2247",width=20,height=2,command=open_contacts)
backtocontacts.grid_forget()

root.mainloop() 