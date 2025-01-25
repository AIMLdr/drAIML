# memory.py
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging
from dataclasses import dataclass, asdict

@dataclass
class DialogEntry:
    """Structure for dialogue entries"""
    query: str
    response: str
    timestamp: str = None
    context: Dict = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.context is None:
            self.context = {}

class MemoryManager:
    """Manages memory operations for drAIML"""
    
    def __init__(self):
        self.logger = logging.getLogger('MemoryManager')
        self.setup_logging()
        self.memory_structure = {
            'root': './memory',
            'folders': {
                'logs': './memory/logs',
                'stm': './memory/stm',
                'ltm': './memory/ltm',
                'medical': './memory/medical',
                'truth': './memory/truth'
            },
            'log_files': {
                'dialog': 'dialog.json',
                'errors': 'errors.log',
                'medical_decisions': 'medical_decisions.json',
                'reasoning': 'reasoning.json'
            }
        }
        self.create_memory_folders()

    def setup_logging(self):
        """Initialize logging configuration"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('./memory/logs/memory_manager.log'),
                logging.StreamHandler()
            ]
        )

    def create_memory_folders(self):
        """Create necessary folder structure"""
        try:
            for folder in self.memory_structure['folders'].values():
                os.makedirs(folder, exist_ok=True)
            self.logger.info("Memory folders created successfully")
        except Exception as e:
            self.logger.error(f"Error creating memory folders: {e}")
            raise

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
            
            # Load existing conversations
            conversations = self._load_json_file(filepath, default=[])
            
            # Add timestamp if not present
            if 'timestamp' not in dialog_data:
                dialog_data['timestamp'] = datetime.now().isoformat()
            
            conversations.append(dialog_data)
            
            # Save updated conversations
            with open(filepath, 'w') as f:
                json.dump(conversations, f, indent=2)
            
            self.logger.debug(f"Saved conversation memory: {dialog_data.get('timestamp')}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving conversation memory: {e}")
            return False

    def save_medical_decision(self, decision_data: Dict):
        """Save medical decision to memory"""
        try:
            filepath = os.path.join(
                self.memory_structure['folders']['medical'],
                self.memory_structure['log_files']['medical_decisions']
            )
            
            decisions = self._load_json_file(filepath, default=[])
            
            # Add metadata
            decision_data.update({
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            })
            
            decisions.append(decision_data)
            
            with open(filepath, 'w') as f:
                json.dump(decisions, f, indent=2)
            
            self.logger.debug(f"Saved medical decision: {decision_data.get('timestamp')}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving medical decision: {e}")
            return False

    def save_reasoning_log(self, reasoning_data: Dict):
        """Save reasoning process to memory"""
        try:
            filepath = os.path.join(
                self.memory_structure['folders']['logs'],
                self.memory_structure['log_files']['reasoning']
            )
            
            reasoning_logs = self._load_json_file(filepath, default=[])
            
            reasoning_data.update({
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            })
            
            reasoning_logs.append(reasoning_data)
            
            with open(filepath, 'w') as f:
                json.dump(reasoning_logs, f, indent=2)
            
            self.logger.debug(f"Saved reasoning log: {reasoning_data.get('timestamp')}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving reasoning log: {e}")
            return False

    def retrieve_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent conversations"""
        try:
            filepath = os.path.join(
                self.memory_structure['folders']['logs'],
                self.memory_structure['log_files']['dialog']
            )
            
            conversations = self._load_json_file(filepath, default=[])
            return conversations[-limit:]
        except Exception as e:
            self.logger.error(f"Error retrieving conversations: {e}")
            return []

    def retrieve_medical_decisions(self, 
                                 start_date: Optional[str] = None, 
                                 end_date: Optional[str] = None) -> List[Dict]:
        """Retrieve medical decisions within date range"""
        try:
            filepath = os.path.join(
                self.memory_structure['folders']['medical'],
                self.memory_structure['log_files']['medical_decisions']
            )
            
            decisions = self._load_json_file(filepath, default=[])
            
            if start_date and end_date:
                filtered_decisions = [
                    d for d in decisions
                    if start_date <= d.get('timestamp', '') <= end_date
                ]
                return filtered_decisions
            
            return decisions
        except Exception as e:
            self.logger.error(f"Error retrieving medical decisions: {e}")
            return []

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
                        os.remove(file_path)
                        self.logger.info(f"Removed old memory file: {file_path}")
                        
            return True
        except Exception as e:
            self.logger.error(f"Error cleaning up memories: {e}")
            return False

# Create global instance
memory_manager = MemoryManager()

# Convenience functions
def create_memory_folders():
    """Create memory folder structure"""
    memory_manager.create_memory_folders()

def store_in_stm(entry: DialogEntry):
    """Store entry in short-term memory"""
    return memory_manager.store_in_stm(entry)

def save_conversation_memory(dialog_data: Dict):
    """Save conversation memory"""
    return memory_manager.save_conversation_memory(dialog_data)

def save_medical_decision(decision_data: Dict):
    """Save medical decision"""
    return memory_manager.save_medical_decision(decision_data)

def save_reasoning_log(reasoning_data: Dict):
    """Save reasoning log"""
    return memory_manager.save_reasoning_log(reasoning_data)
