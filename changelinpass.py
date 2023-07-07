# This is a Python program template for Linux chpasswd simulation

# Import the modules you need
import os
import random
import string


# TODO: Rewrite in OOP Paradigm.
# TODO: Create class for external call
# TODO: Create class for password
# TODO: Create class for user input?



# Define the main function
def main():
    # TODO: Write the main logic of the program here
    # Generated code below, rewrite

    
    # Prompt the user to enter a username
    username = input("Enter a username: ")
    # TODO: check user input for meets linux user naming criterias?

    # Check if user exist in system
    # Dunno if proposed method is legal?
    if os.path.exists(f"/home/{username}"):
        # User exists, proceed to password change
        print(f"User {username} found.")
        change_password(username)
    else:
        # User does not exist, print an error message and exit
        print(f"User {username} does not exist.")
        exit()

# Define the change_password function
def change_password(username):
    # TODO: Write the code for changing password here
    # Generated code below, rewrite


    # Ask the user to input a password or generate a new one if not provided
    password = input("Enter a password or press enter to generate one: ")
    if not password:
        # No password provided, generate a random one
        password = generate_password()
        print(f"Generated password: {password}")

    # Check the password against specified requirements
    requirements = check_password(password)

    # Change password for user using os.system command
    os.system(f"echo '{username}:{password}' | sudo chpasswd")

    # Print the results, including the username, the original or generated password, and whether the password meets the requirements
    print(f"Password changed for user {username}.")
    print(f"Password: {password}")
    print(f"Password meets requirements: {requirements}")

# Define the generate_password function
def generate_password():
    # TODO: Write the code for generating a random password here
    # We can reuse code from prewious work

    # Set the minimum length and the character types for the password
    # Moove to definitions of constants 
    min_length = 8
    char_types = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]

    # Initialize an empty password and a list of random indices
    password = ""
    indices = []


    # Generated code below, rewrite
    # Loop until the password meets the minimum length
    while len(password) < min_length:
        # Choose a random character type and a random character from it
        char_type = random.choice(char_types)
        char = random.choice(char_type)

        # Append the character to the password and its index to the indices list
        password += char
        indices.append(char_types.index(char_type))

    # Shuffle the password to avoid patterns
    password = "".join(random.sample(password, len(password)))

    # Check if the password contains at least one character from each type
    if len(set(indices)) == len(char_types):
        # Password is valid, return it
        return password
    else:
        # Password is invalid, generate a new one recursively
        return generate_password()

# Define the check_password function
def check_password(password):
    # TODO: Write the code for checking the password against specified requirements here
    # This fuction may be used for checking own and generated passwords

    # Generated code below, rewrite
    # Set the minimum length and the character types for the password
    min_length = 8
    char_types = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]

    # Initialize a boolean variable to store the result and a list of counts for each character type
    result = True
    counts = [0] * len(char_types)

    # Loop through each character in the password
    for char in password:
        # Find its character type and increment its count in the list
        for i, char_type in enumerate(char_types):
            if char in char_type:
                counts[i] += 1

    # Check if the password meets the minimum length requirement
    if len(password) < min_length:
        # Password is too short, set result to False and print a message
        result = False
        print(f"Password is too short. Minimum length is {min_length}.")

    # Check if the password contains at least one character from each type
    for i, count in enumerate(counts):
        if count == 0:
            # Password is missing a character type, set result to False and print a message
            result = False
            print(f"Password is missing {char_types[i][0]} characters.")

    # Return the result as a boolean value
    return result

# Call the main function
if __name__ == "__main__":
    main()
