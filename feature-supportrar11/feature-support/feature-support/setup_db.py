import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')
if not os.path.exists(data_dir): os.makedirs(data_dir)

messages_data = [
    {"msg_id": "1", "user_id": "1001", "sender_role": "Customer", "message": "Help! My order is late.", "timestamp": "2025-01-01 10:00:00"},
    {"msg_id": "2", "user_id": "1001", "sender_role": "Admin", "message": "Checking now...", "timestamp": "2025-01-01 10:05:00"},
    {"msg_id": "3", "user_id": "1002", "sender_role": "Customer", "message": "Do you sell Aspirin?", "timestamp": "2025-01-02 12:00:00"},
]

df = pd.DataFrame(messages_data)
df.to_csv(os.path.join(data_dir, 'messages.csv'), index=False)
print("✅ Created dummy messages.")