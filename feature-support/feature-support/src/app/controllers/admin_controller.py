from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from app.models.message_model import MessageModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_data_path():
    return current_app.config['DATA_PATH']

@admin_bp.route('/support')
def inbox():
    # Admin Security Check
    if session.get('role') != 'Admin':
        return "Access Denied: Admins Only"
        
    data_path = get_data_path()
    # Get list of users who have messaged us
    user_ids = MessageModel.get_all_users_with_tickets(data_path)
    return render_template('admin/support_inbox.html', users=user_ids)

@admin_bp.route('/support/<user_id>', methods=['GET', 'POST'])
def reply(user_id):
    if session.get('role') != 'Admin':
        return "Access Denied"
        
    data_path = get_data_path()
    
    # Handle Reply
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            MessageModel.send_message(data_path, user_id, 'Admin', msg)
        return redirect(url_for('admin.reply', user_id=user_id))
        
    # View Conversation
    messages = MessageModel.get_conversation(data_path, user_id)
    return render_template('admin/chat_thread.html', messages=messages, current_customer=user_id)