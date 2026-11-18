import os

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

search_tool = (
    TavilySearch(max_results=5, topic="general")
    if os.getenv("TAVILY_API_KEY")
    else None
)
@tool
def web_search(question: str) -> str:
    """Search the web for current information about a question."""
    if search_tool is None:
        return "Web search is unavailable: set TAVILY_API_KEY in your environment or .env file."

    result = search_tool.invoke({"query": question})
    return str(result)

model = ChatOpenAI(
    model="gpt-6-luna",
    # use_responses_api=False,   # Chat Completions: no reasoning items to carry
    reasoning_effort="none"
)
agent = create_agent(
    # model=model,
    model="openai:gpt-4o-mini",
    tools=[web_search],
    system_prompt="You are a helpful assistant",
)


def streamlit_app():
    """Run a basic Streamlit chat interface for the LangChain agent."""
    st.title("Web Search Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = agent.invoke({"messages": st.session_state.messages})
                answer = result["messages"][-1].content
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")


if __name__ == "__main__":
    streamlit_app()