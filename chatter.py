# chatter.py (c) 2024 Gregory L. Magnusson MIT license

import os
import logging
import json
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime
from openai import OpenAI
from groq import Groq
import subprocess
from logger import get_logger
from config import model_config

def load_system_prompt() -> str:
    """Load system prompt from file"""
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"Error loading system prompt: {e}")
        return "You are a medical AI assistant. Please provide accurate and helpful medical information."

class GPT4o:
    """OpenAI model handler"""
    
    def __init__(self, api_key):
        self.logger = get_logger('openai')
        os.environ["OPENAI_API_KEY"] = api_key
        try:
            self.client = OpenAI()  # No arguments needed
            self.system_prompt = load_system_prompt()
            self.selected_model = "gpt-4"
        except Exception as e:
            self.logger.error(f"OpenAI Error: {e}")
            raise

    def select_model(self, model_id: str) -> bool:
        try:
            self.selected_model = model_id
            self.logger.info(f"Model selected: {model_id}")
            return True
        except Exception as e:
            self.logger.error(f"OpenAI Error selecting model: {e}")
            return False

    def generate_response(self, prompt: str) -> str:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            chat_completion = self.client.chat.completions.create(
                model=self.selected_model,
                messages=messages
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            self.logger.error(f"OpenAI Error: {e}")
            return f"Error generating response: {str(e)}"

    def list_models(self):
        """List available models"""
        return [
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "type": "chat",
                "tokens": 8192,
                "developer": "OpenAI"
            },
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "type": "chat",
                "tokens": 128000,
                "developer": "OpenAI"
            },
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "type": "chat",
                "tokens": 16385,
                "developer": "OpenAI"
            }
        ]

class GroqModel:
    """Groq model handler"""
    
    def __init__(self, api_key):
        self.logger = get_logger('groq')
        os.environ["GROQ_API_KEY"] = api_key
        try:
            self.client = Groq()  # No arguments needed
            self.selected_model = "mixtral-8x7b-32768"
            self.system_prompt = load_system_prompt()
        except Exception as e:
            self.logger.error(f"Groq Error: {e}")
            raise

    def select_model(self, model_id: str) -> bool:
        try:
            self.selected_model = model_id
            return True
        except Exception as e:
            self.logger.error(f"Groq Error selecting model: {e}")
            return False

    def generate_response(self, prompt: str) -> str:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.selected_model,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Groq Error: {e}")
            return f"Error generating response: {str(e)}"

    def list_models(self):
        """List available models"""
        return [
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral-8x7b-Instruct-v0.1",
                "type": "chat",
                "tokens": 32768,
                "developer": "Mistral"
            },
            {
                "id": "llama-3.3-70b-versatile",
                "name": "LLaMA 3.3 70B Versatile",
                "type": "chat",
                "tokens": 8192,
                "developer": "Meta"
            }
        ]

class TogetherModel:
    """Together AI model handler"""
    
    def __init__(self, api_key):
        self.logger = get_logger('together')
        self.api_key = api_key
        self.base_url = "https://api.together.xyz/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = load_system_prompt()
        self.selected_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    def select_model(self, model_id: str) -> bool:
        try:
            self.selected_model = model_id
            self.logger.info(f"Model selected: {model_id}")
            return True
        except Exception as e:
            self.logger.error(f"Together Error selecting model: {e}")
            return False

    def generate_response(self, prompt: str) -> str:
        try:
            payload = {
                "model": self.selected_model,
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
            
            self.logger.debug("Response generated", 
                            extra={'structured_data': {
                                'model': self.selected_model,
                                'status_code': response.status_code
                            }})
            
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            self.logger.error(f"Together Error: {e}")
            return f"Error generating response: {str(e)}"

    def list_models(self):
        """List available models"""
        return [
            {
                "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "name": "Mixtral-8x7B-Instruct",
                "type": "chat",
                "tokens": 32768,
                "developer": "Mistral"
            },
            {
                "id": "meta-llama/Llama-2-70b-chat-hf",
                "name": "Llama-2-70b",
                "type": "chat",
                "tokens": 4096,
                "developer": "Meta"
            }
        ]

class OllamaHandler:
    """Ollama local model handler"""
    
    def __init__(self):
        self.logger = get_logger('ollama')
        self.selected_model = None
        self.last_error = None
        self.system_prompt = load_system_prompt()

    def check_installation(self) -> bool:
        try:
            result = subprocess.run(['ollama', 'list'], 
                                 capture_output=True, 
                                 text=True)
            return result.returncode == 0
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Ollama installation check failed: {e}")
            return False

    def list_models(self) -> List[str]:
        try:
            result = subprocess.run(['ollama', 'list'], 
                                 capture_output=True, 
                                 text=True)
            if result.returncode == 0:
                models = []
                for line in result.stdout.split('\n')[1:]:  # Skip header
                    if line.strip():
                        models.append(line.split()[0])
                return models
            return []
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error listing Ollama models: {e}")
            return []

    def select_model(self, model_name: str) -> bool:
        try:
            if model_name in self.list_models():
                self.selected_model = model_name
                self.logger.info(f"Model selected: {model_name}")
                return True
            self.last_error = f"Model {model_name} not found"
            return False
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error selecting Ollama model: {e}")
            return False

    def generate_response(self, prompt: str) -> str:
        if not self.selected_model:
            return "No model selected"

        try:
            cmd = [
                'ollama', 'run', 
                self.selected_model, 
                f"{self.system_prompt}\n\nUser: {prompt}\nAssistant:"
            ]
            
            result = subprocess.run(cmd, 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                response = result.stdout.strip()
                self.logger.debug("Response generated", 
                                extra={'structured_data': {
                                    'model': self.selected_model,
                                    'response_length': len(response)
                                }})
                return response
            else:
                self.last_error = result.stderr
                return f"Error: {result.stderr}"

        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Ollama Error: {e}")
            return f"Error generating response: {str(e)}"

    def get_last_error(self) -> Optional[str]:
        return self.last_error
