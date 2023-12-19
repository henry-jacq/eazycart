from model.Database import Database

from model.Database import Database

class Wishlist:
    def __init__(self):
        self.db = Database()
        self.table1 = 'wishlists'
        self.table2 = 'wishlists_items'

    def get_wishlist_items_by_wid(self, wishlist_id):
        result = self.db.select(self.table2, ["*"], "wishlist_id = :1", bind_variables=[wishlist_id], fetch_all=True)
        new_list = [list(i) for i in result]
        return new_list
    
    def item_exists(self, wishlist_id, product_id):
        condition = "wishlist_id = :1 AND product_id = :2"
        bind_variables = [wishlist_id, product_id]
        result = self.db.select(self.table2, ["*"], condition, bind_variables)
        return result is not None
    
    def add_item(self, w_id, product_id):
        if not self.item_exists(w_id, product_id):
            data = {"wishlist_id": w_id, "product_id": product_id}
            self.db.insert(self.table2, data)
            return True
        return False

    def remove_item(self, wishlist_id, product_id):
        condition = "wishlist_id = :1 AND product_id = :2"
        bind_variables = [wishlist_id, product_id]
        if self.item_exists(wishlist_id, product_id):
            result = self.db.delete(self.table2, condition, bind_variables)
            return result
        return False

    def create_wishlist(self, customer_id):
        if not self.wishlist_exists(customer_id):
            data = {"customer_id": customer_id}
            result = self.db.insert(self.table1, data)
            return result
        return False

    def wishlist_exists(self, customer_id):
        condition = "customer_id = :1"
        bind_variables = [customer_id]
        result = self.db.select(self.table1, ["*"], condition, bind_variables)
        return result is not None

    def get_wishlist_id(self, customer_id):
        condition = "customer_id = :1"
        bind_variables = [customer_id]
        result = self.db.select(self.table1, ["wishlist_id"], condition, bind_variables)
        return result[0] if result else False
