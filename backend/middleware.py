
from fastapi import Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Rate limiting par IP
        client_ip = request.client.host
        now = datetime.now()
        
        # Nettoyer les anciennes requêtes
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Vérifier la limite
        if len(self.requests[client_ip]) >= self.rate_limit:
            raise HTTPException(status_code=429, detail="Trop de requêtes")
        
        # Enregistrer la requête
        self.requests[client_ip].append(now)
        
        # Headers de sécurité
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        from logger import logger
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"IP: {request.client.host}"
        )
        
        return response
