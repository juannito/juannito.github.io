#!/usr/bin/env python
"""
Script de prueba para los endpoints de Mercury API
"""
import os
import sys
import django
import json
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

def test_society_snapshot():
    """Prueba el formateo de datos de sociedad para snapshot"""
    print("🔍 Probando formateo de snapshot de sociedad...")
    
    # Obtener la primera sociedad disponible
    try:
        sociedad = Sociedad.objects.first()
        if not sociedad:
            print("❌ No hay sociedades en la base de datos")
            return False
            
        print(f"📋 Sociedad encontrada: {sociedad.razon_social}")
        
        # Formatear datos
        formatter = MercuryDataFormatter()
        snapshot_data = formatter.format_society_snapshot(sociedad)
        
        print("✅ Datos formateados exitosamente:")
        print(json.dumps(snapshot_data, indent=2, default=str))
        
        # Validar datos
        validation_errors = formatter.validate_society_data(sociedad)
        if validation_errors:
            print("⚠️ Errores de validación encontrados:")
            print(json.dumps(validation_errors, indent=2))
        else:
            print("✅ Validación exitosa")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_onboarding_data():
    """Prueba el formateo de datos para onboarding"""
    print("\n🔍 Probando formateo de datos para onboarding...")
    
    try:
        sociedad = Sociedad.objects.first()
        if not sociedad:
            print("❌ No hay sociedades en la base de datos")
            return False
            
        print(f"📋 Sociedad: {sociedad.razon_social}")
        
        # Formatear datos de onboarding
        formatter = MercuryDataFormatter()
        onboarding_data = formatter.format_onboarding_data(sociedad)
        
        print("✅ Datos de onboarding formateados:")
        print(json.dumps(onboarding_data, indent=2, default=str))
        
        # Verificar que beneficialOwners es un array
        beneficial_owners = onboarding_data.get('beneficialOwners', [])
        print(f"👥 Número de propietarios beneficiarios: {len(beneficial_owners)}")
        
        for i, owner in enumerate(beneficial_owners):
            print(f"  {i+1}. {owner.get('firstName', '')} {owner.get('lastName', '')} - {owner.get('ownershipPercentage', 0)}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_participants():
    """Prueba la obtención de participantes"""
    print("\n🔍 Probando obtención de participantes...")
    
    try:
        sociedad = Sociedad.objects.first()
        if not sociedad:
            print("❌ No hay sociedades en la base de datos")
            return False
            
        participaciones = Participacion.objects.filter(sociedad=sociedad)
        print(f"📊 Total de participaciones: {participaciones.count()}")
        
        individual_participants = participaciones.filter(perfil__isnull=False)
        society_participants = participaciones.filter(sociedad_participante__isnull=False)
        
        print(f"👤 Participantes individuales: {individual_participants.count()}")
        print(f"🏢 Participantes sociedad: {society_participants.count()}")
        
        for participacion in individual_participants:
            perfil = participacion.perfil
            print(f"  - {perfil.nombre} {perfil.apellido} ({participacion.porcentaje}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de Mercury API...")
    print("=" * 50)
    
    # Ejecutar pruebas
    tests = [
        test_participants,
        test_society_snapshot,
        test_onboarding_data
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
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
    else:
        print("⚠️ Algunas pruebas fallaron")

if __name__ == "__main__":
    main() 