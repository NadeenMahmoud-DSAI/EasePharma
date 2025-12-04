import os
import pandas as pd
import uuid
from types import SimpleNamespace

class UserModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'users.csv')

    def __init__(self, email, password_hash, role='Customer', full_name='', phone='', address=''):
        self.user_id = uuid.uuid4().hex[:10]
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.full_name = full_name
        self.phone = phone
        self.address = address

    @classmethod
    def get_by_email(cls, email, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path):
            return None
        df = pd.read_csv(path)
        user = df[df['email'].astype(str).str.lower() == str(email).lower()]
        if user.empty:
            return None
        r = user.iloc[0].to_dict()
        return r

    def save(self, data_path):
        path = self._file(data_path)
        row = {
            'user_id': self.user_id,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address
        }
        df = pd.DataFrame([row])
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)
