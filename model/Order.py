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
        order_data = self.get_order(order_id)
        order_data[2] = order_data[2].strftime("%b %d, %Y")
        return order_data

    def get_order(self, order_id: int):
        data = self.db.select(self.table1, ['*'], f"order_id = :1", [order_id])
        return list(data)
    
    def get_customer_orders(self, customer_id: int):
        data = self.db.select(self.table1, ['*'], f"customer_id = :1", [customer_id], fetch_all=True)
        if data is not None:
            orders = []
            for i in data:
                i = list(i)
                i[2] = i[2].strftime('%d/%m/%Y')
                orders.append(i)
            return orders
        return False

    def remove_order(self, order_id: int):
        result = self.db.delete(self.table1, f"order_id = {order_id}")
        if result is not None:
            return True
        return False

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
