import mysql.connector
from tkinter import *


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

root = Tk()
