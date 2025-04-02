from lib.llm.base_llm_client import BaseLLMClient
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AnyMessage
from lib.config.llm_config import CohereLLMConfig


class CohereLLMClient(BaseLLMClient):
    """
    Defines a large language model client interface for Cohere.
    """

    def __init__(self):
        # get Cohere API key and model name from config
        cohere_config = CohereLLMConfig()

        self.llm = ChatCohere(cohere_api_key=cohere_config.api_key, model=cohere_config.model_name)

    def invoke(self, prompt: str) -> str:
        """
        Invokes the large language model with the given prompt and returns the generated text.
        """
        
        # Create a HumanMessage object with the prompt
        human_message = HumanMessage(content=prompt)

        # Generate a response using the LLM
        response = self.llm.invoke([human_message])

        # Extract and return the generated text from the response
        return response.content
    
    def invoke(self, prompt: list[AnyMessage]) -> str:

        # Generate a response using the LLM
        response = self.llm.invoke(prompt)

        # Extract and return the generated text from the response
        return response.content


if __name__ == "__main__":
    # Example usage
    cohere_client = CohereLLMClient()
    print(cohere_client.invoke("What is the capital of France?"))