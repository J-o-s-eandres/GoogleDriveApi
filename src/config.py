# src/config.py
import os
from datetime import datetime

class Config:
    """Configuración de la aplicación"""
    # Usando rutas relativas como antes
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    CORS_ORIGINS = [
        "http://localhost:5000",
        "http://192.168.1.8:5000", 
        "http://127.0.0.1:5000"
    ]
    
    # Credenciales - mantener en raíz del proyecto
    CREDENTIALS_PATH = 'credentials_module.json'
    SETTINGS_FILE = 'settings.yaml'
    
    @staticmethod
    def get_timestamp():
        """Obtiene timestamp actual"""
        return datetime.now().isoformat()