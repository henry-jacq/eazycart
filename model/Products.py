from model.Database import Database

class Products:
    def __init__(self):
        self.db = Database()
        self.table = 'products'

    def get_products(self):
        result = self.db.select(self.table, "*", fetchAll=True)
        new_list = []
        for i in result:
            new_list.append(list(i))
        return new_list
    
    def get_products_by_id(self, product_id):
        result = self.db.select(self.table, "*", f"product_id = {product_id}",fetchAll=True)
        new_list = []
        for i in result:
            new_list.append(list(i))
        return new_list[0]
    
    def get_product_qty(self, product_id):
        result = self.db.select(self.table, "stock_quantity", f"product_id = {product_id}")
        if result is not None:
            return result
        return False

    def add_product(self, name, description, quantity, price):
        if not self.product_exists(name):
            result = self.db.insert(self.table, [name, price, quantity, description], sequence="product_seq.NEXTVAL")
            return result
        return False

    def product_exists(self, name):
        result = self.db.select(self.table, "*", f"name = '{name}'")
        if result is not None:
            return True
        return False
