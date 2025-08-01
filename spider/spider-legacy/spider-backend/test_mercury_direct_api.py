#!/usr/bin/env python
"""
Script para probar directamente con la API de Mercury
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_direct_mercury_api():
    """Prueba directamente con la API de Mercury"""
    
    # Configuración
    MERCURY_API_URL = "https://api.mercury.com/api/v2"
    MERCURY_API_KEY = os.environ.get("MERCURY_API_KEY", "your_api_key_here")
    
    # Payload de prueba
    payload = {
        "partner": "Spider Investments",
        "about": {
            "legalBusinessName": "CAF 74 LLC (00S)",
            "website": "",
            "industry": "consulting",
            "countryOfOperation": "US",
            "description": "Real estate investment company",
            "operations": "OnlineBusiness"
        },
        "businessContactDetails": {
            "phoneNumber": "+1888888888"
        },
        "formationDetails": {
            "companyStructure": "LLC",
            "federalEin": "38-4199442",
            "formationDocumentType": "ArticlesOfOrganization"
        },
        "businessLegalAddress": {
            "address1": "12566 Street Name",
            "address2": "",
            "city": "Cleveland",
            "region": "OH",
            "country": "US",
            "postalCode": "44101"
        },
        "businessPhysicalAddress": {
            "address1": "12566 Street Name",
            "address2": "",
            "city": "Cleveland",
            "region": "OH",
            "country": "US",
            "postalCode": "44101"
        },
        "beneficialOwners": [
            {
                "firstName": "Randy",
                "lastName": "Martinez",
                "email": "alexander91-demo0703@example.org",
                "dateOfBirth": "1985-06-15",
                "ssn": "123-45-6789",
                "phoneNumber": "+1888888888",
                "address": {
                    "address1": "12566 Street Name",
                    "address2": "",
                    "city": "Cleveland",
                    "region": "OH",
                    "country": "US",
                    "postalCode": "44101"
                },
                "ownershipPercentage": 100.0
            }
        ],
        "applicationType": "DefaultApplication"
    }
    
    headers = {
        "Api-Secret-Key": MERCURY_API_KEY,  # 👈 Usar Api-Secret-Key como en Postman
        "Content-Type": "application/json",
        "User-Agent": "Spider-Investments/1.0"
    }
    
    print("🚀 Probando directamente con Mercury API...")
    print(f"📡 URL: {MERCURY_API_URL}/submit-onboarding-data")
    print(f"🔑 API Key: {MERCURY_API_KEY[:10]}...")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    print(f"📋 Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.post(
            f"{MERCURY_API_URL}/submit-onboarding-data",
            headers=headers,
            json=payload,  # 👈 Usar json= para serialización automática
            timeout=30
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Éxito! Respuesta de Mercury:")
            print(json.dumps(result, indent=2))
            
            # Verificar el link
            signup_link = result.get('signupLink')
            if signup_link:
                print(f"\n🔗 Signup Link: {signup_link}")
                print("📝 Para probar el link:")
                print("1. Abre el link en un navegador")
                print("2. Verifica que los datos estén prellenados")
                print("3. Completa el onboarding")
            else:
                print("❌ No se encontró signupLink en la respuesta")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📋 Response Text: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def test_local_endpoint():
    """Prueba el endpoint local"""
    
    print("\n" + "="*60)
    print("🧪 Probando endpoint local...")
    
    payload = {
        "partner": "Spider Investments",
        "about": {
            "legalBusinessName": "CAF 74 LLC (00S)",
            "website": "",
            "industry": "consulting",
            "countryOfOperation": "US",
            "description": "Real estate investment company",
            "operations": "OnlineBusiness"
        },
        "businessContactDetails": {
            "phoneNumber": "+1888888888"
        },
        "formationDetails": {
            "companyStructure": "LLC",
            "federalEin": "38-4199442",
            "formationDocumentType": "ArticlesOfOrganization"
        },
        "businessLegalAddress": {
            "address1": "12566 Street Name",
            "address2": "",
            "city": "Cleveland",
            "region": "OH",
            "country": "US",
            "postalCode": "44101"
        },
        "businessPhysicalAddress": {
            "address1": "12566 Street Name",
            "address2": "",
            "city": "Cleveland",
            "region": "OH",
            "country": "US",
            "postalCode": "44101"
        },
        "beneficialOwners": [
            {
                "firstName": "Randy",
                "lastName": "Martinez",
                "email": "alexander91-demo0703@example.org",
                "dateOfBirth": "1985-06-15",
                "ssn": "123-45-6789",
                "phoneNumber": "+1888888888",
                "address": {
                    "address1": "12566 Street Name",
                    "address2": "",
                    "city": "Cleveland",
                    "region": "OH",
                    "country": "US",
                    "postalCode": "44101"
                },
                "ownershipPercentage": 100.0
            }
        ],
        "applicationType": "DefaultApplication"
    }
    
    headers = {
        "Authorization": "Token 3dfe8ff77c99cf689ed007030596a877489db1be",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/mercury/submit-onboarding-data",
            headers=headers,
            json=payload
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Éxito! Respuesta local:")
            print(json.dumps(result, indent=2))
            
            signup_link = result.get('signupLink')
            if signup_link:
                print(f"\n🔗 Signup Link: {signup_link}")
                print("📝 Para probar el link:")
                print("1. Abre el link en un navegador")
                print("2. Verifica que los datos estén prellenados")
                print("3. Completa el onboarding")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def main():
    """Función principal"""
    print("🔧 Herramienta de prueba para Mercury API")
    print("=" * 60)
    
    # Probar endpoint local
    test_local_endpoint()
    
    # Probar API directa (solo si tienes API key real)
    print("\n" + "="*60)
    print("⚠️  Para probar directamente con Mercury API:")
    print("1. Configura MERCURY_API_KEY en tu .env")
    print("2. Descomenta la línea siguiente en el script")
    print("3. Ejecuta: test_direct_mercury_api()")
    
    # Descomenta la siguiente línea cuando tengas API key real:
    test_direct_mercury_api()

if __name__ == "__main__":
    main() 