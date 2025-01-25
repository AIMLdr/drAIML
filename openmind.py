# openmind.py
import os
import time
import logging
import httpx
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv, set_key
from memory import create_memory_folders, store_in_stm, DialogEntry

class OpenMind:
    """
    Enhanced OpenMind system for managing API keys, models, and medical AI interactions
    Integrates with drAIML for comprehensive medical consultation management
    """
    
    def __init__(self):
        self.env_file = '.env'
        self.api_keys = self._load_env()
        self.agi_instance = None
        self.initialization_warning_shown = False
        self.logger = self._setup_logger()
        self.message_container = None
        self.internal_queue = asyncio.Queue()
        self.prompt = ""
        
        # Initialize memory structure
        self.memory_paths = {
            'logs': './memory/logs',
            'medical': './memory/medical',
            'api': './memory/api',
            'models': './memory/models',
            'stm': './memory/stm',
            'ltm': './memory/ltm'
        }
        self._initialize_memory()

    def _setup_logger(self) -> logging.Logger:
        """Initialize comprehensive logging system"""
        logger = logging.getLogger('OpenMind')
        logger.setLevel(logging.DEBUG)

        # Create handlers
        for path in self.memory_paths.values():
            os.makedirs(path, exist_ok=True)

        handlers = {
            'file': logging.FileHandler('./memory/logs/openmind.log'),
            'api': logging.FileHandler('./memory/logs/api.log'),
            'model': logging.FileHandler('./memory/logs/model.log'),
            'medical': logging.FileHandler('./memory/logs/medical.log'),
            'stream': logging.StreamHandler()
        }

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        for handler in handlers.values():
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_memory(self):
        """Initialize memory structure and create necessary folders"""
        create_memory_folders()
        for path in self.memory_paths.values():
            os.makedirs(path, exist_ok=True)

    def _load_env(self) -> Dict[str, str]:
        """Load API keys from environment file"""
        load_dotenv(self.env_file)
        return {
            'together': os.getenv('TOGETHER_API_KEY'),
            'groq': os.getenv('GROQ_API_KEY'),
            'openai': os.getenv('OPENAI_API_KEY')
        }

    def save_api_key(self, service: str, key: str):
        """Save API key to environment file and update current session"""
        try:
            service_upper = service.upper()
            env_var = f"{service_upper}_API_KEY"
            
            # Save to env file
            set_key(self.env_file, env_var, key)
            
            # Update current session
            self.api_keys[service.lower()] = key
            
            # Log API key update (safely)
            self.logger.info(f"API key updated for service: {service}")
            self._log_api_change(service, "key_updated")
            
            # Initialize AGI if needed
            self.initialize_agi()
            
        except Exception as e:
            self.logger.error(f"Error saving API key for {service}: {e}")
            raise

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for specified service"""
        return self.api_keys.get(service.lower())

    def remove_api_key(self, service: str):
        """Remove API key for specified service"""
        try:
            service_upper = service.upper()
            env_var = f"{service_upper}_API_KEY"
            
            # Remove from env file
            set_key(self.env_file, env_var, "")
            
            # Remove from current session
            self.api_keys.pop(service.lower(), None)
            
            # Log removal
            self.logger.info(f"API key removed for service: {service}")
            self._log_api_change(service, "key_removed")
            
        except Exception as e:
            self.logger.error(f"Error removing API key for {service}: {e}")
            raise

    async def initialize_agi(self):
        """Initialize AGI system with appropriate model"""
        try:
            # Check available models
            model_status = self.get_model_status()
            
            # Try to initialize in order of preference
            for service in ['openai', 'groq', 'together', 'ollama']:
                if model_status[service]['available']:
                    self.agi_instance = await self._initialize_model(service)
                    if self.agi_instance:
                        self.logger.info(f"AGI initialized with {service}")
                        return True
            
            if not self.initialization_warning_shown:
                self.logger.warning("No valid API key or model found")
                self.initialization_warning_shown = True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error initializing AGI: {e}")
            return False

    async def _initialize_model(self, service: str):
        """Initialize specific model based on service"""
        try:
            if service == 'ollama':
                if self._check_ollama_running():
                    from chatter import OllamaHandler
                    return OllamaHandler()
            else:
                api_key = self.get_api_key(service)
                if api_key:
                    if service == 'openai':
                        from chatter import GPT4o
                        return GPT4o(api_key)
                    elif service == 'groq':
                        from chatter import GroqModel
                        return GroqModel(api_key)
                    elif service == 'together':
                        from chatter import TogetherModel
                        return TogetherModel(api_key)
            return None
        except Exception as e:
            self.logger.error(f"Error initializing {service} model: {e}")
            return None

    async def process_medical_query(self, query: str) -> Dict:
        """Process medical query and generate response"""
        try:
            if not self.agi_instance:
                await self.initialize_agi()
                
            if not self.agi_instance:
                return {"error": "No available AI model"}

            # Process query
            response = await self.agi_instance.generate_response(query)
            
            # Store interaction
            dialog_entry = DialogEntry(query, response)
            store_in_stm(dialog_entry)
            
            # Log interaction
            self._log_medical_interaction(query, response)
            
            return {
                "query": query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error processing medical query: {e}")
            return {"error": str(e)}

    def _log_medical_interaction(self, query: str, response: str):
        """Log medical interaction"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response,
                "model": type(self.agi_instance).__name__
            }
            
            log_file = os.path.join(self.memory_paths['medical'], 'interactions.json')
            self._append_to_json_log(log_file, log_entry)
            
        except Exception as e:
            self.logger.error(f"Error logging medical interaction: {e}")

    def _check_ollama_running(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = httpx.get('http://localhost:11434')
            return response.status_code == 200
        except Exception:
            return False

    def get_model_status(self) -> Dict[str, Dict]:
        """Get status of all configured models"""
        status = {}
        for service in ['together', 'groq', 'openai', 'ollama']:
            status[service] = self.check_model_availability(service)
        return status

    def check_model_availability(self, model_name: str) -> Dict[str, Union[bool, str]]:
        """Check if a specific model is available"""
        result = {
            "available": False,
            "status": "",
            "error": None
        }
        
        try:
            if model_name.lower() == "ollama":
                result["available"] = self._check_ollama_running()
                result["status"] = "running" if result["available"] else "not running"
            else:
                api_key = self.get_api_key(model_name.lower())
                result["available"] = bool(api_key)
                result["status"] = "configured" if result["available"] else "no api key"
                
        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"Error checking model availability for {model_name}: {e}")
            
        return result

    def load_oath(self) -> Optional[str]:
        """Load Dr. AIML's oath"""
        try:
            with open("oath.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error("oath.txt not found")
            return None
        except Exception as e:
            self.logger.error(f"Error loading oath: {e}")
            return None

    def load_prompt(self) -> Optional[str]:
        """Load Dr. AIML's prompt"""
        try:
            with open("prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error("prompt.txt not found")
            return None
        except Exception as e:
            self.logger.error(f"Error loading prompt: {e}")
            return None

    def _log_api_change(self, service: str, action: str):
        """Log API key changes"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "action": action
            }
            
            log_file = os.path.join(self.memory_paths['api'], 'api_changes.json')
            self._append_to_json_log(log_file, log_entry)
            
        except Exception as e:
            self.logger.error(f"Error logging API change: {e}")

    def _append_to_json_log(self, filepath: str, entry: Dict):
        """Append entry to JSON log file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r+') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
                    data.append(entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
            else:
                with open(filepath, 'w') as f:
                    json.dump([entry], f, indent=2)
                    
        except Exception as e:
            self.logger.error(f"Error appending to JSON log {filepath}: {e}")

    async def check_api_health(self) -> Dict[str, str]:
        """Check health of all API endpoints"""
        health_status = {}
        for service in self.api_keys:
            if self.api_keys[service]:
                status = await self._check_service_health(service)
                health_status[service] = status
        return health_status

    async def _check_service_health(self, service: str) -> str:
        """Check health of specific API service"""
        try:
            if service == 'ollama':
                return "healthy" if self._check_ollama_running() else "unhealthy"
            
            # Basic API key validation
            api_key = self.get_api_key(service)
            return "healthy" if api_key else "unconfigured"
            
        except Exception as e:
            self.logger.error(f"Health check failed for {service}: {e}")
            return "unhealthy"

    def cleanup_old_logs(self, days_threshold: int = 30):
        """Clean up old log files"""
        try:
            current_time = datetime.now()
            
            for path in self.memory_paths.values():
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                        if (current_time - file_time).days > days_threshold:
                            os.remove(file_path)
                            self.logger.info(f"Removed old log file: {file_path}")
                            
        except Exception as e:
            self.logger.error(f"Error cleaning up logs: {e}")
