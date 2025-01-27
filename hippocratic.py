# hippocratic.py (c) 2025 Gregory L. Magnusson MIT license

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from logger import get_logger
from memory import MedicalDecision, store_medical_decision
from logic import LogicTables
from medical_patterns import MedicalPatterns

class HippocraticPrinciples:
    """Core principles based on the Hippocratic Oath and modern medical ethics"""
    
    PRINCIPLES = {
        "do_no_harm": {
            "principle": "First, do no harm (primum non nocere)",
            "description": "Avoid causing harm to patients; every medical decision must first consider safety",
            "validation_rules": [
                "Check for contraindications",
                "Assess risk-benefit ratio",
                "Consider alternative treatments",
                "Evaluate potential side effects"
            ]
        },
        "beneficence": {
            "principle": "Act in the best interest of the patient",
            "description": "Promote well-being and take positive steps to help patients",
            "validation_rules": [
                "Ensure treatment benefits outweigh risks",
                "Consider patient's quality of life",
                "Provide evidence-based recommendations",
                "Focus on patient wellness"
            ]
        },
        "patient_autonomy": {
            "principle": "Respect patient's right to make decisions",
            "description": "Honor patient preferences and right to informed decision-making",
            "validation_rules": [
                "Provide clear information",
                "Respect patient choices",
                "Ensure informed consent",
                "Protect patient rights"
            ]
        },
        "justice": {
            "principle": "Treat all patients fairly and equally",
            "description": "Ensure fair distribution of benefits and risks",
            "validation_rules": [
                "Avoid discrimination",
                "Ensure equal access",
                "Consider resource allocation",
                "Maintain professional standards"
            ]
        },
        "confidentiality": {
            "principle": "Protect patient privacy and information",
            "description": "Maintain strict confidentiality of patient information",
            "validation_rules": [
                "Protect patient data",
                "Secure communications",
                "Limit information sharing",
                "Maintain records securely"
            ]
        },
        "informed_consent": {
            "principle": "Ensure patient understanding and agreement",
            "description": "Obtain informed consent for all medical decisions",
            "validation_rules": [
                "Explain procedures clearly",
                "Document consent",
                "Verify understanding",
                "Allow questions"
            ]
        },
        "professional_ethics": {
            "principle": "Maintain professional standards and ethics",
            "description": "Uphold medical professional standards and ethical conduct",
            "validation_rules": [
                "Follow medical guidelines",
                "Maintain competence",
                "Collaborate appropriately",
                "Document decisions"
            ]
        }
    }

    EMERGENCY_KEYWORDS = [
        "heart attack", "stroke", "bleeding", "unconscious", "breathing difficulty",
        "severe pain", "chest pain", "head injury", "seizure", "anaphylaxis",
        "suicide", "overdose", "emergency", "critical", "severe", "urgent"
    ]

    RISK_LEVELS = {
        "low": {
            "description": "Minimal risk to patient",
            "requires_monitoring": False,
            "requires_immediate_action": False
        },
        "moderate": {
            "description": "Notable risk requiring attention",
            "requires_monitoring": True,
            "requires_immediate_action": False
        },
        "high": {
            "description": "Significant risk requiring close attention",
            "requires_monitoring": True,
            "requires_immediate_action": True
        },
        "critical": {
            "description": "Life-threatening risk requiring emergency response",
            "requires_monitoring": True,
            "requires_immediate_action": True,
            "requires_emergency_services": True
        }
    }

    VALIDATION_LEVELS = {
        "basic": {
            "checks": ["do_no_harm", "confidentiality"],
            "required_score": 0.6
        },
        "standard": {
            "checks": ["do_no_harm", "beneficence", "patient_autonomy", "confidentiality"],
            "required_score": 0.7
        },
        "comprehensive": {
            "checks": list(PRINCIPLES.keys()),
            "required_score": 0.8
        }
    }

    DISCLAIMER = """
    IMPORTANT MEDICAL DISCLAIMER:
    This is AI-assisted medical information. Always consult with qualified 
    healthcare professionals for medical advice, diagnosis, or treatment. 
    Seek immediate emergency care for urgent medical conditions.
    
    This system:
    1. Does not replace professional medical advice
    2. Cannot diagnose conditions or prescribe treatments
    3. Should not be used in medical emergencies
    4. Serves as informational support only
    
    IN CASE OF EMERGENCY:
    - Call emergency services immediately
    - Contact your healthcare provider
    - Seek immediate medical attention
    """

    def __init__(self):
        self.logger = get_logger('hippocratic_principles')
        self.validation_history = []
        self._initialize_logging()

    def _initialize_logging(self):
        """Initialize logging for principle applications"""
        try:
            self.log_paths = {
                'principle_applications': './memory/logs/hippocratic/principles.json',
                'validation_history': './memory/logs/hippocratic/validation.json',
                'ethical_decisions': './memory/logs/hippocratic/decisions.json',
                'emergency_logs': './memory/logs/hippocratic/emergency.json'
            }

            # Create log directories
            for path in self.log_paths.values():
                os.makedirs(os.path.dirname(path), exist_ok=True)

            self.logger.info("Hippocratic logging initialized", 
                           extra={'structured_data': {
                               'log_paths': self.log_paths
                           }})
        except Exception as e:
            self.logger.error(f"Error initializing Hippocratic logging: {e}")
            raise

    def log_principle_application(self, principle: str, context: Dict):
        """Log application of Hippocratic principle"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "principle": principle,
                "context": context,
                "validation_rules_applied": self.PRINCIPLES[principle]["validation_rules"]
            }

            self._append_to_log('principle_applications', entry)
            
            self.logger.info(f"Principle applied: {principle}", 
                           extra={'structured_data': entry})
        except Exception as e:
            self.logger.error(f"Error logging principle application: {e}")

    def log_validation(self, validation_result: Dict):
        """Log validation result"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "validation_result": validation_result,
                "principles_checked": validation_result.get("principles_checked", []),
                "validation_level": validation_result.get("validation_level", "basic")
            }

            self._append_to_log('validation_history', entry)
            self.validation_history.append(entry)
            
            self.logger.info("Validation logged", 
                           extra={'structured_data': entry})
        except Exception as e:
            self.logger.error(f"Error logging validation: {e}")

    def log_emergency(self, context: Dict):
        """Log emergency situation"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "emergency_context": context,
                "keywords_detected": [
                    kw for kw in self.EMERGENCY_KEYWORDS 
                    if kw in context.get("text", "").lower()
                ],
                "risk_level": "critical"
            }

            self._append_to_log('emergency_logs', entry)
            
            self.logger.critical("Emergency situation logged", 
                               extra={'structured_data': entry})
        except Exception as e:
            self.logger.error(f"Error logging emergency: {e}")

    def _append_to_log(self, log_type: str, entry: Dict):
        """Append entry to specified log file"""
        try:
            log_path = self.log_paths[log_type]
            
            try:
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            logs.append(entry)

            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error appending to log {log_type}: {e}")
            
class HippocraticReasoning:
    """Medical ethics reasoning and validation system"""
    
    def __init__(self):
        self.logger = get_logger('hippocratic_reasoning')
        self.principles = HippocraticPrinciples()
        self.logic_tables = LogicTables()
        self.medical_patterns = MedicalPatterns()
        
        # Initialize validation tracking
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "validations_performed": 0,
            "emergency_situations": 0,
            "ethical_conflicts": []
        }
        
        self.logger.info("Hippocratic Reasoning initialized", 
                        extra={'structured_data': {
                            'session_id': self.current_session["session_id"]
                        }})

    def validate_medical_response(self, 
                                response: str, 
                                context: Dict,
                                validation_level: str = "comprehensive",
                                provider: str = None,
                                model: str = None) -> Dict:
        """
        Validate medical response against Hippocratic principles
        """
        try:
            validation_start = datetime.now()
            
            # Check for emergencies first
            is_emergency = self._check_emergency_situation(response, context)
            if is_emergency:
                return self._handle_emergency_response(response, context)

            # Prepare validation context
            validation_context = self._prepare_validation_context(
                response, context, provider, model
            )

            # Perform validation checks
            validation_result = self._perform_validation_checks(
                validation_context, validation_level
            )

            # Add response metadata
            validation_result.update({
                "timestamp": datetime.now().isoformat(),
                "validation_duration": (datetime.now() - validation_start).total_seconds(),
                "provider": provider,
                "model": model,
                "session_id": self.current_session["session_id"]
            })

            # Log validation
            self.principles.log_validation(validation_result)
            self.current_session["validations_performed"] += 1

            return validation_result

        except Exception as e:
            self.logger.error("Validation error", 
                            extra={'structured_data': {
                                'error': str(e),
                                'response': response,
                                'context': context
                            }})
            return {
                "is_valid": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _check_emergency_situation(self, response: str, context: Dict) -> bool:
        """Check if situation requires emergency response"""
        try:
            # Check response and context for emergency keywords
            combined_text = f"{response} {json.dumps(context)}".lower()
            
            emergency_detected = any(
                keyword in combined_text 
                for keyword in self.principles.EMERGENCY_KEYWORDS
            )

            if emergency_detected:
                self.principles.log_emergency({
                    "text": combined_text,
                    "context": context
                })
                self.current_session["emergency_situations"] += 1

            return emergency_detected

        except Exception as e:
            self.logger.error("Emergency check error", 
                            extra={'structured_data': {'error': str(e)}})
            return False

    def _handle_emergency_response(self, response: str, context: Dict) -> Dict:
        """Generate appropriate response for emergency situation"""
        emergency_response = {
            "is_valid": False,
            "emergency": True,
            "message": "MEDICAL EMERGENCY DETECTED",
            "actions_required": [
                "Seek immediate medical attention",
                "Contact emergency services",
                "Do not rely on AI guidance in emergencies"
            ],
            "original_response": response,
            "timestamp": datetime.now().isoformat()
        }

        self.logger.critical("Emergency response generated", 
                           extra={'structured_data': emergency_response})
        return emergency_response

    def _prepare_validation_context(self, 
                                  response: str, 
                                  context: Dict, 
                                  provider: str, 
                                  model: str) -> Dict:
        """Prepare context for validation"""
        return {
            "response": response,
            "context": context,
            "provider": provider,
            "model": model,
            "medical_patterns": self._extract_medical_patterns(response),
            "risk_assessment": self._assess_risk_level(response, context)
        }

    def _extract_medical_patterns(self, text: str) -> Dict:
        """Extract medical patterns from text"""
        patterns = {
            "symptoms": [],
            "conditions": [],
            "treatments": [],
            "risk_factors": []
        }

        try:
            # Extract symptoms
            for category, symptom_patterns in self.medical_patterns.SYMPTOM_PATTERNS.items():
                for subcategory, terms in symptom_patterns.items():
                    matches = [term for term in terms if term in text.lower()]
                    if matches:
                        patterns["symptoms"].append({
                            "category": category,
                            "subcategory": subcategory,
                            "terms": matches
                        })

            # Extract conditions
            for category, indicators in self.medical_patterns.CONDITION_INDICATORS.items():
                matches = [ind for ind in indicators if ind in text.lower()]
                if matches:
                    patterns["conditions"].append({
                        "category": category,
                        "indicators": matches
                    })

            # Extract treatments
            for category, terms in self.medical_patterns.TREATMENT_PATTERNS.items():
                matches = [term for term in terms if term in text.lower()]
                if matches:
                    patterns["treatments"].append({
                        "category": category,
                        "terms": matches
                    })

            # Extract risk factors
            for category, factors in self.medical_patterns.RISK_FACTORS.items():
                matches = [factor for factor in factors if factor in text.lower()]
                if matches:
                    patterns["risk_factors"].append({
                        "category": category,
                        "factors": matches
                    })

            return patterns

        except Exception as e:
            self.logger.error("Error extracting medical patterns", 
                            extra={'structured_data': {'error': str(e)}})
            return patterns

    def _assess_risk_level(self, response: str, context: Dict) -> Dict:
        """Assess risk level of medical situation"""
        try:
            risk_assessment = {
                "level": "low",
                "factors": [],
                "requires_monitoring": False,
                "requires_immediate_action": False
            }

            # Check for critical indicators
            critical_indicators = set(self.principles.EMERGENCY_KEYWORDS)
            found_indicators = [
                indicator for indicator in critical_indicators 
                if indicator in response.lower()
            ]

            if found_indicators:
                risk_assessment.update({
                    "level": "critical",
                    "factors": found_indicators,
                    "requires_monitoring": True,
                    "requires_immediate_action": True
                })
                return risk_assessment

            # Assess severity patterns
            severity_patterns = self.medical_patterns.SYMPTOM_PATTERNS["severity"]
            
            if any(term in response.lower() for term in severity_patterns["severe"]):
                risk_assessment["level"] = "high"
                risk_assessment["requires_monitoring"] = True
                risk_assessment["requires_immediate_action"] = True
            elif any(term in response.lower() for term in severity_patterns["moderate"]):
                risk_assessment["level"] = "moderate"
                risk_assessment["requires_monitoring"] = True

            # Add risk factors
            risk_factors = self._extract_medical_patterns(response)["risk_factors"]
            if risk_factors:
                risk_assessment["factors"].extend([
                    f"{factor['category']}: {', '.join(factor['factors'])}"
                    for factor in risk_factors
                ])

            return risk_assessment

        except Exception as e:
            self.logger.error("Error assessing risk level", 
                            extra={'structured_data': {'error': str(e)}})
            return {"level": "unknown", "error": str(e)}

    def _perform_validation_checks(self, 
                                 validation_context: Dict, 
                                 validation_level: str) -> Dict:
        """Perform validation checks based on Hippocratic principles"""
        try:
            validation_config = self.principles.VALIDATION_LEVELS[validation_level]
            principles_to_check = validation_config["checks"]
            required_score = validation_config["required_score"]

            validation_results = []
            ethical_conflicts = []

            for principle in principles_to_check:
                principle_result = self._validate_principle(
                    principle, validation_context
                )
                validation_results.append(principle_result)
                
                if not principle_result["passed"] and principle_result.get("ethical_conflict"):
                    ethical_conflicts.append(principle_result["ethical_conflict"])

            # Calculate overall validation score
            total_score = sum(r["score"] for r in validation_results) / len(validation_results)
            
            validation_passed = total_score >= required_score and not ethical_conflicts

            result = {
                "is_valid": validation_passed,
                "validation_level": validation_level,
                "overall_score": total_score,
                "required_score": required_score,
                "principles_checked": principles_to_check,
                "principle_results": validation_results,
                "ethical_conflicts": ethical_conflicts,
                "recommendations": self._generate_recommendations(
                    validation_results, validation_context
                )
            }

            if ethical_conflicts:
                self.current_session["ethical_conflicts"].extend(ethical_conflicts)

            return result

        except Exception as e:
            self.logger.error("Error performing validation checks", 
                            extra={'structured_data': {'error': str(e)}})
            return {
                "is_valid": False,
                "error": str(e),
                "validation_level": validation_level
            }

    def _validate_principle(self, principle: str, context: Dict) -> Dict:
        """Validate response against a specific Hippocratic principle"""
        try:
            principle_config = self.principles.PRINCIPLES[principle]
            validation_rules = principle_config["validation_rules"]
            
            rule_results = []
            for rule in validation_rules:
                rule_result = self._check_validation_rule(rule, context)
                rule_results.append(rule_result)

            score = sum(r["score"] for r in rule_results) / len(rule_results)
            passed = score >= 0.7  # Threshold for principle validation

            result = {
                "principle": principle,
                "passed": passed,
                "score": score,
                "rule_results": rule_results
            }

            # Check for ethical conflicts
            if not passed:
                result["ethical_conflict"] = {
                    "principle": principle,
                    "description": principle_config["description"],
                    "violated_rules": [
                        r["rule"] for r in rule_results if not r["passed"]
                    ]
                }

            # Log principle application
            self.principles.log_principle_application(principle, {
                "validation_result": result,
                "context": context
            })

            return result

        except Exception as e:
            self.logger.error(f"Error validating principle {principle}", 
                            extra={'structured_data': {'error': str(e)}})
            return {
                "principle": principle,
                "passed": False,
                "error": str(e)
            }

    def _check_validation_rule(self, rule: str, context: Dict) -> Dict:
        """Check a specific validation rule"""
        try:
            # Rule-specific validation logic
            response_text = context["response"].lower()
            patterns = context["medical_patterns"]
            risk_assessment = context["risk_assessment"]

            rule_result = {
                "rule": rule,
                "passed": True,
                "score": 1.0,
                "details": []
            }

            # Adjust score based on context
            if "contraindications" in rule.lower():
                rule_result["score"] = 0.8 if patterns["risk_factors"] else 1.0
            elif "risk" in rule.lower():
                rule_result["score"] = 0.6 if risk_assessment["level"] in ["high", "critical"] else 1.0
            elif "document" in rule.lower():
                rule_result["score"] = 1.0 if context.get("context") else 0.8

            rule_result["passed"] = rule_result["score"] >= 0.7

            return rule_result

        except Exception as e:
            self.logger.error(f"Error checking validation rule: {rule}", 
                            extra={'structured_data': {'error': str(e)}})
            return {
                "rule": rule,
                "passed": False,
                "score": 0.0,
                "error": str(e)
            }

    def _generate_recommendations(self, 
                                validation_results: List[Dict], 
                                context: Dict) -> List[str]:
        """Generate recommendations based on validation results"""
        try:
            recommendations = []
            
            # Add recommendations based on risk level
            risk_level = context["risk_assessment"]["level"]
            if risk_level in ["high", "critical"]:
                recommendations.append(
                    "Seek immediate professional medical attention"
                )
            elif risk_level == "moderate":
                recommendations.append(
                    "Consider consulting with a healthcare provider"
                )

            # Add principle-specific recommendations
            for result in validation_results:
                if not result["passed"]:
                    principle = result["principle"]
                    principle_config = self.principles.PRINCIPLES[principle]
                    recommendations.append(
                        f"Review {principle_config['principle']}"
                    )

            # Add general recommendations
            recommendations.extend([
                "Document all medical observations",
                "Monitor for changes in symptoms",
                "Keep medical records updated"
            ])

            return recommendations

        except Exception as e:
            self.logger.error("Error generating recommendations", 
                            extra={'structured_data': {'error': str(e)}})
            return ["Seek professional medical advice"]

    def get_session_statistics(self) -> Dict:
        """Get statistics for current validation session"""
        try:
            return {
                "session_id": self.current_session["session_id"],
                "validations_performed": self.current_session["validations_performed"],
                "emergency_situations": self.current_session["emergency_situations"],
                "ethical_conflicts": len(self.current_session["ethical_conflicts"]),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error("Error getting session statistics", 
                            extra={'structured_data': {'error': str(e)}})
            return {}
