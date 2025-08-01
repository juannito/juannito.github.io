from rest_framework import serializers
from spider.models.mercury_onboarding import MercuryOnboarding
from spider.models.sociedad import Sociedad


class MercuryOnboardingSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MercuryOnboarding"""
    
    class Meta:
        model = MercuryOnboarding
        fields = [
            'id', 'sociedad', 'onboarding_data_id', 'signup_link', 
            'status', 'account_number', 'routing_number', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SocietySnapshotSerializer(serializers.Serializer):
    """Serializer para el endpoint de snapshot de sociedad"""
    
    success = serializers.BooleanField(default=True)
    data = serializers.DictField()


class MercuryOnboardingDataSerializer(serializers.Serializer):
    """Serializer para los datos de onboarding de Mercury"""
    
    partner = serializers.CharField()
    about = serializers.DictField()
    businessContactDetails = serializers.DictField()
    formationDetails = serializers.DictField()
    businessLegalAddress = serializers.DictField(allow_null=True)
    businessPhysicalAddress = serializers.DictField(allow_null=True)
    beneficialOwners = serializers.ListField(child=serializers.DictField())
    applicationType = serializers.CharField()


class MercurySubmitResponseSerializer(serializers.Serializer):
    """Serializer para la respuesta del endpoint de submit"""
    
    success = serializers.BooleanField(default=True)
    data = serializers.DictField()


class MercuryWebhookSerializer(serializers.Serializer):
    """Serializer para los webhooks de Mercury"""
    
    event = serializers.CharField()
    onboardingDataId = serializers.CharField()
    accountStatus = serializers.CharField(required=False, allow_blank=True)
    accountNumber = serializers.CharField(required=False, allow_blank=True)
    routingNumber = serializers.CharField(required=False, allow_blank=True)


class MercuryStatusSerializer(serializers.Serializer):
    """Serializer para el estado de Mercury"""
    
    success = serializers.BooleanField(default=True)
    data = serializers.DictField() 