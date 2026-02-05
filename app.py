# app.py
import os
from src import create_app

app = create_app()

if __name__ == '__main__':
    # Crear directorios si no existen
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("=" * 60)
    print("🚀 Google Drive Manager - Estructura Modular")
    print("=" * 60)
    print("📂 Directorio actual:", os.getcwd())
    print("📁 Estructura de módulos cargada correctamente")
    print("=" * 60)
    print("🌐 Accede a la aplicación en: http://localhost:5000")
    print("🔧 API Status: http://localhost:5000/api/status")
    print("🔧 API Test: http://localhost:5000/api/test")
    print("=" * 60)
    print("📋 Rutas disponibles:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"  {rule.rule}")
    print("=" * 60)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
