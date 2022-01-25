from tkinter import *

root=Tk()

def removeall():
    '''Removes all widgets'''
    widgets=root.winfo_children()
    for item in widgets:
        if item.winfo_children():
            widgets.extend(item.winfo_children())
    for item in widgets:
        item.grid_forget()


def login():
    '''Login to email'''
    global sender
    global password
    global options_title
    global contact_mang_button
    global email_mang_button
    sender=username_entry.get()
    password=password_entry.get()
    #print(sender)
    #print(password)
    removeall()
    options_title.grid(row=0,column=1)
    contact_mang_button.grid(row=1,column=0)
    email_mang_button.grid(row=1,column=2)

def email_mang():
    removeall()
    

removeall()
#Login
title=Label(root,text="Email Bot")
title.grid(row=0,column=0)
username_label=Label(root, text="Enter Email")
username_label.grid(row=1, column=0)
username_entry=Entry(root, exportselection=0, fg="blue")
username_entry.grid(row=1, column=1)
password_label=Label(root, text="Enter Password")
password_label.grid(row=2, column=0)
password_entry=Entry(root, exportselection=0, fg="blue", show="●")
password_entry.grid(row=2, column=1)
login_button=Button(root,text="Login",command=login)
login_button.grid(row=3,column=0)

#Options menu
options_title=Label(root,text="Menu")
contact_mang_button=Button(root,text="Contact management")
email_mang_button=Button(root,text="Email management",command=email_mang)


root.mainloop()