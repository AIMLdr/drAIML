# config/__init__.py

import os
import yaml
from pathlib import Path
from typing import Dict, Optional
from logger import get_logger

class ModelConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.logger = get_logger('model_config')
        self.config_path = Path(__file__).parent / 'config.yaml'
        self.models = self._load_config()

    def _load_config(self) -> Dict:
        """Load model configuration from YAML"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.logger.info("Model configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Error loading model configuration: {e}")
            return {}

    def get_provider_models(self, provider: str) -> Dict:
        """Get models for specific provider"""
        return self.models.get(provider.lower(), {})

    def get_model_info(self, provider: str, model_id: str) -> Optional[Dict]:
        """Get specific model information"""
        provider_models = self.get_provider_models(provider)
        return provider_models.get(model_id)

    def get_default_model(self, provider: str) -> Optional[str]:
        """Get default model for provider"""
        provider_models = self.get_provider_models(provider)
        if not provider_models:
            return None
        return next(iter(provider_models.keys()))

# Global instance
model_config = ModelConfig()

# Convenience functions
def get_provider_models(provider: str) -> Dict:
    """Get models for specific provider"""
    return model_config.get_provider_models(provider)

def get_model_info(provider: str, model_id: str) -> Optional[Dict]:
    """Get specific model info"""
    return model_config.get_model_info(provider, model_id)

# Export these names
__all__ = [
    'ModelConfig',
    'model_config',
    'get_provider_models',
    'get_model_info'
]
