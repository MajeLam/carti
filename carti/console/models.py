from django.db import models
from django.conf import settings
import uuid

class RequestLog(models.Model):
    """
    Modèle pour stocker les logs des requêtes API
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    status_code = models.IntegerField()
    response_time = models.FloatField()  # en millisecondes
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['status_code']),
            models.Index(fields=['method']),
            models.Index(fields=['endpoint']),
        ]

class OperationStatus(models.Model):
    """
    Modèle pour suivre le statut des opérations longues
    """
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Terminé'),
        ('FAILED', 'Échoué'),
    ]
    
    operation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    progress = models.IntegerField(default=0)  # Pourcentage de progression
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50)
    details = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['operation_type']),
            models.Index(fields=['user']),
        ] 