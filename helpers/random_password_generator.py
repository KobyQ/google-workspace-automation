import secrets
import string

def genrateRandomPassword():
    # define the allowed password characters i.e. including letters, numbers and special characters
    digits = string.digits
    special_chars = string.punctuation
    letters_uppercase = string.ascii_uppercase
    letters_lowercase = string.ascii_lowercase

    characters = letters_lowercase + letters_uppercase + digits + special_chars

    # set the password length
    pwd_length = 12

    # generate password meeting constraints
    while True:
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(characters))

        if (sum(char in digits for char in pwd)>=1 and
            any(char in special_chars for char in pwd) and 
            sum(char in letters_lowercase for char in pwd)>=1 and
            sum(char in letters_uppercase for char in pwd)>=1):
                break

    return pwd