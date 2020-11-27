# Login system

# Tutorials
# https://pythonprogramming.net/sql-database-python-part-1-inserting-database/
# https://www.pythoncentral.io/introduction-to-sqlite-in-python/


import stdiomask # Module to hide the characters when typing
import sqlite3

#Constants
DATABASE_FILE = "Login DB.db"
LOGIN = 1
CREATE_ACCOUNT = 2
FORGOT_PWD = 3
DEL_ACT = 4

YES = 1
NO = 2

QUIT = 'Q'

# Creating connection to the database
CONN = sqlite3.connect(DATABASE_FILE) # Setting the conneciton to the database
C = CONN.cursor() # Creating the cursor to manipulate the database

def main():

    # Creating the table if it doesnt exist
    C.execute("CREATE TABLE IF NOT EXISTS usernameAndPasswords(\
               username TEXT,\
               password TEXT,\
               email TEXT,\
               question1 TEXT,\
               answer1 TEXT,\
               question2 TEXT,\
               answer2 TEXT)")

    print("Welcome to my first login system.\n")
    # Starting program loop
    while True:
    # Printing out the menu
        print(f"Enter '{QUIT}' at any time to exit the program.\n")
        print("===== Please make a selection =====")
        print("1) Login")
        print("2) Create an account")
        print("3) Forgot password")
        print("4) Delete account (N/A)")
        print("-----------------------")

        user_selection = str(input("Your selection: ")) # Getting user selection
        if user_selection.upper() == QUIT:
            close_program()

        # Input validation 
        while validateInput(user_selection) == False or int(user_selection) < LOGIN or int(user_selection) > FORGOT_PWD:
            print("Please enter a valid selection.")
            user_selection = str(input("Your selection: "))
            if user_selection.upper() == QUIT:
                close_program()

        user_selection = int(user_selection) # Converting user_selection to an integer
        print()
        
        # Acting program based on selection
        if user_selection == LOGIN:
            login()
        elif user_selection == CREATE_ACCOUNT:
            create_account()
        elif user_selection == FORGOT_PWD:
            forgot_pwd()
    
    # Closing the connection to the database
    C.close()
    CONN.close()


def login():
        
        # Getting the user input
        username = input("Username: ").lower()
        if username.upper() == QUIT:
            close_program()
        password = stdiomask.getpass("Password: ")
        if password.upper() == QUIT:
            close_program()

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
                close_program()

            else:
                print("Username or password is not correct.\n")
        except TypeError:
            print("Username not found, please try again.\n")
        except Exception:
            print("Unknown error occcured.\n")


def create_account():

        new_username = input("Please enter a new username: ").lower()
        if new_username.upper() == QUIT:
            close_program()

        try:  # trying to get the username in the database based on the user input
            C.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{new_username}"')
            test_username = C.fetchone() # Getting the results of the cursor and assigning it to a variable
            test_username = ''.join(test_username) # converting the results from a tuple to a string
            if new_username == test_username:
                print("Username already exists, please login or choose forgot password.\n")
                
        except TypeError: # except clause incase username is not found
            while True:
                new_password = stdiomask.getpass("Please enter a new password: ")
                if new_password.upper() == QUIT:
                    close_program()

                conf_password = stdiomask.getpass("Repeat the password: ")
                if conf_password.upper() == QUIT:
                    close_program()

                if new_password == conf_password:
                    break
                print("Passwords did not match, please try again.\n")

            # Getting the account info from the user
            email = input("Email: ")
            if email.upper() == QUIT:
                close_program()

            print("\nSecurity question 1:")
            question1 = "What is your mother's madien name?"
            answer1 = input(question1 + ' ').lower()
            if answer1.upper() == QUIT:
                close_program()

            print("\nSecurity question 2:")
            question2 = "What city were you born?"
            answer2 = input(question2 + ' ').lower()
            if answer2.upper() == QUIT:
                close_program()
            
            # Importing the data into the database
            C.execute(f'INSERT INTO usernameAndPasswords VALUES("{new_username}", "{new_password}", "{email}", "{question1}", "{answer1}", "{question2}", "{answer2}")')
            print() # Empty print statment for spacing
            print("Saving user account information to the database.\n")

        # Committing the change
        CONN.commit()


def forgot_pwd():
    # Asking if they know their username
    print("Do you know your username?\n1) Yes\n2) No")
    print("--------------------------")

    # Input validation and seeing if they need to quit the program
    know_username = input("Your selection: ")
    if know_username.upper() == QUIT:
        close_program()
    while validateInput(know_username) == False or int(know_username) < YES or int(know_username) > NO:
            print("Please enter a valid selection.")
            user_selection = str(input("Your selection: "))
            if user_selection.upper() == QUIT:
                close_program()
    
    # Converting input to an integer for the selection below
    know_username = int(know_username)
    
    # Empty variable to hold the username based on the if / elif statements below
    username = ''
    
    # If the user knows their username....
    if know_username == YES:
        uk_username = input("What is your username? ").lower()  # "Unknown user name" variable from input

        # trying to get the username in the database based on the user input
        try:  
            C.execute(f'SELECT username FROM usernameAndPasswords WHERE username = "{uk_username}"')
            test_username = C.fetchone() # Getting the results of the cursor and assigning it to a variable
            test_username = ''.join(test_username) # converting the results from a tuple to a string
            if uk_username == test_username:

                print("We found a matching username\n")
                username = uk_username
        except Exception:
            print ("We were not able to find the specified username, please try again.")
            close_program()

    # If the user DOES NOT know their username...
    elif know_username == NO:
        email = input("What is the email associated to this email? ")

        # Testing to see if the email is in the database.
        try:  
            C.execute(f'SELECT email FROM usernameAndPasswords WHERE email = "{email}"')
            test_email = C.fetchone() # Getting the results of the cursor and assigning it to a variable
            test_email = ''.join(test_email) # converting the results from a tuple to a string
            if email == test_email: # if user email and db email matches..
                print("We found a username associated to that email.\n")
                C.execute(f'SELECT username FROM usernameAndPasswords WHERE email = "{email}"') # Getting the username associated to the email
                db_username = C.fetchone()
                db_username = ''.join(db_username) # Converting it to the string format from the db
                print(f"This is your username: {db_username}")  # Printing off the username to the host
                username = db_username # assigning the db username to the empty username variable above

        except Exception:
            print ("Specified email was not found in the system.")
            close_program()

    # Getting the security questions and answers from the database
    C.execute(f'SELECT question1 FROM usernameAndPasswords WHERE username = "{username}"') 
    question1 = C.fetchone()
    question1 = ''.join(question1)
    C.execute(f'SELECT answer1 FROM usernameAndPasswords WHERE username = "{username}"') 
    answer1 = C.fetchone()
    answer1 = ''.join(answer1)

    C.execute(f'SELECT question2 FROM usernameAndPasswords WHERE username = "{username}"') 
    question2 = C.fetchone()
    question2 = ''.join(question2)
    C.execute(f'SELECT answer2 FROM usernameAndPasswords WHERE username = "{username}"') 
    answer2 = C.fetchone()
    answer2 = ''.join(answer2)
    
    user_answer1 = input(f"{question1} ").lower()
    user_answer2 = input(f"{question2} ").lower()   

    # If the user got the security questions correct
    if answer1 == user_answer1 and answer2 == user_answer2:
        new_password = input("Please enter a new password: ")
        conf_password = input("Confirm the new password: ")
        while new_password != conf_password:
            print("Passwords did not match.")
            new_password = input("Please enter a new password: ")
            conf_password = input("Confirm the new password: ")
        C.execute(f'UPDATE usernameAndPasswords SET password = "{new_password}" WHERE username = "{username}"')
        print("Password has been updated!\n")
        CONN.commit()

    # If they did not get the security questions correct
    else: 
        print("Sorry, the security questions were incorrect, please try again")
        

def validateInput(value):

    if value.isdigit() == True:
        return True
    else:
        return False
    # End of function
    
def close_program():
    C.close()
    CONN.close()
    exit()



main()