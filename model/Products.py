from model.Database import Database

class Products:
    def __init__(self):
        self.db = Database()
        self.table = 'products'

    def get_products(self):
        fields = ["*"]
        result = self.db.select(self.table, fields, fetch_all=True)
        return [list(row) for row in result] if result else []

    def get_products_by_id(self, product_id):
        fields = ["*"]
        condition = "product_id = :1"
        bind_variables = [product_id]
        result = self.db.select(self.table, fields, condition, bind_variables, fetch_all=True)
        return [list(row) for row in result][0] if result else None

    def get_product_qty(self, product_id):
        fields = ["stock_quantity"]
        condition = "product_id = :1"
        bind_variables = [product_id]
        result = self.db.select(self.table, fields, condition, bind_variables)
        return result[0][0] if result else None

    def add_product(self, name, description, quantity, price):
        data = {"name": name, "description": description, "quantity": quantity, "price": price}
        if not self.product_exists(name):
            result = self.db.insert(self.table, data)
            return result
        return False

    def product_exists(self, name):
        fields = ["*"]
        condition = "name = :1"
        bind_variables = [name]
        result = self.db.select(self.table, fields, condition, bind_variables)
        return result is not None
