# src/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.routes.main import main_bp
from src.routes.api import api_bp
from src.routes.permissions import permissions_bp

def create_app():
    """Factory function para crear la aplicación Flask"""
    # Obtener directorio base
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Configurar Flask
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=os.path.join(base_dir, 'static'),
                template_folder=os.path.join(base_dir, 'templates'))
    
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {"origins": Config.CORS_ORIGINS}
    })
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(permissions_bp)
    
    return app

