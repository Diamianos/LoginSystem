# Login system
# https://pythonprogramming.net/sql-database-python-part-1-inserting-database/
# === Steps for operation ===

# 1. Ask user if they want to login or create an account
# 2. Based on the input either ask them for user name and password and write that to a file
# 3. if login, ask for user name and password and then compare that with the information in the text file.

import stdiomask # Module to hide the characters when typing
import sqlite3

def main():

    conn = sqlite3.connect("Login DB.db") # Setting the conneciton to the database
    c = conn.cursor() # Creating the cursor to manipulate the database

    # Creating the database if it doesnt exist
    c.execute("CREATE TABLE IF NOT EXISTS usernameAndPasswords(username TEXT, password TEXT)")

    print("Welcome to my first login system.\n")
    user_selection = str(input("Please either enter \"1\" to login or \"2\" to create an account: "))

    # Input validation 
    while user_selection != "1" and user_selection != "2":
        user_selection = str(input("Please either enter \"1\" to login or \"2\" to create an account: "))

    # Empty print statment for spacing
    print()

    # If user entered "1" verify their login credentials and log them in
    if user_selection == "1":
        
        # Getting the user input
        username = input("Username: ")
        password = stdiomask.getpass("Password: ")

        # Getting the table based on the user name entered
        c.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{username}"')
        db_username = c.fetchone()

        # Getting the password associated to the username that was entered
        c.execute(f'SELECT password FROM usernameAndPasswords WHERE username = "{username}"')
        db_password = c.fetchone()

        # Assigning the results to a variable and converting the data from a tuple to a string
        db_username = ''.join(db_username)
        db_password = ''.join(db_password)

        # If statement to determine if they got the correct username and password
        if username == db_username and password == db_password:
            print("You are logged in!")

        else:
            print("Something is wrong with the credentials.")

        c.close()
        conn.close()

    # If user enters "2" create a new account, get info and write to a file
    elif user_selection == "2":

        new_username = input("Please enter a new username: ")
        new_password = stdiomask.getpass("Please enter a new password: ")

        c.execute(f'INSERT INTO usernameAndPasswords VALUES("{new_username}", "{new_password}")')
        print() # Empty print statment for spacing
        print("Saving user name and password to the database.")
        conn.commit()
        c.close()
        conn.close()


main()