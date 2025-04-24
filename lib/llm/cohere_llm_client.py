from lib.llm.base_llm_client import BaseLLMClient
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AnyMessage
from lib.config.llm_config import CohereLLMConfig
from lib.output_parsers import CodeOutputParser
from typing import Optional


class CohereLLMClient(BaseLLMClient):
    """
    Defines a large language model client interface for Cohere.
    """

    def __init__(self):
        # get Cohere API key and model name from config
        cohere_config = CohereLLMConfig()

        self.llm = ChatCohere(cohere_api_key=cohere_config.api_key, model=cohere_config.model_name)

    def invoke(self, prompt: list[AnyMessage], parser: Optional[CodeOutputParser] = None) -> str:
        """
        Invokes the large language model with the given prompt and returns the generated text.
        
        Arguments:
            prompt (list[AnyMessage]): The prompt to send to the LLM.
            parser (Optional[CodeOutputParser]): Optional parser to format the output.
        Returns:
            str: The generated text from the LLM.
        """

        # Generate a response using the LLM
        response = self.llm.invoke(prompt)

        content = response.content
        if parser: # parse the content if a parser is provided
            content = parser.parse(content) 

        return content
    


if __name__ == "__main__":
    # Example usage
    cohere_client = CohereLLMClient()
    print(cohere_client.invoke("What is the capital of France?"))