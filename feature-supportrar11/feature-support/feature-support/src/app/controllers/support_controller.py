from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from app.models.message_model import MessageModel

support_bp = Blueprint('support', __name__)

def get_data_path():
    return current_app.config['DATA_PATH']

@support_bp.route('/support', methods=['GET', 'POST'])
def index():
    # 1. Check Login
    if 'user_id' not in session:
        return redirect(url_for('auth_test.login_menu'))
    
    data_path = get_data_path()
    user_id = session['user_id']

    # 2. Handle Sending Message
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            MessageModel.send_message(data_path, user_id, 'Customer', msg)
        return redirect(url_for('support.index'))

    # 3. Load Chat History
    messages = MessageModel.get_conversation(data_path, user_id)
    return render_template('customer/support.html', messages=messages)