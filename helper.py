import json

def get_db_credentials():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config.get('database', {})