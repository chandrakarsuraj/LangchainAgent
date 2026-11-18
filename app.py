from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_tavily import TavilySearch

search_tool = TavilySearch(
    max_results=5,
    topic="general"
)
@tool
def web_search(question:str):
    """Web seach tool"""
    result = search_tool.invoke({
    "query": question
    })
model = ChatOpenAI(
    model="gpt-6-luna",
    # use_responses_api=False,   # Chat Completions: no reasoning items to carry
    reasoning_effort="none"
)
agent = create_agent(
    # model=model,
    model = "openai:gpt-4o-mini",
    tools = [web_search],
    system_prompt="You are a helpful assistant",

)