
import logging
import sys
from datetime import datetime
import os

def setup_logger(name: str = "smartsaas", level: str = "INFO"):
    """Configure le système de logging"""
    
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Éviter les doublons
    if logger.handlers:
        return logger
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour fichier (si en production)
    if not os.getenv("DEBUG", "False").lower() == "true":
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger global
logger = setup_logger()
