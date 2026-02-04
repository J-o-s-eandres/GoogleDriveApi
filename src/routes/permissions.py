# src/routes/permissions.py
from flask import Blueprint, jsonify, request
from src.services.drive_service import DriveService

permissions_bp = Blueprint('permissions', __name__, url_prefix='/api')

@permissions_bp.route('/permissions/<file_id>', methods=['GET'])
def get_permissions(file_id):
    """Obtiene los permisos de un archivo"""
    result = DriveService.list_permissions(file_id)
    return jsonify(result)

@permissions_bp.route('/file/<file_id>', methods=['GET'])
def get_file(file_id):
    """Obtiene información de un archivo"""
    result = DriveService.get_file_info(file_id)
    return jsonify(result)

@permissions_bp.route('/permissions', methods=['POST'])
def grant_permission():
    """Otorga un permiso a un archivo"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    required_fields = ['file_id', 'type', 'value', 'role']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': f'Faltan campos: {", ".join(missing_fields)}'
        }), 400
    
    result = DriveService.grant_permission(
        data['file_id'],
        data['type'],
        data['value'],
        data['role']
    )
    
    return jsonify(result)

@permissions_bp.route('/permissions/<file_id>', methods=['DELETE'])
def delete_permission(file_id):
    """Elimina un permiso por ID o email"""
    data = request.json or {}
    
    permission_id = data.get('permission_id')
    email = data.get('email')
    
    if not permission_id and not email:
        return jsonify({
            'error': 'Debe proporcionar permission_id o email'
        }), 400
    
    result = DriveService.remove_permission(file_id, permission_id, email)
    return jsonify(result)

@permissions_bp.route('/permissions/<file_id>/email', methods=['DELETE'])
def delete_permission_by_email(file_id):
    """Elimina un permiso por email"""
    data = request.json or {}
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Debe proporcionar email'}), 400
    
    result = DriveService.remove_permission(file_id, None, email)
    return jsonify(result)

@permissions_bp.route('/permissions/<file_id>/<permission_id>', methods=['DELETE'])
def delete_permission_by_id(file_id, permission_id):
    """Elimina un permiso por ID"""
    result = DriveService.remove_permission(file_id, permission_id, None)
    return jsonify(result)