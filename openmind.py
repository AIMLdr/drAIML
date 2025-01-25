# openmind.py
import os
import time
import logging
import httpx
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv, set_key

class OpenMind:
    """
    Enhanced OpenMind system for managing API keys, models, and medical AI interactions
    with comprehensive error logging and file handling
    """
    
    def __init__(self):
        self.env_file = '.env'
        self.api_keys = {}  # Initialize empty and load through method
        self.agi_instance = None
        self.initialization_warning_shown = False
        
        # Initialize memory structure
        self.memory_structure = {
            'root': './memory',
            'folders': {
                'logs': './memory/logs',
                'medical': './memory/medical',
                'api': './memory/api',
                'models': './memory/models',
                'stm': './memory/stm',
                'ltm': './memory/ltm',
                'errors': './memory/logs/errors'
            }
        }
        
        try:
            # Create directories first
            self._initialize_memory()
            # Setup logging after directories exist
            self.logger = self._setup_logger()
            # Load API keys after logging is setup
            self.api_keys = self._load_env()
        except Exception as e:
            print(f"Critical initialization error: {e}")
            raise

    def _setup_logger(self) -> logging.Logger:
        """Initialize comprehensive logging system"""
        logger = logging.getLogger('OpenMind')
        logger.setLevel(logging.DEBUG)

        # Ensure log directory exists
        log_dir = self.memory_structure['folders']['logs']
        error_dir = self.memory_structure['folders']['errors']
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(error_dir, exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handlers
        handlers = {
            'debug_file': logging.FileHandler(os.path.join(log_dir, 'debug.log')),
            'error_file': logging.FileHandler(os.path.join(error_dir, 'error.log')),
            'api_file': logging.FileHandler(os.path.join(log_dir, 'api.log')),
            'stream': logging.StreamHandler()
        }

        # Configure handlers
        handlers['debug_file'].setLevel(logging.DEBUG)
        handlers['error_file'].setLevel(logging.ERROR)
        handlers['api_file'].setLevel(logging.INFO)
        handlers['stream'].setLevel(logging.INFO)

        # Set formatters
        handlers['debug_file'].setFormatter(detailed_formatter)
        handlers['error_file'].setFormatter(detailed_formatter)
        handlers['api_file'].setFormatter(simple_formatter)
        handlers['stream'].setFormatter(simple_formatter)

        # Add handlers to logger
        for handler in handlers.values():
            logger.addHandler(handler)

        return logger

    def _initialize_memory(self):
        """Initialize memory structure"""
        try:
            for folder in self.memory_structure['folders'].values():
                os.makedirs(folder, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to create memory structure: {e}")

    def _load_env(self) -> Dict[str, str]:
        """Load API keys from environment file"""
        try:
            load_dotenv(self.env_file)
            keys = {
                'together': os.getenv('TOGETHER_API_KEY'),
                'groq': os.getenv('GROQ_API_KEY'),
                'openai': os.getenv('OPENAI_API_KEY')
            }
            self.logger.debug(f"Loaded API keys for services: {', '.join(k for k, v in keys.items() if v)}")
            return keys
        except Exception as e:
            self.logger.error(f"Error loading environment variables: {e}")
            return {}

    def load_oath(self) -> Optional[str]:
        """Load Dr. AIML's oath from oath.txt"""
        try:
            with open("oath.txt", "r", encoding="utf-8") as f:
                oath_text = f.read()
                self.logger.debug("Successfully loaded oath.txt")
                return oath_text
        except FileNotFoundError:
            self.logger.error("oath.txt not found in current directory")
            return None
        except Exception as e:
            self.logger.error(f"Error loading oath.txt: {e}")
            return None

    def load_prompt(self) -> Optional[str]:
        """Load Dr. AIML's prompt from prompt.txt"""
        try:
            with open("prompt.txt", "r", encoding="utf-8") as f:
                prompt_text = f.read()
                self.logger.debug("Successfully loaded prompt.txt")
                return prompt_text
        except FileNotFoundError:
            self.logger.error("prompt.txt not found in current directory")
            return None
        except Exception as e:
            self.logger.error(f"Error loading prompt.txt: {e}")
            return None

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
            
        except Exception as e:
            self.logger.error(f"Error saving API key for {service}: {e}")
            raise

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for specified service"""
        key = self.api_keys.get(service.lower())
        if not key:
            self.logger.warning(f"No API key found for service: {service}")
        return key

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

    def _log_api_change(self, service: str, action: str):
        """Log API key changes"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "action": action
            }
            
            log_file = os.path.join(self.memory_structure['folders']['api'], 'api_changes.json')
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
                        self.logger.warning(f"Invalid JSON in {filepath}, starting new log")
                        data = []
                    data.append(entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
            else:
                with open(filepath, 'w') as f:
                    json.dump([entry], f, indent=2)
            
            self.logger.debug(f"Successfully appended to log: {filepath}")
                    
        except Exception as e:
            self.logger.error(f"Error appending to JSON log {filepath}: {e}")

    def get_error_logs(self, days: int = 7) -> List[Dict]:
        """Retrieve recent error logs"""
        try:
            error_log = os.path.join(self.memory_structure['folders']['errors'], 'error.log')
            if not os.path.exists(error_log):
                return []

            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            errors = []

            with open(error_log, 'r') as f:
                for line in f:
                    try:
                        # Parse log line
                        timestamp_str = line.split(' - ')[0]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                        
                        if timestamp.timestamp() > cutoff_time:
                            errors.append({
                                'timestamp': timestamp_str,
                                'message': line.strip()
                            })
                    except Exception as e:
                        self.logger.error(f"Error parsing log line: {e}")
                        continue

            return errors

        except Exception as e:
            self.logger.error(f"Error retrieving error logs: {e}")
            return []

    def cleanup_old_logs(self, days: int = 30):
        """Clean up old log files"""
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            for folder in self.memory_structure['folders'].values():
                if not os.path.exists(folder):
                    continue
                    
                for filename in os.listdir(folder):
                    filepath = os.path.join(folder, filename)
                    if os.path.isfile(filepath):
                        file_time = os.path.getmtime(filepath)
                        if file_time < cutoff_time:
                            # Archive instead of delete
                            archive_path = os.path.join(
                                self.memory_structure['folders']['ltm'],
                                f"archived_{filename}"
                            )
                            os.rename(filepath, archive_path)
                            self.logger.info(f"Archived old log file: {filename}")
                            
        except Exception as e:
            self.logger.error(f"Error cleaning up old logs: {e}")
