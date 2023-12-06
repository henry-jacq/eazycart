import cx_Oracle
from config.helper import get_db_credentials

class Database:
    def __init__(self):
        cred = get_db_credentials()
        self.conn = self.__make_conn(
            cred.get('username'), 
            cred.get('password'), 
            cred.get('host'), 
            cred.get('port'), 
            cred.get('service')
        )
        self.cursor = self.conn.cursor()

    def __make_conn(self, username, password, host, port, service):
        dsn = cx_Oracle.makedsn(host, port, service_name=service)
        connection = cx_Oracle.connect(username, password, dsn)
        return connection

    def get_conn(self):
        return self.conn
    
    def get_cursor(self):
        return self.cursor
    
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()
    
    def commit(self):
        return True if self.conn.commit() == None else False

    def close_conn(self):
        try:
            self.cursor.close()
            self.conn.close()
            return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error closing connection: {e}")
            return False
    
    def select(self, table, fields, condition=None, fetchAll=False):
        field_str = ", ".join(fields)
        query = f"SELECT {field_str} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query)
        return self.fetch_one() if fetchAll == False else self.fetch_all()

    def insert(self, table, values, sequence=None):
        formatted_values = [f"'{value}'" if isinstance(value, str) else str(value) for value in values]
        value_str = ", ".join(formatted_values)

        if sequence is None:
            query = f"INSERT INTO {table} VALUES ({value_str})"
        else:
            query = f"INSERT INTO {table} VALUES ({sequence}, {value_str})"
        
        try:
            self.execute_query(query)
            return self.commit()
        except Exception as e:
            print(e) and exit(1)
        
    def update(self, table, set_values, condition):
        set_str = ", ".join(f"{key} = {value}" for key, value in set_values.items())
        query = f"UPDATE {table} SET {set_str} WHERE {condition}"
        self.execute_query(query)

    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)
        
    def __del__(self):
        self.close_conn()

