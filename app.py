from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END 
from lib.config.app_config import app_config
from lib.llm.cohere_llm_client import CohereLLMClient
from lib.output_parsers import CodeOutputParser
from lib.code_parsers import CCodeParser
from lib.file import CodingLanguage, File

llm = CohereLLMClient()

class CodeConversionAgentState(TypedDict):
    """
    TypedDict for the state of the CodeConversionAgent.
    """

    # current_language: str
    # target_language: str
    content: str
    file_data: File
    # file_path: str
    messages: Annotated[list[AnyMessage], add_messages]
    success: bool


def read_file(file_path: str) -> str:
    """
    Function to read a file and return its content.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")


def read_file_step(state: CodeConversionAgentState):
    print("reading file")
    content = read_file(app_config.source_folder_path)
    # human_message = HumanMessage(
    #     content=f"""
    #         Convert the following Pro*C code into Python code. Only generate Python code without additional explanation except for Python comments. 
        
    #         {content}
    #     """)

    return {"content": content}

def get_file_data(state: CodeConversionAgentState):
    print("getting file data")
    # parse the file and get the function definitions and function calls
    c_parser = CCodeParser()
    file_data = c_parser.parse(app_config.source_folder_path)

    # add the file data to the state
    state["file_data"] = file_data

    return {"file_data": file_data}


def convert_code(state: CodeConversionAgentState): 
    print("converting code")
    system_message = SystemMessage(
        content="""
            You are an AI assistant that helps convert C code into Python code. 
            The C code will contain database SQL queries and C code.
            Your task is to convert the C code into equivalent Python code, preserving the logic and functionality of the original code. 
            Handle the SQL code by converting it into Apache Spark code in the Python language. 
            Handle the C code by converting it into Python code. 
            Assume the python environment is running in Databricks and that the tables in the C code are accessible in Databricks as delta tables.   
            Do not invente things. Only generate Python code. You can add Python comments for clarity if needed but nothing else otherwise. 
            In the case where there are functions that are defined in the C code that is not needed for the conversion, you do not need to generate the converted code.

            If there are dependencies between the functions, make sure to include them in the converted code whether in a new file or the same file. 
            Write clean and readable code.
            Along with the C code, you will receive an object describing all the function definitions and function calls from the C code. The format will be of the following: 
                File(path="<path>", language="<coding language of the file>", functions=[<a list of CodeFunction(name=<function name>, args=[<a list of function input arguments>], file_path=<file path of the function>, return_type=<function return type>, code=<code of the function>) describing the functions defined in the file>], function_calls=[<list of function called in the file>])
            Use this information to plan the conversion and to generate the converted code into clean and readable code. Feel free to merge the functions if you see redundancy and reuse them in the conversion.
            """
        # """
        #     You are an AI assistant that helps convert Pro*C code into Python code. 
        #     The Pro*C code will contain embedded SQL queries and C/C++ code.
        #     Your task is to convert the Pro*C code into equivalent Python code, preserving the logic and functionality of the original code. 
        #     Handle the embbeded SQL code by converting it into Apache Spark code in the Python language. 
        #     Handle the C/C++ code by converting it into Python code. 
        #     Assume the python environment is running on Databricks and that the tables the Pro*C are accessible in Databricks as delta tables.   
        #     Do not invente things. Only generate Python code. You can add Python comments for clarity if needed but nothing else otherwise. 

        #     If there are dependencies between the functions, make sure to include them in the converted code.
        #     You will receive with the Pro*C code a list describing all the function definition and function calls from the Pro*C file.
        #     """
    )
    
    human_message = HumanMessage(
        content=f"""
            Convert the following C code into Python code. Only generate Python code without additional explanation except for Python comments. 
            
            Use the following information describing function definition and calls from the file to help you in the conversion:
            {state["file_data"]}

            Code content: 
            {state["content"]}
        """)

    # convert code - the content of the code needed to convert should be in the messages 
    converted_code = llm.invoke([system_message, human_message], parser=CodeOutputParser(CodingLanguage.python))

    # write the converted code to the output folder 
    with open(app_config.target_folder_path, "w") as f: 
        f.write(converted_code)
    
    return {"success": True}

def save_graph_image(graph): 
    graph_image =  graph.get_graph().draw_mermaid_png()

    with open("graph_image.png", "wb") as f:
        f.write(graph_image)


if __name__ == "__main__": 

    #  build the graph 
    graph_builder = StateGraph(CodeConversionAgentState)
    
    # add the nodes
    graph_builder.add_node("read_file_step", read_file_step)
    graph_builder.add_node("get_file_data", get_file_data)
    graph_builder.add_node("convert_code", convert_code)

    # add the edges
    graph_builder.add_edge(START, "read_file_step")
    graph_builder.add_edge("read_file_step", "get_file_data")
    graph_builder.add_edge("get_file_data", "convert_code" )
    graph_builder.add_edge("convert_code", END)

    graph = graph_builder.compile()

    # save the graph image
    save_graph_image(graph)

    # invoke the graph 
    graph.invoke({})






