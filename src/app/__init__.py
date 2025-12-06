from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__, 
                template_folder='views/templates',
                static_folder='views/static')

    app.config['SECRET_KEY'] = 'dev_key'

    
    from src.app.controllers.admin_controller import admin_bp
    app.register_blueprint(admin_bp)

    
    @app.route('/')
    def home():
        return redirect(url_for('admin.products'))


    return app