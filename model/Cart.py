from model.Database import Database

class Cart:
    def __init__(self):
        self.db = Database()
        self.table1 = 'shopping_cart'
        self.table2 = 'cart_items'

    def get_items_by_cart_id(self, cart_id):
        result = self.db.select(self.table2, "*", f"cart_id = {cart_id}", fetchAll=True)
        new_list = []
        for i in result:
            new_list.append(list(i))
        return new_list
    
    # Item exists in cart
    def item_exists(self, cart_id, product_id):
        result = self.db.select(self.table2, "*", f"cart_id = {cart_id} AND product_id = {product_id}")
        if result is not None:
            return True
        return False
    
    # Add item to cart
    def add_item(self, cart_id, product_id, quantity):
        if self.item_exists(cart_id, product_id) == False:
            self.db.insert(self.table2, [cart_id, product_id, quantity], sequence="cart_item_seq.NEXTVAL")
            return True
        return False

    def remove_item(self, cart_id, product_id):
        if self.item_exists(cart_id, product_id) == True:
            result = self.db.delete(self.table2, f"cart_id = {cart_id} AND product_id = {product_id}")
            return result
        return False

    # Change quantity of item
    def change_qty(self, cart_id, cart_data):
        for item in cart_data:
            quantity = item["qty"]
            product_id = item["product_id"]
            if self.item_exists(cart_id, product_id) != False:
                result = self.db.update(self.table2, {'quantity': quantity}, f"cart_id = {cart_id} AND product_id = {product_id}")
                if result is not False:
                    continue
                else:
                    return False
            return False
        return True

    def create_cart(self, customer_id):
        if self.cart_exists(customer_id) != True:
            result = self.db.insert(self.table1, [customer_id], sequence="cart_seq.NEXTVAL")
            return result
        return False

    def cart_exists(self, customer_id):
        result = self.db.select(self.table1, "*", f"customer_id = {customer_id}")
        if result is not None:
            return True
        return False

    def get_cart_id(self, customer_id):
        result = self.db.select(self.table1, ['cart_id'], f"customer_id = {customer_id}")
        if result is not None:
            return result[0]
        return False