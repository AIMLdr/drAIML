# memory.py (c) 2025 Gregory L. Magnusson MIT license

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
import shutil
import hashlib
from logger import get_logger
from pathlib import Path

@dataclass
class DialogEntry:
    """Structure for dialogue entries with enhanced medical context"""
    query: str
    response: str
    timestamp: str = None
    context: Dict = None
    medical_context: Dict = None
    provider: str = None
    model: str = None
    validation: Dict = None
    ethical_checks: List[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.context is None:
            self.context = {}
        if self.medical_context is None:
            self.medical_context = {
                "symptoms": [],
                "conditions": [],
                "severity": "unknown",
                "urgency": "unknown",
                "risk_factors": [],
                "ethical_considerations": []
            }
        if self.ethical_checks is None:
            self.ethical_checks = []

@dataclass
class MedicalDecision:
    """Enhanced structure for medical decisions and recommendations"""
    condition: str
    recommendation: str
    confidence: float
    severity: str
    urgency: str
    timestamp: str = None
    context: Dict = None
    validation: Dict = None
    reasoning: Dict = None
    patient_data: Dict = None
    provider: str = None
    model: str = None
    ethical_validation: Dict = None
    hippocratic_checks: List[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.context is None:
            self.context = {}
        if self.validation is None:
            self.validation = {
                "validated": False,
                "validation_timestamp": None,
                "validation_method": None,
                "validation_score": None,
                "validation_checks": []
            }
        if self.reasoning is None:
            self.reasoning = {
                "premises": [],
                "conclusions": [],
                "confidence_factors": {},
                "logical_path": [],
                "ethical_considerations": []
            }
        if self.patient_data is None:
            self.patient_data = {
                "symptoms": [],
                "history": [],
                "risk_factors": [],
                "ethical_factors": []
            }
        if self.ethical_validation is None:
            self.ethical_validation = {
                "validated": False,
                "principles_checked": [],
                "ethical_concerns": [],
                "recommendations": []
            }
        if self.hippocratic_checks is None:
            self.hippocratic_checks = []

class MemoryManager:
    """Enhanced memory management system for drAIML"""
    
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.logger = get_logger('memory')
        
        # Define simplified memory structure
        self.memory_structure = {
            'root': './memory',
            'folders': {
                'errors': './memory/errors',      # Error logs and exceptions
                'stm': './memory/stm',           # Short-term memory (conversations)
                'ltm': './memory/ltm',           # Long-term memory (future use)
                'reasoning': './memory/reasoning' # Decisions, validation, medical
            }
        }
        
        # Initialize system
        self._initialize_memory_system()
        
        # Start new session
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "operations": [],
            "errors": []
        }

    def _initialize_memory_system(self):
        """Initialize complete memory system"""
        try:
            # Create folder structure
            self._create_folder_structure()
            
            # Initialize memory stores
            self.memory_stores = {
                'medical_decisions': [],
                'ethical_validations': [],
                'session_data': {},
                'analytics': {},
                'context': {}
            }
            
            # Load existing data
            self._load_existing_memories()
            
            # Verify system integrity
            self._verify_system_integrity()
            
        except Exception as e:
            self.logger.error("Critical error initializing memory system: %s", str(e))
            raise

    def _create_folder_structure(self):
        """Create and verify memory folder structure"""
        try:
            created_folders = []
            failed_folders = []
            
            for folder in self.memory_structure['folders'].values():
                try:
                    os.makedirs(folder, exist_ok=True)
                    created_folders.append(folder)
                except Exception as e:
                    failed_folders.append((folder, str(e)))
            
            self.logger.info("Memory structure created - Success: %d, Failed: %d", 
                           len(created_folders), len(failed_folders))
            
            if failed_folders:
                raise Exception(f"Failed to create folders: {failed_folders}")
                
        except Exception as e:
            self.logger.error("Error creating folder structure: %s", str(e))
            raise

    def _verify_system_integrity(self):
        """Verify memory system integrity"""
        try:
            verification_results = {
                'folders_exist': all(os.path.exists(f) for f in self.memory_structure['folders'].values()),
                'stores_initialized': all(store for store in self.memory_stores.values() is not None),
                'session_active': bool(self.current_session)
            }
            
            self.logger.info("System integrity verified - Results: %s", str(verification_results))
            
            return all(verification_results.values())
            
        except Exception as e:
            self.logger.error("Error verifying system integrity: %s", str(e))
            return False

    def _load_existing_memories(self):
        """Load existing memory data"""
        try:
            for store_name in self.memory_stores:
                store_path = os.path.join(self.memory_structure['folders']['reasoning'], f"{store_name}.json")
                if os.path.exists(store_path):
                    with open(store_path, 'r') as f:
                        self.memory_stores[store_name] = json.load(f)
            
            self.logger.info("Existing memories loaded - Stores: %s", 
                           list(self.memory_stores.keys()))
                           
        except Exception as e:
            self.logger.error("Error loading existing memories: %s", str(e))

    def store_dialog_entry(self, entry: DialogEntry) -> bool:
        """Store dialog entry with enhanced tracking"""
        try:
            entry_dict = asdict(entry)
            entry_id = hashlib.md5(f"{entry.timestamp}{entry.query}".encode()).hexdigest()
            
            # Add metadata
            entry_dict.update({
                'entry_id': entry_id,
                'session_id': self.current_session["session_id"],
                'storage_timestamp': datetime.now().isoformat()
            })
            
            # Store in STM
            stm_path = os.path.join(self.memory_structure['folders']['stm'], f"dialog_{entry_id}.json")
            with open(stm_path, 'w') as f:
                json.dump(entry_dict, f, indent=2)
            
            # Track operation
            self.current_session["operations"].append({
                "type": "dialog_entry",
                "entry_id": entry_id,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info("Dialog entry stored - ID: %s, Session: %s", 
                           entry_id, self.current_session["session_id"])
            
            return True
            
        except Exception as e:
            self.logger.error("Error storing dialog entry: %s", str(e))
            return False

    def store_medical_decision(self, decision: MedicalDecision) -> bool:
        """Store medical decision with validation"""
        try:
            decision_dict = asdict(decision)
            decision_id = hashlib.md5(
                f"{decision.timestamp}{decision.condition}{decision.recommendation}".encode()
            ).hexdigest()
            
            # Add metadata
            decision_dict.update({
                'decision_id': decision_id,
                'session_id': self.current_session["session_id"],
                'storage_timestamp': datetime.now().isoformat()
            })
            
            # Store decision in reasoning folder
            decision_path = os.path.join(
                self.memory_structure['folders']['reasoning'], 
                f"decision_{decision_id}.json"
            )
            with open(decision_path, 'w') as f:
                json.dump(decision_dict, f, indent=2)
            
            # Store in memory store
            self.memory_stores['medical_decisions'].append(decision_dict)
            
            # Track operation
            self.current_session["operations"].append({
                "type": "medical_decision",
                "decision_id": decision_id,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info("Medical decision stored - ID: %s, Session: %s", 
                           decision_id, self.current_session["session_id"])
            
            return True
            
        except Exception as e:
            self.logger.error("Error storing medical decision: %s", str(e))
            return False

    def get_medical_decision_history(
        self,
        condition: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Get medical decision history with filters"""
        try:
            decisions = self.memory_stores['medical_decisions']
            
            if condition:
                decisions = [d for d in decisions if d['condition'] == condition]
            if start_date:
                decisions = [d for d in decisions if d['timestamp'] >= start_date]
            if end_date:
                decisions = [d for d in decisions if d['timestamp'] <= end_date]
            
            self.logger.info("Retrieved medical decision history - Condition: %s, Count: %d", 
                           condition or "All", len(decisions))
            
            return decisions
            
        except Exception as e:
            self.logger.error("Error retrieving medical decision history: %s", str(e))
            return []

    def cleanup_old_memories(self, days: int = 30) -> bool:
        """Archive old memory files to LTM"""
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            archived_files = []
            
            for folder in ['stm', 'reasoning']:
                folder_path = self.memory_structure['folders'][folder]
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        filepath = os.path.join(folder_path, filename)
                        if os.path.isfile(filepath):
                            file_time = os.path.getmtime(filepath)
                            if file_time < cutoff_time:
                                archive_path = os.path.join(
                                    self.memory_structure['folders']['ltm'],
                                    f"archived_{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                                )
                                shutil.move(filepath, archive_path)
                                archived_files.append(filename)
            
            self.logger.info("Cleaned up old memories - Archived: %d files", 
                           len(archived_files))
            
            return True
            
        except Exception as e:
            self.logger.error("Error cleaning up memories: %s", str(e))
            return False

# Global instance
memory_manager = MemoryManager()

# Convenience functions
def create_memory_folders() -> bool:
    """Create memory folder structure"""
    try:
        return bool(memory_manager)
    except Exception as e:
        print(f"Error creating memory folders: {e}")
        return False

def store_dialog_entry(entry: DialogEntry) -> bool:
    """Store dialog entry"""
    if memory_manager:
        return memory_manager.store_dialog_entry(entry)
    return False

def store_medical_decision(decision: MedicalDecision) -> bool:
    """Store medical decision"""
    if memory_manager:
        return memory_manager.store_medical_decision(decision)
    return False

def get_medical_decision_history(
    condition: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict]:
    """Get medical decision history"""
    if memory_manager:
        return memory_manager.get_medical_decision_history(condition, start_date, end_date)
    return []

def cleanup_memories(days: int = 30) -> bool:
    """Clean up old memories"""
    if memory_manager:
        return memory_manager.cleanup_old_memories(days)
    return False

# Module exports
__all__ = [
    'DialogEntry',
    'MedicalDecision',
    'MemoryManager',
    'create_memory_folders',
    'store_dialog_entry',
    'store_medical_decision',
    'get_medical_decision_history',
    'cleanup_memories'
]
