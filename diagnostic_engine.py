"""
Medical Diagnostic Engine for Ghana
Implements rule-based diagnosis for common conditions in Ghana
"""

import json
from typing import List, Dict, Any

class DiagnosticEngine:
    def __init__(self):
        self.conditions = {
            "malaria": {
                "name": "Malaria",
                "description": "A mosquito-borne infectious disease common in Ghana",
                "primary_symptoms": ["fever", "chills", "headache", "sweating"],
                "secondary_symptoms": ["nausea", "vomiting", "fatigue", "body_aches"],
                "severity_indicators": ["high_fever", "severe_headache", "confusion"],
                "recommendations": [
                    "Seek immediate medical attention for proper testing",
                    "Get a malaria rapid diagnostic test (RDT) or blood test",
                    "Take prescribed antimalarial medication if confirmed",
                    "Use mosquito nets and repellents for prevention",
                    "Stay hydrated and get plenty of rest"
                ],
                "urgency": "high"
            },
            "typhoid": {
                "name": "Typhoid Fever", 
                "description": "A bacterial infection spread through contaminated food and water",
                "primary_symptoms": ["prolonged_fever", "abdominal_pain", "diarrhea", "constipation"],
                "secondary_symptoms": ["headache", "weakness", "rose_spots", "enlarged_spleen"],
                "severity_indicators": ["high_fever", "severe_abdominal_pain", "bloody_stool"],
                "recommendations": [
                    "Visit a healthcare facility for blood tests",
                    "Complete full course of antibiotics if prescribed",
                    "Drink clean, boiled water only",
                    "Eat well-cooked, hot foods",
                    "Practice good hand hygiene"
                ],
                "urgency": "high"
            },
            "flu": {
                "name": "Influenza (Flu)",
                "description": "A viral respiratory infection",
                "primary_symptoms": ["fever", "cough", "sore_throat", "runny_nose"],
                "secondary_symptoms": ["body_aches", "fatigue", "headache", "chills"],
                "severity_indicators": ["difficulty_breathing", "chest_pain", "persistent_vomiting"],
                "recommendations": [
                    "Get plenty of rest and sleep",
                    "Drink lots of fluids",
                    "Take paracetamol for fever and aches",
                    "Stay home to avoid spreading to others",
                    "See a doctor if symptoms worsen or persist"
                ],
                "urgency": "medium"
            },
            "common_cold": {
                "name": "Common Cold",
                "description": "A mild viral infection of the nose and throat",
                "primary_symptoms": ["runny_nose", "sneezing", "mild_cough", "sore_throat"],
                "secondary_symptoms": ["mild_headache", "low_fever", "congestion"],
                "severity_indicators": ["high_fever", "severe_headache", "difficulty_breathing"],
                "recommendations": [
                    "Rest and drink plenty of fluids",
                    "Use warm salt water to gargle for sore throat",
                    "Take paracetamol for mild aches",
                    "Use steam inhalation for congestion",
                    "Symptoms usually resolve in 7-10 days"
                ],
                "urgency": "low"
            },
            "anemia": {
                "name": "Anemia",
                "description": "A condition where you lack healthy red blood cells",
                "primary_symptoms": ["fatigue", "weakness", "pale_skin", "shortness_of_breath"],
                "secondary_symptoms": ["dizziness", "cold_hands", "brittle_nails", "fast_heartbeat"],
                "severity_indicators": ["severe_fatigue", "chest_pain", "irregular_heartbeat"],
                "recommendations": [
                    "See a doctor for blood tests to confirm",
                    "Eat iron-rich foods like beans, leafy greens, and meat",
                    "Take iron supplements if prescribed",
                    "Treat underlying causes like heavy periods",
                    "Follow up regularly with healthcare provider"
                ],
                "urgency": "medium"
            }
        }
        
        # Symptom mappings to standardized terms
        self.symptom_mappings = {
            "fever": ["fever", "high temperature", "hot body"],
            "chills": ["chills", "shivering", "feeling cold"],
            "headache": ["headache", "head pain", "severe headache"],
            "sweating": ["sweating", "night sweats", "excessive sweating"],
            "nausea": ["nausea", "feeling sick", "want to vomit"],
            "vomiting": ["vomiting", "throwing up", "being sick"],
            "fatigue": ["fatigue", "tiredness", "feeling weak"],
            "body_aches": ["body aches", "muscle pain", "joint pain"],
            "abdominal_pain": ["stomach pain", "belly pain", "abdominal pain"],
            "diarrhea": ["diarrhea", "loose stool", "watery stool"],
            "constipation": ["constipation", "hard stool", "difficulty passing stool"],
            "cough": ["cough", "coughing", "dry cough"],
            "sore_throat": ["sore throat", "throat pain", "painful swallowing"],
            "runny_nose": ["runny nose", "nasal discharge", "blocked nose"],
            "sneezing": ["sneezing", "frequent sneezing"],
            "shortness_of_breath": ["shortness of breath", "difficulty breathing", "breathless"],
            "pale_skin": ["pale skin", "looking pale", "loss of color"],
            "dizziness": ["dizziness", "feeling faint", "lightheaded"],
            "weakness": ["weakness", "feeling weak", "lack of strength"]
        }

    def normalize_symptoms(self, symptoms_text: str) -> List[str]:
        """Convert free-text symptoms to standardized symptom codes"""
        if not symptoms_text:
            return []
            
        text_lower = symptoms_text.lower()
        normalized = []
        
        for standard_symptom, variations in self.symptom_mappings.items():
            for variation in variations:
                if variation in text_lower:
                    normalized.append(standard_symptom)
                    break
                    
        return list(set(normalized))  # Remove duplicates

    def calculate_condition_score(self, user_symptoms: List[str], condition: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate how well user symptoms match a condition"""
        primary_matches = sum(1 for symptom in condition["primary_symptoms"] if symptom in user_symptoms)
        secondary_matches = sum(1 for symptom in condition["secondary_symptoms"] if symptom in user_symptoms)
        severity_matches = sum(1 for symptom in condition["severity_indicators"] if symptom in user_symptoms)
        
        # Weighted scoring
        primary_weight = 3
        secondary_weight = 1
        severity_weight = 2
        
        total_score = (primary_matches * primary_weight + 
                      secondary_matches * secondary_weight + 
                      severity_matches * severity_weight)
        
        max_possible = (len(condition["primary_symptoms"]) * primary_weight + 
                       len(condition["secondary_symptoms"]) * secondary_weight +
                       len(condition["severity_indicators"]) * severity_weight)
        
        confidence = (total_score / max_possible) * 100 if max_possible > 0 else 0
        
        # Determine urgency level
        urgency = "low"
        if severity_matches > 0:
            urgency = "urgent"
        elif condition["urgency"] == "high" and primary_matches >= 2:
            urgency = "high"
        elif primary_matches >= 1:
            urgency = condition["urgency"]
            
        return {
            "condition": condition["name"],
            "description": condition["description"],
            "confidence": round(confidence, 1),
            "primary_matches": primary_matches,
            "secondary_matches": secondary_matches,
            "severity_matches": severity_matches,
            "recommendations": condition["recommendations"],
            "urgency": urgency,
            "matched_symptoms": [s for s in user_symptoms if s in condition["primary_symptoms"] + condition["secondary_symptoms"] + condition["severity_indicators"]]
        }

    def diagnose(self, selected_symptoms: List[str], text_symptoms: str = "") -> Dict[str, Any]:
        """Main diagnosis function"""
        # Normalize and combine symptoms
        normalized_text_symptoms = self.normalize_symptoms(text_symptoms)
        all_symptoms = list(set(selected_symptoms + normalized_text_symptoms))
        
        if not all_symptoms:
            return {
                "diagnoses": [],
                "message": "No symptoms provided. Please select symptoms or describe how you feel.",
                "total_symptoms": 0
            }
        
        # Calculate scores for all conditions
        condition_scores = []
        for condition_key, condition_data in self.conditions.items():
            score = self.calculate_condition_score(all_symptoms, condition_data)
            if score["confidence"] > 0:  # Only include conditions with some match
                condition_scores.append(score)
        
        # Sort by confidence score
        condition_scores.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Filter to top 3 most likely conditions
        top_conditions = condition_scores[:3]
        
        # Generate summary message
        if not top_conditions:
            message = "Based on your symptoms, we cannot match them to common conditions in our database. Please consult a healthcare professional for proper evaluation."
        elif top_conditions[0]["confidence"] > 70:
            message = f"Your symptoms strongly suggest {top_conditions[0]['condition']}. Please seek medical attention for proper diagnosis and treatment."
        elif top_conditions[0]["confidence"] > 40:
            message = f"Your symptoms may indicate {top_conditions[0]['condition']} or similar conditions. Medical evaluation is recommended."
        else:
            message = "Your symptoms match several possible conditions. A healthcare professional can provide proper diagnosis."
            
        return {
            "diagnoses": top_conditions,
            "message": message,
            "total_symptoms": len(all_symptoms),
            "processed_symptoms": all_symptoms
        }

    def get_example_symptom_bundles(self) -> List[Dict[str, Any]]:
        """Get example symptom combinations for common conditions"""
        return [
            {
                "name": "Feeling feverish and weak",
                "symptoms": ["fever", "fatigue", "headache", "body_aches"],
                "description": "High temperature with general weakness"
            },
            {
                "name": "Stomach problems",
                "symptoms": ["abdominal_pain", "nausea", "diarrhea", "fever"],
                "description": "Stomach pain with digestive issues"
            },
            {
                "name": "Cold-like symptoms",
                "symptoms": ["runny_nose", "sneezing", "sore_throat", "mild_cough"],
                "description": "Common cold symptoms"
            },
            {
                "name": "Feeling very tired",
                "symptoms": ["fatigue", "weakness", "pale_skin", "shortness_of_breath"],
                "description": "Persistent tiredness and weakness"
            }
        ]

    def get_all_symptoms(self) -> List[Dict[str, str]]:
        """Get all available symptoms for the form"""
        symptoms = []
        all_symptom_codes = set()
        
        # Collect all unique symptoms from conditions
        for condition in self.conditions.values():
            all_symptom_codes.update(condition["primary_symptoms"])
            all_symptom_codes.update(condition["secondary_symptoms"])
            all_symptom_codes.update(condition["severity_indicators"])
        
        # Convert to user-friendly format
        symptom_display = {
            "fever": "Fever/High temperature",
            "chills": "Chills/Shivering",
            "headache": "Headache",
            "sweating": "Excessive sweating",
            "nausea": "Nausea/Feeling sick",
            "vomiting": "Vomiting",
            "fatigue": "Fatigue/Tiredness",
            "body_aches": "Body aches/Muscle pain",
            "abdominal_pain": "Stomach/Belly pain",
            "diarrhea": "Diarrhea/Loose stool",
            "constipation": "Constipation",
            "cough": "Cough",
            "sore_throat": "Sore throat",
            "runny_nose": "Runny/Blocked nose",
            "sneezing": "Sneezing",
            "shortness_of_breath": "Difficulty breathing",
            "pale_skin": "Pale skin",
            "dizziness": "Dizziness/Feeling faint",
            "weakness": "Weakness",
            "high_fever": "Very high fever",
            "severe_headache": "Severe headache",
            "confusion": "Confusion",
            "prolonged_fever": "Fever for several days",
            "rose_spots": "Rose-colored spots on skin",
            "enlarged_spleen": "Swollen abdomen",
            "bloody_stool": "Blood in stool",
            "difficulty_breathing": "Severe breathing problems",
            "chest_pain": "Chest pain",
            "persistent_vomiting": "Cannot stop vomiting",
            "mild_cough": "Mild cough",
            "low_fever": "Low-grade fever",
            "congestion": "Nasal congestion",
            "mild_headache": "Mild headache",
            "cold_hands": "Cold hands and feet",
            "brittle_nails": "Brittle fingernails",
            "fast_heartbeat": "Fast heartbeat",
            "severe_fatigue": "Extreme tiredness",
            "irregular_heartbeat": "Irregular heartbeat"
        }
        
        for code in sorted(all_symptom_codes):
            symptoms.append({
                "code": code,
                "display": symptom_display.get(code, code.replace("_", " ").title())
            })
            
        return symptoms
