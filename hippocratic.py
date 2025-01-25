# hippocratic.py
import logging
from datetime import datetime
import os
import json
from typing import Dict, List, Optional

class HippocraticPrinciples:
    """Core principles based on the Hippocratic Oath"""
    
    PRINCIPLES = {
        "do_no_harm": "First, do no harm (primum non nocere)",
        "confidentiality": "Respect patient privacy and confidentiality",
        "beneficence": "Act in the best interest of the patient",
        "patient_autonomy": "Respect patient's right to make decisions",
        "justice": "Treat all patients fairly and equally",
        "informed_consent": "Ensure patient understanding and consent",
        "professional_ethics": "Maintain professional standards and ethics",
        "medical_accuracy": "Provide accurate medical information",
        "referral_awareness": "Know when to refer to human healthcare providers",
        "emergency_protocol": "Recognize and appropriately handle medical emergencies"
    }

    EMERGENCY_KEYWORDS = [
        "heart attack", "stroke", "bleeding", "unconscious", "breathing difficulty",
        "severe pain", "chest pain", "head injury", "seizure", "anaphylaxis",
        "suicide", "overdose", "emergency", "critical", "severe", "urgent"
    ]

    DISCLAIMER = """
    IMPORTANT: This is AI-assisted medical information. Always consult with qualified 
    healthcare professionals for medical advice, diagnosis, or treatment. Seek immediate 
    emergency care for urgent medical conditions.
    """

class HippocraticReasoning:
    """Medical reasoning system based on Hippocratic principles"""
    
    def __init__(self):
        self.logger = logging.getLogger('HippocraticReasoning')
        self.principles = HippocraticPrinciples.PRINCIPLES
        self.emergency_keywords = HippocraticPrinciples.EMERGENCY_KEYWORDS
        self.disclaimer = HippocraticPrinciples.DISCLAIMER
        self.decisions_log = []
        self.ethical_checks = []
        self._setup_logging()
        
    def _setup_logging(self):
        """Initialize logging system"""
        log_dir = './memory/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up medical decisions log
        handler = logging.FileHandler(f'{log_dir}/medical_decisions.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def evaluate_medical_decision(self, 
                                proposed_action: str, 
                                patient_context: Dict,
                                severity_level: str = "moderate") -> Dict:
        """
        Evaluate a medical decision against Hippocratic principles
        """
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "proposed_action": proposed_action,
            "severity_level": severity_level,
            "ethical_checks": [],
            "is_approved": True,
            "warnings": [],
            "recommendations": [],
            "emergency_status": self._check_emergency(proposed_action)
        }

        # Perform ethical checks
        checks = [
            self._check_no_harm(proposed_action, patient_context),
            self._check_confidentiality(patient_context),
            self._check_beneficence(proposed_action, patient_context),
            self._check_patient_autonomy(patient_context),
            self._check_informed_consent(proposed_action, patient_context),
            self._check_medical_accuracy(proposed_action),
            self._check_referral_needs(proposed_action, patient_context)
        ]

        for check in checks:
            evaluation["ethical_checks"].append(check)
            if not check["passed"]:
                evaluation["is_approved"] = False
                evaluation["warnings"].append(check["warning"])
                evaluation["recommendations"].append(check["recommendation"])

        self._log_decision(evaluation)
        return evaluation

    def _check_emergency(self, text: str) -> bool:
        """Check if the situation requires emergency care"""
        return any(keyword in text.lower() for keyword in self.emergency_keywords)

    def _check_no_harm(self, action: str, context: Dict) -> Dict:
        """Evaluate potential harm"""
        check = {
            "principle": "do_no_harm",
            "passed": True,
            "warning": None,
            "recommendation": None
        }
        
        risk_words = ["dangerous", "risk", "harm", "death", "fatal", "severe"]
        if any(word in action.lower() for word in risk_words):
            check.update({
                "passed": False,
                "warning": "Potential harm detected in proposed action",
                "recommendation": "Consider safer alternatives or additional safeguards"
            })
        
        return check

    def _check_medical_accuracy(self, action: str) -> Dict:
        """Evaluate medical information accuracy"""
        check = {
            "principle": "medical_accuracy",
            "passed": True,
            "warning": None,
            "recommendation": "Verify information with current medical guidelines"
        }
        
        uncertainty_indicators = ["maybe", "possibly", "might", "unclear", "unknown"]
        if any(indicator in action.lower() for indicator in uncertainty_indicators):
            check["recommendation"] = "Clarify medical information and provide more specific guidance"
            
        return check

    def _check_confidentiality(self, context: Dict) -> Dict:
        """Evaluate privacy considerations"""
        check = {
            "principle": "confidentiality",
            "passed": True,
            "warning": None,
            "recommendation": None
        }
        
        sensitive_fields = ["personal_info", "contact", "identity"]
        if any(field in context for field in sensitive_fields):
            check["recommendation"] = "Ensure proper data protection measures"
            
        return check

    def _check_beneficence(self, action: str, context: Dict) -> Dict:
        """Evaluate patient benefit"""
        return {
            "principle": "beneficence",
            "passed": True,
            "warning": None,
            "recommendation": "Continue monitoring patient response"
        }

    def _check_patient_autonomy(self, context: Dict) -> Dict:
        """Evaluate respect for patient autonomy"""
        return {
            "principle": "patient_autonomy",
            "passed": True,
            "warning": None,
            "recommendation": "Ensure patient is involved in decision-making"
        }

    def _check_informed_consent(self, action: str, context: Dict) -> Dict:
        """Evaluate informed consent requirements"""
        return {
            "principle": "informed_consent",
            "passed": True,
            "warning": None,
            "recommendation": "Document patient consent and understanding"
        }

    def _check_referral_needs(self, action: str, context: Dict) -> Dict:
        """Evaluate if human healthcare provider referral is needed"""
        check = {
            "principle": "referral_awareness",
            "passed": True,
            "warning": None,
            "recommendation": None
        }
        
        if self._check_emergency(action):
            check.update({
                "passed": False,
                "warning": "Emergency situation detected",
                "recommendation": "Seek immediate emergency medical care"
            })
            
        return check

    def _log_decision(self, evaluation: Dict):
        """Log medical decision and evaluation"""
        self.decisions_log.append(evaluation)
        self.logger.info(f"Medical decision evaluated: {json.dumps(evaluation, indent=2)}")
        
        # Save to file
        log_file = './memory/logs/medical_decisions.json'
        try:
            with open(log_file, 'w') as f:
                json.dump(self.decisions_log, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving decision log: {e}")

    def validate_medical_response(self, 
                                response: str, 
                                context: Dict,
                                severity: str = "moderate") -> Dict:
        """
        Validate an AI-generated medical response
        """
        evaluation = self.evaluate_medical_decision(response, context, severity)
        
        validation_result = {
            "original_response": response,
            "is_valid": evaluation["is_approved"],
            "warnings": evaluation["warnings"],
            "recommendations": evaluation["recommendations"],
            "emergency_status": evaluation["emergency_status"],
            "modified_response": response
        }

        # Modify response if necessary
        if not evaluation["is_approved"] or evaluation["emergency_status"]:
            validation_result["modified_response"] = self._modify_response(
                response, 
                evaluation["warnings"],
                evaluation["emergency_status"]
            )

        return validation_result

    def _modify_response(self, 
                        response: str, 
                        warnings: List[str],
                        is_emergency: bool) -> str:
        """Modify response based on ethical concerns and emergency status"""
        modified = response
        
        # Add emergency warning if needed
        if is_emergency:
            emergency_warning = "\n\n🚨 EMERGENCY WARNING: This appears to be a medical emergency. " \
                              "Seek immediate emergency medical care or call your local emergency services.\n"
            modified = emergency_warning + modified

        # Add disclaimers or modifications based on warnings
        if warnings:
            disclaimer = "\n\nImportant considerations:\n"
            for warning in warnings:
                disclaimer += f"- {warning}\n"
            modified += disclaimer
            
        # Always add general medical disclaimer
        modified += f"\n\n{self.disclaimer}"
            
        return modified
