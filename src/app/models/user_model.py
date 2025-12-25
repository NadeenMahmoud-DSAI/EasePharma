import os
import pandas as pd
import uuid
from werkzeug.security import check_password_hash

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
        
        try:
            df = pd.read_csv(path)
            if 'email' not in df.columns: 
                return None
            
            user = df[df['email'].astype(str).str.lower() == str(email).lower()]
            if user.empty: 
                return None
            
            return user.iloc[0].fillna('').to_dict()
        except Exception as e:
            print(f"Error reading users db: {e}")
            return None

    def save(self, data_path):
        path = self._file(data_path)        
        new_data = {
            'user_id': self.user_id,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'full_name_en': self.full_name,  
            'phone': self.phone,
            'address': self.address,
            'status': 'Active',
            'age': '', 'gender': '', 'governorate': '', 'city': '', 
            'join_date': pd.Timestamp.now().strftime('%Y-%m-%d'), 
            'total_spent': 0.0,
            'first_name_ar': '', 'last_name_ar': ''
        }

        # 2. Load existing data
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                
                new_row = pd.DataFrame([new_data])
                
                df_final = pd.concat([df, new_row], ignore_index=True)
                
                df_final.to_csv(path, index=False)
                print(f"User {self.email} saved successfully.")
                return True
                
            except Exception as e:
                print(f"Error saving user: {e}")
                return False
        else:
            df = pd.DataFrame([new_data])
            df.to_csv(path, index=False)
            return True