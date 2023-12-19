from model.Database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        self.table = 'customers'
    
    def create_user(self, fname, lname, email, password):
        data = {
            "first_name": fname, "last_name": lname, "email": email, "password": password
        }
        if not self.mail_exists(email):
            result = self.db.insert(self.table, data)
            return result
        return False
        
    def login(self, email, password):
        fields = ["*"]
        condition = "email = :1 AND password = :2"
        bind_variables = [email, password]
        result = self.db.select(self.table, fields, condition, bind_variables)
        print(result)
        if result and result[3] == email and result[4] == password:
            return result
        return False
    
    def mail_exists(self, email):
        fields = ["*"]
        condition = "email = :1"
        bind_variables = [email]
        result = self.db.select(self.table, fields, condition, bind_variables)
        return result is not None
