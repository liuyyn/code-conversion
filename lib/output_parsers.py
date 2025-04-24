from typing import TypedDict
import re
from lib.file import CodingLanguage 

class CodeOutputParser:

    def __init__(self, language: CodingLanguage): 
        self.language = language

    def parse(self, llm_output: str) -> str:
        """
        Parses an LLM response into defined language format, remove starting and trailing strings. 
        Returns the input string if no match.

        Arguments:
            llm_output (str): The output string from the LLM to parse.
        Returns:
            str: The parsed string.
        """ 
        regex_patern = fr"```{self.language}(.*?)```"
        match = re.search(regex_patern, llm_output, re.DOTALL) # check if pattern is matched in the output string 

        return match.group(1).strip() if match else llm_output


if __name__ == "__main__": 

    p = CodeOutputParser(CodingLanguage.python)
    
    llm_output = """
                python```
                print("hello world!")
                ``` 
                """
    
    print(p.parse(llm_output))



