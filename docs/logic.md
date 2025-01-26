# logic.md

logic.py is an advanced module system designed for medical pattern recognition, confidence scoring, and logical reasoning within medical contexts. It consists of three main classes:

MedicalPatterns: Defines various medical-related patterns such as symptoms, conditions, treatments, and risk factors.
ConfidenceScoring: Implements a comprehensive confidence scoring mechanism to evaluate the reliability of medical data and conclusions.
LogicTables: Facilitates medical reasoning, logical validation, and decision-making based on the patterns and confidence scores.
This document provides a detailed explanation of each component within the logic.py module, outlining their structure, functionalities, and interactions.

# Table of Contents
MedicalPatterns Class
ConfidenceScoring Class
LogicTables Class
External Dependencies and Data
Logging Mechanism
Conclusion
MedicalPatterns Class

```python

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
}
```


The MedicalPatterns class serves as a repository for various medical-related patterns used in recognizing and categorizing medical information. It contains four main dictionaries:

# SYMPTOM_PATTERNS: Categorizes symptom descriptors based on different attributes:
```text
Temporal: Describes the onset and duration of symptoms (e.g., acute, chronic).
Severity: Indicates the intensity of symptoms (e.g., mild, severe).
Quality: Details the nature or type of symptoms (e.g., sharp pain, tingling sensation).
Location: Specifies where the symptoms are experienced in the body (e.g., localized, bilateral).
CONDITION_INDICATORS: Identifies phrases that signal various condition-related contexts:

Diagnostic: Terms indicating a confirmed diagnosis.
Suspected: Terms suggesting a possible condition.
Differential: Phrases used to differentiate between potential conditions.
Comorbid: Indicators of concurrent conditions.
TREATMENT_PATTERNS: Lists terms related to different treatment modalities:

Medication: Terms associated with drug treatments.
Procedure: Terms related to medical procedures.
Therapy: Types of therapeutic interventions.
Lifestyle: Lifestyle modifications as treatments.
RISK_FACTORS: Enumerates various risk factors influencing medical conditions:

Demographic: Factors like age and gender.
Lifestyle: Habits such as smoking or diet.
Medical: Previous medical history.
Environmental: External factors like exposure to toxins.
```

Patterns are utilized throughout the logic.pymodule to recognize and categorize medical information from textual data. By matching input data against these patterns, the system can identify relevant medical terms, symptoms, treatments, and risk factors, facilitating accurate medical reasoning and decision-making.

# ConfidenceScoring Class
```python

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
        ```

ConfidenceScoring class provides a robust mechanism to evaluate the confidence level of medical data and conclusions. It assesses various factors and their components to compute an overall confidence score, categorize the confidence level, and generate reliability indicators.


# CONFIDENCE_FACTORS: A dictionary defining the factors influencing confidence scores. Each factor has:

weight: The importance of the factor in the overall score.
components: Sub-factors with individual weights contributing to the factor's score.

Main factors include:
```text
medical_context: Evaluates medical terminology, pattern matching, and context relevance.
logical_structure: Assesses syntax, coherence, and completeness.
evidence_support: Looks at symptom clarity, condition correlation, and temporal relationships.
consistency: Checks internal consistency and alignment with the knowledge base.
severity_assessment: Evaluates the clarity of severity, urgency recognition, and risk assessment.
calculate_confidence(validation_data):
```
Purpose: Computes the overall confidence score based on the provided validation_data.
Process: Iterates through each confidence factor.

Calculates individual factor scores by evaluating their components.
Aggregates weighted factor scores to determine the overall confidence.
Determines the confidence level (e.g., High, Moderate) based on the score.
Generates reliability indicators highlighting strengths or weaknesses.
```python
_calculate_factor_score(validation_data, factor, config):
```
Purpose: Calculates the score for a specific confidence factor.
Process:
Iterates through each component of the factor.
Evaluates each component's score.
Aggregates the weighted component scores to derive the factor's score.
```python
_evaluate_component(validation_data, factor, component):
```
Purpose: Evaluates individual components within a confidence factor.
Process:
Determines the appropriate evaluation method based on the factor and component.
Returns a normalized score between 0 and 1.
Defaults to a mid-score (0.5) if specific evaluation is not defined.
```python
_evaluate_terminology(validation_data), _evaluate_patterns(validation_data), _evaluate_context(validation_data):
```
Purpose: Specific evaluation methods for components under medical_context.
Process:
Terminology: Normalizes the count of medical terms.
Patterns: Normalizes the count of identified patterns.
Context Relevance: Uses a provided context score or defaults to 0.5.
```python
_get_confidence_level(score):
```
Purpose: Categorizes the overall confidence score into qualitative levels.
Levels:
```text
0.9 and above: Very High
0.75 to 0.89: High
0.6 to 0.74: Moderate
0.4 to 0.59: Low
Below 0.4: Very Low
```
```python
_get_reliability_indicators(factor_scores, validation_data):
```
Purpose: Generates indicators that highlight specific strengths or weaknesses in the confidence assessment.
Process:
Flags factors with low (<0.5) or strong (>0.8) scores.
Checks for additional issues like contradictions, missing context, or emergency indicators.

ConfidenceScoring class is integral in evaluating the reliability of medical data and conclusions derived from it. By providing a structured and weighted approach, it ensures that multiple aspects of the data are considered, leading to a nuanced confidence assessment.

# LogicTables Class
```
python

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
```

The LogicTables class is the core component responsible for medical reasoning, logical validation, and decision-making. It integrates medical patterns and confidence scoring to assess the validity and reliability of medical conclusions based on given premises.

Key Components
Initialization (__init__):

Logger Setup: Initializes a logger for tracking operations and debugging.
Variables and Data Structures:
variables, expressions, valid_truths, contradictions, symptom_relationships, condition_relationships: Various data structures to store logical elements and relationships.
Component Initialization:
MedicalPatterns: Instance to access medical patterns.
ConfidenceScoring: Instance to evaluate confidence scores.
Data Loading: Loads medical conditions, terminology, and symptom patterns from external JSON files or creates default structures if files are missing.

# Logging (setup_logging):

Purpose: Configures the logging system to record events, errors, and debugging information.
Process:
Creates a logs directory if it doesn't exist.
Sets up a file handler with a specific format for log messages.
Sets the logging level to DEBUG to capture detailed logs.

# Tautology Validation (tautology):

Purpose: Determines if a statement is logically sound.
Criteria:
The statement must be a non-empty string.
Contains sufficient context (more than three words).
Includes recognized medical terms.
Possesses a valid logical structure (e.g., contains logical indicators like "if", "because").

# Medical Terminology Check (_contains_medical_terms):

Purpose: Verifies if the statement includes recognized medical terms.
Process:
Compares words in the statement against a set of known medical conditions.
Logical Structure Check (_check_logical_structure):

Purpose: Ensures the statement has a valid logical framework.
Indicators: Looks for words like "if", "then", "because", etc.

# Unifying Variables (unify_variables):

Purpose: Checks if two statements are logically equivalent.
Process:
Normalizes both statements (lowercase and stripped of whitespace).
Direct comparison or evaluates semantic similarity based on word overlap (threshold > 70%).

# Semantic Similarity Check (_check_semantic_similarity):

Purpose: Determines if two statements share a significant overlap in meaning.
Process:
Calculates the ratio of overlapping words to total unique words.
Considers statements similar if the ratio exceeds 0.7.

# Conclusion Validation (validate_conclusion):

Purpose: Assesses whether a medical conclusion logically follows from given premises.
Process:
Checks for the presence of conclusion and premises.
Validates the conclusion's tautology.
Calculates a confidence score if valid.
Provides reasons for validation results.

# Confidence Calculation (_calculate_confidence):

Purpose: Computes a confidence score for the conclusion based on premises.
Factors:
Premise Factor: Proportion of premises provided (capped at 1.0).
Logic Factor: Based on the conclusion's logical structure.
Medical Factor: Based on the presence of medical terms in the conclusion.
Process: Averages the three factors to derive the confidence score.

# Data Loading Methods:
```python
_load_medical_conditions, _load_medical_terminology, _load_symptom_patterns:
```
Purpose: Load respective data from JSON files.
Fallback: If files are not found, create default data structures.
Default Data Creation Methods:
```python
_create_default_medical_conditions, _create_default_medical_terminology, _create_default_symptom_patterns:
```
Purpose: Provide baseline data structures to ensure the system operates even without external data files.

LogicTables class is pivotal for validating medical conclusions and ensuring logical consistency within medical reasoning. By integrating pattern recognition and confidence scoring, it provides a structured approach to assess the validity and reliability of medical statements and decisions.

# External Dependencies and Data
The LogicTables class relies on external JSON files to populate its databases. These files include:

medical_conditions.json: Contains a comprehensive list of medical conditions with details such as severity, common symptoms, contraindications, and related conditions.

medical_terminology.json: Houses a collection of medical terms categorized into symptoms, conditions, procedures, and medications.

symptom_patterns.json: Defines various symptom patterns categorized by their nature (acute, chronic, emergency, common).

# Handling Missing Files
If any of these JSON files are missing, the class automatically generates default data structures to ensure the system remains operational. This design choice promotes robustness and prevents runtime errors due to missing data.

# Logging Mechanism
Logging is a critical aspect of the LogicTables class, facilitating monitoring, debugging, and auditing of the system's operations.

Logger Initialization (setup_logging):

Log Directory: Ensures that a designated directory (./memory/logs) exists to store log files.
File Handler: Configures a file handler to write logs to logic.log within the log directory.
Formatter: Sets a consistent format for log messages, including timestamps, logger name, log level, and the message.
Log Level: Configured to DEBUG to capture detailed information, which is essential for troubleshooting and analysis.
Usage Across Methods:

Throughout the LogicTables class, the logger can be utilized to record significant events, errors, and informational messages. This practice aids in maintaining transparency and facilitating maintenance.

logic.py module presents a framework for medical pattern recognition, confidence evaluation, and logical reasoning. By compartmentalizing functionalities into dedicated classes—MedicalPatterns, ConfidenceScoring, and LogicTables—the system ensures modularity, scalability, and maintainability. The integration of external data sources, comprehensive confidence scoring mechanisms, and robust logging further enhances the system's reliability and effectiveness in medical decision-making processes.


```python

# Example usage of LogicTables

from logic import LogicTables

# Initialize the LogicTables system
logic_system = LogicTables()

# Define premises and conclusion
premises = [
    "The patient has a persistent cough and fever.",
    "Testing showed elevated white blood cell count.",
    "Chest X-ray indicates possible pneumonia."
]

conclusion = "The patient is diagnosed with pneumonia."

# Validate the conclusion
validation_result = logic_system.validate_conclusion(conclusion, premises)

print(validation_result)
Expected Output
json
Copy
{
    "valid": True,
    "reason": "Logically sound conclusion",
    "confidence": 0.83
}
```
This example demonstrates how to utilize the LogicTables class to validate a medical conclusion based on provided premises. The system assesses the logical structure, presence of medical terms, and other factors to determine the validity and confidence level of the conclusion.
