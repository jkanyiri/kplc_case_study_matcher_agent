from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from src.prompt import AGENT_PROMPT
from langchain.chat_models import init_chat_model
from src.schema import CaseStudySearchQuery
from langchain_tavily import TavilySearch


llm = init_chat_model(model="gpt-4", temperature=0.0)


class AgentState(MessagesState):
    query: str
    case_studies: list[str]


def generate_query(state: AgentState) -> str:
    """Node to generate a query to search for case studies"""

    project_details = state["messages"][-1].content

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
    tavily_search = TavilySearch(max_results=20)
    results = tavily_search.invoke(query)

    return {
        "case_studies": results["results"],
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node("generate_query", generate_query)
graph_builder.add_node("search_case_studies", search_case_studies)

graph_builder.add_edge(START, "generate_query")
graph_builder.add_edge("generate_query", "search_case_studies")
graph_builder.add_edge("search_case_studies", END)

agent = graph_builder.compile()
