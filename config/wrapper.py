from model.Auth import Auth
from model.Products import Products
from model.Cart import Cart
from model.Order import Order
from model.Wishlist import Wishlist
from datetime import datetime

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

def product_in_cart(customer_id: int):
    new_list = []
    for _ in get_cart_list(customer_id):
        new_list.append(_[2])
    return new_list

def get_cart_list(customer_id: int):
    c = Cart()
    res = c.get_items_by_cart_id(c.get_cart_id(customer_id))
    return res

def getOrderSummary(customer_id: int):
    cartList = get_cart_list(customer_id)
    products = get_cart_items_info(customer_id)
    total_price = 0
    for item in cartList:
        for p in products:
            if item[2] == p[0]:
                # Product price with no of quantity
                total_price += p[2] * item[3]
                
    return total_price

def get_cart_items_info(customer_id: int):
    pids = product_in_cart(customer_id)
    p = Products()
    products_list = []
    
    for pid in pids:
        products_list.append(p.get_products_by_id(pid))    

    return products_list
    
def update_cart_items(customer_id, cart_data):
    c = Cart()
    cart_id = c.get_cart_id(customer_id)
    return c.change_qty(cart_id, cart_data)

def create_order(customer_id: int):
    o = Order()
    return o.create_order(
        customer_id, 'Pending', getOrderSummary(customer_id)
    )

def remove_order(data):
    o = Order()
    order_id = data['order_id']
    return o.remove_order(order_id)

def get_customer_orders(customer_id: int):
    o = Order()
    return o.get_customer_orders(customer_id)

def add_to_wishlist(customer_id: int, product_id: int):
    w = Wishlist()
    if not w.wishlist_exists(customer_id):
        w.create_wishlist(customer_id)
    res = w.add_item(w.get_wishlist_id(customer_id), product_id)
    return res

def remove_from_wishlist(customer_id: int, product_id: int):
    w = Wishlist()
    if w.wishlist_exists(customer_id):
        return w.remove_item(w.get_wishlist_id(customer_id), product_id)
    return False

def get_wishlist_items(customer_id: int):
    w = Wishlist()
    res = w.get_wishlist_items_by_wid(w.get_wishlist_id(customer_id))
    return res

def product_in_wishlist(customer_id: int):
    new_list = []
    for _ in get_wishlist_items(customer_id):
        new_list.append(_[2])
    return new_list

def get_wishlist_items_info(customer_id: int):
    pids = product_in_wishlist(customer_id)
    p = Products()
    products_list = []
    
    for pid in pids:
        products_list.append(p.get_products_by_id(pid))    

    return products_list