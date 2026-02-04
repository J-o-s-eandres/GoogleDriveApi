# src/utils/auth.py
import os
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from src.config import Config

def get_authenticated_drive():
    """
    Autentica y devuelve un cliente autorizado de Google Drive
    
    Returns:
        GoogleDrive: Cliente autenticado
    """
    gauth = GoogleAuth(settings_file=Config.SETTINGS_FILE)
    
    # Configurar para obtener refresh token
    if not gauth.settings.get('get_refresh_token'):
        gauth.settings['get_refresh_token'] = True
    if not gauth.settings.get('access_type'):
        gauth.settings['access_type'] = 'offline'
    
    # Cargar credenciales existentes
    if os.path.exists(Config.CREDENTIALS_PATH):
        try:
            gauth.LoadCredentialsFile(Config.CREDENTIALS_PATH)
            print("✅ Credenciales cargadas del archivo")
        except Exception as e:
            print(f"❌ Error cargando credenciales: {e}")
    
    # Verificar refresh token
    has_refresh_token = (
        gauth.credentials and 
        hasattr(gauth.credentials, 'refresh_token') and 
        gauth.credentials.refresh_token
    )
    
    # Sin credenciales o sin refresh token -> autenticar
    if gauth.credentials is None or not has_refresh_token:
        print("🔐 No hay credenciales válidas. Autenticando...")
        if not has_refresh_token and gauth.credentials:
            print("🔄 Forzando nueva autenticación para obtener refresh_token...")
            gauth.settings['approval_prompt'] = 'force'
        
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(Config.CREDENTIALS_PATH)
        print(f"💾 Credenciales guardadas en: {Config.CREDENTIALS_PATH}")
    
    # Token expirado -> refrescar
    elif gauth.access_token_expired:
        print("🔄 Token expirado. Refrescando...")
        try:
            gauth.Refresh()
            gauth.SaveCredentialsFile(Config.CREDENTIALS_PATH)
            print("✅ Token refrescado")
        except Exception as e:
            print(f"❌ Error refrescando token: {e}")
            print("🔐 Reautenticando...")
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(Config.CREDENTIALS_PATH)
    else:
        gauth.Authorize()
        print("✅ Credenciales válidas")
    
    # Crear cliente Drive
    drive = GoogleDrive(gauth)
    return drive

def validate_credentials():
    """Valida que las credenciales existan y tengan refresh token"""
    if not os.path.exists(Config.CREDENTIALS_PATH):
        return False, 'No se encontró archivo de credenciales'
    
    try:
        with open(Config.CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        
        if not creds.get('refresh_token'):
            return False, 'No hay refresh_token en las credenciales'
        
        return True, 'Credenciales válidas'
    except Exception as e:
        return False, f'Error leyendo credenciales: {e}'