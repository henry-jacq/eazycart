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

    def execute_query(self, query, bind_variables=None):
        try:
            if bind_variables:
                self.cursor.execute(query, bind_variables)
            else:
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
        try:
            self.conn.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error committing transaction: {e}")
            return False

    def rollback(self):
        try:
            self.conn.rollback()
            return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error rolling back transaction: {e}")
            return False

    def select(self, table, fields="*", condition=None, bind_variables=None, fetch_all=False):
        try:
            field_str = ", ".join(fields)
            query = f"SELECT {field_str} FROM {table}"
            if condition:
                query += f" WHERE {condition}"

            self.execute_query(query, bind_variables)

            if fetch_all:
                return self.fetch_all()
            else:
                return self.fetch_one()

        except cx_Oracle.DatabaseError as e:
            print(f"Error in SELECT query: {e}")
            return None

    def insert(self, table, data):
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join([':' + str(i + 1) for i in range(len(values))])

        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        if self.execute_query(query, values):
            return self.commit()
        return False

    def update(self, table, set_values, condition, condition_values=None):
        set_str = ', '.join([f"{key} = :{i + 1}" for i, (key, _) in enumerate(set_values.items())])
        query = f"UPDATE {table} SET {set_str} WHERE {condition}"
        
        bind_variables = list(set_values.values())
        if condition_values:
            bind_variables.extend(condition_values)

        if self.execute_query(query, bind_variables):
            return self.commit()
        return False

    def delete(self, table, condition, values=None):
        query = f"DELETE FROM {table} WHERE {condition}"
        bind_variables = values if values else []
        
        if self.execute_query(query, bind_variables):
            return self.commit()
        return False

    def exec_raw(self, query, bind_variables=None):
        return self.execute_query(query, bind_variables)

    def close_conn(self):
        try:
            self.cursor.close()
            self.conn.close()
            return True
        except cx_Oracle.DatabaseError as e:
            print(f"Error closing connection: {e}")
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_conn()
