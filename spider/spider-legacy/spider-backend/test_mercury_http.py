#!/usr/bin/env python
"""
Script para probar los endpoints HTTP de Mercury API
"""
import requests
import json
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Token de prueba (necesitarás un token válido)
AUTH_TOKEN = "cf168a676aa44c8b58d60ef0de33e0673014c33b"

def test_society_snapshot():
    """Prueba el endpoint GET /api/society/{id}/snapshot"""
    print("🔍 Probando endpoint GET /api/society/{id}/snapshot...")
    
    # Usar un ID de sociedad de ejemplo (necesitarás un ID real)
    society_id = "1"  # Cambiar por un ID real
    
    url = f"{API_BASE}/society/{society_id}/snapshot"
    headers = {
        "Authorization": f"Token {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_mercury_status():
    """Prueba el endpoint GET /api/society/{id}/mercury-status"""
    print("\n🔍 Probando endpoint GET /api/society/{id}/mercury-status...")
    
    society_id = "1"  # Cambiar por un ID real
    
    url = f"{API_BASE}/society/{society_id}/mercury-status"
    headers = {
        "Authorization": f"Token {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_submit_onboarding_data():
    """Prueba el endpoint POST /api/mercury/submit-onboarding-data"""
    print("\n🔍 Probando endpoint POST /api/mercury/submit-onboarding-data...")
    
    url = f"{API_BASE}/mercury/submit-onboarding-data"
    headers = {
        "Authorization": f"Token {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Datos de ejemplo para Mercury API
    payload = {
        "partner": "Spider Investments",
        "about": {
            "legalBusinessName": "Test Company LLC",
            "website": "testcompany.com",
            "industry": "consulting",
            "countryOfOperation": "US",
            "description": "Test company for Mercury integration",
            "operations": "OnlineBusiness"
        },
        "businessContactDetails": {
            "phoneNumber": "+15551234567"
        },
        "formationDetails": {
            "companyStructure": "LLC",
            "federalEin": "12-3456789",
            "formationDocumentType": "ArticlesOfOrganization"
        },
        "businessLegalAddress": {
            "address1": "123 Test St",
            "city": "San Francisco",
            "region": "CA",
            "country": "US",
            "postalCode": "94102"
        },
        "businessPhysicalAddress": {
            "address1": "123 Test St",
            "city": "San Francisco",
            "region": "CA",
            "country": "US",
            "postalCode": "94102"
        },
        "beneficialOwners": [
            {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@testcompany.com",
                "dob": "1980-01-01",
                "address": {
                    "address1": "456 Owner St",
                    "city": "San Francisco",
                    "region": "CA",
                    "country": "US",
                    "postalCode": "94103"
                },
                "ownershipPercentage": 100,
                "phoneNumber": "+15551234567",
                "ssn": "123456789"
            }
        ],
        "applicationType": "DefaultApplication",
        "society_id": "1"  # ID de la sociedad
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_mercury_webhook():
    """Prueba el endpoint POST /api/mercury/webhooks"""
    print("\n🔍 Probando endpoint POST /api/mercury/webhooks...")
    
    url = f"{API_BASE}/mercury/webhooks"
    headers = {
        "Content-Type": "application/json",
        "Mercury-Signature": "t=1234567890,v1=test_signature"
    }
    
    # Payload de ejemplo de webhook de Mercury
    payload = {
        "event": "signed_up",
        "onboardingDataId": "test-onboarding-id-123"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas HTTP de Mercury API...")
    print("=" * 60)
    print("⚠️  Nota: Asegúrate de que el servidor Django esté ejecutándose")
    print("⚠️  Nota: Necesitarás IDs reales de sociedades y tokens válidos")
    print("=" * 60)
    
    # Ejecutar pruebas
    tests = [
        test_society_snapshot,
        test_mercury_status,
        test_submit_onboarding_data,
        test_mercury_webhook
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en prueba: {str(e)}")
            results.append(False)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS HTTP:")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas HTTP pasaron!")
    else:
        print("⚠️ Algunas pruebas HTTP fallaron")
        print("\n💡 Posibles causas:")
        print("  - Servidor Django no está ejecutándose")
        print("  - Token de autenticación inválido")
        print("  - IDs de sociedad no existen")
        print("  - Base de datos no configurada")

if __name__ == "__main__":
    main() 