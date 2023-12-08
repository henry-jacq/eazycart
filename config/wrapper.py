from model.Auth import Auth
from model.Products import Products
from model.Cart import Cart

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

def add_item_to_cart(customer_id: int, product_id: int, product_qty: int):
    c = Cart()
    if not c.cart_exists(customer_id):
        c.create_cart(customer_id)
    res = c.add_item(c.get_cart_id(customer_id), product_id, product_qty)
    return res

def remove_from_cart(customer_id: int, product_id: int):
    c = Cart()
    if c.cart_exists(customer_id):
        return c.remove_item(c.get_cart_id(customer_id), product_id)
    return False