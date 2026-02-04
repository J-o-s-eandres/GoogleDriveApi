# src/services/drive_service.py
from src.utils.auth import get_authenticated_drive, validate_credentials
from src.config import Config

class DriveService:
    """Servicio para operaciones con Google Drive"""
    
    @staticmethod
    def list_permissions(file_id, verbose=False):
        """Lista los permisos de un archivo de Google Drive"""
        # Validar file_id
        if not file_id or not isinstance(file_id, str):
            return {'error': 'file_id inválido'}
        
        # Validar credenciales
        is_valid, message = validate_credentials()
        if not is_valid:
            return {'error': message}
        
        try:
            drive = get_authenticated_drive()
            file = drive.CreateFile({'id': file_id})
            file.FetchMetadata()
            permissions = file.GetPermissions()
            
            all_permissions = []
            for perm in permissions:
                perm_info = {
                    'id': perm.get('id'),
                    'type': perm.get('type'),
                    'role': perm.get('role'),
                    'email': perm.get('emailAddress'),
                    'name': perm.get('name'),
                    'domain': perm.get('domain'),
                    'deleted': perm.get('deleted', False)
                }
                all_permissions.append(perm_info)
            
            return {
                'success': True,
                'file_id': file_id,
                'file_title': file.get('title', 'Sin título'),
                'permissions': all_permissions,
                'count': len(all_permissions)
            }
            
        except Exception as e:
            return {'error': f'Error obteniendo permisos: {e}'}
    
    @staticmethod
    def grant_permission(file_id, perm_type, value, role):
        """Otorga un permiso a un archivo"""
        try:
            drive = get_authenticated_drive()
            file = drive.CreateFile({'id': file_id})
            
            permission = file.InsertPermission({
                'type': perm_type,
                'value': value,
                'role': role
            })
            
            return {
                'success': True,
                'message': 'Permiso otorgado exitosamente',
                'permission_id': permission.get('id'),
                'type': perm_type,
                'value': value,
                'role': role
            }
            
        except Exception as e:
            return {'error': f'Error otorgando permiso: {e}'}
    
    @staticmethod
    def remove_permission(file_id, permission_id=None, email=None):
        """Elimina un permiso por ID o email"""
        try:
            drive = get_authenticated_drive()
            file = drive.CreateFile({'id': file_id})
            permissions = file.GetPermissions()
            
            if permission_id:
                file.DeletePermission(permission_id)
                return {
                    'success': True,
                    'message': f'Permiso con ID {permission_id} eliminado.',
                    'permission_id': permission_id
                }
                
            elif email:
                for perm in permissions:
                    if perm.get('emailAddress') == email:
                        file.DeletePermission(perm.get('id'))
                        return {
                            'success': True,
                            'message': f'Permiso para {email} eliminado.',
                            'email': email,
                            'permission_id': perm.get('id')
                        }
                
                return {
                    'success': False,
                    'error': f'No se encontró permiso para el email: {email}'
                }
            else:
                return {
                    'success': False,
                    'error': 'Debe proporcionar permission_id o email'
                }
                
        except Exception as e:
            return {'error': f'Error eliminando permiso: {e}'}
    
    @staticmethod
    def get_file_info(file_id):
        """Obtiene información básica de un archivo"""
        try:
            drive = get_authenticated_drive()
            file = drive.CreateFile({'id': file_id})
            file.FetchMetadata()
            
            return {
                'success': True,
                'id': file.get('id'),
                'title': file.get('title'),
                'mimeType': file.get('mimeType'),
                'createdDate': file.get('createdDate'),
                'modifiedDate': file.get('modifiedDate'),
                'owners': file.get('owners', []),
                'size': file.get('fileSize', 'N/A')
            }
        except Exception as e:
            return {'error': f'Error obteniendo información: {e}'}
    
    @staticmethod
    def check_status():
        """Verifica el estado del servicio"""
        is_valid, message = validate_credentials()
        
        return {
            'status': 'online' if is_valid else 'offline',
            'credentials_valid': is_valid,
            'credentials_message': message,
            'timestamp': Config.get_timestamp()
        }