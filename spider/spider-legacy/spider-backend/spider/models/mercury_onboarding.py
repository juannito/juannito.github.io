from django.db import models
from django.utils import timezone
from spider.models.sociedad import Sociedad


class MercuryOnboarding(models.Model):
    """
    Modelo para tracking del proceso de onboarding de Mercury
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('signed_up', 'Signed Up'),
        ('submitted', 'Submitted'),
        ('information_requested', 'Information Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.CharField(max_length=255, primary_key=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, related_name='mercury_onboardings')
    onboarding_data_id = models.CharField(max_length=255, unique=True)
    signup_link = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    account_number = models.CharField(max_length=50, null=True, blank=True)
    routing_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mercury_onboarding'
        verbose_name = 'Mercury Onboarding'
        verbose_name_plural = 'Mercury Onboardings'
    
    def __str__(self):
        return f"Mercury Onboarding {self.id} - {self.sociedad.nombre} ({self.status})"
    
    @property
    def is_completed(self):
        """Retorna True si el onboarding está completado (approved o rejected)"""
        return self.status in ['approved', 'rejected']
    
    @property
    def is_approved(self):
        """Retorna True si la cuenta fue aprobada"""
        return self.status == 'approved' 