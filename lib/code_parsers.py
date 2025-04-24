from abc import ABC, abstractmethod
from lib.config.app_config import app_config
from lib.file import CodeFunction, File, CodingLanguage
import clang.cindex
from clang.cindex import CursorKind, TranslationUnit

class CodeParser:
        
    @abstractmethod
    def parse(self, path: str):
        """
        Given a file path, parses the code and extracts relevant information from the code used as input to the LLM for code conversion.
        """
        pass 

class CCodeParser(CodeParser):
    """
    Parses C code and extracts relevant information.
    """
    def __init__(self):
        # initializes clang compiler 

        # Point to your libclang shared library
        clang.cindex.Config.set_library_file(app_config.libclang_path)  
        self.index = clang.cindex.Index.create()

    def get_cursor(self, path: str):
        """
        Returns the cursor for the given path.
        """

        translation_unit = self.index.parse(path)
        cursor  = translation_unit.cursor

        return cursor
        
    def extract_information(self, cursor, path: str) -> File:
        definitions = []
        calls = set()

        #  traverse the AST and extract the functions definitions and function calls
        for node in cursor.walk_preorder():
            if node.kind == CursorKind.FUNCTION_DECL and node.is_definition(): # don't include function declarations without definitions
                #  get the function name and arguments
                function_name = node.spelling
                args = [arg.spelling for arg in node.get_arguments()]
                return_type = node.type.get_result().spelling

                # get the code of the function
                function_tokens = node.get_tokens()
                function_code = ' '.join([token.spelling for token in function_tokens])

                cf = CodeFunction(name=function_name, args=args, file_path=path, return_type=return_type, code=function_code)
    
                definitions.append(cf)

                # TODO add the function calls called by the current function here

            elif node.kind == CursorKind.CALL_EXPR:
                #  get the function call name 
                function_call = node.spelling
                calls.add(function_call)
        
        file = File(path=path, language=CodingLanguage.c, functions=definitions, function_calls=list(calls))
        
        return file
    
    def parse(self, path: str) -> File:
        """
        Parses the .c file and extracts relevant information.
        """
        # build the AST of the file and get the cursor object to traverse the AST
        cursor = self.get_cursor(path)

        # extract the function definitions and function calls and put into a File object
        file = self.extract_information(cursor, path)

        return file
    
    
        
if __name__ == "__main__":
    # Example usage
    c_parser = CCodeParser()
    file = c_parser.parse("/mnt/d/yyl/code-conversion/input/main.c")
    
    print("Function definitions: ", file.functions)
    print("Function calls: ", file.function_calls)
    print("File path: ", file.path)
    print("File language: ", file.language)

        

        
