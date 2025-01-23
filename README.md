# explore_gen_ai_apis

This project contains exploration of some of available API's, here is a short list of tasks and API's used:

1. Image generation:
   1. Stability AI
   2. replicate.com
   3. getimg.ai
2. Text summarization using LangChain
   1. OpenAI
   2. Anthropic
   3. Google Vertex
3. Text summarization w/out LangChain
   1. OpenAI
   2. Anthropic
   3. TogetherAI
4. Video TTS (Voiceover)
   1. tavus.ai
5. TTS
   1. elevenlabs
   2. ~~lovo~~
   3. murf
6. Translation
   1. rapidapi
   2. deepl

## Setup

1. You need to create `.env` file in project directory, here is an example of such file

```bash
# LLM
OPENAI_API_KEY=<api-key>
ANTHROPIC_API_KEY=<api-key>
TOGETHER_API_KEY=<api-key>
GOOGLE_APPLICATION_CREDENTIALS="./credentials/service_account.json"

# Image gen
STABILITY_AI_API_KEY=<api-key>
REPLICATE_API_TOKEN=<api-key>
GETIMG_AI_API_KEY=<api-key>

# Video tts
TAVUS_API_KEY=<api-key>

# TTS
ELEVENLABS_API_KEY=<api-key>
LOVO_API_KEY=<api-key>
MURF_API_KEY=<api-key>

# Translation
RAPIDAPI_API_KEY=<api-key>
DEEPL_API_KEY=<api-key>

```

2. To enable Vertex you need to place `service_account.json` file - service account credentials in `./credentials`
3. Run `poetry install`

## Usage

1. Run `poetry run streamlit run st_entrypoint.py`
2. Go to [demo_website](http://localhost:8501)
3. Select a demo you are interested in a sidebar.

## Demo

[Google Drive](https://drive.google.com/file/d/18queIjy7OPOuyC-XTuw2RbubCedYwk04/view?usp=sharing) - here you can see a usage demo for this repository.
