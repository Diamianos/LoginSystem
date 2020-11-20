# Login system
# https://pythonprogramming.net/sql-database-python-part-1-inserting-database/


import stdiomask # Module to hide the characters when typing
import sqlite3

def main():

    conn = sqlite3.connect("Login DB.db") # Setting the conneciton to the database
    c = conn.cursor() # Creating the cursor to manipulate the database

    # Creating the database if it doesnt exist
    c.execute("CREATE TABLE IF NOT EXISTS usernameAndPasswords(username TEXT, password TEXT, email TEXT, question1 TEXT, question2 TEXT)")

    print("Welcome to my first login system.\n")
    print("===== Please make a selection =====")
    print("1) Login")
    print("2) Create an account")
    print("3) Forgot password (N/A)")
    print("4) Delete account (N/A)\n")
    user_selection = str(input("Your selection: "))

    # Input validation 
    while user_selection != "1" and user_selection != "2":
        print("Please enter a valid selection.")
        user_selection = str(input("Your selection: "))

    # Empty print statment for spacing
    print()

    # If user entered "1" verify their login credentials and log them in
    if user_selection == "1":
        
        # Getting the user input
        username = input("Username: ").lower()
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
            print("Username or password is not correct.")

        c.close()
        conn.close()

    # If user enters "2" create a new account, get info and write to a file
    elif user_selection == "2":

        new_username = input("Please enter a new username: ").lower()

        try:
            c.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{new_username}"')
            test_username = c.fetchone() # Getting the results of the cursor and assigning it to a variable
            test_username = ''.join(test_username) # converting the results from a tuple to a string
            if new_username == test_username:
                print("Username already exists, please login or choose forgot password.")
        except TypeError:
            while True:
                new_password = stdiomask.getpass("Please enter a new password: ")
                conf_password = stdiomask.getpass("Repeat the password: ")
                if new_password == conf_password:
                    break
                print("Passwords did not match, please try again.")

            email = input("Email: ")
            print("\nSecurity question 1:")
            question1 = input("What is your mother's madien name? ").lower()
            print("\nSecurity question 2:")
            question2 = input("What city were you born? ").lower()
            c.execute(f'INSERT INTO usernameAndPasswords VALUES("{new_username}", "{new_password}", "{email}", "{question1}", "{question2}")')
            print() # Empty print statment for spacing
            print("Saving user account information to the database.")

        
        
        conn.commit()
        c.close()
        conn.close()


main()