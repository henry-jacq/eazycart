from model.Auth import Auth
from model.Products import Products

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

def get_products():
    p = Products()
    return p.get_products()