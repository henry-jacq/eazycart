from model.Database import Database

from model.Database import Database

class Cart:
    def __init__(self):
        self.db = Database()
        self.table1 = 'shopping_cart'
        self.table2 = 'cart_items'

    def get_items_by_cart_id(self, cart_id):
        result = self.db.select(self.table2, ["*"], "cart_id = :1", bind_variables=[cart_id], fetch_all=True)
        new_list = [list(i) for i in result]
        return new_list
    
    def item_exists(self, cart_id, product_id):
        condition = "cart_id = :1 AND product_id = :2"
        bind_variables = [cart_id, product_id]
        result = self.db.select(self.table2, ["*"], condition, bind_variables)
        return result is not None
    
    def add_item(self, cart_id, product_id, quantity):
        if not self.item_exists(cart_id, product_id):
            data = {"cart_id": cart_id, "product_id": product_id, "quantity": quantity}
            self.db.insert(self.table2, data)
            return True
        return False

    def remove_item(self, cart_id, product_id):
        condition = "cart_id = :1 AND product_id = :2"
        bind_variables = [cart_id, product_id]
        if self.item_exists(cart_id, product_id):
            result = self.db.delete(self.table2, condition, bind_variables)
            return result
        return False

    def change_qty(self, cart_id, cart_data):
        for item in cart_data:
            quantity = item["qty"]
            product_id = item["product_id"]
            condition = "cart_id = :1 AND product_id = :2"
            bind_variables = [cart_id, product_id]
            if self.item_exists(cart_id, product_id):
                result = self.db.update(self.table2, {"quantity": quantity}, condition, bind_variables)
                if not result:
                    return False
            else:
                return False
        return True

    def create_cart(self, customer_id):
        if not self.cart_exists(customer_id):
            data = {"customer_id": customer_id}
            result = self.db.insert(self.table1, data)
            return result
        return False

    def cart_exists(self, customer_id):
        condition = "customer_id = :1"
        bind_variables = [customer_id]
        result = self.db.select(self.table1, ["*"], condition, bind_variables)
        return result is not None

    def get_cart_id(self, customer_id):
        condition = "customer_id = :1"
        bind_variables = [customer_id]
        result = self.db.select(self.table1, ["cart_id"], condition, bind_variables)
        return result[0] if result else False
