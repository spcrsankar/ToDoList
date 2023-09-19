import re

def is_valid_email(email):
    pattern = r'^\S+@\S+\.\S+$'
    return bool(re.match(pattern, email))

def signup_validation(user_name, password, email):
    print('validation.py')
    if(len(user_name) < 6 or len(password) < 6):
        return "minimum length of username and password is 6"
    if(is_valid_email(email) == False):
        return "invalid email"
    return "Ok"

def login_validation(email, password):
    if(is_valid_email(email) == False or len(password) < 6):
        return "Invalid email or password"
    return "Ok"