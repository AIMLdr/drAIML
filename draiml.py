# app.py
import streamlit as st
import time
from datetime import datetime
from socratic import SocraticReasoning
from chatter import GPT4o, GroqModel, TogetherModel, OllamaHandler
from openmind import OpenMind
from memory import create_memory_folders, store_in_stm, DialogEntry
from hippocratic import HippocraticReasoning
import os

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'premises' not in st.session_state:
    st.session_state.premises = []
if 'conclusions' not in st.session_state:
    st.session_state.conclusions = []
if 'provider' not in st.session_state:
    st.session_state.provider = "Together"
if 'hippocratic' not in st.session_state:
    st.session_state.hippocratic = HippocraticReasoning()

def check_ollama_status():
    """Check if Ollama is running and return available models"""
    ollama = OllamaHandler()
    if ollama.check_installation():
        models = ollama.list_models()
        return True, models
    return False, []

def initialize_agi(openmind):
    """Initialize AI model based on selected provider"""
    provider = st.session_state.provider
    
    if provider == "Together":
        key = openmind.get_api_key('together')
        if key:
            return TogetherModel(key)
        else:
            st.error("Together API key not found")
            return None
            
    elif provider == "Groq":
        key = openmind.get_api_key('groq')
        if key:
            return GroqModel(key)
        else:
            st.error("Groq API key not found")
            return None
            
    elif provider == "Ollama":
        ollama = OllamaHandler()
        if ollama.check_installation():
            available_models = ollama.list_models()
            if available_models:
                return ollama
            else:
                st.error("No Ollama models found. Please pull a model first.")
                return None
        else:
            st.error("Ollama is not running. Please start Ollama service.")
            return None
            
    return None

def process_medical_response(user_input: str, ai_response: str) -> str:
    """Process and validate medical response"""
    context = {
        "query": user_input,
        "timestamp": datetime.now().isoformat(),
        "severity": "moderate"
    }
    
    validation = st.session_state.hippocratic.validate_medical_response(
        response=ai_response,
        context=context
    )
    
    return validation["modified_response"]

def main():
    st.title("drAIML - Medical AI Consultant")
    openmind = OpenMind()
    
    with st.sidebar:
        st.header("AI Configuration")
        
        # Check Ollama status and show indicator if running
        ollama_running, ollama_models = check_ollama_status()
        if ollama_running:
            st.markdown("""
                <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                    <span style='color: #00ff00; font-size: 1.5em; margin-right: 0.5rem;'>●</span>
                    <span style='color: #666666;'>Ollama Running</span>
                </div>
                """, unsafe_allow_html=True)
            if ollama_models:
                st.caption(f"Available models: {', '.join(ollama_models)}")
        
        st.session_state.provider = st.selectbox(
            "Select AI Provider", 
            ["Together", "Groq", "Ollama"], 
            index=0
        )
        
        if st.session_state.provider != "Ollama":
            api_key = st.text_input(f"{st.session_state.provider} API Key", type="password")
            if api_key:
                openmind.save_api_key(st.session_state.provider.lower(), api_key)

        # View options with default unchecked
        st.header("View Sections")
        show_oath = st.checkbox("Show Oath of Dr. AIML", value=False)
        show_prompt = st.checkbox("Show Dr. AIML Prompt", value=False)

    # Load and display Oath if checkbox is checked
    if show_oath:
        oath_text = openmind.load_oath()
        if oath_text:
            st.header("The Oath of Dr. AIML")
            st.markdown(oath_text)
        else:
            st.error("Oath file not found. Please ensure 'oath.txt' is in the same directory.")
    
    # Load and display Prompt if checkbox is checked
    if show_prompt:
        prompt_text = openmind.load_prompt()
        if prompt_text:
            st.header("Dr. AIML: The Apex of Autonomous Healthcare")
            st.markdown(prompt_text)
        else:
            st.error("Prompt file not found. Please ensure 'prompt.txt' is in the same directory.")

    # Main consultation interface
    st.header("Consult with Dr. AIML")
    user_input = st.text_input("Please describe your symptoms or ask a health question:")
    
    if user_input:
        # Initialize the AI model
        agi = initialize_agi(openmind)
        if agi is None:
            st.error("AI model not initialized. Please check your configuration.")
        else:
            with st.spinner("Dr. AIML is analyzing your input..."):
                try:
                    # Generate response based on provider
                    if st.session_state.provider == "Ollama":
                        raw_response = agi.generate_response(user_input)
                    else:
                        raw_response = agi.generate_response(user_input)
                    
                    # Process and validate the response
                    response = process_medical_response(user_input, raw_response)
                    st.write(response)
                    
                    # Store the conversation history
                    st.session_state.history.append({
                        'user': user_input,
                        'drAIML': response,
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

    # Display conversation history
    if st.session_state.history:
        st.header("Conversation History")
        for entry in st.session_state.history:
            st.write(f"You: {entry['user']}")
            st.write(f"Dr. AIML: {entry['drAIML']}")
            if 'timestamp' in entry:
                st.write(f"Time: {entry['timestamp']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
