import httpx
import json
from typing import List, Dict, Any
from config import settings

class LLMClient:
    def __init__(self):
        self.base_url = settings.llm_api_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_api_model
        self.timeout = settings.timeout_seconds

    def chat(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send chat completion request to LLM."""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")
