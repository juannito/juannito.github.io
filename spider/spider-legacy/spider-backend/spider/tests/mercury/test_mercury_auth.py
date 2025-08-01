#!/usr/bin/env python
"""
Script para probar diferentes formatos de autenticación con Mercury API
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_different_auth_formats():
    """Prueba diferentes formatos de autenticación"""
    
    MERCURY_API_URL = "https://api.mercury.com/api/v2"
    MERCURY_API_KEY = "b9FTM5UEH8jtessQXqEStsJjg/POHCKQWkJtz3CNQJ8Z"
    
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
    
    # Diferentes formatos de autenticación a probar
    auth_formats = [
        {
            "name": "Bearer Token",
            "headers": {
                "Authorization": f"Bearer {MERCURY_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "Spider-Investments/1.0",
                "Accept": "application/json"
            }
        },
        {
            "name": "API Key Header",
            "headers": {
                "X-API-Key": MERCURY_API_KEY,
                "Content-Type": "application/json",
                "User-Agent": "Spider-Investments/1.0",
                "Accept": "application/json"
            }
        },
        {
            "name": "Mercury API Key",
            "headers": {
                "Mercury-API-Key": MERCURY_API_KEY,
                "Content-Type": "application/json",
                "User-Agent": "Spider-Investments/1.0",
                "Accept": "application/json"
            }
        },
        {
            "name": "API Key (sin Bearer)",
            "headers": {
                "Authorization": MERCURY_API_KEY,
                "Content-Type": "application/json",
                "User-Agent": "Spider-Investments/1.0",
                "Accept": "application/json"
            }
        },
        {
            "name": "Partner ID Header",
            "headers": {
                "Authorization": f"Bearer {MERCURY_API_KEY}",
                "X-Partner-ID": "Spider Investments",
                "Content-Type": "application/json",
                "User-Agent": "Spider-Investments/1.0",
                "Accept": "application/json"
            }
        }
    ]
    
    print("🔧 Probando diferentes formatos de autenticación con Mercury API")
    print("=" * 70)
    
    for auth_format in auth_formats:
        print(f"\n🧪 Probando: {auth_format['name']}")
        print(f"📋 Headers: {json.dumps(auth_format['headers'], indent=2)}")
        
        try:
            response = requests.post(
                f"{MERCURY_API_URL}/submit-onboarding-data",
                headers=auth_format['headers'],
                json=payload,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ ÉXITO! Respuesta:")
                print(json.dumps(result, indent=2))
                break
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📋 Response Text: {response.text}")
                
        except Exception as e:
            print(f"❌ Error de conexión: {str(e)}")
    
    print("\n" + "=" * 70)
    print("📝 Resumen:")
    print("- Si ninguna funciona, la API key puede estar expirada o ser inválida")
    print("- Verifica la documentación de Mercury para el formato correcto")
    print("- Contacta a Mercury para verificar la API key")

if __name__ == "__main__":
    test_different_auth_formats() 