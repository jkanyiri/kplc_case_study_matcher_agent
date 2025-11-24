import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from src.prompt import AGENT_PROMPT
from langchain.chat_models import init_chat_model
from src.schema import CaseStudySearchQuery
from langchain_tavily import TavilySearch
from typing import TypedDict


load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is missing. Please set it in your .env file.")


llm = init_chat_model(model="gpt-4", temperature=0.0)


class AgentState(TypedDict):
    project_idea: str
    query: str
    case_studies: list[str]


class InputState(TypedDict):
    project_idea: str


class OutputState(TypedDict):
    case_studies: list[str]


def generate_query(state: AgentState) -> str:
    """Node to generate a query to search for case studies"""

    project_details = state["project_idea"]

    system_instruction = AGENT_PROMPT.format(
        project_details=project_details,
    )

    messages = [
        {
            "role": "system",
            "content": system_instruction,
        },
        {
            "role": "user",
            "content": "Generate a query to search for case studies that are relevant to the project.",
        },
    ]

    structured_llm = llm.with_structured_output(CaseStudySearchQuery)
    response = structured_llm.invoke(messages)

    return {
        "query": response.query,
    }


def search_case_studies(state: AgentState) -> str:

    query = state["query"]
    tavily_search = TavilySearch(api_key=TAVILY_API_KEY, max_results=20)
    results = tavily_search.invoke(query)

    return {
        "case_studies": results,
    }


graph_builder = StateGraph(
    AgentState, input_schema=InputState, output_schema=OutputState
)

graph_builder.add_node("generate_query", generate_query)
graph_builder.add_node("search_case_studies", search_case_studies)

graph_builder.add_edge(START, "generate_query")
graph_builder.add_edge("generate_query", "search_case_studies")
graph_builder.add_edge("search_case_studies", END)

agent = graph_builder.compile()
