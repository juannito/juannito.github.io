import requests
import json
import hmac
import hashlib
import time
import uuid
from typing import Dict, Any, Optional
from django.conf import settings


class MercuryAPIClient:
    """
    Cliente para interactuar con la API de Mercury
    """
    
    def __init__(self):
        self.api_url = getattr(settings, 'MERCURY_API_URL', 'https://api.mercury.com/api/v2')
        self.api_key = getattr(settings, 'MERCURY_API_KEY', 'b9FTM5UEH8jtessQXqEStsJjg/POHCKQWkJtz3CNQJ8Z')
        self.webhook_secret = getattr(settings, 'MERCURY_WEBHOOK_SECRET', '')
        self.partner_id = "Spider Investments"
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtiene los headers necesarios para las requests a Mercury API"""
        return {
            'Api-Secret-Key': self.api_key,  # 👈 Usar Api-Secret-Key como en Postman
            'Content-Type': 'application/json',
            'User-Agent': 'Spider-Investments/1.0',
            'Accept': 'application/json'
        }
    
    def submit_onboarding_data(self, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envía los datos de onboarding a Mercury API
        
        Args:
            onboarding_data: Datos formateados para Mercury API
            
        Returns:
            Dict con la respuesta de Mercury API
        """
        url = f"{self.api_url}/submit-onboarding-data"
        
        print(f"DEBUG: Iniciando submit_onboarding_data")
        print(f"DEBUG: URL: {url}")
        print(f"DEBUG: API Key: {self.api_key[:10]}...")
        
        try:
            # DESCOMENTAR PARA USAR LA API REAL:
            print(f"DEBUG: Usando API real de Mercury")
            print(f"DEBUG: Payload a enviar: {json.dumps(onboarding_data, indent=2)}")
            print(f"DEBUG: Headers a enviar: {self._get_headers()}")
            
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=onboarding_data,  # 👈 Usar json= para serialización automática
                timeout=30
            )
            
            print(f"DEBUG: Status Code: {response.status_code}")
            print(f"DEBUG: Response Headers: {dict(response.headers)}")
            
            response.raise_for_status()
            result = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(result, indent=2)}")
            return result
            
            # TEMPORAL: Simular respuesta exitosa para pruebas
            # print(f"DEBUG: Usando simulación de Mercury API")
            # print(f"DEBUG: Payload a enviar: {json.dumps(onboarding_data, indent=2)}")
            # print(f"DEBUG: Headers a enviar: {self._get_headers()}")
            # 
            # # Simular la respuesta exacta de Mercury API
            # alpha_code = f"Spider%20Investments-{uuid.uuid4().hex[:16].upper()}"
            # 
            # result = {
            #     'signupLink': f'https://app.mercury.com/signup?alphaCode={alpha_code}&utm_source=Spider%20Investments&utm_campaign=Spider%20Investments&utm_medium=onboarding_api',
            #     'onboardingDataId': f"{uuid.uuid4()}"
            # }
            # 
            # print(f"DEBUG: Simulando respuesta de Mercury: {json.dumps(result, indent=2)}")
            # return result
            
            # TEMPORAL: Simular respuesta exitosa para pruebas
            # print(f"DEBUG: Usando simulación de Mercury API")
            # print(f"Simulando respuesta de Mercury API para: {onboarding_data.get('about', {}).get('legalBusinessName', 'Unknown')}")
            # 
            # # Generar un alphaCode similar al real
            # alpha_code = f"Spider%20Investments-{uuid.uuid4().hex[:16].upper()}"
            # 
            # result = {
            #     'signupLink': f'https://app.mercury.com/signup?alphaCode={alpha_code}&utm_source=Spider%20Investments&utm_campaign=Spider%20Investments&utm_medium=onboarding_api',
            #     'onboardingDataId': f"{uuid.uuid4()}"
            # }
            # 
            # print(f"DEBUG: Retornando resultado simulado: {result}")
            # return result
            
        except Exception as e:
            print(f"DEBUG: Error en submit_onboarding_data: {str(e)}")
            raise Exception(f"Error comunicándose con Mercury API: {str(e)}")
    
    def verify_webhook_signature(self, payload: str, signature: str, timestamp: str) -> bool:
        """
        Verifica la firma del webhook de Mercury
        
        Args:
            payload: Cuerpo del webhook
            signature: Firma del webhook
            timestamp: Timestamp del webhook
            
        Returns:
            True si la firma es válida
        """
        if not self.webhook_secret:
            # Si no hay secret configurado, asumimos que es válido en desarrollo
            return True
        
        # Construir el mensaje que debe ser firmado
        message = f"{timestamp}.{payload}"
        
        # Calcular la firma esperada
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Extraer la firma del header
        # Formato: t=timestamp,v1=signature
        try:
            signature_parts = signature.split(',')
            for part in signature_parts:
                if part.startswith('v1='):
                    received_signature = part.split('=')[1]
                    break
            else:
                return False
        except (IndexError, AttributeError):
            return False
        
        # Comparar firmas
        return hmac.compare_digest(expected_signature, received_signature)
    
    def get_webhook_timestamp(self, signature: str) -> Optional[str]:
        """
        Extrae el timestamp del header de firma
        
        Args:
            signature: Header de firma completo
            
        Returns:
            Timestamp como string o None si no se puede extraer
        """
        try:
            signature_parts = signature.split(',')
            for part in signature_parts:
                if part.startswith('t='):
                    return part.split('=')[1]
        except (IndexError, AttributeError):
            pass
        return None 