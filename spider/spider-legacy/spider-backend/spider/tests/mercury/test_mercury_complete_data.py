#!/usr/bin/env python
"""
Script para probar Mercury API con datos completos de la base de datos
"""
import os
import sys
import django
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from spider.models.sociedad import Sociedad
from spider.models.participacion import Participacion
from spider.models.perfil import Perfil
from spider.mercury.service import MercuryDataFormatter

def find_society_with_complete_data():
    """Busca una sociedad con datos completos para las pruebas"""
    print("🔍 Buscando sociedad con datos completos...")
    
    # Buscar sociedades con tax ID, phone y address
    sociedades = Sociedad.objects.filter(
        tax_id__isnull=False
    ).exclude(
        tax_id=''
    ).filter(
        phone_number__isnull=False
    ).exclude(
        phone_number=''
    ).filter(
        address_line_1__isnull=False
    ).exclude(
        address_line_1=''
    )[:10]
    
    for sociedad in sociedades:
        # Verificar que tenga participaciones que sumen 100%
        participaciones = Participacion.objects.filter(sociedad=sociedad)
        if participaciones.count() == 0:
            continue
            
        total = sum([
            float(pp.porcentaje) for pp in participaciones 
            if pp.porcentaje and str(pp.porcentaje) != 'NaN'
        ])
        
        if total >= 95:  # Permitir un pequeño margen de error
            print(f"✅ Sociedad encontrada: {sociedad.nombre}")
            print(f"   Tax ID: {sociedad.tax_id}")
            print(f"   Phone: {sociedad.phone_number}")
            print(f"   Address: {sociedad.address_line_1}, {sociedad.city}, {sociedad.state}")
            print(f"   Participaciones: {participaciones.count()}")
            print(f"   Total participación: {total}%")
            return sociedad
    
    print("❌ No se encontró sociedad con datos completos")
    return None

def test_complete_onboarding(sociedad):
    """Prueba el onboarding con datos completos"""
    print(f"\n🚀 Probando onboarding para: {sociedad.nombre}")
    
    # Generar datos de onboarding usando el formatter
    formatter = MercuryDataFormatter()
    onboarding_data = formatter.format_onboarding_data(sociedad)
    
    # Agregar society_id al payload (opcional)
    # onboarding_data['society_id'] = str(sociedad.id)
    
    print("📋 Payload generado:")
    print(json.dumps(onboarding_data, indent=2, default=str))
    
    # Probar el endpoint
    base_url = "http://127.0.0.1:8000"
    headers = {
        'Authorization': 'Token 3dfe8ff77c99cf689ed007030596a877489db1be',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/mercury/submit-onboarding-data",
            headers=headers,
            json=onboarding_data
        )
        
        print(f"\n📊 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Onboarding exitoso!")
            print(f"   Signup Link: {data.get('signupLink', 'N/A')}")
            print(f"   Onboarding ID: {data.get('onboardingDataId', 'N/A')}")
            
            # Verificar que se guardó en la base de datos
            from spider.models.mercury_onboarding import MercuryOnboarding
            onboardings = MercuryOnboarding.objects.filter(sociedad=sociedad)
            print(f"   Registros en BD: {onboardings.count()}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def test_snapshot_endpoint(sociedad):
    """Prueba el endpoint de snapshot"""
    print(f"\n📡 Probando snapshot para: {sociedad.nombre}")
    
    base_url = "http://127.0.0.1:8000"
    headers = {
        'Authorization': 'Token 3dfe8ff77c99cf689ed007030596a877489db1be',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f"{base_url}/api/society/{sociedad.id}/snapshot",
            headers=headers
        )
        
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Snapshot exitoso!")
            print(f"   Participantes: {len(data.get('data', {}).get('participants', []))}")
            print(f"   Warnings: {data.get('warnings', 'None')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas con datos completos...")
    print("=" * 60)
    
    # Buscar sociedad con datos completos
    sociedad = find_society_with_complete_data()
    if not sociedad:
        print("❌ No se puede continuar sin datos completos")
        return
    
    # Probar snapshot
    test_snapshot_endpoint(sociedad)
    
    # Probar onboarding
    test_complete_onboarding(sociedad)
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    main() 