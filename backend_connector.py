# backend_connector.py
import json
from typing import Dict, Any, List
from guideline_processor import load_guidelines
from llm_interface import generate_recommendation
from text_extractor import extract_patient_data

# Load guidelines once when the module is imported
guidelines = load_guidelines()

def get_guidelines() -> Dict[str, Any]:
    """Return the loaded guidelines"""
    return guidelines

def process_user_input(user_input: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Process user input and return recommendations.

    Args:
        user_input: The user's question or patient information
        conversation_history: List of previous messages in the conversation

    Returns:
        Dictionary containing recommendations and other processed data
    """
    try:
        # Extract patient data from input
        patient_data = extract_patient_data(user_input)

        # Generate recommendation using LLM with conversation history
        recommendation = generate_recommendation(user_input, guidelines, conversation_history)

        return {
            "success": True,
            "recommendations": recommendation,
            "patient_data": patient_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recommendations": f"Error processing request: {str(e)}"
        }