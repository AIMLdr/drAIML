# socratic.py
import logging
import os
import pathlib
import json
from datetime import datetime
from typing import List, Dict, Optional, Union
from logic import LogicTables
from memory import DialogEntry, memory_manager
from hippocratic import HippocraticReasoning

class SocraticReasoning:
    """
    Enhanced Socratic reasoning system for medical dialogue and decision-making
    """
    
    def __init__(self, chatter):
        # Initialize components
        self.premises: List[str] = []
        self.logger = self._setup_logger()
        self.logic_tables = LogicTables()
        self.hippocratic = HippocraticReasoning()
        self.chatter = chatter
        self.dialogue_history: List[Dict] = []
        self.logical_conclusion: str = ""
        self.max_tokens: int = 100

        # File paths
        self.file_paths = self._initialize_file_paths()
        
        # Create necessary directories
        self._create_directories()

    def _setup_logger(self) -> logging.Logger:
        """Initialize logging system"""
        logger = logging.getLogger('SocraticReasoning')
        logger.setLevel(logging.DEBUG)

        # Create handlers
        log_dir = './memory/logs'
        os.makedirs(log_dir, exist_ok=True)

        handlers = {
            'file': logging.FileHandler('./memory/logs/socratic.log'),
            'socratic': logging.FileHandler('./memory/logs/socratic_reasoning.log'),
            'premises': logging.FileHandler('./memory/logs/premises.log'),
            'stream': logging.StreamHandler()
        }

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set up handlers
        for handler in handlers.values():
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_file_paths(self) -> Dict[str, str]:
        """Initialize file paths for various logs"""
        return {
            'socratic_logs': './memory/logs/socraticlogs.txt',
            'premises': './memory/logs/premises.json',
            'not_premises': './memory/logs/notpremise.json',
            'conclusions': './memory/logs/conclusions.txt',
            'truth_tables': './memory/logs/truth.json',
            'medical_reasoning': './memory/logs/medical_reasoning.json'
        }

    def _create_directories(self):
        """Create necessary directories"""
        for filepath in self.file_paths.values():
            pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    def add_premise(self, premise: str) -> bool:
        """
        Add a premise to the reasoning system
        
        Args:
            premise: The premise to add
            
        Returns:
            bool: Success status
        """
        try:
            # Validate premise
            if not self._validate_premise(premise):
                self.log_not_premise(f'Invalid premise format: {premise}')
                return False

            # Check medical validity
            medical_validation = self.hippocratic.validate_medical_response(
                premise,
                {"context": "premise_validation"}
            )

            if not medical_validation["is_valid"]:
                self.log_not_premise(f'Medical validation failed: {premise}')
                return False

            # Add premise if valid
            if premise not in self.premises:
                self.premises.append(premise)
                self._save_premises()
                self.logger.info(f'Added premise: {premise}')
                return True

            return False

        except Exception as e:
            self.logger.error(f"Error adding premise: {e}")
            return False

    def draw_conclusion(self) -> str:
        """
        Draw a conclusion based on current premises
        
        Returns:
            str: The derived conclusion
        """
        if not self.premises:
            return "No premises available for reasoning."

        try:
            # Generate initial conclusion
            conclusion = self._generate_initial_conclusion()
            
            # Validate conclusion
            if not self._validate_conclusion(conclusion):
                self.logger.warning("Initial conclusion failed validation")
                conclusion = self._refine_conclusion(conclusion)

            # Validate with Hippocratic principles
            medical_validation = self.hippocratic.validate_medical_response(
                conclusion,
                {"context": "conclusion_validation"}
            )

            if not medical_validation["is_valid"]:
                self.logger.warning("Medical validation failed")
                conclusion = medical_validation["modified_response"]

            # Store the conclusion
            self._store_conclusion(conclusion)
            
            return conclusion

        except Exception as e:
            self.logger.error(f"Error drawing conclusion: {e}")
            return "Error generating conclusion."

    def _generate_initial_conclusion(self) -> str:
        """Generate initial conclusion from premises"""
        try:
            # Combine recent premises for context
            context = " ".join(self.premises[-3:])
            
            prompt = f"""Based on these premises:
            {context}
            
            Please provide a medical conclusion that:
            1. Is directly related to the premises
            2. Is logically sound
            3. Follows medical best practices
            4. Is clear and actionable
            
            Conclusion:"""

            conclusion = self.chatter.generate_response(prompt)
            return conclusion.strip()

        except Exception as e:
            self.logger.error(f"Error generating initial conclusion: {e}")
            return ""

    def _validate_conclusion(self, conclusion: str) -> bool:
        """Validate a conclusion"""
        if not conclusion:
            return False

        # Logical validation
        logical_validation = self.logic_tables.validate_conclusion(
            conclusion,
            self.premises
        )

        if not logical_validation["valid"]:
            self.logger.warning(f"Logical validation failed: {logical_validation['reason']}")
            return False

        return True

    def _refine_conclusion(self, conclusion: str) -> str:
        """Refine an invalid conclusion"""
        try:
            prompt = f"""The following medical conclusion needs refinement:
            {conclusion}

            Please improve it to ensure:
            1. Logical consistency with premises
            2. Medical accuracy
            3. Clear actionable recommendations
            4. Patient safety considerations

            Refined conclusion:"""

            refined = self.chatter.generate_response(prompt)
            return refined.strip()

        except Exception as e:
            self.logger.error(f"Error refining conclusion: {e}")
            return conclusion

    def _store_conclusion(self, conclusion: str):
        """Store conclusion in memory"""
        try:
            # Save to conclusions file
            with open(self.file_paths['conclusions'], 'a') as f:
                f.write(f"{datetime.now().isoformat()}: {conclusion}\n")

            # Save with premises for context
            conclusion_entry = {
                "timestamp": datetime.now().isoformat(),
                "premises": self.premises,
                "conclusion": conclusion,
                "validation": {
                    "logical": self.logic_tables.validate_conclusion(conclusion, self.premises),
                    "medical": self.hippocratic.validate_medical_response(
                        conclusion,
                        {"context": "conclusion_storage"}
                    )
                }
            }

            # Save to medical reasoning log
            self._save_json_log(
                self.file_paths['medical_reasoning'],
                conclusion_entry
            )

        except Exception as e:
            self.logger.error(f"Error storing conclusion: {e}")

    def _validate_premise(self, premise: str) -> bool:
        """Validate a premise"""
        if not premise or not isinstance(premise, str):
            return False

        # Basic validation
        if len(premise.strip()) < 3:
            return False

        # Logical validation
        return self.logic_tables.tautology(premise)

    def _save_premises(self):
        """Save premises to file"""
        try:
            premises_entry = {
                "timestamp": datetime.now().isoformat(),
                "premises": self.premises
            }
            self._save_json_log(self.file_paths['premises'], premises_entry)
        except Exception as e:
            self.logger.error(f"Error saving premises: {e}")

    def log_not_premise(self, message: str, level: str = 'warning'):
        """Log invalid premises"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message
            }
            self._save_json_log(self.file_paths['not_premises'], entry)
            
            if level == 'warning':
                self.logger.warning(message)
            else:
                self.logger.error(message)

        except Exception as e:
            self.logger.error(f"Error logging not premise: {e}")

    def _save_json_log(self, filepath: str, entry: Dict):
        """Save entry to JSON log file"""
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
            self.logger.error(f"Error saving to JSON log {filepath}: {e}")

    def get_reasoning_history(self) -> List[Dict]:
        """Get reasoning history"""
        try:
            return self._load_json_file(self.file_paths['medical_reasoning'])
        except Exception as e:
            self.logger.error(f"Error getting reasoning history: {e}")
            return []

    def _load_json_file(self, filepath: str) -> List[Dict]:
        """Load JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error loading JSON file {filepath}: {e}")
            return []
