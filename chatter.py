# chatter.py
import openai
from groq import Groq
import aiohttp
import logging
import os
import requests
import asyncio
import json
from typing import Dict, List, Optional, Union


logging.basicConfig(level=logging.DEBUG)

def load_system_prompt():
    """Load system prompt from prompt.txt"""
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logging.warning("prompt.txt not found, using default prompt")
        return "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."
    except Exception as e:
        logging.error(f"Error loading prompt: {e}")
        return "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."

class GPT4o:
    def __init__(self, api_key):
        self.client = openai.Client(api_key=api_key)
        self.system_prompt = load_system_prompt()
        
    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI Error: {e}")
            return f"Error generating response: {str(e)}"

class GroqModel:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.system_prompt = load_system_prompt()
        
    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }],
                model="mixtral-8x7b-32768"
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Groq Error: {e}")
            return f"Error generating response: {str(e)}"

class TogetherModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.together.xyz/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = load_system_prompt()

    def generate_response(self, prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            logging.error(f"Together.ai Error: {e}")
            return f"Error generating response: {str(e)}"

class OllamaHandler:
    """Class to interact with local Ollama models"""
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.headers = {"Content-Type": "application/json"}
        self.available_models = self.list_models()
        self.selected_model = None
        self.system_prompt = load_system_prompt()
        self.last_error = None

    def check_installation(self):
        """Check if Ollama is installed and running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self):
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except requests.RequestException as e:
            logging.error(f"Error listing Ollama models: {e}")
            return []

    def select_model(self, model_name: str) -> bool:
        """Select a model from available models"""
        if not model_name:
            self.last_error = "No model specified"
            return False
        if model_name in self.available_models:
            self.selected_model = model_name
            self.last_error = None
            return True
        self.last_error = f"Model {model_name} not found in available models"
        return False

    def get_last_error(self):
        """Get the last error message"""
        return self.last_error

    def generate_response(self, prompt, model=None):
        """Synchronous wrapper for async generation"""
        if not self.selected_model and not model:
            return "Please select a model first"
        try:
            return asyncio.run(self.generate_response_async(prompt, model))
        except Exception as e:
            logging.error(f"Ollama Sync Error: {e}")
            self.last_error = str(e)
            return f"Error generating response: {str(e)}"

    async def generate_response_async(self, prompt, model=None):
        """Generate response using Ollama's API asynchronously"""
        try:
            use_model = model or self.selected_model
            if not use_model:
                available = ", ".join(self.available_models)
                self.last_error = f"No model selected. Available models: {available}"
                return self.last_error

            if use_model not in self.available_models:
                available = ", ".join(self.available_models)
                self.last_error = f"Model {use_model} not found. Available models: {available}"
                return self.last_error

            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": use_model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
                
                try:
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json=payload,
                        headers=self.headers,
                        timeout=600  # Add timeout in seconds default 10 mins
                    ) as response:
                        response.raise_for_status()
                        data = await response.json()
                        self.last_error = None
                        return data.get("message", {}).get("content", "")
                except aiohttp.ClientResponseError as e:
                    if e.status == 500:
                        self.last_error = f"Error: The model '{use_model}' encountered an error. Please try another model."
                        return self.last_error
                    raise
                except asyncio.TimeoutError:
                    self.last_error = f"Request timed out. The model '{use_model}' took too long to respond."
                    return self.last_error
                    
        except Exception as e:
            error_msg = f"Ollama Error: {str(e)}"
            logging.error(error_msg)
            self.last_error = error_msg
            return error_msg

    def get_model_info(self, model_name: str = None) -> Dict:
        """Get information about a specific model or currently selected model"""
        try:
            model = model_name or self.selected_model
            if not model:
                return {"error": "No model specified or selected"}
            
            response = requests.get(f"{self.base_url}/api/show/{model}")
            if response.status_code == 200:
                return response.json()
            return {"error": f"Failed to get info for model {model}"}
        except Exception as e:
            return {"error": f"Error getting model info: {str(e)}"}

def get_model_instance(provider, api_key=None):
    """Factory function to get the appropriate model instance"""
    if provider == "Together":
        return TogetherModel(api_key) if api_key else None
    elif provider == "Groq":
        return GroqModel(api_key) if api_key else None
    elif provider == "Ollama":
        return OllamaHandler()
    elif provider == "GPT4":
        return GPT4o(api_key) if api_key else None
    return None
