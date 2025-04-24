from dataclasses import dataclass
from typing import TypedDict

class CodingLanguage(TypedDict): 
    """
    Defines the coding languages.
    """
    c = "c"
    python = "python" # maps to the output from the llm that wraps the code between 

@dataclass
class FileDependency:
    """
    Defines a file dependency interface.
    """
    value: str 

@dataclass
class CodeFunction: 
    """
    Defines a file functions interface.
    """
    name: str
    args: list[str]
    return_type: str
    description: str = None
    file_path: str = None
    code: str = None
    
@dataclass
class File: 
    path: str
    language: CodingLanguage
    # dependencies: list[FileDependency] = None
    functions: list[CodeFunction] = None
    function_calls: list[str] = None


# class File:
#     """
#     Defines a file interface.
#     """

#     def __init__(self, path: str):
#         self.path: str = path
#         self.language: CodingLanguage = None
#         self.functions: list[FileFunction] = []
#         self.function_calls: list[str] = []

#     def read(self, path: str) -> str:
#         """
#         Reads the content of the file at the given path and returns it as a string.
#         """
#         pass