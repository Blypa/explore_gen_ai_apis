"""Streamlit page for image generation."""

import os
from typing import Callable

import requests
import streamlit as st
from dotenv import load_dotenv

import replicate


load_dotenv()

st.set_page_config(page_title="Image generation demo")

st.markdown("# Image generation demo")
st.sidebar.header("Image generation demo")
st.markdown("Please select provider in a sidebar.")


class Generator:
    """Class that contains all generate methods."""
    @staticmethod
    def generate_stability(prompt: str) -> bytes:
        """Generate image using Stability AI ultra model.

        Parameters
        ----------
        prompt : str
            Input prompt for Text to Image

        Returns
        -------
        bytes
            Output image
        """
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
            headers={
                "authorization": f"Bearer {os.environ['STABILITY_AI_API_KEY']}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "webp",
            },
        )
        return response.content

    @staticmethod
    def generate_replicate(prompt: str) -> bytes:
        """Generate image using replicate.com and flux-1.1-pro

        Parameters
        ----------
        prompt : str
            Input prompt for Text to Image

        Returns
        -------
        bytes
            Output Image
        """
        client = replicate.Client(
            api_token=os.environ["REPLICATE_API_TOKEN"],
            headers={
                "User-Agent": "my-app/1.0",
            }
        )
        output = client.run(
            "black-forest-labs/flux-1.1-pro",
            input={"prompt": prompt}
        )
        return output.read()

    @staticmethod
    def generate_getimg_ai(prompt: str) -> bytes:
        """Generate image using getimg.ai and flux-schnell

        Parameters
        ----------
        prompt : str
            Input prompt for Text to Image

        Returns
        -------
        bytes
            Output Image
        """
        url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"

        payload = {
            "response_format": "url",
            "output_format": "png",
            "prompt": prompt
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {os.environ["GETIMG_AI_API_KEY"]}"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()['url']

    def execute(self, prompt: str, provider) -> bytes:
        """Generate image.

        Parameters
        ----------
        prompt : str
            Input prompt for Text to Image
        provider
            Provider for Image generation

        Returns
        -------
        bytes
            Output Image
        """
        generate: Callable[[str], bytes] = None
        match provider:
            case "Stability AI":
                generate = self.generate_stability
            case "replicate.com":
                generate = self.generate_replicate
            case "getimg.ai":
                generate = self.generate_getimg_ai

        return generate(prompt)


image_generator = Generator()

provider = st.sidebar.selectbox(
    "Select model provider",
    ("Stability AI", "replicate.com", "getimg.ai")
)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "High quality purple crystal in a cave.",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.image(image_generator.execute(prompt=text, provider=provider))
