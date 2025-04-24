from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END 
from lib.config.app_config import AppConfig
from lib.llm.cohere_llm_client import CohereLLMClient
from lib.output_parsers import CodeOutputParser

app_config = AppConfig() # load the app config object
llm = CohereLLMClient()

class CodeConversionAgentState(TypedDict):
    """
    TypedDict for the state of the CodeConversionAgent.
    """

    # current_language: str
    # target_language: str
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
    human_message = HumanMessage(
        content=f"""
    Convert the following Pro*C code into Python code. Only generate Python code without additional explanation except for Python comments. 
    
    {content}
    """)

    return {"messages": [human_message]}

def convert_code(state: CodeConversionAgentState): 
    print("converting code")
    system_message = SystemMessage(
        content="""
            You are an AI assistant that helps convert Pro*C code into Python code. 
            The Pro*C code will contain embedded SQL queries and C/C++ code.
            Your task is to convert the Pro*C code into equivalent Python code, preserving the logic and functionality of the original code. 
            Handle the embbeded SQL code by converting it into Apache Spark code in the Python language. 
            Handle the C/C++ code by converting it into Python code. 
            Assume the python environment is running on Databricks and that the tables the Pro*C are accessible in Databricks as delta tables.   
            Do not invente things. Only generate Python code. You can add Python comments for clarity if needed but nothing else otherwise. 
            """
    )
    
    # convert code - the content of the code needed to convert should be in the messages 
    converted_code = llm.invoke([system_message] + state["messages"], parser=CodeOutputParser(CodingLanguage.python))

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
    graph_builder.add_node("convert_code", convert_code)

    # add the edges
    graph_builder.add_edge(START, "read_file_step")
    graph_builder.add_edge("read_file_step", "convert_code" )
    graph_builder.add_edge("convert_code", END)

    graph = graph_builder.compile()

    # save the graph image
    save_graph_image(graph)

    # invoke the graph 
    graph.invoke({})

    # TODO parser class to parse output






