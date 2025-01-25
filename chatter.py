# chatter.py
import openai
from groq import Groq
import aiohttp
import logging
import os
import requests
import asyncio
import subprocess
import json

logging.basicConfig(level=logging.DEBUG)

class GPT4o:
    def __init__(self, api_key):
        self.client = openai.Client(api_key=api_key)
        
    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."
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
        
    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."
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

    def generate_response(self, prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
        try:
            system_prompt = "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
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
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.headers = {"Content-Type": "application/json"}
        self.available_models = self.list_models()

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

    async def generate_response_async(self, prompt, model="llama2"):
        """Generate response using Ollama's API asynchronously"""
        try:
            system_prompt = "You are Dr. AIML, a medical AI consultant. Provide accurate, ethical medical information and always encourage consulting with healthcare professionals."
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    headers=self.headers
                ) as response:
                    if response.status == 404:
                        return f"Model {model} not found. Available models: {', '.join(self.available_models)}"
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("message", {}).get("content", "")
        except aiohttp.ClientError as e:
            logging.error(f"Ollama Error: {e}")
            return f"Error generating response: {str(e)}"

    def generate_response(self, prompt, model="llama2"):
        """Synchronous wrapper for async generation"""
        try:
            return asyncio.run(self.generate_response_async(prompt, model))
        except Exception as e:
            logging.error(f"Ollama Sync Error: {e}")
            return f"Error generating response: {str(e)}"

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
