"""
Gemini API Client Module
Handles communication with Google Gemini API for generating content.
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

import httpx
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerateContentResponse

from ..utils.logger import get_logger
from ..utils.config import GeminiConfig


logger = get_logger("gemini-client")


@dataclass
class APIRequest:
    """API request data structure."""
    system_instruction: Dict[str, Any]
    contents: List[Dict[str, Any]]


class GeminiApiClient:
    """
    Client for interacting with Google Gemini API.
    """
    
    def __init__(self, config: GeminiConfig):
        """
        Initialize Gemini API client.
        
        Args:
            config: Gemini configuration
            
        Raises:
            ValueError: If API key is not provided
        """
        if not config.api_key or config.api_key == "YOUR_GEMINI_API_KEY":
            raise ValueError("Gemini API key is required")
        
        self.config = config
        self.api_key = config.api_key
        self.model_name = config.model
        
        # Set API key for Google Generative AI
        os.environ["GOOGLE_API_KEY"] = self.api_key
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
        except ImportError:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
    
    def _get_model(self) -> GenerativeModel:
        """
        Get configured model instance.
        
        Returns:
            GenerativeModel instance
        """
        generation_config = {
            "temperature": self.config.temperature,
            "top_k": self.config.top_k,
            "top_p": self.config.top_p,
            "max_output_tokens": self.config.max_output_tokens,
        }
        
        return self.genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config
        )
    
    async def generate_content(self, api_request: APIRequest) -> str:
        """
        Generate content using Gemini API.
        
        Args:
            api_request: Formatted API request
            
        Returns:
            Generated analysis text
            
        Raises:
            Exception: If API request fails
        """
        try:
            logger.info("Sending request to Gemini API")
            
            model = self._get_model()
            
            # Create chat session with system instruction
            system_text = api_request.system_instruction["parts"][0]["text"]
            user_text = api_request.contents[0]["parts"][0]["text"]
            
            chat = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [{"text": system_text}]
                },
                {
                    "role": "model",
                    "parts": [{"text": "이해했습니다. 글로벌 투자 은행의 선임 주식 분석가로서 제공된 재무 지표를 기반으로 객관적인 가치 평가와 투자 관점을 제시하겠습니다."}]
                }
            ])
            
            # Send user query
            response = await asyncio.to_thread(chat.send_message, user_text)
            text = response.text
            
            logger.info("Received response from Gemini API", {
                "response_length": len(text)
            })
            
            return text
            
        except Exception as error:
            logger.error("Gemini API request failed", {
                "error": str(error)
            })
            raise Exception(f"Gemini API Error: {str(error)}")
    
    async def generate_simple_content(self, prompt: str) -> str:
        """
        Generate simple text content.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            Generated text
            
        Raises:
            Exception: If generation fails
        """
        try:
            model = self._get_model()
            response = await asyncio.to_thread(model.generate_content, prompt)
            text = response.text
            
            return text
            
        except Exception as error:
            logger.error("Simple content generation failed", {
                "error": str(error)
            })
            raise Exception(f"Gemini API Error: {str(error)}")
    
    async def test_connection(self) -> bool:
        """
        Test API connection.
        
        Returns:
            True if connection is successful
        """
        try:
            test_prompt = "테스트 메시지입니다. '연결 성공'이라고 답변해주세요."
            response = await self.generate_simple_content(test_prompt)
            
            is_connected = "연결 성공" in response
            
            logger.info("API connection test completed", {
                "success": is_connected
            })
            
            return is_connected
            
        except Exception as error:
            logger.error("API connection test failed", {
                "error": str(error)
            })
            
            return False


def create_gemini_client(config: GeminiConfig) -> GeminiApiClient:
    """
    Factory function to create Gemini API client.
    
    Args:
        config: Gemini configuration
        
    Returns:
        GeminiApiClient instance
    """
    return GeminiApiClient(config)
