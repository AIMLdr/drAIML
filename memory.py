# memory.py
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
import logging
from dataclasses import dataclass, asdict
import shutil
import hashlib

@dataclass
class DialogEntry:
    """Structure for dialogue entries"""
    query: str
    response: str
    timestamp: str = None
    context: Dict = None
    medical_context: Dict = None
    
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
                "urgency": "unknown"
            }

@dataclass
class MedicalDecision:
    """Structure for medical decisions and recommendations"""
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
                "confidence_factors": {}
            }
        if self.patient_data is None:
            self.patient_data = {
                "symptoms": [],
                "history": [],
                "risk_factors": []
            }

class MemoryManager:
    """Enhanced memory management system for drAIML"""
    
    def __init__(self):
        self.logger = logging.getLogger('MemoryManager')
        self.memory_structure = {
            'root': './memory',
            'folders': {
                'logs': './memory/logs',
                'stm': './memory/stm',
                'ltm': './memory/ltm',
                'medical': './memory/medical',
                'analytics': './memory/analytics',
                'backup': './memory/backup'
            },
            'log_files': {
                'dialog': 'dialog.json',
                'errors': 'errors.log',
                'medical_decisions': 'medical_decisions.json',
                'medical_analytics': 'medical_analytics.json'
            }
        }
        # Initialize system
        self.create_memory_folders()
        self.setup_logging()
        self.initialize_memory_stores()

    def create_memory_folders(self):
        """Create necessary folder structure"""
        try:
            # Create root memory directory
            os.makedirs(self.memory_structure['root'], exist_ok=True)
            
            # Create all subdirectories
            for folder in self.memory_structure['folders'].values():
                os.makedirs(folder, exist_ok=True)
            
            self._create_gitignore()
            return True
        except Exception as e:
            print(f"Error creating memory folders: {e}")
            return False

    def _create_gitignore(self):
        """Create .gitignore file for sensitive data"""
        gitignore_content = """
        # Sensitive data
        *.log
        *.json
        /backup/*
        
        # Except example files
        !example_*.json
        """
        try:
            with open(os.path.join(self.memory_structure['root'], '.gitignore'), 'w') as f:
                f.write(gitignore_content.strip())
        except Exception as e:
            print(f"Error creating .gitignore: {e}")

    def setup_logging(self):
        """Initialize comprehensive logging system"""
        try:
            log_file = os.path.join(self.memory_structure['folders']['logs'], 'memory_manager.log')
            
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )
            
            self.logger.debug("Logging initialized successfully")
        except Exception as e:
            print(f"Error setting up logging: {e}")
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def initialize_memory_stores(self):
        """Initialize memory storage systems"""
        self.memory_stores = {
            'medical_decisions': [],
            'analytics': {},
            'cache': {}
        }
        self._load_existing_memories()

    def _load_existing_memories(self):
        """Load existing memories from storage"""
        try:
            for store_name, store_data in self.memory_stores.items():
                file_path = os.path.join(
                    self.memory_structure['folders']['medical'],
                    f"{store_name}.json"
                )
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        self.memory_stores[store_name] = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading existing memories: {e}")

    def store_medical_decision(self, decision: MedicalDecision):
        """Store medical decision with comprehensive validation and tracking"""
        try:
            decision_dict = asdict(decision)
            
            # Add metadata
            decision_dict.update({
                'storage_timestamp': datetime.now().isoformat(),
                'decision_id': self._generate_decision_id(decision),
                'validation_status': self._validate_medical_decision(decision)
            })
            
            # Store in memory
            self.memory_stores['medical_decisions'].append(decision_dict)
            
            # Save to file
            self._save_to_file(
                'medical_decisions',
                decision_dict,
                subfolder='medical'
            )
            
            # Update analytics
            self._update_medical_analytics(decision_dict)
            
            # Log the decision
            self.logger.info(f"Stored medical decision: {decision_dict['decision_id']}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error storing medical decision: {e}")
            return False

    def _generate_decision_id(self, decision: MedicalDecision) -> str:
        """Generate unique ID for decision"""
        decision_string = f"{decision.timestamp}{decision.condition}{decision.recommendation}"
        return hashlib.md5(decision_string.encode()).hexdigest()

    def _validate_medical_decision(self, decision: MedicalDecision) -> Dict:
        """Comprehensive medical decision validation"""
        validation = {
            "is_valid": True,
            "checks": [],
            "timestamp": datetime.now().isoformat(),
            "validation_level": "comprehensive"
        }
        
        # Confidence check
        if decision.confidence < 0.5:
            validation["checks"].append({
                "check": "confidence",
                "result": "low_confidence",
                "value": decision.confidence,
                "threshold": 0.5
            })
            validation["is_valid"] = False
        
        # Urgency check
        if decision.urgency == "emergency":
            validation["checks"].append({
                "check": "urgency",
                "result": "emergency_case",
                "value": decision.urgency,
                "requires_immediate_action": True
            })
        
        # Severity check
        if decision.severity in ["severe", "critical"]:
            validation["checks"].append({
                "check": "severity",
                "result": "high_severity",
                "value": decision.severity,
                "requires_attention": True
            })
        
        # Context validation
        if not decision.context:
            validation["checks"].append({
                "check": "context",
                "result": "missing_context",
                "recommendation": "Add medical context"
            })
        
        # Reasoning validation
        if not decision.reasoning["premises"]:
            validation["checks"].append({
                "check": "reasoning",
                "result": "missing_premises",
                "recommendation": "Add reasoning premises"
            })
        
        return validation

    def _update_medical_analytics(self, decision: Dict):
        """Update medical decision analytics"""
        try:
            analytics = self.memory_stores.get('analytics', {})
            
            # Initialize condition analytics if not exists
            condition = decision['condition']
            if condition not in analytics:
                analytics[condition] = {
                    'count': 0,
                    'confidence_sum': 0,
                    'severity_levels': {},
                    'urgency_levels': {},
                    'recommendations': {},
                    'temporal_distribution': {}
                }
            
            # Update statistics
            analytics[condition]['count'] += 1
            analytics[condition]['confidence_sum'] += decision['confidence']
            
            # Update severity distribution
            severity = decision['severity']
            analytics[condition]['severity_levels'][severity] = \
                analytics[condition]['severity_levels'].get(severity, 0) + 1
            
            # Update urgency distribution
            urgency = decision['urgency']
            analytics[condition]['urgency_levels'][urgency] = \
                analytics[condition]['urgency_levels'].get(urgency, 0) + 1
            
            # Update temporal distribution
            date = decision['timestamp'][:10]  # Get just the date part
            analytics[condition]['temporal_distribution'][date] = \
                analytics[condition]['temporal_distribution'].get(date, 0) + 1
            
            # Save updated analytics
            self._save_to_file(
                'medical_analytics',
                analytics,
                subfolder='analytics'
            )
            
        except Exception as e:
            self.logger.error(f"Error updating medical analytics: {e}")

    def store_in_stm(self, entry: DialogEntry):
        """Store dialog entry in short-term memory"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"memory_{timestamp}.json"
            filepath = os.path.join(self.memory_structure['folders']['stm'], filename)
            
            entry_dict = asdict(entry)
            
            with open(filepath, 'w') as f:
                json.dump(entry_dict, f, indent=2)
            
            self.logger.debug(f"Stored dialog entry in STM: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error storing in STM: {e}")
            return False

    def save_conversation_memory(self, dialog_data: Dict):
        """Save conversation to memory"""
        try:
            filepath = os.path.join(
                self.memory_structure['folders']['logs'],
                self.memory_structure['log_files']['dialog']
            )
            
            conversations = self._load_json_file(filepath, default=[])
            
            if 'timestamp' not in dialog_data:
                dialog_data['timestamp'] = datetime.now().isoformat()
            
            conversations.append(dialog_data)
            
            with open(filepath, 'w') as f:
                json.dump(conversations, f, indent=2)
            
            self.logger.debug(f"Saved conversation memory: {dialog_data.get('timestamp')}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving conversation memory: {e}")
            return False

    def get_medical_decision_history(self, 
                                   condition: Optional[str] = None,
                                   start_date: Optional[str] = None,
                                   end_date: Optional[str] = None) -> List[Dict]:
        """Retrieve medical decision history with filters"""
        try:
            decisions = self.memory_stores['medical_decisions']
            
            if condition:
                decisions = [d for d in decisions if d['condition'] == condition]
            
            if start_date:
                decisions = [d for d in decisions if d['timestamp'] >= start_date]
                
            if end_date:
                decisions = [d for d in decisions if d['timestamp'] <= end_date]
                
            return decisions
            
        except Exception as e:
            self.logger.error(f"Error retrieving medical decision history: {e}")
            return []

    def get_medical_analytics(self, condition: Optional[str] = None) -> Dict:
        """Get medical decision analytics"""
        try:
            analytics = self.memory_stores['analytics']
            
            if condition:
                return analytics.get(condition, {})
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error retrieving medical analytics: {e}")
            return {}

    def _save_to_file(self, name: str, data: Any, subfolder: str = None):
        """Save data to file with backup"""
        try:
            folder = self.memory_structure['folders'].get(subfolder, self.memory_structure['folders']['medical'])
            filepath = os.path.join(folder, f"{name}.json")
            
            # Create backup
            if os.path.exists(filepath):
                backup_path = os.path.join(
                    self.memory_structure['folders']['backup'],
                    f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                )
                shutil.copy2(filepath, backup_path)
            
            # Save new data
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving to file: {e}")
            raise

    def _load_json_file(self, filepath: str, default: Union[List, Dict] = None) -> Union[List, Dict]:
        """Helper method to load JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return default if default is not None else []
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from {filepath}")
            return default if default is not None else []

    def cleanup_old_memories(self, days_threshold: int = 30):
        """Clean up old memory files"""
        try:
            current_time = datetime.now()
            
            for folder in ['stm', 'ltm']:
                folder_path = self.memory_structure['folders'][folder]
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if (current_time - file_time).days > days_threshold:
                        # Backup before deletion
                        backup_path = os.path.join(
                            self.memory_structure['folders']['backup'],
                            f"archived_{filename}"
                        )
                        shutil.move(file_path, backup_path)
                        self.logger.info(f"Archived old memory file: {file_path}")
                        
            return True
        except Exception as e:
            self.logger.error(f"Error cleaning up memories: {e}")
            return False

# Create global instance
try:
    memory_manager = MemoryManager()
except Exception as e:
    print(f"Error initializing MemoryManager: {e}")
    memory_manager = None

# Convenience functions
def create_memory_folders():
    """Create memory folder structure"""
    if memory_manager:
        return memory_manager.create_memory_folders()
    return False

def store_in_stm(entry: DialogEntry):
    """Store entry in short-term memory"""
    if memory_manager:
        return memory_manager.store_in_stm(entry)
    return False

def save_conversation_memory(dialog_data: Dict):
    """Save conversation memory"""
    if memory_manager:
        return memory_manager.save_conversation_memory(dialog_data)
    return False

def store_medical_decision(decision: MedicalDecision):
    """Store medical decision"""
    if memory_manager:
        return memory_manager.store_medical_decision(decision)
    return False

def get_medical_decision_history(condition: Optional[str] = None,
                               start_date: Optional[str] = None,
                               end_date: Optional[str] = None) -> List[Dict]:
    """Get medical decision history"""
    if memory_manager:
        return memory_manager.get_medical_decision_history(condition, start_date, end_date)
    return []

def get_medical_analytics(condition: Optional[str] = None) -> Dict:
    """Get medical analytics"""
    if memory_manager:
        return memory_manager.get_medical_analytics(condition)
    return {}
