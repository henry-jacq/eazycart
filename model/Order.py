from model.Database import Database
from datetime import datetime

class Order:
    def __init__(self):
        self.db = Database()
        self.table1 = 'orders'
        self.table2 = 'order_items'
        
    def create_order(self, customer_id, status, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        sql = f"INSERT INTO orders VALUES (ORDER_SEQ.NEXTVAL, {customer_id}, TO_DATE('{date}', 'YYYY-MM-DD'), '{status}', {amount})"
        query = self.db.exec_raw(sql)
        self.db.commit()      
        return query

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