# draiml.py
import streamlit as st
import time
from datetime import datetime
from socratic import SocraticReasoning
from chatter import GPT4o, GroqModel, TogetherModel, OllamaHandler
from openmind import OpenMind
from memory import create_memory_folders, store_in_stm, DialogEntry
import os

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'premises' not in st.session_state:
    st.session_state.premises = []
if 'conclusions' not in st.session_state:
    st.session_state.conclusions = []
if 'provider' not in st.session_state:
    st.session_state.provider = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'ollama_instance' not in st.session_state:
    st.session_state.ollama_instance = None

def check_ollama_status():
    """Check if Ollama is running and return available models"""
    if not st.session_state.ollama_instance:
        st.session_state.ollama_instance = OllamaHandler()
    
    if st.session_state.ollama_instance.check_installation():
        models = st.session_state.ollama_instance.list_models()
        return True, models
    return False, []

def initialize_agi(openmind):
    """Initialize AI model based on selected provider"""
    provider = st.session_state.provider
    
    if not provider:
        st.info("Please select an AI Provider")
        return None
    
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
        if not st.session_state.ollama_instance:
            st.session_state.ollama_instance = OllamaHandler()
            
        if st.session_state.ollama_instance.check_installation():
            available_models = st.session_state.ollama_instance.list_models()
            if available_models:
                # Model selection in sidebar
                selected_model = st.session_state.selected_model
                if not selected_model:
                    st.info("Please select an Ollama model to continue")
                    return None
                
                if st.session_state.ollama_instance.select_model(selected_model):
                    return st.session_state.ollama_instance
                else:
                    st.error(st.session_state.ollama_instance.get_last_error())
                    return None
            else:
                st.error("No Ollama models found. Please pull a model first.")
                return None
        else:
            st.error("Ollama is not running. Please start Ollama service.")
            return None
            
    return None

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
        
        # Provider selection
        previous_provider = st.session_state.provider
        st.session_state.provider = st.selectbox(
            "Select AI Provider", 
            [None, "Together", "Groq", "Ollama"],
            format_func=lambda x: "Select Provider" if x is None else x
        )
        
        # Reset model selection when provider changes
        if previous_provider != st.session_state.provider:
            st.session_state.selected_model = None
        
        # Show appropriate configuration based on provider
        if st.session_state.provider == "Ollama":
            if ollama_models:
                st.session_state.selected_model = st.selectbox(
                    "Select Ollama Model",
                    options=ollama_models,
                    key='ollama_model_select'
                )
                
                # Show model info if selected
                if st.session_state.selected_model:
                    model_info = st.session_state.ollama_instance.get_model_info(st.session_state.selected_model)
                    if 'error' not in model_info:
                        st.caption("Model Information:")
                        st.json(model_info)
        
        elif st.session_state.provider in ["Together", "Groq"]:
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
        if not st.session_state.provider:
            st.warning("Please select an AI Provider first")
            return
            
        # Initialize the AI model
        agi = initialize_agi(openmind)
        if agi is None:
            if st.session_state.provider == "Ollama" and not st.session_state.selected_model:
                st.info("Please select an Ollama model to continue")
            return
        
        with st.spinner("Dr. AIML is analyzing your input..."):
            try:
                response = agi.generate_response(user_input)
                
                if st.session_state.provider == "Ollama" and st.session_state.ollama_instance.get_last_error():
                    st.error(st.session_state.ollama_instance.get_last_error())
                    return
                
                st.write(response)
                
                # Store the conversation history
                st.session_state.history.append({
                    'user': user_input,
                    'drAIML': response,
                    'timestamp': datetime.now().isoformat(),
                    'model': st.session_state.selected_model if st.session_state.provider == "Ollama" else st.session_state.provider
                })
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

    # Display conversation history
    if st.session_state.history:
        st.header("Conversation History")
        for entry in st.session_state.history:
            st.write(f"You: {entry['user']}")
            st.write(f"Dr. AIML: {entry['drAIML']}")
            st.write(f"Model: {entry['model']}")
            st.write(f"Time: {entry['timestamp']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
