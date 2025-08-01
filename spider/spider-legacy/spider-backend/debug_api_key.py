#!/usr/bin/env python
"""
Script para debuggear la API key de Mercury
"""
import os
import sys
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from spider.mercury.client import MercuryAPIClient

def debug_api_key():
    """Debuggear la API key"""
    
    print("🔍 Debuggeando API key de Mercury...")
    print("=" * 50)
    
    # Verificar variables de entorno
    env_api_key = os.environ.get("MERCURY_API_KEY")
    print(f"📋 MERCURY_API_KEY desde .env: {env_api_key}")
    
    # Verificar settings de Django
    from django.conf import settings
    settings_api_key = getattr(settings, 'MERCURY_API_KEY', None)
    print(f"📋 MERCURY_API_KEY desde settings: {settings_api_key}")
    
    # Crear cliente y verificar
    client = MercuryAPIClient()
    print(f"📋 API Key en cliente: {client.api_key}")
    print(f"📋 API Key completa: {client.api_key}")
    
    # Verificar headers
    headers = client._get_headers()
    print(f"📋 Headers completos: {headers}")
    
    # Verificar que la API key sea la correcta
    expected_key = "b9FTM5UEH8jtessQXqEStsJjg/POHCKQWkJtz3CNQJ8Z"
    if client.api_key == expected_key:
        print("✅ API Key correcta")
    else:
        print("❌ API Key incorrecta")
        print(f"   Esperada: {expected_key}")
        print(f"   Actual:   {client.api_key}")
    
    print("\n" + "=" * 50)
    print("📝 Resumen:")
    print(f"- API Key configurada: {client.api_key}")
    print(f"- Headers generados: {headers}")
    print(f"- URL base: {client.api_url}")

if __name__ == "__main__":
    debug_api_key() 