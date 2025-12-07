import json
import os

class UserModel:
    def __init__(self, email, password_hash, full_name, phone, address, role='Customer', user_id=None):
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.phone = phone
        self.address = address
        self.role = role
        self.user_id = user_id or os.urandom(4).hex()

    @staticmethod
    def get_by_email(email, data_path):
        if not os.path.exists(data_path): return None
        with open(data_path, 'r') as f:
            users = json.load(f)
            for u in users:
                if u['email'] == email: return u
        return None

    def save(self, data_path):
        users = []
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                try: users = json.load(f)
                except: users = []
        users.append(self.__dict__)
        with open(data_path, 'w') as f: json.dump(users, f, indent=4)
