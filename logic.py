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
        
        # Calculate scores for each major factor
        for factor, config in ConfidenceScoring.CONFIDENCE_FACTORS.items():
            factor_score = ConfidenceScoring._calculate_factor_score(
                validation_data, 
                factor, 
                config
            )
            confidence_result["factor_scores"][factor] = factor_score
            confidence_result["overall_confidence"] += factor_score * config["weight"]

        confidence_result["overall_confidence"] = round(
            confidence_result["overall_confidence"], 
            3
        )
        
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
            score = ConfidenceScoring._evaluate_component(
                validation_data, 
                factor, 
                component
            )
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
    """
    Enhanced logic system for medical reasoning and decision validation
    Implements comprehensive medical context validation and relationship tracking
    """
    
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
        """Initialize comprehensive logging system"""
        log_dir = './memory/logs'
        medical_log_dir = os.path.join(log_dir, 'medical')
        os.makedirs(medical_log_dir, exist_ok=True)
        
        # Configure handlers
        handlers = {
            'main': logging.FileHandler(f'{log_dir}/logic.log'),
            'medical': logging.FileHandler(f'{medical_log_dir}/medical_reasoning.log'),
            'patterns': logging.FileHandler(f'{medical_log_dir}/pattern_analysis.log'),
            'validation': logging.FileHandler(f'{medical_log_dir}/validation.log')
        }
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        for handler in handlers.values():
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG)

    def analyze_statement(self, statement: str) -> Dict:
        """Comprehensive medical statement analysis"""
        try:
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "original_statement": statement,
                "patterns_identified": self._identify_patterns(statement),
                "medical_context": self._validate_medical_context(statement),
                "logical_structure": self._check_logical_structure(statement),
                "contradictions": self._check_contradictions(statement),
                "relationships": self._analyze_medical_relationships(statement),
                "severity": self._determine_severity(statement),
                "emergency_indicators": self._check_emergency_indicators(statement)
            }
            
            # Calculate confidence with enhanced scoring
            analysis["confidence"] = self.confidence_scorer.calculate_confidence(analysis)
            
            # Add reasoning chain
            analysis["reasoning_chain"] = self._generate_reasoning_chain(analysis)
            
            self._log_analysis(analysis)
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing statement: {e}")
            return {"error": str(e)}

    def _identify_patterns(self, statement: str) -> Dict:
        """Enhanced pattern recognition"""
        return {
            "temporal": self._identify_temporal_patterns(statement),
            "severity": self._identify_severity_patterns(statement),
            "quality": self._identify_quality_patterns(statement),
            "location": self._identify_location_patterns(statement),
            "condition": self._identify_condition_patterns(statement),
            "treatment": self._identify_treatment_patterns(statement),
            "risk_factors": self._identify_risk_patterns(statement)
        }

    def _validate_medical_context(self, statement: str) -> Dict:
        """Validate medical context with detailed analysis"""
        context_analysis = {
            "has_medical_terms": False,
            "has_medical_patterns": False,
            "identified_terms": [],
            "context_score": 0.0,
            "context_type": "unknown"
        }
        
        # Check medical terminology
        medical_terms = self._extract_medical_terms(statement)
        context_analysis["has_medical_terms"] = bool(medical_terms)
        context_analysis["identified_terms"] = medical_terms
        
        # Check medical patterns
        pattern_matches = []
        for pattern_type, patterns in self.patterns.SYMPTOM_PATTERNS.items():
            for category, terms in patterns.items():
                if any(term in statement.lower() for term in terms):
                    pattern_matches.append(f"{pattern_type}:{category}")
        
        context_analysis["has_medical_patterns"] = bool(pattern_matches)
        context_analysis["identified_patterns"] = pattern_matches
        
        # Calculate context score
        context_analysis["context_score"] = self._calculate_context_score(
            context_analysis["has_medical_terms"],
            context_analysis["has_medical_patterns"],
            len(medical_terms),
            len(pattern_matches)
        )
        
        # Determine context type
        context_analysis["context_type"] = self._determine_context_type(
            medical_terms,
            pattern_matches
        )
        
        return context_analysis

    def _check_contradictions(self, statement: str) -> List[Dict]:
        """Check for medical contradictions with detailed analysis"""
        contradictions = []
        
        # Check against existing truths
        for truth in self.valid_truths:
            if self._are_contradictory(statement, truth):
                contradictions.append({
                    "type": "truth_contradiction",
                    "statement": statement,
                    "contradicts": truth,
                    "reason": self._analyze_contradiction(statement, truth)
                })
        
        # Check internal consistency
        internal_contradictions = self._check_internal_contradictions(statement)
        if internal_contradictions:
            contradictions.extend(internal_contradictions)
        
        # Check against medical knowledge base
        kb_contradictions = self._check_knowledge_base_contradictions(statement)
        if kb_contradictions:
            contradictions.extend(kb_contradictions)
        
        return contradictions

    def _analyze_medical_relationships(self, statement: str) -> Dict:
        """Analyze medical relationships and correlations"""
        analysis = {
            "symptoms": [],
            "conditions": [],
            "relationships": [],
            "correlations": [],
            "confidence": 0.0
        }
        
        # Extract symptoms and conditions
        symptoms, conditions = self._extract_medical_entities(statement)
        analysis["symptoms"] = symptoms
        analysis["conditions"] = conditions
        
        # Analyze relationships
        for symptom in symptoms:
            for condition in conditions:
                relationship = self._analyze_symptom_condition_relationship(
                    symptom,
                    condition
                )
                if relationship:
                    analysis["relationships"].append(relationship)
        
        # Calculate correlations
        analysis["correlations"] = self._calculate_medical_correlations(
            symptoms,
            conditions
        )
        
        # Calculate confidence
        analysis["confidence"] = self._calculate_relationship_confidence(
            analysis["relationships"],
            analysis["correlations"]
        )
        
        return analysis

    def _generate_reasoning_chain(self, analysis: Dict) -> List[Dict]:
        """Generate medical reasoning chain"""
        reasoning_chain = []
        
        # Add context reasoning
        if analysis["medical_context"]["has_medical_terms"]:
            reasoning_chain.append({
                "step": "context",
                "reasoning": "Medical context identified based on terminology",
                "confidence": analysis["medical_context"]["context_score"]
            })
        
        # Add pattern reasoning
        if analysis["patterns_identified"]:
            reasoning_chain.append({
                "step": "patterns",
                "reasoning": "Medical patterns detected in statement",
                "patterns": analysis["patterns_identified"]
            })
        
        # Add relationship reasoning
        if analysis["relationships"]["relationships"]:
            reasoning_chain.append({
                "step": "relationships",
                "reasoning": "Medical relationships identified",
                "relationships": analysis["relationships"]["relationships"]
            })
        
        # Add contradiction reasoning
        if analysis["contradictions"]:
            reasoning_chain.append({
                "step": "contradictions",
                "reasoning": "Contradictions found in statement",
                "contradictions": analysis["contradictions"]
            })
        
        return reasoning_chain

    def _log_analysis(self, analysis: Dict):
        """Log comprehensive analysis results"""
        log_entry = {
            "timestamp": analysis["timestamp"],
            "statement": analysis["original_statement"],
            "analysis_results": {
                "patterns": analysis["patterns_identified"],
                "context": analysis["medical_context"],
                "relationships": analysis["relationships"],
                "contradictions": analysis["contradictions"],
                "confidence": analysis["confidence"]
            },
            "reasoning_chain": analysis["reasoning_chain"]
        }
        
        try:
            # Log to pattern analysis file
            with open('./memory/logs/medical/pattern_analysis.json', 'a+') as f:
                self._append_to_json_log(f, log_entry)
            
            # Log to medical reasoning file
            with open('./memory/logs/medical/medical_reasoning.json', 'a+') as f:
                self._append_to_json_log(f, log_entry)
                
            self.logger.info(f"Analysis logged successfully for statement: {analysis['original_statement'][:50]}...")
            
        except Exception as e:
            self.logger.error(f"Error logging analysis: {e}")

    def _append_to_json_log(self, file_handle, entry: Dict):
        """Append entry to JSON log file"""
        file_handle.seek(0)
        try:
            logs = json.load(file_handle)
        except json.JSONDecodeError:
            logs = []
        
        logs.append(entry)
        file_handle.seek(0)
        file_handle.truncate()
        json.dump(logs, file_handle, indent=2)

    # Helper methods for loading and saving data
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

    # Default data creation methods
    def _create_default_medical_conditions(self) -> Dict:
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
        return {
            "symptoms": {},
            "conditions": {},
            "procedures": {},
            "medications": {}
        }

    def _create_default_symptom_patterns(self) -> Dict:
        return {
            "acute": [],
            "chronic": [],
            "emergency": [],
            "common": []
        }
