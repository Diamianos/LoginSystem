# Login system
# https://pythonprogramming.net/sql-database-python-part-1-inserting-database/


import stdiomask # Module to hide the characters when typing
import sqlite3

#Constants
DATABASE_FILE = "Login DB.db"
LOGIN = 1
CREATE_ACCOUNT = 2
FORGOT_PWD = 3
DEL_ACT = 4

# Creating connection to the database
CONN = sqlite3.connect(DATABASE_FILE) # Setting the conneciton to the database
C = CONN.cursor() # Creating the cursor to manipulate the database

def main():

    # Creating the table if it doesnt exist
    C.execute("CREATE TABLE IF NOT EXISTS usernameAndPasswords(username TEXT, password TEXT, email TEXT, question1 TEXT, question2 TEXT)")

    # Printing out the menu
    print("Welcome to my first login system.\n")
    print("===== Please make a selection =====")
    print("1) Login")
    print("2) Create an account")
    print("3) Forgot password (N/A)")
    print("4) Delete account (N/A)\n")

    user_selection = str(input("Your selection: ")) # Getting user selection

    # Input validation 
    while validateInput(user_selection) == False or int(user_selection) < LOGIN or int(user_selection) > CREATE_ACCOUNT:
        print("Please enter a valid selection.")
        user_selection = str(input("Your selection: "))

    user_selection = int(user_selection) # Converting user_selection to an integer
    print()
    
    # Acting program based on selection
    if user_selection == LOGIN:
        login()
    elif user_selection == CREATE_ACCOUNT:
        create_account()
    
    # Closing the connection to the database
    C.close()
    CONN.close()


def login():
        
        # Getting the user input
        username = input("Username: ").lower()
        password = stdiomask.getpass("Password: ")

        # Getting the table based on the user name entered
        C.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{username}"')
        db_username = C.fetchone()

        # Getting the password associated to the username that was entered
        C.execute(f'SELECT password FROM usernameAndPasswords WHERE username = "{username}"')
        db_password = C.fetchone()

        try:
            # Assigning the results to a variable and converting the data from a tuple to a string
            db_username = ''.join(db_username)
            db_password = ''.join(db_password)

            # If statement to determine if they got the correct username and password
            if username == db_username and password == db_password:
                print("You are logged in!")

            else:
                print("Username or password is not correct.")
        except TypeError:
            print("Username not found, please try again.\n")
        except Exception:
            print("Unknown error occcured.\n")


def create_account():

        new_username = input("Please enter a new username: ").lower()

        try:  # trying to get the username in the database based on the user input
            C.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{new_username}"')
            test_username = C.fetchone() # Getting the results of the cursor and assigning it to a variable
            test_username = ''.join(test_username) # converting the results from a tuple to a string
            if new_username == test_username:
                print("Username already exists, please login or choose forgot password.")
                
        except TypeError: # except clause incase username is not found
            while True:
                new_password = stdiomask.getpass("Please enter a new password: ")
                conf_password = stdiomask.getpass("Repeat the password: ")
                if new_password == conf_password:
                    break
                print("Passwords did not match, please try again.")

            # Getting the account info from the user
            email = input("Email: ")
            print("\nSecurity question 1:")
            question1 = input("What is your mother's madien name? ").lower()
            print("\nSecurity question 2:")
            question2 = input("What city were you born? ").lower()
            C.execute(f'INSERT INTO usernameAndPasswords VALUES("{new_username}", "{new_password}", "{email}", "{question1}", "{question2}")')
            print() # Empty print statment for spacing
            print("Saving user account information to the database.")

        # Committing the change
        CONN.commit()


def validateInput(value):
    if value.isdigit() == True:
        return True
    else:
        return False
    # End of function


main()