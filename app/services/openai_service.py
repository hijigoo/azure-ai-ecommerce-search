"""
Azure OpenAI Service module.
Provides methods for chat completion, embeddings, and text generation.
"""

import numpy as np
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from config import Config


class OpenAIService:
    """Service for Azure OpenAI operations"""
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        
        # Use Azure managed identity authentication
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        self.client = AzureOpenAI(
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider
        )
        
        self.gpt_deployment = Config.AZURE_OPENAI_DEPLOYMENT_NAME
        self.embedding_deployment = Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for the given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        # Clean text
        text = text.replace("\n", " ").strip()
        
        # Call embedding API
        response = self.client.embeddings.create(
            input=[text],
            model=self.embedding_deployment
        )
        
        return np.array(response.data[0].embedding)
    
    def chat_completion(
        self,
        messages: list,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        temperature = temperature or Config.DEFAULT_TEMPERATURE
        max_tokens = max_tokens or Config.MAX_TOKENS
        
        response = self.client.chat.completions.create(
            model=self.gpt_deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def generate_text(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant.",
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: User prompt
            system_message: System message for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages, temperature, max_tokens)


# Singleton instance
_openai_service = None


def get_openai_service() -> OpenAIService:
    """Get or create OpenAI service instance"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service
