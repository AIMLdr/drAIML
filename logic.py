# logic.py
import logging
from typing import Set, List, Dict, Union, Optional, Tuple
from datetime import datetime
import os
import json
import re

class MedicalPatterns:
    """Enhanced medical pattern recognition system"""
    
    SYMPTOM_PATTERNS = {
        "temporal": {
            "acute": ["sudden", "abrupt", "recent", "new onset", "immediate"],
            "chronic": ["long-term", "ongoing", "persistent", "continuous", "lasting"],
            "intermittent": ["comes and goes", "periodic", "recurring", "occasional", "fluctuating"],
            "progressive": ["worsening", "increasing", "deteriorating", "advancing", "developing"]
        },
        "severity": {
            "mild": ["slight", "minor", "minimal", "light", "gentle"],
            "moderate": ["medium", "intermediate", "moderate-intensity", "substantial"],
            "severe": ["intense", "extreme", "severe", "excruciating", "unbearable"],
            "critical": ["life-threatening", "emergency", "critical", "urgent", "serious"]
        },
        "quality": {
            "pain": ["sharp", "dull", "throbbing", "burning", "stabbing", "aching"],
            "sensation": ["tingling", "numbness", "itching", "pressure", "tightness"],
            "visual": ["blurred", "double vision", "spots", "flashing", "dimness"],
            "auditory": ["ringing", "buzzing", "muffled", "loss of hearing"]
        },
        "location": {
            "specific": ["localized", "focused", "specific area", "point tenderness"],
            "radiating": ["spreading", "moving", "radiating to", "extending"],
            "bilateral": ["both sides", "bilateral", "symmetrical"],
            "systemic": ["throughout body", "generalized", "systemic", "widespread"]
        }
    }
    
    CONDITION_INDICATORS = {
        "diagnostic": ["diagnosed with", "confirmed", "testing showed", "results indicate"],
        "suspected": ["suspected", "possible", "probable", "likely", "consistent with"],
        "differential": ["rule out", "versus", "differential includes", "to consider"],
        "comorbid": ["along with", "associated with", "complicated by", "concurrent"]
    }
    
    TREATMENT_PATTERNS = {
        "medication": ["prescribed", "taking", "administered", "dosage", "frequency"],
        "procedure": ["underwent", "performed", "scheduled for", "completed"],
        "therapy": ["physical therapy", "occupational therapy", "counseling", "rehabilitation"],
        "lifestyle": ["diet", "exercise", "sleep", "stress management", "lifestyle changes"]
    }
    
    RISK_FACTORS = {
        "demographic": ["age", "gender", "ethnicity", "family history"],
        "lifestyle": ["smoking", "alcohol", "diet", "exercise", "occupation"],
        "medical": ["previous condition", "chronic disease", "medication history"],
        "environmental": ["exposure to", "travel history", "living conditions"]
    }

class ConfidenceScoring:
    """Enhanced confidence scoring system"""
    
    CONFIDENCE_FACTORS = {
        "medical_context": {
            "weight": 0.25,
            "components": {
                "terminology": 0.4,
                "pattern_match": 0.3,
                "context_relevance": 0.3
            }
        },
        "logical_structure": {
            "weight": 0.20,
            "components": {
                "syntax": 0.3,
                "coherence": 0.4,
                "completeness": 0.3
            }
        },
        "evidence_support": {
            "weight": 0.25,
            "components": {
                "symptom_clarity": 0.35,
                "condition_correlation": 0.35,
                "temporal_relationship": 0.30
            }
        },
        "consistency": {
            "weight": 0.15,
            "components": {
                "internal_consistency": 0.5,
                "knowledge_base_alignment": 0.5
            }
        },
        "severity_assessment": {
            "weight": 0.15,
            "components": {
                "severity_clarity": 0.4,
                "urgency_recognition": 0.3,
                "risk_assessment": 0.3
            }
        }
    }

    @staticmethod
    def calculate_confidence(validation_data: Dict) -> Dict[str, Union[float, Dict]]:
        """Calculate comprehensive confidence score"""
        confidence_result = {
            "overall_confidence": 0.0,
            "component_scores": {},
            "factor_scores": {},
            "confidence_level": "",
            "reliability_indicators": []
        }
        
        for factor, config in ConfidenceScoring.CONFIDENCE_FACTORS.items():
            factor_score = ConfidenceScoring._calculate_factor_score(
                validation_data, 
                factor, 
                config
            )
            confidence_result["factor_scores"][factor] = factor_score
            confidence_result["overall_confidence"] += factor_score * config["weight"]

        confidence_result["overall_confidence"] = round(confidence_result["overall_confidence"], 3)
        confidence_result["confidence_level"] = ConfidenceScoring._get_confidence_level(
            confidence_result["overall_confidence"]
        )
        confidence_result["reliability_indicators"] = ConfidenceScoring._get_reliability_indicators(
            confidence_result["factor_scores"],
            validation_data
        )

        return confidence_result

    @staticmethod
    def _calculate_factor_score(validation_data: Dict, factor: str, config: Dict) -> float:
        """Calculate score for individual confidence factor"""
        component_scores = {}
        for component, weight in config["components"].items():
            score = ConfidenceScoring._evaluate_component(validation_data, factor, component)
            component_scores[component] = score * weight
        return sum(component_scores.values())

    @staticmethod
    def _evaluate_component(validation_data: Dict, factor: str, component: str) -> float:
        """Evaluate individual component score"""
        if factor == "medical_context":
            if component == "terminology":
                return ConfidenceScoring._evaluate_terminology(validation_data)
            elif component == "pattern_match":
                return ConfidenceScoring._evaluate_patterns(validation_data)
            elif component == "context_relevance":
                return ConfidenceScoring._evaluate_context(validation_data)
        return 0.5

    @staticmethod
    def _evaluate_terminology(validation_data: Dict) -> float:
        """Evaluate medical terminology usage"""
        if "medical_terms" in validation_data:
            return len(validation_data["medical_terms"]) / 10.0  # Normalize to 0-1
        return 0.0

    @staticmethod
    def _evaluate_patterns(validation_data: Dict) -> float:
        """Evaluate medical pattern matches"""
        if "patterns_identified" in validation_data:
            return len(validation_data["patterns_identified"]) / 5.0  # Normalize to 0-1
        return 0.0

    @staticmethod
    def _evaluate_context(validation_data: Dict) -> float:
        """Evaluate medical context relevance"""
        if "context_score" in validation_data:
            return validation_data["context_score"]
        return 0.5

    @staticmethod
    def _get_confidence_level(score: float) -> str:
        """Determine confidence level from score"""
        if score >= 0.9:
            return "Very High"
        elif score >= 0.75:
            return "High"
        elif score >= 0.6:
            return "Moderate"
        elif score >= 0.4:
            return "Low"
        else:
            return "Very Low"

    @staticmethod
    def _get_reliability_indicators(factor_scores: Dict, validation_data: Dict) -> List[str]:
        """Generate reliability indicators"""
        indicators = []
        for factor, score in factor_scores.items():
            if score < 0.5:
                indicators.append(f"Low {factor.replace('_', ' ')} confidence")
            elif score > 0.8:
                indicators.append(f"Strong {factor.replace('_', ' ')} confidence")

        if validation_data.get("contradictions"):
            indicators.append("Contains contradictions")
        if validation_data.get("missing_context"):
            indicators.append("Incomplete context")
        if validation_data.get("emergency_indicators"):
            indicators.append("Emergency indicators present")

        return indicators

class LogicTables:
    """Enhanced logic system for medical reasoning and decision validation"""
    
    def __init__(self):
        self.logger = logging.getLogger('LogicTables')
        self.variables: Set[str] = set()
        self.expressions: List[str] = []
        self.valid_truths: Set[str] = set()
        self.contradictions: List[Dict] = []
        self.symptom_relationships: Dict[str, List[str]] = {}
        self.condition_relationships: Dict[str, Dict] = {}
        
        # Initialize components
        self.patterns = MedicalPatterns()
        self.confidence_scorer = ConfidenceScoring()
        self.medical_conditions = self._load_medical_conditions()
        self.medical_terminology = self._load_medical_terminology()
        self.symptom_patterns = self._load_symptom_patterns()
        
        self.setup_logging()

    def setup_logging(self):
        """Initialize logging system"""
        log_dir = './memory/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        handler = logging.FileHandler(f'{log_dir}/logic.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def tautology(self, statement: str) -> bool:
        """Validate if a statement is logically sound"""
        if not statement or not isinstance(statement, str):
            return False

        has_context = len(statement.split()) > 3
        has_medical_terms = self._contains_medical_terms(statement)
        has_logical_structure = self._check_logical_structure(statement)

        return has_context and has_medical_terms and has_logical_structure

    def _contains_medical_terms(self, statement: str) -> bool:
        """Check if statement contains recognized medical terminology"""
        medical_terms = set(self.medical_conditions.keys())
        statement_words = set(statement.lower().split())
        return bool(medical_terms.intersection(statement_words))

    def _check_logical_structure(self, statement: str) -> bool:
        """Check if statement has valid logical structure"""
        logical_indicators = ['if', 'then', 'because', 'therefore', 'due to', 'causes']
        return any(indicator in statement.lower() for indicator in logical_indicators)

    def unify_variables(self, statement1: str, statement2: str) -> bool:
        """Check if two statements are logically equivalent"""
        if not statement1 or not statement2:
            return False

        norm1 = self._normalize_statement(statement1)
        norm2 = self._normalize_statement(statement2)

        if norm1 == norm2:
            return True

        return self._check_semantic_similarity(norm1, norm2)

    def _normalize_statement(self, statement: str) -> str:
        """Normalize statement for comparison"""
        return statement.lower().strip()

    def _check_semantic_similarity(self, stmt1: str, stmt2: str) -> bool:
        """Check if statements are semantically similar"""
        words1 = set(stmt1.split())
        words2 = set(stmt2.split())
        
        overlap = words1.intersection(words2)
        total_words = words1.union(words2)
        
        similarity_ratio = len(overlap) / len(total_words) if total_words else 0
        return similarity_ratio > 0.7

    def validate_conclusion(self, conclusion: str, premises: List[str]) -> Dict[str, Union[bool, str, float]]:
        """Validate a medical conclusion based on premises"""
        validation = {
            "valid": False,
            "reason": "",
            "confidence": 0.0
        }

        if not conclusion or not premises:
            validation["reason"] = "Missing conclusion or premises"
            return validation

        if self.tautology(conclusion):
            validation["valid"] = True
            validation["confidence"] = self._calculate_confidence(conclusion, premises)
            validation["reason"] = "Logically sound conclusion"
        else:
            validation["reason"] = "Invalid logical structure"

        return validation

    def _calculate_confidence(self, conclusion: str, premises: List[str]) -> float:
        """Calculate confidence score for conclusion"""
        if not conclusion or not premises:
            return 0.0

        premise_factor = min(len(premises) / 3, 1.0)
        logic_factor = 1.0 if self._check_logical_structure(conclusion) else 0.5
        medical_factor = 1.0 if self._contains_medical_terms(conclusion) else 0.7

        confidence = (premise_factor + logic_factor + medical_factor) / 3
        return round(confidence, 2)

    def _load_medical_conditions(self) -> Dict:
        """Load medical conditions database"""
        try:
            with open('medical_conditions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_medical_conditions()

    def _load_medical_terminology(self) -> Dict:
        """Load medical terminology database"""
        try:
            with open('medical_terminology.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_medical_terminology()

    def _load_symptom_patterns(self) -> Dict:
        """Load symptom pattern database"""
        try:
            with open('symptom_patterns.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_symptom_patterns()

    def _create_default_medical_conditions(self) -> Dict:
        """Create default medical conditions structure"""
        return {
            "general": {
                "requires_professional": True,
                "severity": "variable",
                "common_symptoms": [],
                "contraindications": [],
                "related_conditions": []
            }
        }

    def _create_default_medical_terminology(self) -> Dict:
        """Create default medical terminology structure"""
        return {
            "symptoms": {},
            "conditions": {},
            "procedures": {},
            "medications": {}
        }

    def _create_default_symptom_patterns(self) -> Dict:
        """Create default symptom patterns structure"""
        return {
            "acute": [],
            "chronic": [],
            "emergency": [],
            "common": []
        }
