# openmind.py (c) 2024 Gregory L. Magnusson MIT license

import os
import time
import httpx
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv, set_key, find_dotenv
from logger import get_logger
from pathlib import Path

class OpenMind:
    """Central configuration and resource management for drAIML"""
    
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenMind, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.env_file = '.env'
        self.api_keys = {}
        self.agi_instance = None
        self.logger = get_logger('openmind')
        
        # Define base paths
        self.base_path = Path(__file__).parent
        
        # System resources paths (in project root)
        self.system_resources = {
            'prompt': str(self.base_path / 'prompt.txt'),
            'oath': str(self.base_path / 'oath.txt'),
            'system_prompt': str(self.base_path / 'prompt.txt')  # Using prompt.txt as system prompt
        }
        
        # Memory structure
        self.memory_structure = {
            'root': str(self.base_path / 'memory'),
            'folders': {
                'logs': str(self.base_path / 'memory/logs'),
                'medical': str(self.base_path / 'memory/medical'),
                'api': str(self.base_path / 'memory/api'),
                'models': str(self.base_path / 'memory/models'),
                'stm': str(self.base_path / 'memory/stm'),
                'ltm': str(self.base_path / 'memory/ltm'),
                'errors': str(self.base_path / 'memory/logs/errors'),
                'audit': str(self.base_path / 'memory/logs/audit'),
                'sessions': str(self.base_path / 'memory/sessions')
            }
        }
        
        # Resource cache
        self._resource_cache = {}
        
        # Session tracking
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "api_operations": [],
            "resources_loaded": set(),
            "errors": []
        }
        
        try:
            self._initialize_system()
        except Exception as e:
            self.logger.error("Critical initialization error", 
                            extra={'structured_data': {'error': str(e)}})
            raise

    def _initialize_system(self):
        """Initialize complete system"""
        try:
            # Create directory structure
            self._initialize_memory()
            
            # Verify resources exist
            self._verify_resources()
            
            # Ensure .env file exists
            env_path = Path(self.env_file)
            if not env_path.exists():
                env_path.touch()
            
            # Load API keys
            self.api_keys = self._load_env()
            
            self.logger.info("System initialized successfully", 
                           extra={'structured_data': {
                               'session_id': self.current_session["session_id"]
                           }})
            
        except Exception as e:
            self.logger.error("System initialization failed", 
                            extra={'structured_data': {'error': str(e)}})
            raise

    def _initialize_memory(self):
        """Initialize memory structure"""
        try:
            created_folders = []
            for folder in self.memory_structure['folders'].values():
                os.makedirs(folder, exist_ok=True)
                created_folders.append(folder)
            
            self.logger.info("Memory structure initialized", 
                           extra={'structured_data': {
                               'created_folders': created_folders
                           }})
            
        except Exception as e:
            self.logger.error("Failed to create memory structure", 
                            extra={'structured_data': {'error': str(e)}})
            raise

    def _verify_resources(self):
        """Verify system resources exist"""
        try:
            missing_resources = []
            for resource_name, resource_path in self.system_resources.items():
                if not os.path.exists(resource_path):
                    missing_resources.append(resource_name)
            
            if missing_resources:
                raise FileNotFoundError(
                    f"Missing required resource files: {', '.join(missing_resources)}"
                )
            
            self.logger.info("Resource verification completed")
            
        except Exception as e:
            self.logger.error("Resource verification failed", 
                            extra={'structured_data': {'error': str(e)}})
            raise

    def _load_env(self) -> Dict[str, str]:
        """Load environment variables and API keys"""
        try:
            # Force reload the .env file
            dotenv_path = find_dotenv(self.env_file)
            load_dotenv(dotenv_path, override=True)
            
            keys = {
                'together': os.getenv('TOGETHER_API_KEY'),
                'groq': os.getenv('GROQ_API_KEY'),
                'openai': os.getenv('OPENAI_API_KEY')
            }
            
            # Set environment variables
            for service, key in keys.items():
                if key:
                    os.environ[f"{service.upper()}_API_KEY"] = key
            
            loaded_services = [k for k, v in keys.items() if v]
            self.logger.info("API keys loaded", 
                           extra={'structured_data': {
                               'services': loaded_services
                           }})
            
            # Update instance cache
            self.api_keys = keys
            
            return keys
            
        except Exception as e:
            self.logger.error("Error loading environment variables", 
                            extra={'structured_data': {'error': str(e)}})
            return {}

    def get_system_prompt(self) -> Optional[str]:
        """Get system prompt for models"""
        return self._load_resource('prompt')

    def get_oath(self) -> Optional[str]:
        """Get Hippocratic oath"""
        return self._load_resource('oath')

    def _load_resource(self, resource_name: str) -> Optional[str]:
        """Load a system resource with caching"""
        try:
            # Check cache first
            if resource_name in self._resource_cache:
                return self._resource_cache[resource_name]
            
            # Load from file
            resource_path = self.system_resources.get(resource_name)
            if not resource_path:
                self.logger.error(f"Unknown resource: {resource_name}")
                return None
                
            if not os.path.exists(resource_path):
                self.logger.error(f"Resource file not found: {resource_path}")
                return None
                
            with open(resource_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                self._resource_cache[resource_name] = content
                
                # Track resource loading
                self.current_session["resources_loaded"].add(resource_name)
                
                self.logger.debug(f"Resource loaded: {resource_name}", 
                                extra={'structured_data': {
                                    'resource': resource_name,
                                    'size': len(content)
                                }})
                return content
                
        except Exception as e:
            self.logger.error(f"Error loading resource: {resource_name}", 
                            extra={'structured_data': {'error': str(e)}})
            self.current_session["errors"].append({
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "resource": resource_name
            })
            return None

    def save_api_key(self, service: str, key: str):
        """Save API key with validation"""
        try:
            service_upper = service.upper()
            env_var = f"{service_upper}_API_KEY"
            
            # Validate key format
            if not self._validate_api_key(service, key):
                raise ValueError(f"Invalid API key format for {service}")
            
            # Save to env file
            set_key(self.env_file, env_var, key)
            
            # Set environment variable
            os.environ[env_var] = key
            
            # Update current session
            self.api_keys[service.lower()] = key
            
            # Force reload environment
            load_dotenv(self.env_file, override=True)
            
            # Track operation
            self.current_session["api_operations"].append({
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "action": "key_updated"
            })
            
            self.logger.info("API key updated", 
                           extra={'structured_data': {
                               'service': service,
                               'action': 'key_updated'
                           }})
            
            self._log_api_change(service, "key_updated")
            
        except Exception as e:
            self.logger.error("Error saving API key", 
                            extra={'structured_data': {
                                'service': service,
                                'error': str(e)
                            }})
            raise

    def _validate_api_key(self, service: str, key: str) -> bool:
        """Validate API key format"""
        try:
            if not key:
                return False
                
            # Service-specific validation
            if service.lower() == 'openai':
                return key.startswith('sk-') and len(key) > 20
            elif service.lower() == 'together':
                return len(key) > 20
            elif service.lower() == 'groq':
                return len(key) > 20
                
            return True
            
        except Exception as e:
            self.logger.error("Error validating API key", 
                            extra={'structured_data': {
                                'service': service,
                                'error': str(e)
                            }})
            return False

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key with logging"""
        # Force reload environment variables
        self._load_env()
        
        key = self.api_keys.get(service.lower())
        if not key:
            self.logger.warning("API key not found", 
                              extra={'structured_data': {'service': service}})
        return key

    def remove_api_key(self, service: str):
        """Remove API key with cleanup"""
        try:
            service_upper = service.upper()
            env_var = f"{service_upper}_API_KEY"
            
            # Remove from env file
            set_key(self.env_file, env_var, "")
            
            # Remove from environment
            if env_var in os.environ:
                del os.environ[env_var]
            
            # Remove from current session
            self.api_keys.pop(service.lower(), None)
            
            # Force reload environment
            load_dotenv(self.env_file, override=True)
            
            # Track operation
            self.current_session["api_operations"].append({
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "action": "key_removed"
            })
            
            self.logger.info("API key removed", 
                           extra={'structured_data': {
                               'service': service,
                               'action': 'key_removed'
                           }})
            
            self._log_api_change(service, "key_removed")
            
        except Exception as e:
            self.logger.error("Error removing API key", 
                            extra={'structured_data': {
                                'service': service,
                                'error': str(e)
                            }})
            raise

    def _log_api_change(self, service: str, action: str):
        """Log API key changes"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "action": action,
                "session_id": self.current_session["session_id"]
            }
            
            log_file = os.path.join(
                self.memory_structure['folders']['api'], 
                'api_changes.json'
            )
            
            self._append_to_json_log(log_file, log_entry)
            
        except Exception as e:
            self.logger.error("Error logging API change", 
                            extra={'structured_data': {
                                'service': service,
                                'action': action,
                                'error': str(e)
                            }})

    def _append_to_json_log(self, filepath: str, entry: Dict):
        """Append entry to JSON log file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r+') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        self.logger.warning(f"Invalid JSON in {filepath}, starting new log")
                        data = []
                    data.append(entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
            else:
                with open(filepath, 'w') as f:
                    json.dump([entry], f, indent=2)
            
            self.logger.debug("Successfully appended to log", 
                            extra={'structured_data': {'filepath': filepath}})
                    
        except Exception as e:
            self.logger.error("Error appending to JSON log", 
                            extra={'structured_data': {
                                'filepath': filepath,
                                'error': str(e)
                            }})

    def get_session_status(self) -> Dict:
        """Get current session status"""
        try:
            return {
                "session_id": self.current_session["session_id"],
                "start_time": self.current_session["start_time"],
                "duration": (datetime.now() - datetime.fromisoformat(
                    self.current_session["start_time"]
                )).total_seconds(),
                "api_operations": len(self.current_session["api_operations"]),
                "resources_loaded": list(self.current_session["resources_loaded"]),
                "error_count": len(self.current_session["errors"]),
                "active_services": [k for k, v in self.api_keys.items() if v]
            }
        except Exception as e:
            self.logger.error("Error getting session status", 
                            extra={'structured_data': {'error': str(e)}})
            return {}
