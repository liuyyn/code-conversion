from abc import ABC, abstractmethod
from langchain_core.messages import AnyMessage



class BaseLLMClient(ABC):
    """
    Defines a large language model client interface.
    """ 

    @abstractmethod
    def invoke(self, prompt: list[AnyMessage]) -> str:
        """
        Invokes the large language model with the given prompt and returns the generated text.
        """
        pass
