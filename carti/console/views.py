from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import RequestLog, OperationStatus
import json
from datetime import datetime, timedelta

@login_required
@permission_classes([IsAdminUser])
def console_view(request):
    """
    Vue principale de la console d'administration
    """
    # Récupérer les logs des dernières 24 heures par défaut
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    # Filtrer par date si spécifié
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d')
    
    # Récupérer les logs
    logs = RequestLog.objects.filter(
        timestamp__range=(start_date, end_date)
    ).order_by('-timestamp')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(logs, 50)  # 50 logs par page
    logs_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total_requests': logs.count(),
        'success_rate': logs.filter(status_code__lt=400).count() / logs.count() * 100 if logs.count() > 0 else 0,
        'error_rate': logs.filter(status_code__gte=400).count() / logs.count() * 100 if logs.count() > 0 else 0,
        'avg_response_time': logs.aggregate(avg_time=Avg('response_time'))['avg_time'] or 0
    }
    
    context = {
        'logs': logs_page,
        'stats': stats,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    return render(request, 'console/dashboard.html', context)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_log_details(request, log_id):
    """
    API endpoint pour récupérer les détails d'un log spécifique
    """
    log = get_object_or_404(RequestLog, id=log_id)
    return JsonResponse({
        'id': str(log.id),
        'timestamp': log.timestamp,
        'method': log.method,
        'endpoint': log.endpoint,
        'status_code': log.status_code,
        'response_time': log.response_time,
        'request_data': log.request_data,
        'response_data': log.response_data,
        'user': log.user.username if log.user else None,
        'ip_address': log.ip_address
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_operation_status(request):
    """
    API endpoint pour récupérer le statut des opérations en temps réel
    """
    operation_id = request.GET.get('operation_id')
    
    if operation_id:
        status = OperationStatus.objects.filter(operation_id=operation_id).first()
        if status:
            return JsonResponse({
                'operation_id': status.operation_id,
                'status': status.status,
                'progress': status.progress,
                'message': status.message,
                'timestamp': status.timestamp
            })
        return JsonResponse({'error': 'Operation not found'}, status=404)
    
    # Récupérer tous les statuts actifs
    active_operations = OperationStatus.objects.filter(
        status__in=['PENDING', 'IN_PROGRESS']
    ).order_by('-timestamp')
    
    return JsonResponse({
        'operations': [{
            'operation_id': op.operation_id,
            'status': op.status,
            'progress': op.progress,
            'message': op.message,
            'timestamp': op.timestamp
        } for op in active_operations]
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def search_logs(request):
    """
    API endpoint pour rechercher dans les logs
    """
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status_code = request.GET.get('status_code')
    
    logs = RequestLog.objects.all()
    
    if query:
        logs = logs.filter(
            Q(endpoint__icontains=query) |
            Q(method__icontains=query) |
            Q(request_data__icontains=query) |
            Q(response_data__icontains=query)
        )
    
    if start_date:
        logs = logs.filter(timestamp__gte=start_date)
    if end_date:
        logs = logs.filter(timestamp__lte=end_date)
    if status_code:
        logs = logs.filter(status_code=status_code)
    
    logs = logs.order_by('-timestamp')[:100]  # Limiter à 100 résultats
    
    return JsonResponse({
        'logs': [{
            'id': log.id,
            'timestamp': log.timestamp,
            'method': log.method,
            'endpoint': log.endpoint,
            'status_code': log.status_code,
            'response_time': log.response_time,
            'request_data': log.request_data,
            'response_data': log.response_data
        } for log in logs]
    }) 