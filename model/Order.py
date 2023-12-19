from model.Database import Database
from datetime import datetime

class Order:
    def __init__(self):
        self.db = Database()
        self.table1 = 'orders'
        self.table2 = 'order_items'
        
    def create_order(self, customer_id, status, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        order_id = self.db.call_func(
            'createOrder', [customer_id, date, status, amount]
        )
        order_data = self.db.select(self.table1, ['*'], f"order_id = :1", [order_id])
        order_data = list(order_data)
        order_data[2] = order_data[2].strftime("%b %d, %Y")
        return order_data

    def order_exists(self, customer_id):
        result = self.db.select(self.table1, "*", f"customer_id = {customer_id}")
        if result is not None:
            return True
        return False

    def get_order_id(self, customer_id, fetchModeAll=False):
        result = self.db.select(self.table1, ['order_id'], f"customer_id = {customer_id}", fetchAll=fetchModeAll)
        if result is not None:
            return result[0]
        return False
    
    # Add item to order items
    def add_item(self, order_id, product_id, quantity, unit_price):
        result = self.db.insert(self.table2, [order_id, product_id, quantity, unit_price], sequence="ORDER_ITEM_SEQ.NEXTVAL")
        if result:
            return True
        return False