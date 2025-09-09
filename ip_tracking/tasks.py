from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP, RequestLog

@shared_task
def flag_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Count requests per IP in the last hour
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1


    print("my array", ip_counts)
    # Flag IPs exceeding 5 requests/hour (adjust if needed)
    for ip, count in ip_counts.items():
        if count > 5:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={"reason": f"{count} requests in the last hour"}
            )

    # Flag IPs accessing sensitive paths
    sensitive_paths = ["/admin", "/login"]
    sensitive_logs = logs.filter(path__in=sensitive_paths)
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            defaults={"reason": f"Accessed sensitive path: {log.path}"}
        )
