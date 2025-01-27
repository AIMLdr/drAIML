# medical_patterns.py (c) drAIML MIT license

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
