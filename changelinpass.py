#!/usr/bin/env python3


##Linux strong password generator and changer y KeeFeeRe(c)2023

import os
import getpass
import subprocess
import string
import random
from sys import platform  # for detecting os platform

# Define global variables with the possible characters for the password using the string module
# https://docs.python.org/3/library/string.html
uppercase_letters = string.ascii_uppercase
lowercase_letters = string.ascii_lowercase
numbers = string.digits
special_characters = string.punctuation

# Define the minimum and maximum password length
def_length = 8


class NewPassword:
    """
    Class for generating new password or validate the one that was entered by user
    """

    def generate_password(self, lenght):
        # Initialize an empty password
        password = ""

        # Loop until the password is valid
        while not NewPassword().check_password_requirements(password, lenght):
            # Reset the password to empty string
            password = ""
            # Generate a random password of the desired length using the string module's join method 
            # https://www.w3schools.com/python/ref_random_choices.asp
            password = "".join(
                random.choices(uppercase_letters + lowercase_letters + numbers + special_characters, k=lenght))
        return password

    def check_password_requirements(self, password, lenght):
        # Define the minimum length requirement
        if len(password) < lenght:
            return False

        # Check for the presence of different character types
        # https://stackoverflow.com/questions/39356688/python-2-7-if-not-any-syntax
        # Check if the password contains at least one uppercase letter
        if not any(char in uppercase_letters for char in password):
            return False
        # Check if the password contains at least one lowercase letter
        if not any(char in lowercase_letters for char in password):
            return False
        # Check if the password contains at least one number
        if not any(char in numbers for char in password):
            return False
        # Check if the password contains at least one special character
        if not any(char in special_characters for char in password):
            return False
        # If all the checks pass, return True
        return True


class PasswordChanger:
    def set_password(self):
        """
        Sets the user's password using the 'chpasswd' command with sudo privileges.
        """
        command = ['sudo', 'chpasswd']
        input_string = f"{self.username}:{self.password}"

        # Run the command with input string
        subprocess.run(command, input=input_string, text=True)

        # Save the password to a file
        with open("password.txt", "w") as file:
            file.write(f"Username: {self.username}\n")
            file.write(f"Password: {self.password}")

        print("The password was successfully set and saved in the password.txt file")







class UserInputValidator:
    def validate_username(self, username):
        command = f"id -u {username} >/dev/null 2>&1"
        return subprocess.call(command, shell=True) == 0


def main():
    if not (platform == "linux" or platform == "linux2"):
        print("Detected platform is", platform, "\nThis program runs only on Linux platform. Sorry")
        return

    # Check if the program is running with administrative privileges
    if not check_admin_privileges():
        print("This program needs to be run with administrative privileges.")
        return

    # Prompt the user to enter a username
    ##TODO: cycle if empty responce, exit if KeyboardInterrupt
    username = input("Enter the username: ")

    # Check if the user exists in the system
    if not UserInputValidator().validate_username(username):
        print(f"User '{username}' does not exist.")
        return

    # Prompt the user to enter a password or generate a new one
    ##TODO: exit if KeyboardInterrupt
    password = getpass.getpass("Enter a new password (leave blank to generate one): ")
    if not password:
        password = NewPassword().generate_password(def_length)

    # Check if the password meets the requirements
    ##TODO: cycle if does not meet
    if not NewPassword().check_password_requirements(password, def_length):
        print("The password does not meet the requirements.")
        return

    # Change the password for the user
    password_changer = PasswordChanger()
    if password_changer.change_password(username, password):
        print("Password changed successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("Meets requirements: Yes")
    else:
        print("An error occurred while changing the password.")


def check_admin_privileges():
    return os.geteuid() == 0


if __name__ == "__main__":
    main()
