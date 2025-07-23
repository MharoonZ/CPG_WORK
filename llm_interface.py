"""
LLM Interface Module

Handles interactions with the OpenAI API for generating recommendations.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

import openai
from openai import OpenAI

from text_extractor import extract_patient_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")

client = OpenAI(api_key=api_key)

def generate_recommendation(patient_input: str, guidelines: Dict[str, Any], conversation_history: List[Dict[str, str]] = None) -> str:
    """Generate recommendation based on patient input and guidelines."""
    # Extract patient data
    patient_data = extract_patient_data(patient_input)

    # Prepare prompt context
    prompt_context = prepare_context(patient_data, guidelines)

    # Create system message
    system_message = """You are a clinical decision support system using the 2022 AHA/ACC/HFSA Heart Failure Guidelines (Chapter 7).
You should maintain context from previous interactions and use it to provide more relevant and contextual responses.
When answering follow-up questions, reference previous recommendations and explain any changes or additional information."""

    # Create messages list with conversation history
    messages = [{"role": "system", "content": system_message}]

    # Add conversation history if available
    if conversation_history:
        messages.extend(conversation_history)

    # Add current prompt
    current_prompt = f"""
RELEVANT GUIDELINE SECTIONS:
{prompt_context}

Based strictly on the 2022 Heart Failure Guidelines above, provide evidence-based recommendations for this patient. Include:
1. A brief summary of the patient's current status
2. Specific medication recommendations with class of recommendation (COR) and level of evidence (LOE)
3. Citations to relevant guideline sections
4. Any medication adjustments needed (e.g., dosages that need optimization)
5. Only provide recommendations that are directly supported by the guidelines

Format your response in clear, concise bullet points with appropriate citations.
Do not include any speculative recommendations not supported by the guidelines.
"""
    messages.append({"role": "user", "content": current_prompt})

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.1,
            max_tokens=1000
        )

        recommendation = response.choices[0].message.content
        return recommendation if recommendation is not None else "No recommendation could be generated."

    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return f"Error generating recommendation: {str(e)}\n\nPlease try again."
def create_static_hfref_recommendation(patient_data: Dict[str, Any]) -> str:
    """Create a static evidence-based recommendation for a HFrEF patient."""
    lvef = patient_data.get("lvef", 0)
    nyha_class = patient_data.get("nyha_class", 0)
    has_angioedema = patient_data.get("angioedema_history", False)
    
    # Get lab values
    potassium = patient_data.get("lab_values", {}).get("potassium", 0)
    egfr = patient_data.get("lab_values", {}).get("egfr", 0)
    
    # Get current medications
    meds = []
    for med in patient_data.get("medications", []):
        name = med.get("name", "").lower()
        dose = med.get("dose", 0)
        
        if "lisinopril" in name:
            meds.append(f"Lisinopril {dose}mg daily")
        elif "metoprolol" in name and "succinate" in name:
            meds.append(f"Metoprolol Succinate {dose}mg daily")
    
    # Build patient summary
    age = patient_data.get("age", "")
    sex = patient_data.get("sex", "")
    
    patient_summary = f"PATIENT SUMMARY:\n"
    if age and sex:
        patient_summary += f"- {age}-year-old {sex} with Stage C Heart Failure with Reduced Ejection Fraction (HFrEF)\n"
    if lvef:
        patient_summary += f"- LVEF {lvef}%, NYHA Class {nyha_class} symptoms\n"
    if meds:
        patient_summary += f"- Currently on {', '.join(meds)}\n"
    if potassium and egfr:
        patient_summary += f"- Labs: K+ {potassium} mEq/L, eGFR {egfr} mL/min/1.73m²\n"
    patient_summary += f"- {'History of' if has_angioedema else 'No history of'} angioedema\n"
    
    # Build recommendations
    recommendations = "\nRECOMMENDATIONS:\n\n"
    
    # ARNi recommendation
    if not has_angioedema and nyha_class in [2, 3]:
        recommendations += """1. Consider switching ACEi (Lisinopril) to ARNi (Sacubitril/Valsartan)
   - Class 1, Level of Evidence B-R (Section 7.3.1, Recommendation 4)
   - Rationale: Patient has HFrEF with NYHA class II symptoms, is currently on an ACEi, and has no history of angioedema
   - Start with 49/51 mg twice daily and titrate to target dose of 97/103 mg twice daily as tolerated\n\n"""
    
    # MRA recommendation
    if egfr > 30 and potassium < 5.0:
        recommendations += """2. Add Mineralocorticoid Receptor Antagonist (MRA) - Spironolactone or Eplerenone
   - Class 1, Level of Evidence A (Section 7.3.3, Recommendation 1)
   - Rationale: Patient has HFrEF with NYHA class II symptoms, eGFR >30 mL/min/1.73m² (55), and K+ <5.0 mEq/L (4.1)
   - Start with Spironolactone 25 mg daily or Eplerenone 25 mg daily
   - Monitor potassium and renal function at initiation and regularly thereafter\n\n"""
    
    # SGLT2i recommendation
    if egfr >= 20:
        recommendations += """3. Add SGLT2 inhibitor (Dapagliflozin or Empagliflozin)
   - Class 1, Level of Evidence A (Section 7.3.4, Recommendation 1)
   - Rationale: Patient has symptomatic HFrEF
   - Dose: Dapagliflozin 10 mg daily or Empagliflozin 10 mg daily
   - Benefit occurs irrespective of presence of diabetes\n\n"""
    
    # Beta blocker optimization
    for med in patient_data.get("medications", []):
        name = med.get("name", "").lower()
        dose = med.get("dose", 0)
        
        if "metoprolol" in name and "succinate" in name:
            if dose < 200:
                recommendations += f"""4. Optimize Beta-Blocker dosing
   - Current dose of Metoprolol Succinate ({dose} mg daily) is below target dose (200 mg daily)
   - Consider uptitration to target dose as tolerated (Section 7.3.8)
   - Monitor for bradycardia and hypotension during uptitration\n\n"""
    
    # Additional recommendations
    recommendations += """ADDITIONAL RECOMMENDATIONS:
- Continue heart failure education and self-care support (Section 7.1.1)
- Ensure vaccination against respiratory illnesses (Section 7.1.1)
- Consider screening for depression, social isolation, and frailty (Section 7.1.1)
- Avoid excessive sodium intake (Section 7.1.2)"""
    
    return patient_summary + recommendations

def prepare_context(patient_data: Dict[str, Any], guidelines: Dict[str, Any]) -> str:
    """Prepare context with relevant guidelines sections based on patient data."""
    def clean_text(text):
        return text.replace('²', '2').replace('≥', '>=').replace('≤', '<=').replace('α', 'alpha')
        
    context_parts = []
    
    # Add relevant guideline sections based on patient data
    if patient_data.get("hf_type") == "HFrEF":
        context_parts.append(guidelines.get("hfref", {}).get("content", ""))
    
    if patient_data.get("angioedema_history"):
        context_parts.append("NOTE: Patient has history of angioedema, which is a contraindication for ACEi/ARNI.")
    
    if "Diabetes" in patient_data.get("comorbidities", []):
        context_parts.append("NOTE: Patient has diabetes, which is relevant for SGLT2i recommendation.")
    
    return "\n\n".join(context_parts)
