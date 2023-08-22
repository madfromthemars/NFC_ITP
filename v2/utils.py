import secrets
import string
import random

def generate_Password():
    password = ''
    for i in range(6):
        adder = random.choice((
            string.ascii_lowercase, string.ascii_uppercase, string.digits
        ))
        password += secrets.choice(adder)
    return password

