import json

from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, \
    ChatCompletionMessageParam

from scraper import fetch_recipe_data

SYSTEM_PROMPT = """
"""

OLLAMA_LOCAL_URL = "http://localhost:11434/v1"
OLLAMA_MODEL = "qwen2.5-coder:7b"
OLLAMA_FALLBACK_MODEL = "gemma4:latest"

ollama = OpenAI(base_url=OLLAMA_LOCAL_URL, api_key='ollama')

def get_ollama_recipe(url: str):
    print("Fetching website contents...")
    ingredients_and_servings = fetch_recipe_data(url)


    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(
            role="system",
            content=SYSTEM_PROMPT,
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content="placeholder",
        ),
    ]

    print("Sending request to Ollama...")
    response = ollama.chat.completions.create(model=OLLAMA_MODEL, messages=messages, temperature=0)
    print(response.choices[0].message.content)
    return response.choices[0].message.content
