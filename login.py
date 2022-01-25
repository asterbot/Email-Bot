from tkinter import *

root=Tk()

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


root.mainloop()

def removeall():
    for widgets in root.winfo_children():
        widgets.destroy()