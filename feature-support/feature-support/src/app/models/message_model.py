import os
import pandas as pd
import uuid
from datetime import datetime

class MessageModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'messages.csv')

    @classmethod
    def send_message(cls, data_path, user_id, sender_role, message):
        path = cls._file(data_path)
        new_row = {
            'msg_id': uuid.uuid4().hex[:8],
            'user_id': str(user_id),
            'sender_role': sender_role, # 'Customer' or 'Admin'
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        df = pd.DataFrame([new_row])
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)
        return True

    @classmethod
    def get_conversation(cls, data_path, user_id):
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path).fillna('')
            # Filter messages related to this user (either FROM them or TO them)
            df['user_id'] = df['user_id'].astype(str)
            chat = df[df['user_id'] == str(user_id)]
            return chat.to_dict('records')
        except: return []

    @classmethod
    def get_all_users_with_tickets(cls, data_path):
        # For Admin Inbox: Find all unique user_ids who have sent messages
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path)
            # Get unique IDs
            return df['user_id'].unique().tolist()
        except: return []