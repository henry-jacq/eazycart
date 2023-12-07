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
