from typing import Optional
from dataclasses import dataclass, field
from abc import ABC

import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BaseLLMConfig(ABC):
    """
    Base class for all LLM configurations.
    """
    api_key: str
    model_name: str 
    # max_tokens: Optional[int] = field(default=1000)
    # temperature: Optional[float] = field(default=0.7)

@dataclass
class CohereLLMConfig(BaseLLMConfig):
    """
    Configuration class for Cohere LLM.
    """
    api_key: str = field(default=os.environ["COHERE_API_KEY"], repr=False) # do not expose API key in repr
    model_name: str = field(default=os.environ["COHERE_MODEL_NAME"])
    
    
if __name__ == "__main__":
    # Example usage
    cohere_config = CohereLLMConfig()
    print(cohere_config)