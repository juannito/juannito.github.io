import uuid
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from spider.models.sociedad import Sociedad
from spider.models.mercury_onboarding import MercuryOnboarding
from spider.mercury.client import MercuryAPIClient
from spider.mercury.service import MercuryDataFormatter
from spider.serializers.mercury import (
    SocietySnapshotSerializer, MercuryOnboardingDataSerializer,
    MercurySubmitResponseSerializer, MercuryWebhookSerializer,
    MercuryStatusSerializer
)


from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["GET"])
def society_snapshot(request, society_id):
    """
    GET /api/society/{id}/snapshot
    
    Obtiene todos los datos de una sociedad y sus participantes formateados para Mercury API
    """
    try:
        # Obtener la sociedad
        sociedad = Sociedad.objects.get(id=society_id)
        
        # Verificar que el usuario tiene acceso a esta sociedad
        # Comentado temporalmente para pruebas
        # if not request.user.has_perm('spider.view_sociedad', sociedad):
        #     return Response(
        #         {'error': 'No tienes permisos para acceder a esta sociedad'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        
        # Formatear datos
        formatter = MercuryDataFormatter()
        try:
            snapshot_data = formatter.format_society_snapshot(sociedad)
            print(f"Snapshot data generated successfully")
        except Exception as e:
            print(f"Error formatting snapshot data: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'error': 'Error formatting data for Mercury API',
                'details': str(e),
                'type': 'formatting_error'
            }, status=500)
        
        # Validar datos
        validation_errors = formatter.validate_society_data(sociedad)
        
        # Si hay errores críticos, devolver error HTTP
        if validation_errors:
            return JsonResponse({
                'error': 'Datos de sociedad incompletos',
                'details': validation_errors,
                'type': 'validation_error'
            }, status=400)
        
        # Si no hay errores, devolver directamente los datos
        return JsonResponse(snapshot_data, status=200, safe=False)
        
    except Sociedad.DoesNotExist:
        return JsonResponse({
            'error': 'Sociedad no encontrada',
            'details': f'No se encontró la sociedad con ID {society_id}',
            'type': 'society_not_found'
        }, status=404)
    except Exception as e:
        import traceback
        print(f"Unexpected error in society_snapshot: {str(e)}")
        traceback.print_exc()
        return JsonResponse({
            'error': 'Error interno del servidor',
            'details': str(e),
            'type': 'internal_server_error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_onboarding_data(request):
    """
    POST /api/mercury/submit-onboarding-data
    
    Envía los datos formateados a Mercury API y devuelve el enlace de registro
    """
    try:
        # Validar datos de entrada
        import json
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Invalid JSON payload'
                },
                status=400
            )
        
        serializer = MercuryOnboardingDataSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Invalid data provided',
                    'details': serializer.errors
                },
                status=400
            )
        
        # Validar direcciones según restricciones de Mercury
        address_errors = MercuryDataFormatter.validate_mercury_addresses(data)
        if address_errors:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Address validation failed',
                    'details': address_errors
                },
                status=400
            )
        
        # Extraer society_id del payload (para uso interno) - opcional
        society_id = data.get('society_id')
        
        # Crear copia de datos sin society_id para enviar a Mercury
        mercury_payload = serializer.validated_data.copy()
        if 'society_id' in mercury_payload:
            del mercury_payload['society_id']
        
        # Enviar datos a Mercury API
        client = MercuryAPIClient()
        mercury_response = client.submit_onboarding_data(mercury_payload)
        
        # Extraer datos de la respuesta
        signup_link = mercury_response.get('signupLink')
        onboarding_data_id = mercury_response.get('onboardingDataId')
        
        if not signup_link or not onboarding_data_id:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Invalid response from Mercury API'
                },
                status=500
            )
        
        # Crear registro de onboarding (solo si se proporciona society_id)
        if society_id:
            onboarding_id = str(uuid.uuid4())
            onboarding = MercuryOnboarding.objects.create(
                id=onboarding_id,
                sociedad_id=society_id,
                onboarding_data_id=onboarding_data_id,
                signup_link=signup_link,
                status='pending'
            )
        
        return JsonResponse({
            'signupLink': signup_link,
            'onboardingDataId': onboarding_data_id
        })
        
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'error': f'Error submitting onboarding data: {str(e)}'
            },
            status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
def mercury_webhook(request):
    """
    POST /api/mercury/webhooks
    
    Endpoint para recibir webhooks de Mercury
    """
    try:
        # Verificar firma del webhook
        client = MercuryAPIClient()
        signature = request.headers.get('Mercury-Signature')
        
        if not signature:
            return JsonResponse(
                {'error': 'Missing Mercury-Signature header'},
                status=400
            )
        
        # Extraer timestamp y verificar firma
        timestamp = client.get_webhook_timestamp(signature)
        if not timestamp:
            return JsonResponse(
                {'error': 'Invalid signature format'},
                status=400
            )
        
        payload = request.body.decode('utf-8')
        if not client.verify_webhook_signature(payload, signature, timestamp):
            return JsonResponse(
                {'error': 'Invalid webhook signature'},
                status=400
            )
        
        # Parsear datos del webhook
        webhook_data = json.loads(payload)
        serializer = MercuryWebhookSerializer(data=webhook_data)
        
        if not serializer.is_valid():
            return JsonResponse(
                {'error': 'Invalid webhook data'},
                status=400
            )
        
        # Actualizar estado del onboarding
        onboarding_data_id = serializer.validated_data['onboardingDataId']
        event = serializer.validated_data['event']
        
        try:
            onboarding = MercuryOnboarding.objects.get(
                onboarding_data_id=onboarding_data_id
            )
            
            # Mapear eventos de Mercury a estados internos
            status_mapping = {
                'signed_up': 'signed_up',
                'application_submitted': 'submitted',
                'information_requested': 'information_requested',
                'approved': 'approved',
                'rejected': 'rejected'
            }
            
            new_status = status_mapping.get(event, 'pending')
            onboarding.status = new_status
            
            # Si es approved, guardar datos de cuenta
            if event == 'approved':
                onboarding.account_number = serializer.validated_data.get('accountNumber', '')
                onboarding.routing_number = serializer.validated_data.get('routingNumber', '')
            
            onboarding.save()
            
            return JsonResponse({'success': True})
            
        except MercuryOnboarding.DoesNotExist:
            return JsonResponse(
                {'error': 'Onboarding not found'},
                status=404
            )
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON payload'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'error': f'Internal server error: {str(e)}'},
            status=500
        )


from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["GET"])
def mercury_status(request, society_id):
    """
    GET /api/society/{id}/mercury-status
    
    Obtiene el estado actual del onboarding de Mercury para una sociedad
    """
    try:
        # Obtener la sociedad
        sociedad = Sociedad.objects.get(id=society_id)
        
        # Verificar permisos
        # Comentado temporalmente para pruebas
        # if not request.user.has_perm('spider.view_sociedad', sociedad):
        #     return JsonResponse(
        #         {'error': 'No tienes permisos para acceder a esta sociedad'},
        #         status=403
        #     )
        
        # Buscar onboarding más reciente
        onboarding = MercuryOnboarding.objects.filter(
            sociedad=sociedad
        ).order_by('-created_at').first()
        
        if not onboarding:
            return JsonResponse({
                'success': True,
                'data': {
                    'status': None,
                    'hasOnboarding': False
                }
            })
        
        return JsonResponse({
            'success': True,
            'data': {
                'status': onboarding.status,
                'accountNumber': onboarding.account_number,
                'routingNumber': onboarding.routing_number,
                'onboardingDataId': onboarding.onboarding_data_id,
                'hasOnboarding': True,
                'createdAt': onboarding.created_at.isoformat(),
                'updatedAt': onboarding.updated_at.isoformat()
            }
        })
        
    except Sociedad.DoesNotExist:
        return JsonResponse(
            {'error': 'Sociedad no encontrada'},
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'error': f'Error interno del servidor: {str(e)}'},
            status=500
        ) 