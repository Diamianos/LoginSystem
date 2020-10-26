# Login system
# https://pythonprogramming.net/sql-database-python-part-1-inserting-database/
# === Steps for operation ===

# 1. Ask user if they want to login or create an account
# 2. Based on the input either ask them for user name and password and write that to a file
# 3. if login, ask for user name and password and then compare that with the information in the text file.

import stdiomask # Module to hide the characters when typing
import sqlite3

conn = sqlite3.connect("Login DB.db") # Setting the conneciton to the database
c = conn.cursor() # Creating the cursor to manipulate the database

def main():

    # Creating the database if it doesnt exist
    c.execute("CREATE TABLE IF NOT EXISTS usernameAndPasswords(username TEXT, password TEXT)")

    print("Welcome to my first login system.\n")
    print("Please choose from the following:" + 
            "\n(1) Login" +
            "\n(2) Create a new account")

    print()
    user_selection = str(input("-- "))

    # Input validation 
    while user_selection != "1" and user_selection != "2":
        user_selection = str(input("Please either enter \"1\" to login or \"2\" to create an account: "))

    # If user entered "1" verify their login credentials and log them in
    if user_selection == "1":
        login()
    elif user_selection == "2":
        createNewUser()


def login():
    # Getting the user input
    print("Please enter your username and password when prompted.")
    username = input("Username: ").lower()
    password = stdiomask.getpass("Password: ")

    # Getting the username data based on the user name entered
    c.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{username}"')
    db_username = c.fetchone()

    while db_username == None:
        print("\nUsername not found please try again or create another account.")

        # Asking for credentials again
        username = input("Username: ").lower()
        password = stdiomask.getpass("Password: ")

        # Getting the username data based on the user name entered
        c.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{username}"')
        db_username = c.fetchone()

    # Getting the password data associated to the username that was entered
    c.execute(f'SELECT password FROM usernameAndPasswords WHERE username = "{username}"')
    db_password = c.fetchone()

    # Assigning the results to a variable and converting the data from a tuple to a string
    db_username = ''.join(db_username)
    db_password = ''.join(db_password)

    # If statement to determine if they got the correct username and password
    if username == db_username.lower() and password == db_password:
        print("\nYou are logged in!")

    else:
        print("\nSomething is wrong with the credentials, please try again")

    c.close()
    conn.close()

    

def createNewUser():
    new_username = input("Please enter a new username: ").lower()
    new_password = stdiomask.getpass("Password: ")
    repeat_password = stdiomask.getpass("Repeat password: ")

    while new_password != repeat_password:
        print()
        print("Passwords did not match")
        new_password = stdiomask.getpass("Password: ")
        repeat_password = stdiomask.getpass("Repeat password: ")

    c.execute(f'INSERT INTO usernameAndPasswords VALUES("{new_username}", "{new_password}")')
    print() # Empty print statment for spacing
    print("Saving user name and password to the database.")
    conn.commit()
    c.close()
    conn.close()


main()