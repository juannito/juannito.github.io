#!/usr/bin/env python
"""
Script final para probar los endpoints de Mercury API
"""
import os
import sys
import django
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Configurar variables de entorno para Mercury
os.environ.setdefault('MERCURY_API_URL', 'https://api.mercury.com/api/v2')
os.environ.setdefault('MERCURY_API_KEY', 'b9FTM5UEH8jtessQXqEStsJjg/POHCKQWkJtz3CNQJ8Z')
os.environ.setdefault('MERCURY_WEBHOOK_SECRET', 'test_webhook_secret')

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from spider.models.sociedad import Sociedad
from spider.models.participacion import Participacion
from spider.models.perfil import Perfil
from spider.mercury.service import MercuryDataFormatter

def test_database_access():
    """Prueba el acceso a la base de datos"""
    print("🔍 Probando acceso a la base de datos...")
    
    try:
        # Obtener una sociedad de ejemplo
        sociedad = Sociedad.objects.first()
        if sociedad:
            print(f"✅ Sociedad encontrada: {sociedad.nombre}")
            
            # Obtener participaciones
            participaciones = Participacion.objects.filter(sociedad=sociedad)
            print(f"📊 Participaciones: {participaciones.count()}")
            
            return sociedad
        else:
            print("❌ No se encontraron sociedades en la base de datos")
            return None
            
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {str(e)}")
        return None

def test_mercury_formatter(sociedad):
    """Prueba el formateo de datos para Mercury"""
    print("\n🔍 Probando formateo de datos para Mercury...")
    
    try:
        formatter = MercuryDataFormatter()
        
        # Probar snapshot
        snapshot = formatter.format_society_snapshot(sociedad)
        print("✅ Snapshot formateado exitosamente")
        print(f"   Participantes: {len(snapshot.get('participants', []))}")
        
        # Probar onboarding data
        onboarding_data = formatter.format_onboarding_data(sociedad)
        print("✅ Datos de onboarding formateados exitosamente")
        print(f"   Propietarios beneficiarios: {len(onboarding_data.get('beneficialOwners', []))}")
        
        return snapshot, onboarding_data
        
    except Exception as e:
        print(f"❌ Error en formateo: {str(e)}")
        return None, None

def test_http_endpoints():
    """Prueba los endpoints HTTP"""
    print("\n🌐 Probando endpoints HTTP...")
    
    base_url = "http://127.0.0.1:8000"
    headers = {
        'Authorization': 'Token cf168a676aa44c8b58d60ef0de33e0673014c33b',
        'Content-Type': 'application/json'
    }
    
    # Obtener una sociedad para las pruebas
    sociedad = Sociedad.objects.first()
    if not sociedad:
        print("❌ No hay sociedades disponibles para las pruebas")
        return
    
    society_id = sociedad.id
    
    # 1. Probar GET /api/society/{id}/snapshot
    print(f"\n📡 Probando GET /api/society/{society_id}/snapshot...")
    try:
        response = requests.get(f"{base_url}/api/society/{society_id}/snapshot", headers=headers)
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   Participantes: {len(data.get('data', {}).get('participants', []))}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
    
    # 2. Probar GET /api/society/{id}/mercury-status
    print(f"\n📡 Probando GET /api/society/{society_id}/mercury-status...")
    try:
        response = requests.get(f"{base_url}/api/society/{society_id}/mercury-status", headers=headers)
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   Estado: {data.get('data', {}).get('status', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
    
    # 3. Probar POST /api/mercury/submit-onboarding-data
    print(f"\n📡 Probando POST /api/mercury/submit-onboarding-data...")
    try:
        # Crear datos de ejemplo para onboarding
        onboarding_payload = {
            "partner": "Spider Investments",
            "about": {
                "legalBusinessName": "Test Company",
                "website": "",
                "industry": "consulting",
                "countryOfOperation": "US",
                "description": "Test company for Mercury API",
                "operations": "OnlineBusiness"
            },
            "businessContactDetails": {
                "phoneNumber": "+1234567890"
            },
            "formationDetails": {
                "companyStructure": "LLC",
                "federalEin": "123456789",
                "formationDocumentType": "ArticlesOfOrganization"
            },
            "businessLegalAddress": {
                "address1": "123 Test St",
                "city": "Test City",
                "region": "CA",
                "country": "US",
                "postalCode": "12345"
            },
            "businessPhysicalAddress": {
                "address1": "123 Test St",
                "city": "Test City",
                "region": "CA",
                "country": "US",
                "postalCode": "12345"
            },
            "beneficialOwners": [
                {
                    "firstName": "John",
                    "lastName": "Doe",
                    "email": "john@test.com",
                    "dateOfBirth": "1990-01-01",
                    "ssn": "123456789",
                    "phoneNumber": "+1234567890",
                    "address": {
                        "address1": "123 Test St",
                        "city": "Test City",
                        "region": "CA",
                        "country": "US",
                        "postalCode": "12345"
                    },
                    "ownershipPercentage": 100
                }
            ],
            "applicationType": "DefaultApplication",
            "society_id": str(society_id)
        }
        
        response = requests.post(
            f"{base_url}/api/mercury/submit-onboarding-data",
            headers=headers,
            json=onboarding_payload
        )
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   Signup Link: {data.get('data', {}).get('signupLink', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
    
    # 4. Probar POST /api/mercury/webhooks
    print(f"\n📡 Probando POST /api/mercury/webhooks...")
    try:
        webhook_payload = {
            "event": "signed_up",
            "onboardingDataId": "test_onboarding_id_123",
            "accountStatus": "pending",
            "accountNumber": "",
            "routingNumber": ""
        }
        
        webhook_headers = {
            'Content-Type': 'application/json',
            'Mercury-Signature': 't=1234567890,v1=test_signature'
        }
        
        response = requests.post(
            f"{base_url}/api/mercury/webhooks",
            headers=webhook_headers,
            json=webhook_payload
        )
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Webhook endpoint funcionando correctamente")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas completas de Mercury API...")
    print("=" * 60)
    
    # 1. Probar acceso a base de datos
    sociedad = test_database_access()
    if not sociedad:
        print("❌ No se puede continuar sin acceso a la base de datos")
        return
    
    # 2. Probar formateo de datos
    snapshot, onboarding_data = test_mercury_formatter(sociedad)
    if not snapshot:
        print("❌ No se puede continuar sin formateo de datos")
        return
    
    # 3. Probar endpoints HTTP
    test_http_endpoints()
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas!")
    print("📋 Resumen:")
    print("   ✅ Acceso a base de datos")
    print("   ✅ Formateo de datos")
    print("   ✅ Endpoints HTTP (verificar resultados arriba)")

if __name__ == "__main__":
    main() 