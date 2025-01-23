"""Streamlit page for text summarization using LangChain."""
import os

import streamlit as st
from dotenv import load_dotenv

from langchain_core.language_models import BaseChatModel
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI


load_dotenv()

st.set_page_config(page_title="Text summarization demo")

st.markdown("# Text summarization demo")
st.sidebar.header("Text summarization demo")
st.markdown("Please select provider in a sidebar.")


def generate_response(input_text: str, model: BaseChatModel) -> str:
    """Generate LLM summarization response

    Parameters
    ----------
    input_text : str
        Input text
    model : langchain_core.language_models.BaseChatModel
        LangChain ChatModel to use for summarization.

    Returns
    -------
    str
        Summarized text.
    """
    prompt_template = ChatPromptTemplate.from_messages([
        (
            'system',
            'Imagine you are extremely proficient in summarization, summarize incoming text'
        ),
        (
            'human',
            'Summarize this:\n{input_text}'
        )
    ])
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({'input_text': input_text})


provider = st.sidebar.selectbox(
    "Select LLM provider",
    ("OpenAI", "Vertex", "Anthropic")
)

llm = None
match provider:
    case "OpenAI":
        llm = ChatOpenAI(model='gpt-4o', temperature=0, api_key=os.environ['OPENAI_API_KEY'])
    case "Vertex":
        llm = ChatVertexAI(model="gemini-1.5-flash-001")
    case "Anthropic":
        llm = ChatAnthropic(model='claude-3-5-haiku-20241022')

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        (
            "Data science is an interdisciplinary field that combines techniques from statistics, computer science, "
            "and domain expertise to extract meaningful insights from data. It involves various stages, including data "
            "collection, cleaning, exploration, analysis, and visualization. Machine learning, a subset of artificial "
            "intelligence, plays a crucial role in predictive modeling by enabling algorithms to learn patterns from "
            "data and make informed decisions. However, the success of data science projects heavily depends on the "
            "quality and relevance of the data. Ethical considerations, such as bias, privacy, and transparency, are "
            "also critical to ensure responsible use of data science methods. As businesses increasingly adopt "
            "data-driven strategies, the demand for skilled data scientists continues to grow, highlighting the "
            "importance of ongoing learning and adaptability in the field."
        )
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(generate_response(text, model=llm))
