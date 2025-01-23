"""Streamlit page for text summarization using API."""
from typing import Callable

import streamlit as st
from dotenv import load_dotenv

from together import Together
from openai import OpenAI
from anthropic import Anthropic


load_dotenv()

st.set_page_config(page_title="Text summarization demo")

st.markdown("# Text summarization demo")
st.sidebar.header("Text summarization demo")
st.markdown("Please select provider in a sidebar.")


class Generator:
    """Class that contains all generate methods."""
    @staticmethod
    def generate_openai(prompt: str) -> str:
        """Generate summarization using OpenAI API and GPT-4o.

        Parameters
        ----------
        prompt : str
            Input prompt.

        Returns
        -------
        str
            Summarized text.
        """
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "Imagine you are extremely proficient in summarization, summarize incoming text"},
                {"role": "user", "content": f'Summarize this: "{prompt}"'}
            ]
        )

        return completion.choices[0].message.content

    @staticmethod
    def generate_anhtropic(prompt: str) -> str:
        """Generate summarization using Anthropic API and Claude-3.5-sonnet.

        Parameters
        ----------
        prompt : str
            Input prompt.

        Returns
        -------
        str
            Summarized text.
        """
        client = Anthropic()

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            temperature=0,
            max_tokens=1000,
            system="Imagine you are extremely proficient in summarization, summarize incoming text",
            messages=[
                {"role": "user", "content": f'Summarize this: "{prompt}"'}
            ]
        )

        return message.content[0].text

    @staticmethod
    def generate_together(prompt: str) -> str:
        """Generate summarization using TogetherAI and LLama 3.2 3B Instruct Turbo.

        Parameters
        ----------
        prompt : str
            Input prompt.

        Returns
        -------
        str
            Summarized text.
        """
        client = Together()

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "Imagine you are extremely proficient in summarization, summarize incoming text"},
                {"role": "user", "content": f'Summarize this: "{prompt}"'}
            ],
        )

        return response.choices[0].message.content

    def execute(self, prompt: str, provider) -> bytes:
        """Generate summarization.

        Parameters
        ----------
        prompt : str
            Input prompt
        provider
            LLM provider

        Returns
        -------
        bytes
            Output Image
        """
        generate: Callable[[str], str] = None
        match provider:
            case "OpenAI":
                generate = self.generate_openai
            case "Anthropic":
                generate = self.generate_anhtropic
            case "TogetherAI":
                generate = self.generate_together

        return generate(prompt)


text_summarization = Generator()

provider = st.sidebar.selectbox(
    "Select LLM provider",
    ("OpenAI", "Anthropic", "TogetherAI")
)

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
        st.info(text_summarization.execute(prompt=text, provider=provider))
