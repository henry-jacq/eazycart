from model.Auth import Auth


auth = Auth()

print(auth.create_user('Henry', 'Jacob', 'henry@gmail.com ', 'mypassword'))
    
# print(auth.login("test@example.com", "test"))

# Example usage:
# db = Database()
# db.select("customers", "*", "first_name = 'John'")
# result = db.fetch_all()
# print(result)

# db.insert("example_table", [1, 'value', 42])
# db.update("example_table", {"column1": 'new_value'}, "column2 = 'value'")
# db.delete("example_table", "column3 = 'value'")

# # Don't forget to close the connection when you are done
# db.close_conn()