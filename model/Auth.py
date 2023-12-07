from model.Database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        self.table = 'customers'
    
    def create_user(self, fname, lname, email, password):
        if self.mail_exists(email) == False:
            result = self.db.insert(self.table, [fname, lname, email, password], sequence="auth_seq.NEXTVAL")
            return result
        return False
        
    def login(self, email, password):
        result = self.db.select(self.table, "*", f"email = '{email}' AND password = '{password}'")
        if result is not None and result[3] == email and result[4] == password:
            return result
        return False
    
    def mail_exists(self, email):
        result = self.db.select(self.table, "*", f"email = '{email}'")
        if result is not None and result[3] == email:
            return True
        return False
    
        
        