import re, os
import json, secrets, string

# Path Constants
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.abspath(os.path.join(CONFIG_PATH, '..'))

# Helper functions
def get_db_credentials():
    with open(f'{CONFIG_PATH + os.sep}config.json', 'r') as file:
        config = json.load(file)
    return config.get('database', {})

def get_app_details():
    with open(f'{CONFIG_PATH + os.sep}config.json', 'r') as file:
        config = json.load(file)
    return config.get('app', {})

def is_valid_email(email: str):
    pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(pattern, email))

def is_strong_password(password: str):
    return len(password) >= 8

def generate_random_bytes(length: int):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def rename_config_file():
    old_name = "example.config.json"
    new_name = "config.json"
    old_file_path = os.path.join(CONFIG_PATH, old_name)
    new_file_path = os.path.join(CONFIG_PATH, new_name)

    try:
        os.rename(old_file_path, new_file_path)
        return True
    except FileNotFoundError:
        return f"The example config file was not found."
    except FileExistsError:
        return f"The config file already exists."