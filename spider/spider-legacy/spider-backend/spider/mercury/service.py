import re
from datetime import datetime
from typing import Dict, Any, List
from spider.models.sociedad import Sociedad
from spider.models.participacion import Participacion


class MercuryDataFormatter:
    """
    Servicio para formatear datos de sociedad y participantes para Mercury API
    """
    
    @staticmethod
    def format_society_snapshot(sociedad: Sociedad) -> Dict[str, Any]:
        """
        Formatea los datos de una sociedad para el endpoint de snapshot
        
        Args:
            sociedad: Instancia de Sociedad
            
        Returns:
            Dict con los datos formateados
        """
        # Obtener participantes
        participaciones = Participacion.objects.filter(sociedad=sociedad)
        
        # Formatear datos de la sociedad
        society_data = {
            "id": str(sociedad.id),
            "legalBusinessName": sociedad.razon_social,
            "taxId": sociedad.tax_id,
            "businessType": sociedad.company_type or "LLC",
            "formationDocumentType": "ArticlesOfOrganization",
            "formationDate": sociedad.fecha_de_creacion.strftime('%Y-%m-%d') if sociedad.fecha_de_creacion else None,
            "website": "",
            "industry": "consulting",
            "businessDescription": sociedad.description or "",
            "operations": "OnlineBusiness",
            "phoneNumber": sociedad.phone_number,
            "address": {
                "address1": sociedad.address_line_1 or "",
                "address2": sociedad.address_line_2 or "",
                "city": sociedad.city or "",
                "region": getattr(sociedad.state, 'abbreviation', '') if sociedad.state else "",
                "country": "US",
                "postalCode": sociedad.zipcode or ""
            }
        }
        
        # Formatear participantes
        participants_data = []
        for participacion in participaciones:
            if participacion.perfil:  # Participante individual
                participant_data = {
                    "id": str(participacion.id),
                    "firstName": participacion.perfil.nombre or "",
                    "lastName": participacion.perfil.apellido or "",
                    "email": participacion.perfil.user.email if participacion.perfil.user else "",
                    "dateOfBirth": participacion.perfil.fecha_de_nacimiento.strftime('%Y-%m-%d') if participacion.perfil.fecha_de_nacimiento else None,
                    "ssn": getattr(participacion.perfil, 'personal_id', None),
                    "phoneNumber": getattr(participacion.perfil, 'telefono', None),
                    "address": MercuryDataFormatter._format_address(participacion.perfil),
                    "ownershipPercentage": float(participacion.porcentaje) if participacion.porcentaje and str(participacion.porcentaje) != 'NaN' else 0
                }
                participants_data.append(participant_data)
        
        return {
            "society": society_data,
            "participants": participants_data,
            "partner": "Spider Investments"
        }
    
    @staticmethod
    def format_onboarding_data(sociedad: Sociedad) -> Dict[str, Any]:
        """
        Formatea los datos para enviar a Mercury API
        
        Args:
            sociedad: Instancia de Sociedad
            
        Returns:
            Dict con los datos formateados para onboarding
        """
        # Obtener participantes
        participaciones = Participacion.objects.filter(sociedad=sociedad)
        
        # Formatear datos de la empresa
        about_data = {
            "legalBusinessName": sociedad.razon_social,
            "website": "",
            "industry": "consulting",
            "countryOfOperation": "US",
            "description": sociedad.description or "",
            "operations": "OnlineBusiness"
        }
        
        # Formatear detalles de formación
        formation_data = {
            "companyStructure": sociedad.company_type or "LLC",
            "federalEin": sociedad.tax_id,
            "formationDocumentType": "ArticlesOfOrganization"
        }
        
        # Formatear direcciones de la empresa
        business_legal_address = {
            "address1": sociedad.address_line_1 or "",
            "address2": sociedad.address_line_2 or "",
            "city": sociedad.city or "",
            "region": getattr(sociedad.state, 'abbreviation', '') if sociedad.state else "",
            "country": "US",
            "postalCode": sociedad.zipcode or ""
        }
        
        # Por defecto, usar la misma dirección para física y legal
        business_physical_address = business_legal_address.copy()
        
        # Formatear propietarios beneficiarios
        beneficial_owners = []
        for participacion in participaciones:
            if participacion.perfil:  # Solo participantes individuales
                owner_data = {
                    "firstName": participacion.perfil.nombre or "",
                    "lastName": participacion.perfil.apellido or "",
                    "email": participacion.perfil.user.email if participacion.perfil.user else "",
                    "dateOfBirth": participacion.perfil.fecha_de_nacimiento.strftime('%Y-%m-%d') if participacion.perfil.fecha_de_nacimiento else None,
                    "address": MercuryDataFormatter._format_address(participacion.perfil),
                    "ownershipPercentage": float(participacion.porcentaje) if participacion.porcentaje and str(participacion.porcentaje) != 'NaN' else 0,
                    "phoneNumber": getattr(participacion.perfil, 'telefono', None),
                    "ssn": getattr(participacion.perfil, 'personal_id', None)
                }
                beneficial_owners.append(owner_data)
        
        return {
            "partner": "Spider Investments",
            "about": about_data,
            "businessContactDetails": {
                "phoneNumber": sociedad.telefono if hasattr(sociedad, 'telefono') else None
            },
            "formationDetails": formation_data,
            "businessLegalAddress": business_legal_address,
            "businessPhysicalAddress": business_physical_address,
            "beneficialOwners": beneficial_owners,
            "applicationType": "DefaultApplication"
        }
    
    @staticmethod
    def _format_address(perfil) -> Dict[str, str]:
        """
        Formatea una dirección para Mercury API
        
        Args:
            perfil: Objeto Perfil
            
        Returns:
            Dict con la dirección formateada (siempre devuelve un dict válido)
        """
        if not perfil:
            return {
                "address1": "",
                "city": "",
                "region": "",
                "country": "US",
                "postalCode": ""
            }
        
        address_data = {
            "address1": getattr(perfil, 'direccion_linea_1', '') or "",
            "city": getattr(perfil, 'ciudad', '') or "",
            "region": getattr(perfil, 'state', '') or "",
            "country": "US",
            "postalCode": getattr(perfil, 'zipcode', '') or ""
        }
        
        # Agregar address2 solo si existe y no está vacío
        address2 = getattr(perfil, 'direccion_linea_2', '') or ""
        if address2:
            address_data["address2"] = address2
        
        return address_data
    
    @staticmethod
    def validate_society_data(sociedad: Sociedad) -> Dict[str, List[str]]:
        """
        Valida los datos de la sociedad para Mercury API
        
        Args:
            sociedad: Instancia de Sociedad
            
        Returns:
            Dict con errores de validación
        """
        errors = {}
        
        # Validar EIN
        if hasattr(sociedad, 'ein') and sociedad.ein:
            if not re.match(r'^\d{2}-\d{7}$', sociedad.ein):
                errors['ein'] = ['Invalid EIN format. Must be XX-XXXXXXX']
        
        # Validar teléfono
        if hasattr(sociedad, 'telefono') and sociedad.telefono:
            if not re.match(r'^\+1\d{10}$', sociedad.telefono):
                errors['phoneNumber'] = ['Invalid phone number format. Must be +1XXXXXXXXXX']
        
        # Validar dirección
        if hasattr(sociedad, 'direccion') and sociedad.direccion:
            address_errors = []
            if not getattr(sociedad.direccion, 'codigo_postal', None):
                address_errors.append('Postal code is required')
            if not getattr(sociedad.direccion, 'estado', None):
                address_errors.append('State is required')
            if address_errors:
                errors['address'] = address_errors
        
        # Validar participantes (solo como advertencia, no bloqueante)
        participaciones = Participacion.objects.filter(sociedad=sociedad)
        if not participaciones.exists():
            errors['participants'] = ['No participants found - Mercury will require at least one']
        else:
            # Calcular porcentaje total solo de participantes individuales
            individual_participations = participaciones.filter(perfil__isnull=False)
            if individual_participations.exists():
                total_percentage = sum(
                    float(p.porcentaje) if p.porcentaje else 0 for p in individual_participations
                )
                if total_percentage != 100:
                    errors['ownership'] = [
                        f'Total ownership percentage is {total_percentage:.2f}% (should be 100%)',
                        f'Mercury may require adjustment of participant percentages',
                        f'Participants found: {individual_participations.count()}'
                    ]
            else:
                errors['participants'] = ['No individual participants found - Mercury will require at least one']
        
        return errors
    
    @staticmethod
    def validate_mercury_addresses(onboarding_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Valida las direcciones según las restricciones de Mercury API
        
        Args:
            onboarding_data: Datos de onboarding a validar
            
        Returns:
            Dict con errores de validación
        """
        errors = {}
        
        # Validar businessLegalAddress (no soporta internacionales, mail centers, PO Box)
        legal_address = onboarding_data.get('businessLegalAddress', {})
        if legal_address:
            address1 = legal_address.get('address1', '').lower()
            if any(keyword in address1 for keyword in ['po box', 'p.o. box', 'mail center', 'post office']):
                errors['businessLegalAddress'] = ['PO Box, mail center, or post office addresses are not supported']
            
            # Validar que no sea dirección internacional (debe ser US)
            country = legal_address.get('country', '')
            if country and country.upper() != 'US':
                errors['businessLegalAddress'] = ['International addresses are not supported for legal address']
        
        # Validar businessPhysicalAddress (soporta internacionales pero no Registered Agent o PO Box)
        physical_address = onboarding_data.get('businessPhysicalAddress', {})
        if physical_address:
            address1 = physical_address.get('address1', '').lower()
            if any(keyword in address1 for keyword in ['po box', 'p.o. box', 'registered agent']):
                errors['businessPhysicalAddress'] = ['PO Box or Registered Agent addresses are not supported']
        
        # Validar direcciones de beneficialOwners (deben ser residencia, no oficina)
        beneficial_owners = onboarding_data.get('beneficialOwners', [])
        for i, owner in enumerate(beneficial_owners):
            owner_address = owner.get('address', {})
            if owner_address:
                address1 = owner_address.get('address1', '').lower()
                if any(keyword in address1 for keyword in ['suite', 'office', 'industrial', 'warehouse', 'factory']):
                    errors[f'beneficialOwners[{i}].address'] = [
                        'Owner address must be residential, not office or industrial'
                    ]
        
        return errors 