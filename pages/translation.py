"""Streamlit page for text translation."""
import os
from typing import Callable

import streamlit as st
import requests
import deepl
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="Translation demo")

st.markdown("# Translation demo (any language -> Spanish)")
st.sidebar.header("Translation demo")
st.markdown("Please select provider in a sidebar.")


class Generator:
    """Class that contains all generate methods."""
    @staticmethod
    def generate_rapidapi(prompt: str) -> str:
        """Generate Spanish translation using rapidai.

        Parameters
        ----------
        prompt : str
            Input text.

        Returns
        -------
        str
            Spanish translation.
        """
        url = "https://nlp-translation.p.rapidapi.com/v1/translate"

        payload = {
            "text": prompt,
            "to": "es",
            "from": "en"
        }

        headers = {
            "x-rapidapi-key": os.environ['RAPIDAPI_API_KEY'],
            "x-rapidapi-host": "nlp-translation.p.rapidapi.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)

        return response.json()['translated_text']['es']

    @staticmethod
    def generate_deepl(prompt: str) -> str:
        """Generate Spanish translation using deepl.

        Parameters
        ----------
        prompt : str
            Input text.

        Returns
        -------
        str
            Spanish translation.
        """
        translator = deepl.Translator(os.environ['DEEPL_API_KEY'])
        return translator.translate_text(prompt, target_lang="ES").text

    def execute(self, prompt: str, provider) -> str:
        """Generate summarization.

        Parameters
        ----------
        prompt : str
            Input text.
        provider
            Translation provider.

        Returns
        -------
        str
            Spanish translation.
        """
        generate: Callable[[str], str] = None
        match provider:
            case "rapidapi":
                generate = self.generate_rapidapi
            case "deepl":
                generate = self.generate_deepl

        return generate(prompt)


translator = Generator()

provider = st.sidebar.selectbox(
    "Select model provider",
    ("rapidapi", "deepl")
)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "London is the capital of Great Britain.",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(translator.execute(prompt=text, provider=provider))
