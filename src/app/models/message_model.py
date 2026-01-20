import os
import pandas as pd
import uuid
from datetime import datetime

class MessageModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'messages.csv')

    def __init__(self, msg_id, user_id, sender_role, message, timestamp):
        self.msg_id = msg_id
        self.user_id = user_id
        self.sender_role = sender_role 
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def send_message(cls, data_path, user_id, sender_role, message):
        path = cls._file(data_path)
        new_row = {
            'msg_id': uuid.uuid4().hex[:8],
            'user_id': user_id,
            'sender_role': sender_role,
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
            df = pd.read_csv(path)
            df['user_id'] = df['user_id'].astype(str)
            user_msgs = df[df['user_id'] == str(user_id)]
            return [cls(r['msg_id'], r['user_id'], r['sender_role'], r['message'], r['timestamp']) for _, r in user_msgs.iterrows()]
        except: return []

    @classmethod
    def get_all_conversations_summary(cls, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path)
            users = df['user_id'].unique()
            return users
        except: return []