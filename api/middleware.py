import re
from django.http import HttpResponseForbidden
from django.conf import settings


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for suspicious patterns in request
        if self._is_suspicious_request(request):
            return HttpResponseForbidden("Suspicious request detected")
        
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

    def _is_suspicious_request(self, request):
        """Check for suspicious patterns in the request"""
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
            r'../',
            r'\.\./',
            r'%2e%2e%2f',
            r'%252e%252e%252f',
        ]
        
        # Check URL
        url = request.get_full_path()
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        # Check POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if isinstance(value, str):
                    for pattern in suspicious_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            return True
        
        return False


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}

    def __call__(self, request):
        # Simple rate limiting by IP
        client_ip = self._get_client_ip(request)
        
        if self._is_rate_limited(client_ip):
            return HttpResponseForbidden("Rate limit exceeded")
        
        response = self.get_response(request)
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _is_rate_limited(self, client_ip):
        # Simple in-memory rate limiting (use Redis in production)
        import time
        current_time = time.time()
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Remove requests older than 1 hour
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < 3600
        ]
        
        # Check if too many requests
        if len(self.request_counts[client_ip]) >= 100:  # 100 requests per hour
            return True
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        return False 