# src/routes/main.py
from flask import Blueprint, render_template, send_from_directory
from src.config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ruta principal - Renderiza la página principal"""
    return render_template('index.html')

@main_bp.route('/css/<path:filename>')
def serve_css(filename):
    """Sirve archivos CSS"""
    return send_from_directory('static/css', filename)