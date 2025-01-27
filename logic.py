# logic.py (c) 2025 Gregory L. Magnusson MIT license

import os
import json
from datetime import datetime
from typing import Set, List, Dict, Union, Optional, Tuple
import re
from logger import get_logger
from medical_patterns import MedicalPatterns

class LogicTables:
    """Enhanced logic system for medical reasoning and decision validation"""
    
    def __init__(self):
        self.logger = get_logger('logic')
        self.variables: Set[str] = set()
        self.expressions: List[str] = []
        self.valid_truths: Set[str] = set()
        self.contradictions: List[Dict] = []
        self.symptom_relationships: Dict[str, List[str]] = {}
        self.condition_relationships: Dict[str, Dict] = {}
        
        # Initialize components
        self.patterns = MedicalPatterns()
        self.medical_conditions = self._load_medical_conditions()
        self.medical_terminology = self._load_medical_terminology()
        self.symptom_patterns = self._load_symptom_patterns()
        
        # Initialize truth tables
        self._initialize_truth_tables()

    def _initialize_truth_tables(self):
        """Initialize truth table structure"""
        self.truth_tables = {
            "logical": {
                "variables": set(),
                "expressions": [],
                "valid_truths": set()
            },
            "medical": {
                "symptoms": {},
                "conditions": {},
                "relationships": {},
                "contradictions": []
            }
        }

    def tautology(self, statement: str) -> bool:
        """Validate if a statement is logically sound"""
        try:
            if not statement or not isinstance(statement, str):
                self.logger.debug("Invalid statement format", 
                                extra={'structured_data': {'statement': statement}})
                return False

            # Check basic logical structure
            has_context = len(statement.split()) > 3
            has_medical_terms = self._contains_medical_terms(statement)
            has_logical_structure = self._check_logical_structure(statement)
            
            # Check for contradictions
            if self._check_contradictions(statement):
                return False

            result = has_context and has_medical_terms and has_logical_structure
            
            self.logger.debug("Tautology check completed", 
                            extra={'structured_data': {
                                'statement': statement,
                                'has_context': has_context,
                                'has_medical_terms': has_medical_terms,
                                'has_logical_structure': has_logical_structure,
                                'result': result
                            }})
            
            return result
        except Exception as e:
            self.logger.error("Error in tautology check", 
                            extra={'structured_data': {
                                'error': str(e),
                                'statement': statement
                            }})
            return False

    def _check_contradictions(self, statement: str) -> bool:
        """Check for logical and medical contradictions"""
        try:
            # Split statement into components
            components = self._parse_logical_components(statement)
            
            # Check for direct contradictions
            for i, comp1 in enumerate(components):
                for comp2 in components[i+1:]:
                    if self._are_contradictory(comp1, comp2):
                        self.contradictions.append({
                            'statement': statement,
                            'component1': comp1,
                            'component2': comp2,
                            'timestamp': datetime.now().isoformat()
                        })
                        return True
            
            # Check medical contradictions
            return self._check_medical_contradictions(components)
            
        except Exception as e:
            self.logger.error("Error checking contradictions", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _parse_logical_components(self, statement: str) -> List[str]:
        """Parse statement into logical components"""
        components = []
        current_component = []
        
        # Split on logical operators
        words = statement.lower().split()
        for word in words:
            if self._is_logical_operator(word):
                if current_component:
                    components.append(' '.join(current_component))
                    current_component = []
            current_component.append(word)
            
        if current_component:
            components.append(' '.join(current_component))
            
        return components

    def _is_logical_operator(self, word: str) -> bool:
        """Check if word is a logical operator"""
        logical_operators = {
            "and", "or", "not", "if", "then", "because",
            "therefore", "implies", "since", "while"
        }
        return word.lower() in logical_operators

    def _are_contradictory(self, comp1: str, comp2: str) -> bool:
        """Check if two components are contradictory"""
        # Check direct negations
        negation_words = {"not", "no", "never", "without"}
        comp1_words = set(comp1.lower().split())
        comp2_words = set(comp2.lower().split())
        
        # Check if one component negates the other
        has_negation = bool(comp1_words.intersection(negation_words) or 
                          comp2_words.intersection(negation_words))
        
        if has_negation:
            # Remove negation words and compare remaining terms
            comp1_terms = comp1_words - negation_words
            comp2_terms = comp2_words - negation_words
            if comp1_terms.intersection(comp2_terms):
                return True
                
        # Check medical contradictions
        return self._check_medical_contradiction(comp1, comp2)

    def _check_medical_contradiction(self, comp1: str, comp2: str) -> bool:
        """Check for medical contradictions between components"""
        try:
            # Check temporal contradictions
            temporal1 = self._extract_temporal_patterns(comp1)
            temporal2 = self._extract_temporal_patterns(comp2)
            if temporal1 and temporal2 and self._are_temporal_contradictory(temporal1, temporal2):
                return True
            
            # Check severity contradictions
            severity1 = self._extract_severity_patterns(comp1)
            severity2 = self._extract_severity_patterns(comp2)
            if severity1 and severity2 and self._are_severity_contradictory(severity1, severity2):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error("Error in medical contradiction check", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _extract_temporal_patterns(self, text: str) -> List[str]:
        """Extract temporal patterns from text"""
        patterns = []
        for category, terms in self.patterns.SYMPTOM_PATTERNS["temporal"].items():
            if any(term in text.lower() for term in terms):
                patterns.append(category)
        return patterns

    def _extract_severity_patterns(self, text: str) -> List[str]:
        """Extract severity patterns from text"""
        patterns = []
        for category, terms in self.patterns.SYMPTOM_PATTERNS["severity"].items():
            if any(term in text.lower() for term in terms):
                patterns.append(category)
        return patterns

    def _are_temporal_contradictory(self, temporal1: List[str], temporal2: List[str]) -> bool:
        """Check if temporal patterns are contradictory"""
        contradictions = {
            ("acute", "chronic"),
            ("sudden", "persistent"),
            ("new onset", "long-term")
        }
        return any((t1, t2) in contradictions or (t2, t1) in contradictions 
                  for t1 in temporal1 for t2 in temporal2)

    def _are_severity_contradictory(self, severity1: List[str], severity2: List[str]) -> bool:
        """Check if severity patterns are contradictory"""
        contradictions = {
            ("mild", "severe"),
            ("minimal", "extreme"),
            ("light", "critical")
        }
        return any((s1, s2) in contradictions or (s2, s1) in contradictions 
                  for s1 in severity1 for s2 in severity2)

    def _check_medical_contradictions(self, components: List[str]) -> bool:
        """Check for medical contradictions in components"""
        try:
            # Extract medical elements
            medical_elements = self._extract_medical_elements(' '.join(components))
            
            # Check symptom contradictions
            if self._check_symptom_contradictions(medical_elements.get("symptoms", [])):
                return True
            
            # Check condition contradictions
            if self._check_condition_contradictions(medical_elements.get("conditions", [])):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error("Error checking medical contradictions", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _check_symptom_contradictions(self, symptoms: List[str]) -> bool:
        """Check for contradictory symptoms"""
        try:
            for i, symptom1 in enumerate(symptoms):
                for symptom2 in symptoms[i+1:]:
                    if (symptom1, symptom2) in self.symptom_relationships.get("contradicts", []):
                        self.contradictions.append({
                            'type': 'symptom',
                            'symptom1': symptom1,
                            'symptom2': symptom2,
                            'timestamp': datetime.now().isoformat()
                        })
                        return True
            return False
        except Exception as e:
            self.logger.error("Error checking symptom contradictions", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _check_condition_contradictions(self, conditions: List[str]) -> bool:
        """Check for contradictory conditions"""
        try:
            for i, condition1 in enumerate(conditions):
                for condition2 in conditions[i+1:]:
                    if (condition1, condition2) in self.condition_relationships.get("contradicts", []):
                        self.contradictions.append({
                            'type': 'condition',
                            'condition1': condition1,
                            'condition2': condition2,
                            'timestamp': datetime.now().isoformat()
                        })
                        return True
            return False
        except Exception as e:
            self.logger.error("Error checking condition contradictions", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _contains_medical_terms(self, statement: str) -> bool:
        """Check if statement contains recognized medical terminology"""
        try:
            medical_terms = set(self.medical_terminology.keys())
            statement_words = set(statement.lower().split())
            matches = medical_terms.intersection(statement_words)
            
            self.logger.debug("Medical terms check completed", 
                            extra={'structured_data': {
                                'matches_found': list(matches)
                            }})
            
            return bool(matches)
        except Exception as e:
            self.logger.error("Error checking medical terms", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _check_logical_structure(self, statement: str) -> bool:
        """Check if statement has valid logical structure"""
        try:
            logical_indicators = ['if', 'then', 'because', 'therefore', 'implies', 'since']
            found_indicators = [i for i in logical_indicators if i in statement.lower()]
            
            self.logger.debug("Logical structure check completed", 
                            extra={'structured_data': {
                                'found_indicators': found_indicators
                            }})
            
            return bool(found_indicators)
        except Exception as e:
            self.logger.error("Error checking logical structure", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _load_medical_conditions(self) -> Dict:
        """Load medical conditions database"""
        try:
            conditions_file = './memory/medical/conditions.json'
            if os.path.exists(conditions_file):
                with open(conditions_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error("Error loading medical conditions", 
                            extra={'structured_data': {'error': str(e)}})
            return {}

    def _load_medical_terminology(self) -> Dict:
        """Load medical terminology database"""
        try:
            terminology_file = './memory/medical/terminology.json'
            if os.path.exists(terminology_file):
                with open(terminology_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error("Error loading medical terminology", 
                            extra={'structured_data': {'error': str(e)}})
            return {}

    def _load_symptom_patterns(self) -> Dict:
        """Load symptom pattern database"""
        try:
            patterns_file = './memory/medical/symptom_patterns.json'
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error("Error loading symptom patterns", 
                            extra={'structured_data': {'error': str(e)}})
            return {}
