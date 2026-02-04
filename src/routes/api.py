# src/routes/api.py
from flask import Blueprint, jsonify, request
from src.services.drive_service import DriveService
from src.config import Config

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status', methods=['GET'])
def status():
    """Endpoint de estado del servicio"""
    return jsonify(DriveService.check_status())

@api_bp.route('/test', methods=['GET'])
def test_api():
    """Endpoint de prueba"""
    return jsonify({
        'status': 'ok',
        'message': 'API funcionando',
        'timestamp': Config.get_timestamp()
    })