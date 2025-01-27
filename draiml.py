# draiml.py (c) 2025 Gregory L. Magnusson MIT license

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import streamlit as st
import time
from datetime import datetime
from socratic import SocraticReasoning
from chatter import GPT4o, GroqModel, TogetherModel, OllamaHandler
from openmind import OpenMind
from config import model_config
from logger import get_logger

# Initialize logger
logger = get_logger('draiml')

# Load external CSS
def load_css(css_file: str):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
load_css('styles.css')

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'provider' not in st.session_state:
    st.session_state.provider = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'model_capabilities' not in st.session_state:
    st.session_state.model_capabilities = []
if 'cost_tracking' not in st.session_state:
    st.session_state.cost_tracking = {"total": 0.0, "session": 0.0}

# Initialize model instances
if 'model_instances' not in st.session_state:
    st.session_state.model_instances = {
        'ollama': None,
        'groq': None,
        'together': None,
        'openai': None
    }

if 'openmind' not in st.session_state:
    st.session_state.openmind = OpenMind()

def check_ollama_status():
    """Check Ollama installation and available models"""
    if not st.session_state.model_instances['ollama']:
        st.session_state.model_instances['ollama'] = OllamaHandler()
    
    if st.session_state.model_instances['ollama'].check_installation():
        models = st.session_state.model_instances['ollama'].list_models()
        return True, models
    return False, []

def initialize_model(provider: str):
    """Initialize or retrieve model instance"""
    try:
        if not provider:
            st.info("select an AI Provider")
            return None
        
        if provider == "Together":
            key = st.session_state.openmind.get_api_key('together')
            if key:
                if not st.session_state.model_instances['together']:
                    instance = TogetherModel(key)
                    st.session_state.model_instances['together'] = instance
                return st.session_state.model_instances['together']
            else:
                st.error("Together API key not found")
                return None
                
        elif provider == "Groq":
            key = st.session_state.openmind.get_api_key('groq')
            if key:
                try:
                    if not st.session_state.model_instances['groq']:
                        st.session_state.model_instances['groq'] = GroqModel(key)
                    return st.session_state.model_instances['groq']
                except Exception as e:
                    st.error(f"Error initializing Groq: {str(e)}")
                    return None
            else:
                st.error("Groq API key not found")
                return None
                
        elif provider == "OpenAI":
            key = st.session_state.openmind.get_api_key('openai')
            if key:
                try:
                    if not st.session_state.model_instances['openai']:
                        st.session_state.model_instances['openai'] = GPT4o(key)
                    return st.session_state.model_instances['openai']
                except Exception as e:
                    st.error(f"Error initializing OpenAI: {str(e)}")
                    return None
            else:
                st.error("OpenAI API key not found")
                return None
                
        elif provider == "Ollama":
            if not st.session_state.model_instances['ollama']:
                st.session_state.model_instances['ollama'] = OllamaHandler()
                
            if st.session_state.model_instances['ollama'].check_installation():
                available_models = st.session_state.model_instances['ollama'].list_models()
                if available_models:
                    if not st.session_state.selected_model:
                        st.info("Please select an Ollama model to continue")
                        return None
                    
                    if st.session_state.model_instances['ollama'].select_model(st.session_state.selected_model):
                        return st.session_state.model_instances['ollama']
                    else:
                        st.error(st.session_state.model_instances['ollama'].get_last_error())
                        return None
                else:
                    st.error("Ollama model not found. Please pull a model first.")
                    return None
            else:
                st.error("Ollama is not running. start Ollama service.")
                return None
                
        return None
    except Exception as e:
        logger.error(f"Error initializing model: {e}")
        st.error(f"Error initializing model: {str(e)}")
        return None

def update_cost_tracking(response_length: int):
    """Update cost tracking based on current model and response length"""
    try:
        if st.session_state.provider and st.session_state.selected_model:
            model_info = model_config.get_model_info(
                st.session_state.provider.lower(),
                st.session_state.selected_model
            )
            if model_info and 'cost' in model_info:
                cost_str = model_info['cost']
                if '/1M tokens' in cost_str:
                    base_cost = float(cost_str.split('$')[1].split('/')[0])
                    tokens = response_length / 4  # Approximate tokens
                    cost = (tokens / 1000000) * base_cost
                elif '/1K tokens' in cost_str:
                    base_cost = float(cost_str.split('$')[1].split('/')[0])
                    tokens = response_length / 4
                    cost = (tokens / 1000) * base_cost
                else:
                    cost = 0.0
                
                st.session_state.cost_tracking["session"] += cost
                st.session_state.cost_tracking["total"] += cost
    except Exception as e:
        logger.error(f"Error updating cost tracking: {e}")

def display_model_info():
    """Display current model information"""
    if st.session_state.provider and st.session_state.selected_model:
        model_info = model_config.get_model_info(
            st.session_state.provider.lower(),
            st.session_state.selected_model
        )
        if model_info:
            st.sidebar.markdown("### Model Information")
            st.sidebar.markdown(f"""
            <div class="model-info">
                <p><strong>Model:</strong> {model_info['name']}</p>
                <p><strong>Developer:</strong> {model_info['developer']}</p>
                <p><strong>Max Tokens:</strong> {model_info['tokens']}</p>
                <p><strong>Cost:</strong> {model_info['cost']}</p>
                <div><strong>Capabilities:</strong></div>
                {''.join([f'<span class="capability-tag">{cap}</span>' for cap in model_info.get('capabilities', [])])}
            </div>
            """, unsafe_allow_html=True)

def process_message(prompt):
    """Process and generate response to user message"""
    if not st.session_state.provider:
        st.warning("select an AI Provider first")
        return
        
    model = initialize_model(st.session_state.provider)
    if not model:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_response(prompt)
                
                if st.session_state.provider == "Ollama" and model.get_last_error():
                    st.error(model.get_last_error())
                    return
                
                st.markdown(response)
                update_cost_tracking(len(response))
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                st.error(f"Error generating response: {str(e)}")

def main():
    st.title("drAIML - Medical AI Consultant")
    
    # Display cost tracker
    st.markdown(f"""
        <div class="cost-tracker">
            Session Cost: ${st.session_state.cost_tracking['session']:.4f}<br>
            Total Cost: ${st.session_state.cost_tracking['total']:.4f}
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("AI Configuration")
        
        # Check Ollama status
        ollama_running, ollama_models = check_ollama_status()
        if ollama_running:
            st.markdown("""
                <div class="api-key-status">
                    <span class="checkmark">●</span>
                    <span class="text">Ollama Running</span>
                </div>
                """, unsafe_allow_html=True)
            if ollama_models:
                st.caption(f"Available models: {', '.join(ollama_models)}")
        
        # Provider selection
        previous_provider = st.session_state.provider
        st.session_state.provider = st.selectbox(
            "Select AI Provider", 
            [None, "OpenAI", "Together", "Groq", "Ollama"],
            format_func=lambda x: "Select Provider" if x is None else x
        )
        
        if previous_provider != st.session_state.provider:
            st.session_state.selected_model = None
            st.session_state.model_capabilities = []
        
        # Model selection based on provider
        if st.session_state.provider:
            if st.session_state.provider == "Ollama":
                if ollama_models:
                    st.session_state.selected_model = st.selectbox(
                        "Select Ollama Model",
                        options=ollama_models,
                        key='ollama_model_select'
                    )
            else:
                provider_models = model_config.get_provider_models(st.session_state.provider.lower())
                if provider_models:
                    st.session_state.selected_model = st.selectbox(
                        f"Select {st.session_state.provider} Model",
                        options=list(provider_models.keys()),
                        format_func=lambda x: f"{provider_models[x]['name']} ({provider_models[x]['cost']})",
                        key=f"{st.session_state.provider.lower()}_model_select"
                    )
                    
                    # Display API key status and input
                    if st.session_state.provider in ["OpenAI", "Together", "Groq"]:
                        # Check if API key exists
                        existing_key = st.session_state.openmind.get_api_key(
                            st.session_state.provider.lower()
                        )
                        
                        # Show API key status
                        if existing_key:
                            st.markdown(f"""
                                <div class="api-key-status">
                                    <span class="checkmark">✓</span>
                                    <span class="text">{st.session_state.provider} API Key Stored</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # API key input
                        api_key = st.text_input(
                            f"{st.session_state.provider} API Key",
                            type="password",
                            key=f"{st.session_state.provider.lower()}_api_key"
                        )
                        
                        if api_key:
                            st.session_state.openmind.save_api_key(
                                st.session_state.provider.lower(), 
                                api_key
                            )
                            # Force refresh to show checkmark
                            st.experimental_rerun()
        
        # Display model information
        display_model_info()

    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input(
        "describe your symptoms or ask a health question...",
        key="chat_input"
    )
    
    if prompt:
        process_message(prompt)

if __name__ == "__main__":
    main()
