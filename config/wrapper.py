from model.Auth import Auth

# This contains wrapper functions for models

def validate_credentials(email, password):
    a = Auth()
    return a.login(email, password)

def create_customer(fname, lname, email, password):
    a = Auth()
    result = a.create_user(fname, lname, email, password)
    if result is not False:
        return result
    return False