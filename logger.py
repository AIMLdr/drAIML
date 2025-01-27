# logger.py (c) 2025 Gregory L. Magnusson MIT license

import logging
import logging.handlers
import os
from typing import Dict, Optional, Any, Union, List
from datetime import datetime
import json
import gzip
import shutil
from pathlib import Path
from functools import lru_cache

class DrAIMLLogger:
    """Enhanced centralized logging system for drAIML"""
    
    _instance = None  # Singleton instance
    
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DrAIMLLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.log_structure = {
            'root': './memory',
            'folders': {
                'errors': './memory/errors',      # Error logs and exceptions
                'stm': './memory/stm',           # Short-term memory (conversations)
                'ltm': './memory/ltm',           # Long-term memory (future use)
                'reasoning': './memory/reasoning' # Decisions, validation, medical
            },
            'files': {
                'errors': {
                    'system': 'system_errors.log',
                    'api': 'api_errors.log',
                    'chat': 'chat_errors.log'
                },
                'stm': {
                    'interactions': 'interactions.json',
                    'context': 'context.json',
                    'session': 'session.log'
                },
                'reasoning': {
                    'decisions': 'decisions.json',
                    'validation': 'validation.log',
                    'medical': 'medical.json',
                    'analytics': 'analytics.json'
                }
            }
        }
        
        # Initialize logging system
        self._initialize_logging()

    def _initialize_logging(self):
        """Initialize complete logging system with verification"""
        try:
            # Create and verify directory structure
            self._create_log_structure()
            
            # Configure root logger with reduced output
            logging.basicConfig(
                level=logging.WARNING,  # Increase base level to reduce noise
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Configure external loggers to minimize noise
            self._configure_external_loggers()
            
            # Initialize default handlers
            self._initialize_default_handlers()
            
            # Verify initialization
            self._verify_logging_setup()
            
        except Exception as e:
            print(f"Critical error initializing logging system: {e}")
            raise

    def _create_log_structure(self):
        """Create and verify complete logging directory structure"""
        try:
            created_folders = []
            failed_folders = []
            
            for folder in self.log_structure['folders'].values():
                try:
                    os.makedirs(folder, exist_ok=True)
                    created_folders.append(folder)
                except Exception as e:
                    failed_folders.append((folder, str(e)))
            
            # Create .gitignore
            self._create_gitignore()
            
            if failed_folders:
                raise Exception(f"Failed to create folders: {failed_folders}")
                
        except Exception as e:
            print(f"Error creating log structure: {e}")
            raise

    def _create_gitignore(self):
        """Create .gitignore file for log directories"""
        try:
            gitignore_content = """
            # Log files
            *.log
            *.json
            
            # Compressed logs
            *.gz
            *.zip
            
            # Except examples and schemas
            !example_*.json
            !schema_*.json
            
            # Memory files
            /stm/*
            /ltm/*
            
            # Sensitive data
            *.env
            *.key
            
            # System files
            .DS_Store
            __pycache__/
            *.pyc
            """
            
            gitignore_path = os.path.join(self.log_structure['root'], '.gitignore')
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content.strip())
                
        except Exception as e:
            print(f"Error creating .gitignore file: {e}")

    def _configure_external_loggers(self):
        """Configure external logging levels to minimize noise"""
        external_loggers = {
            'watchdog': logging.ERROR,      
            'urllib3': logging.ERROR,       
            'requests': logging.ERROR,      
            'streamlit': logging.ERROR,     
            'matplotlib': logging.ERROR,    
            'PIL': logging.ERROR,          
            'asyncio': logging.ERROR,      
            'websockets': logging.ERROR    
        }
        
        for logger_name, level in external_loggers.items():
            logging.getLogger(logger_name).setLevel(level)

    def _initialize_default_handlers(self):
        """Initialize default logging handlers with buffering"""
        try:
            # System error handler with buffering
            error_handler = logging.handlers.MemoryHandler(
                capacity=1024,  # Buffer size
                flushLevel=logging.ERROR,
                target=logging.handlers.RotatingFileHandler(
                    os.path.join(self.log_structure['folders']['errors'], 'system_errors.log'),
                    maxBytes=2 * 1024 * 1024,  # 2MB
                    backupCount=3
                )
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(self._get_formatter(detailed=True))
            
            # Add handler to root logger
            root_logger = logging.getLogger()
            root_logger.addHandler(error_handler)
            
        except Exception as e:
            print(f"Error initializing default handlers: {e}")
            raise

    def _verify_logging_setup(self):
        """Verify logging system initialization"""
        try:
            verification_results = {
                'folders_exist': self._verify_folders(),
                'files_accessible': self._verify_file_access()
            }
            
            return all(verification_results.values())
            
        except Exception as e:
            print(f"Error verifying system integrity: {e}")
            return False

    def _verify_folders(self) -> bool:
        """Verify all logging folders exist"""
        return all(os.path.exists(folder) for folder in self.log_structure['folders'].values())

    def _verify_file_access(self) -> bool:
        """Verify log files are writable"""
        try:
            test_file = os.path.join(self.log_structure['folders']['errors'], 'test.log')
            with open(test_file, 'w') as f:
                f.write('Test log entry\n')
            os.remove(test_file)
            return True
        except Exception as e:
            print(f"Error verifying file access: {e}")
            return False

    def _get_formatter(self, detailed: bool = False) -> logging.Formatter:
        """Get log formatter"""
        if detailed:
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
        return logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

    @lru_cache(maxsize=32)
    def get_logger(self, name: str, level: str = 'INFO') -> logging.Logger:
        """Get configured logger for module with caching"""
        logger = logging.getLogger(name)
        logger.setLevel(self.LOG_LEVELS.get(level, logging.INFO))
        
        # Remove existing handlers
        logger.handlers = []
        
        # Add appropriate handlers based on logger name
        handlers = self._get_handlers(name)
        for handler in handlers:
            logger.addHandler(handler)
        
        return logger

    def _get_handlers(self, name: str) -> list:
        """Get appropriate handlers for module with buffering"""
        handlers = []
        
        # Determine appropriate folder based on logger name
        folder_mapping = {
            'chat': 'stm',
            'session': 'stm',
            'interaction': 'stm',
            'medical': 'reasoning',
            'decision': 'reasoning',
            'validation': 'reasoning'
        }
        
        base_name = name.split('.')[0].lower()
        log_folder = folder_mapping.get(base_name, 'reasoning')
        folder_path = self.log_structure['folders'][log_folder]
        
        # Add buffered main handler
        main_handler = logging.handlers.MemoryHandler(
            capacity=512,  # Buffer size
            flushLevel=logging.WARNING,
            target=logging.handlers.RotatingFileHandler(
                os.path.join(folder_path, f"{name}.log"),
                maxBytes=1024 * 1024,  # 1MB
                backupCount=3
            )
        )
        main_handler.setFormatter(self._get_formatter())
        handlers.append(main_handler)
        
        # Add error handler
        error_handler = logging.handlers.MemoryHandler(
            capacity=128,  # Smaller buffer for errors
            flushLevel=logging.ERROR,
            target=logging.handlers.RotatingFileHandler(
                os.path.join(self.log_structure['folders']['errors'], f"{name}_errors.log"),
                maxBytes=1024 * 1024,
                backupCount=3
            )
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self._get_formatter(detailed=True))
        handlers.append(error_handler)
        
        return handlers

    def cleanup_old_logs(self, days: int = 30):
        """Archive old log files to LTM"""
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            archived_files = []
            
            for folder in ['stm', 'reasoning', 'errors']:
                folder_path = self.log_structure['folders'][folder]
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        filepath = os.path.join(folder_path, filename)
                        if os.path.isfile(filepath):
                            file_time = os.path.getmtime(filepath)
                            if file_time < cutoff_time:
                                # Compress and move to LTM
                                archive_path = os.path.join(
                                    self.log_structure['folders']['ltm'],
                                    f"archived_{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.gz"
                                )
                                with open(filepath, 'rb') as f_in:
                                    with gzip.open(archive_path, 'wb') as f_out:
                                        shutil.copyfileobj(f_in, f_out)
                                os.remove(filepath)
                                archived_files.append(filename)
            
        except Exception as e:
            print(f"Error cleaning up old logs: {e}")

# Global logger instance
draiml_logger = DrAIMLLogger()

def get_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """Convenience function to get a logger"""
    return draiml_logger.get_logger(name, level)

def cleanup_logs(days: int = 30):
    """Convenience function to cleanup old logs"""
    draiml_logger.cleanup_old_logs(days)

# Module exports
__all__ = [
    'get_logger',
    'cleanup_logs'
]
