import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder='views/templates',
        static_folder='views/static'
    )

    # default config
    base_dir = os.getcwd()  # project root where src folder is
    default_data = os.path.join(base_dir, 'src', 'data')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'easepharma_secret_key_2025'),
        DATA_PATH=os.environ.get('DATA_PATH', default_data)
    )

    if test_config:
        app.config.update(test_config)

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)

    return app
