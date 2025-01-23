"""Streamlit page for TTS."""
import os
from typing import Callable

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="TTS demo")

st.markdown("# TTS demo")
st.sidebar.header("TTS demo")
st.markdown("Please select provider in a sidebar.")


class Generator:
    """Class that contains all generate methods."""
    @staticmethod
    def generate_elevenlabs(prompt: str) -> str:
        """TTS using elevenlabs.

        Parameters
        ----------
        prompt : str
            Inout text.

        Returns
        -------
        str
            Url to audio.
        """
        url = "https://api.elevenlabs.io/v1/text-to-speech/9BWtsMINqrJLrRacOk9x"

        payload = {
            "text": prompt,
        }
        headers = {
            "xi-api-key": os.environ['ELEVENLABS_API_KEY'],
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.content

    @staticmethod
    def generate_lovo(prompt: str) -> str:
        """TTS using lovo.

        Parameters
        ----------
        prompt : str
            Input text.

        Returns
        -------
        str
            Url to audio.
        """
        url = "https://api.genny.lovo.ai/api/v1/tts/sync"

        payload = {
            "text": prompt,
            "speaker": "62e8c3581ffadc3ff72832aa"
        }
        headers = {
            "x-api-key": os.environ['LOVO_API_KEY'],
            "Content-Type": "application/json"
        }

        # It has timeout of 90 seconds, after that you would need to retrieve the recording
        response = requests.post(url, json=payload, headers=headers)

        return response.json()['data']['urls'][0]

    @staticmethod
    def generate_murf(prompt: str) -> str:
        """TTS using murf.ai.

        Parameters
        ----------
        prompt : str
            Input text.

        Returns
        -------
        str
            Url to audio.
        """
        url = "https://api.murf.ai/v1/speech/generate"

        payload = {
            "voiceId": "en-US-natalie",
            "text": prompt,
            "format": "MP3",
            "channelType": "MONO",
            "modelVersion": "GEN2",
        }
        headers = {
            "api-key": os.environ['MURF_API_KEY'],
            "Content-Type": "application/json"
        }

        # It has timeout of 90 seconds, after that you would need to retrieve the recording
        response = requests.post(url, json=payload, headers=headers)

        return response.json()['audioFile']

    def execute(self, prompt: str, provider) -> str:
        """TTS.

        Parameters
        ----------
        prompt : str
            Input text.
        provider
            Translation provider.

        Returns
        -------
        str
            Url to audio.
        """
        generate: Callable[[str], str] = None
        match provider:
            case "elevenlabs":
                generate = self.generate_elevenlabs
            case "lovo":
                generate = self.generate_lovo
            case "murf":
                generate = self.generate_murf

        return generate(prompt)


tts_generator = Generator()

provider = st.sidebar.selectbox(
    "Select model provider",
    ("elevenlabs", "lovo", "murf")
)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Hi, how is your day?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.audio(tts_generator.execute(prompt=text, provider=provider))
