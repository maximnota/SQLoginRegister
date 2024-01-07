import sqlite3
from iPyQT import *

def selectAll(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    rows = c.fetchall()
    return rows

def selectRow(conn, rowName):
    c = conn.cursor()
    c.execute(f"SELECT {rowName} FROM data")
    rows = c.fetchall()
    return rows

def insertData(conn, username, password):
    c = conn.cursor()
    c.execute(f"INSERT INTO data VALUES ('{username}', '{password}');")
    conn.commit()

def createConnection(database_file):
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except:
        print("Error when connecting")

def executeCommand(conn, command):
    c = conn.cursor()
    c.execute(command)
    returnValue = c.fetchall()
    return returnValue

def mainWin():
    win.HideAll()
    win.changeWindowTitle("Main Window")
    mainText = win.addText("Main window", 50, "Center")
    win.changeFont("Text", mainText, "Kabel-Heavy", 50)
    win.addButton("Register", registerWindow)
    win.addButton("Log in", loginWindow)

def register():
    win.HideAll()
    insertData(conn, win.getTextFieldValue(newUsernamedTextField), win.getTextFieldValue(newPasswordTextField))
    win.addText("Registered user", 25, "Center")
    win.addButton("Main window", mainWin)

def registerWindow():
    win.HideAll()
    win.changeWindowTitle("Register Window")
    RegisterText = win.addText("Register", 50, "Center-top")
    win.changeFont("Text", RegisterText, "Kabel-Heavy", 50)
    win.addText("Username", 25, "Center-top")
    global newUsernamedTextField
    newUsernamedTextField = win.addTextField(25, 50, "Center-top")
    win.addText("Password", 25, "Center-top")
    global newPasswordTextField
    newPasswordTextField = win.addTextField(25, 50, "Center-top")
    win.addButton("Register", register)

def login():
    win.HideAll()
    usernameRows = selectRow(conn, "username")
    userExists = False
    for username in usernameRows:
        if username[0] == win.getTextFieldValue(usernameTextField):
            print("User found")
            userExists = True
            break
    if userExists == False:
        win.addText("User doesn't exist", 25, "Center")
        win.addButton("Retry", loginWindow)
        win.addButton("Main window", mainWin)
    if userExists:
        realPasswords = executeCommand(conn, f"SELECT password FROM data WHERE username = '{win.getTextFieldValue(usernameTextField)}'")
        passwords = [row[0] for row in realPasswords]
        if win.getTextFieldValue(passwordTextField) in passwords:
            win.addText("You have logged in", 25, "Center-top")
            win.addButton("Log out", mainWin)
        else:
            win.addText("Incorrect password", 25, "Center-top")
            win.addButton("Retry", loginWindow)
            win.addButton("Main window", mainWin)


def loginWindow():
    win.HideAll()
    win.changeWindowTitle("Log in")
    LoginText = win.addText("Username", 50, "Center-top")
    win.changeFont("Text", LoginText, "Kabel-Heavy", 50)
    global usernameTextField
    usernameTextField = win.addTextField(25, 50, "Center-top")
    win.addText("Password", 25, "Center-top")
    global passwordTextField
    passwordTextField = win.addTextField(25, 50, "Center-top")
    win.addButton("Log in", login)

win = CustomWindow(300, 350, "Main Window")
win.create()
mainText1 = win.addText("Main window", 50, "Center")
win.changeFont("Text", mainText1, "Kabel-Heavy", 50)
conn = createConnection("data.db")
win.addButton("Register", registerWindow)
win.addButton("Log in", loginWindow)
win.init()

