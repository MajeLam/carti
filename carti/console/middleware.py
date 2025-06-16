import time
import json
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware pour logger toutes les requêtes API
    """
    
    def process_request(self, request):
        # Stocker le temps de début
        request.start_time = time.time()
        
        # Ne logger que les requêtes API
        if not request.path.startswith('/api/'):
            return None
            
        # Stocker les données de la requête
        request.request_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request.request_data = json.loads(request.body)
            except:
                request.request_data = request.POST.dict()
    
    def process_response(self, request, response):
        # Ne logger que les requêtes API
        if not request.path.startswith('/api/'):
            return response
            
        # Calculer le temps de réponse
        duration = time.time() - request.start_time
        
        # Créer le log
        RequestLog.objects.create(
            method=request.method,
            endpoint=request.path,
            status_code=response.status_code,
            response_time=duration * 1000,  # Convertir en millisecondes
            request_data=request.request_data,
            response_data=self._get_response_data(response),
            user=request.user if request.user.is_authenticated else None,
            ip_address=self._get_client_ip(request)
        )
        
        return response
    
    def _get_response_data(self, response):
        """
        Extraire les données de la réponse
        """
        try:
            if hasattr(response, 'content'):
                return json.loads(response.content)
        except:
            pass
        return None
    
    def _get_client_ip(self, request):
        """
        Obtenir l'adresse IP du client
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 