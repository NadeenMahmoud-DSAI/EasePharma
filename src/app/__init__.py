import os
from flask import Flask

def create_app(test_config=None):
    app_folder = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(app_folder, 'views', 'static')
    template_path = os.path.join(app_folder, 'views', 'templates')

    
    app = Flask(
        __name__,
        template_folder=template_path,
        static_folder=static_path
    )

    # 3. CONFIGURATION
    src_folder = os.path.dirname(app_folder)
    data_dir = os.path.join(os.path.dirname(src_folder), 'src', 'data')
    if not os.path.exists(data_dir):
        data_dir = os.path.join(src_folder, 'data')

    app.config.from_mapping(
        SECRET_KEY='easepharma_secret_key_2025',
        DATA_PATH=data_dir
    )

    # 4. REGISTER BLUEPRINTS
    try:
        from app.controllers.product_controller import product_bp
        app.register_blueprint(product_bp)
    except ImportError as e:
        print(f"Product Controller Error: {e}")

    try:
        from app.controllers.auth_controller import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError as e:
        print(f"Auth Controller Error: {e}")

    try:
        from app.controllers.admin_controller import admin_bp
        app.register_blueprint(admin_bp)
    except ImportError as e:
        print(f"Admin Controller Error: {e}")

    return app