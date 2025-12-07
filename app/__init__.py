from flask import Flask
import os

def create_app():
    # Note: We assume the folder is named 'templates' now
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'supersecretkey'
    app.config['DATA_PATH'] = os.path.join(app.root_path, '../users.json')

    from .auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from .product_controller import product_bp
    app.register_blueprint(product_bp)

    return app
