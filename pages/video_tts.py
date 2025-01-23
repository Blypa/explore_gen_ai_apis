"""Streamlit page for Video TTS/Voiceover."""
import os
import time
from typing import Callable

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="Video TTS demo")

st.markdown("# Video TTS demo")
st.sidebar.header("Video TTS demo")
st.markdown("Please select provider in a sidebar.")


class Generator:
    """Class that contains all generate methods."""
    @staticmethod
    def video_generate_tavus(prompt: str) -> str:
        """Gnerate video TTS using tavus.

        Parameters
        ----------
        prompt : str
            Input prompt.

        Returns
        -------
        str
            Url to video.

        Raises
        ------
        Exception
            If video generation takes > 100 seconds of If video generation failed.
        """
        url = "https://tavusapi.com/v2/videos"

        payload = {
            "script": prompt,
            "replica_id": "r7dbef2aab"
        }
        headers = {
            "x-api-key": os.environ['TAVUS_API_KEY'],
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        video_id = response.json()['video_id']

        #FIXME tavus intends that we have a callback, but that would be a bit too much work to do in streamlit
        # So I will brute-force this, and yes, I know that this is not the best approach
        for __ in range(100):
            response = requests.get(
                f'https://tavusapi.com/v2/videos/{video_id}',
                headers=headers
            )
            video_status = response.json()['status']
            if video_status == 'ready':
                break
            elif video_status in ('deleted', 'error'):
                raise Exception(f'Video failed with status [{video_status}] - {response.json()['status_details']}')
            
            time.sleep(1)

        else:
            raise Exception(f'Failed to generate video in 100 seconds, aborting')

        return response.json()['download_url']

    def execute(self, prompt: str, provider) -> str:
        """Generate summarization.

        Parameters
        ----------
        prompt : str
            Input prompt
        provider
            TTS provider

        Returns
        -------
        str
            Url to video.
        """
        generate: Callable[[str], str] = None
        match provider:
            case "tavus.io":
                generate = self.video_generate_tavus

        return generate(prompt)


video_tts_generator = Generator()

provider = st.sidebar.selectbox(
    "Select model provider",
    ("tavus.io")
)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Hi, how is your day?.",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.video(video_tts_generator.execute(prompt=text, provider=provider))
