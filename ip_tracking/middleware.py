from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.cache import cache
import requests
from .models import RequestLog, BlockedIP

class RequestLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path
        timestamp = timezone.now()

        # Block IPs first
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Get geolocation from cache or API
        location = cache.get(ip_address)
        if location is None:
            location = self.get_geolocation(ip_address)
            if location:
                cache.set(ip_address, location, timeout=86400)  # 24 hours cache

        # Ensure location is a dictionary with country and city keys
        country = location.get("country") if location else None
        city = location.get("city") if location else None

        # Save log to DB
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=timestamp,
            path=path,
            country=country,
            city=city
        )

    def get_client_ip(self, request):
        """Retrieve client IP from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geolocation(self, ip_address):
        """
        Get geolocation information using ip-api.com.
        Returns a dictionary with keys: 'country' and 'city'.
        """
        try:
            url = f"http://ip-api.com/json/{ip_address}?fields=country,city,status"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(data)
            if data.get("status") == "success":
                return {"country": data.get("country"), "city": data.get("city")}
            else:
                return {"country": None, "city": None}
        except requests.RequestException:
            # Fail silently if API fails
            return {"country": None, "city": None}
