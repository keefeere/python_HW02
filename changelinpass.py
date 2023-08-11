#!/usr/bin/env python3

# Linux strong password generator and changer by KeeFeeRe(c)2023

import platform
import os
import getpass
import subprocess
import string
import random

# Define the minimum and maximum password length
def_length = 8

# Define global variables with the possible characters for the password using the string module
# https://docs.python.org/3/library/string.html
uppercase_letters = string.ascii_uppercase
lowercase_letters = string.ascii_lowercase
numbers = string.digits
special_characters = string.punctuation


class NewPassword:
    """
    Class for generating a new password or validating the one entered by the user
    """

    def generate_password(self, length):
        # Initialize an empty password
        password = ""

        # Loop until the password is valid
        while not self.check_password_requirements(password, length):
            # Reset the password to an empty string
            password = ""
            # Generate a random password of the desired length using the string module's join method
            password = "".join(
                random.choices(uppercase_letters + lowercase_letters + numbers + special_characters, k=length))
        return password

    def check_password_requirements(self, password, length):
        # Define the minimum length requirement
        if len(password) < length:
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
    def change_password(self, username, password):
        """
        Sets the user's password using the 'chpasswd' command with sudo privileges.
        """
        command = ['sudo', 'chpasswd']
        input_string = f"{username}:{password}"

        # Run the command with input string
        subprocess.run(command, input=input_string, text=True)

        # Save the password to a file
        with open("password.txt", "w") as file:
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}")

        print("\nThe password was successfully set and saved in the password.txt file.\n")
        return True


class UserInputValidator:
    def validate_username(self, username):
        command = f"id -u {username} >/dev/null 2>&1"
        return subprocess.call(command, shell=True) == 0


def main():
    try:
        if not (platform.system() == "Linux"):
            print(f"Detected platform is {platform.system()}. This program runs only on Linux platform. Sorry")
            return

        max_attempts = 3

        # Prompt the user to enter a username
        username = input("Welcome to secure password change application!\nEnter the username: ")
        if not username:
            print("You entered an empty value. Please enter a username.")
            return

        # Check if the user exists in the system
        if not UserInputValidator().validate_username(username):
            print(f"User '{username}' does not exist. Please, check the data and try again.")
            return

        # Check whether we change pass for self or other user
        if not getpass.getuser() == username:
            # If not for self than check if the program is running with administrative privileges
            if not check_admin_privileges():
                print(
                    "To change other user's password this program needs to be run with administrative privileges.\nPlease restart program with admin privileges")
                return

        for attempt in range(1, max_attempts + 1):
            # Prompt the user to enter a password or generate a new one
            password = getpass.getpass("\nEnter a new password\n"
                                       "Password should meet secure requirements:\n"
                                       f"    - at least {def_length} characters long\n"
                                       f"    - at least one uppercase letter of {uppercase_letters}\n"
                                       f"    - at least one lowercase letter of {lowercase_letters}\n"
                                       f"    - at least one number of numbers {numbers}\n"
                                       f"    - at least one special character of {special_characters}\n"
                                       "    or leave blank to generate one: ")
            if not password:
                password = NewPassword().generate_password(def_length)

            # Check if the password meets the requirements
            if not NewPassword().check_password_requirements(password, def_length):
                print("\nThe password does not meet the requirements. Please try again!\n")
            else:
                break
        else:
            print(f"You entered an incorrect password {max_attempts} times. Please check the input and try again!")
            return

        # Change the password for the user
        password_changer = PasswordChanger()
        if password_changer.change_password(username, password):
            print(f"Username: {username}")
            print(f"Password: {password}")
            print("Meets requirements: Yes")

    # exit if KeyboardInterrupt  (Ctrl+C is pressed)
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")
        exit(1)


def check_admin_privileges():
    return os.geteuid() == 0


if __name__ == "__main__":
    main()
