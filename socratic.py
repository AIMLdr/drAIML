# socratic.py (c) 2025 Gregory L. Magnusson MIT license

import logging
import os
import pathlib
import ujson
from datetime import datetime
from typing import List, Dict, Optional, Union, Any
from logger import get_logger
from memory import (
    MedicalDecision, 
    store_medical_decision, 
    DialogEntry, 
    store_dialog_entry,
    MemoryManager
)
from hippocratic import HippocraticPrinciples, HippocraticReasoning
from logic import LogicTables
from config import model_config

class SocraticReasoning:
    """Original Socratic Reasoning implementation"""
    
    def __init__(self, chatter):
        """
        Initializes the SocraticReasoning instance with necessary configurations.
        
        Args:
            chatter: An instance of the model used for generating responses.
        """
        self.premises = []  # List to hold premises
        self.logger = get_logger('socratic')
        
        # Initialize memory manager
        self.memory_manager = MemoryManager()
        
        # File paths for saving premises, non-premises, conclusions, and truth tables
        self.memory_paths = {
            'socratic_logs': './memory/logs/socraticlogs.txt',
            'premises': './memory/logs/premises.json',
            'not_premises': './memory/logs/notpremise.json',
            'conclusions': './memory/logs/conclusions.txt',
            'truth_tables': './memory/logs/truth.json'
        }

        # Create necessary directories
        for path in self.memory_paths.values():
            pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

        self.max_tokens = 100  # Default max tokens
        self.chatter = chatter  # Chatter model for generating responses
        self.logic_tables = LogicTables()  # Logic tables for reasoning
        self.dialogue_history = []  # List to hold the history of dialogues
        self.logical_conclusion = ""  # Variable to store the conclusion

        # Initialize session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_data = {
            "premises_added": 0,
            "conclusions_drawn": 0,
            "validations_performed": 0
        }

        self.logger.info("Socratic reasoning initialized", 
                        extra={'structured_data': {
                            'session_id': self.session_id
                        }})

    def socraticlogs(self, message, level='info'):
        """Log Socratic reasoning process"""
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        self._log_to_file(message, level)

    def _log_to_file(self, message, level):
        """Write to Socratic log file"""
        try:
            with open(self.memory_paths['socratic_logs'], 'a') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"{timestamp} - {level.upper()}: {message}\n")
        except Exception as e:
            self.logger.error(f"Error writing to Socratic log: {e}")

    def add_premise(self, premise):
        """Add a premise with validation"""
        try:
            if self.parse_statement(premise):
                self.premises.append(premise)
                self.save_premises()
                self.session_data["premises_added"] += 1
                
                self.logger.info("Premise added", 
                               extra={'structured_data': {
                                   'premise': premise,
                                   'session_id': self.session_id
                               }})
                return True
            else:
                self.log_not_premise(f'Invalid premise: {premise}', level='error')
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding premise: {e}")
            return False

    def parse_statement(self, statement):
        """Validate statement structure"""
        try:
            if not isinstance(statement, str) or not statement.strip():
                return False
                
            # Basic validation
            min_words = 3
            max_words = 100
            words = statement.split()
            
            if not min_words <= len(words) <= max_words:
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error parsing statement: {e}")
            return False

    def generate_new_premise(self, premise):
        """Generate new premise based on existing one"""
        try:
            premise_text = f"Based on the premise: {premise}\nGenerate a related premise:"
            new_premise = self.chatter.generate_response(premise_text)
            
            self.logger.debug("Generated new premise", 
                            extra={'structured_data': {
                                'original': premise,
                                'generated': new_premise
                            }})
            
            return new_premise.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating premise: {e}")
            return ""

    def challenge_premise(self, premise):
        """Challenge and potentially remove a premise"""
        try:
            if premise in self.premises:
                self.premises.remove(premise)
                self.remove_equivalent_premises(premise)
                self.save_premises()
                
                self.logger.info("Premise challenged and removed", 
                               extra={'structured_data': {
                                   'premise': premise,
                                   'session_id': self.session_id
                               }})
                return True
            else:
                self.log_not_premise(f'Premise not found: {premise}', level='error')
                return False
                
        except Exception as e:
            self.logger.error(f"Error challenging premise: {e}")
            return False

    def remove_equivalent_premises(self, premise):
        """Remove logically equivalent premises"""
        try:
            equivalent_premises = [
                p for p in self.premises 
                if self.logic_tables.unify_variables(premise, p)
            ]
            
            for p in equivalent_premises:
                self.premises.remove(p)
                self.log_not_premise(f'Removed equivalent premise: {p}')
                
            self.save_premises()
            
        except Exception as e:
            self.logger.error(f"Error removing equivalent premises: {e}")

    def save_premises(self):
        """Save current premises to file"""
        try:
            with open(self.memory_paths['premises'], 'w') as file:
                ujson.dump(self.premises, file, indent=2)
                
            self.logger.debug("Premises saved", 
                            extra={'structured_data': {
                                'count': len(self.premises)
                            }})
                
        except Exception as e:
            self.logger.error(f"Error saving premises: {e}")

    def log_not_premise(self, message, level='info'):
        """Log invalid or rejected premises"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level.upper(),
                "message": message,
                "session_id": self.session_id
            }
            
            with open(self.memory_paths['not_premises'], 'a') as file:
                ujson.dump(entry, file, indent=2)
                file.write('\n')
                
            self.logger.info(f"Not premise logged: {message}", 
                           extra={'structured_data': entry})
                
        except Exception as e:
            self.logger.error(f"Error logging not premise: {e}")

    def draw_conclusion(self):
        """Draw logical conclusion from premises"""
        try:
            if not self.premises:
                return "No premises available for logic as conclusion."

            current_premise = self.premises[0]
            additional_premises_count = 0
            
            while additional_premises_count < 5:
                new_premise = self.generate_new_premise(current_premise)
                if not self.parse_statement(new_premise):
                    continue
                    
                self.premises.append(new_premise)
                self.save_premises()
                additional_premises_count += 1

                raw_response = self.chatter.generate_response(current_premise)
                conclusion = raw_response.strip()
                self.logical_conclusion = conclusion

                if self.validate_conclusion():
                    self.session_data["conclusions_drawn"] += 1
                    break
                else:
                    self.log_not_premise(
                        'Invalid conclusion. Generating more premises.',
                        level='error'
                    )

            # Save conclusion
            self._save_conclusion()

            # Clear premises for next round
            self.premises = []
            
            self.logger.info("Conclusion drawn", 
                           extra={'structured_data': {
                               'conclusion': self.logical_conclusion,
                               'session_id': self.session_id
                           }})

            return self.logical_conclusion
            
        except Exception as e:
            self.logger.error(f"Error drawing conclusion: {e}")
            return "Error generating conclusion."

    def _save_conclusion(self):
        """Save conclusion and related data"""
        try:
            conclusion_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id,
                "premises": self.premises,
                "conclusion": self.logical_conclusion
            }
            
            # Save to premises file
            with open(self.memory_paths['premises'], 'w') as file:
                ujson.dump(conclusion_entry, file, indent=2)

            # Log to conclusions file
            with open(self.memory_paths['conclusions'], 'a') as file:
                file.write(f"\n{datetime.now().isoformat()}\n")
                file.write(f"Session ID: {self.session_id}\n")
                file.write(f"Premises: {self.premises}\n")
                file.write(f"Conclusion: {self.logical_conclusion}\n")

            # Save as truth if valid
            if self.validate_conclusion():
                self.save_truth(self.logical_conclusion)
                
            self.logger.info("Conclusion saved", 
                           extra={'structured_data': conclusion_entry})
                
        except Exception as e:
            self.logger.error(f"Error saving conclusion: {e}")

    def validate_conclusion(self):
        """Validate logical conclusion"""
        try:
            is_valid = self.logic_tables.tautology(self.logical_conclusion)
            
            self.session_data["validations_performed"] += 1
            
            self.logger.debug("Conclusion validated", 
                            extra={'structured_data': {
                                'conclusion': self.logical_conclusion,
                                'is_valid': is_valid
                            }})
            
            return is_valid
            
        except Exception as e:
            self.logger.error(f"Error validating conclusion: {e}")
            return False

    def save_truth(self, truth):
        """Save validated truth"""
        try:
            truth_entry = {
                "truth": truth,
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id
            }
            
            with open(self.memory_paths['truth_tables'], 'a') as file:
                ujson.dump(truth_entry, file, indent=2)
                file.write('\n')
                
            self.logger.info("Truth saved", 
                           extra={'structured_data': truth_entry})
                
        except Exception as e:
            self.logger.error(f"Error saving truth: {e}")

    def update_logic_tables(self, variables, expressions, valid_truths):
        """Update logic tables with new data"""
        try:
            self.logic_tables.variables = variables
            self.logic_tables.expressions = expressions
            self.logic_tables.valid_truths = valid_truths

            # Save truth tables
            truth_tables_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id,
                "variables": variables,
                "expressions": expressions,
                "valid_truths": valid_truths
            }
            
            with open(self.memory_paths['truth_tables'], 'w') as file:
                ujson.dump(truth_tables_entry, file, indent=2)

            # Save timestamped belief file
            belief_path = f'./memory/truth/belief_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
            pathlib.Path(belief_path).parent.mkdir(parents=True, exist_ok=True)
            with open(belief_path, 'w') as file:
                ujson.dump(truth_tables_entry, file, indent=2)

            self.logger.info("Logic tables updated", 
                           extra={'structured_data': truth_tables_entry})
                
        except Exception as e:
            self.logger.error(f"Error updating logic tables: {e}")

    def set_max_tokens(self, max_tokens):
        """Set maximum tokens for responses"""
        try:
            self.max_tokens = max_tokens
            self.logger.info(f"Max tokens set to: {max_tokens}")
        except Exception as e:
            self.logger.error(f"Error setting max tokens: {e}")

    def get_session_summary(self) -> Dict:
        """Get current session summary"""
        try:
            return {
                "session_id": self.session_id,
                "start_time": self.session_id[:8],
                "premises_added": self.session_data["premises_added"],
                "conclusions_drawn": self.session_data["conclusions_drawn"],
                "validations_performed": self.session_data["validations_performed"]
            }
        except Exception as e:
            self.logger.error(f"Error getting session summary: {e}")
            return {}

    def interact(self):
        """Interactive Socratic dialogue session"""
        self.logger.info("Starting Socratic dialogue session", 
                        extra={'structured_data': {
                            'session_id': self.session_id
                        }})
        
        while True:
            try:
                self.socraticlogs("\nCommands: add, challenge, conclude, set_tokens, exit")
                cmd = input("> ").strip().lower()

                if cmd == 'exit':
                    self.socraticlogs('Exiting Socratic Reasoning.')
                    break
                elif cmd == 'add':
                    premise = input("Enter the premise: ").strip()
                    self.add_premise(premise)
                elif cmd == 'challenge':
                    premise = input("Enter the premise to challenge: ").strip()
                    self.challenge_premise(premise)
                elif cmd == 'conclude':
                    conclusion = self.draw_conclusion()
                    print(conclusion)
                elif cmd == 'set_tokens':
                    tokens = input("Enter the maximum number of tokens: ").strip()
                    if tokens.isdigit():
                        self.set_max_tokens(int(tokens))
                    else:
                        self.socraticlogs("Invalid number of tokens.", level='error')
                else:
                    self.log_not_premise('Invalid command.', level='error')
                    
            except Exception as e:
                self.logger.error(f"Error in interaction: {e}")
                print(f"An error occurred: {str(e)}")

# Initialize medical components if needed
try:
    from medical_socratic import MedicalSocraticReasoning
except ImportError:
    pass
