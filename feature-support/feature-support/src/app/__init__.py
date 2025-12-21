import os
from flask import Flask

def create_app():
    # Setup Paths
    app_folder = os.path.dirname(os.path.abspath(__file__))
    src_folder = os.path.dirname(app_folder)
    views_folder = os.path.join(src_folder, 'views')
    data_path = os.path.join(src_folder, 'data')

    app = Flask(__name__, 
                template_folder=os.path.join(views_folder, 'templates'),
                static_folder=os.path.join(views_folder, 'static'))

    app.config['SECRET_KEY'] = 'menna_key'
    app.config['DATA_PATH'] = data_path
    if not os.path.exists(data_path): os.makedirs(data_path)

    # Register Blueprints
    from app.controllers.support_controller import support_bp
    app.register_blueprint(support_bp)

    from app.controllers.admin_controller import admin_bp
    app.register_blueprint(admin_bp)

    return app