import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, \
    ChatCompletionMessageParam

from app.ai.schemas import ListWithScale

from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "ai" / "prompts" / "shopping_list_prompt.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

OLLAMA_LOCAL_URL = "http://localhost:11434/v1"
OLLAMA_MODEL = "qwen2.5:7b-instruct"
GPT_MODEL = "gpt-5.6-luna"

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

ollama = OpenAI(base_url=OLLAMA_LOCAL_URL, api_key='ollama')
gpt = OpenAI(api_key=api_key)

def get_ai_result(recipes_data: list[dict]) -> ListWithScale:
    user_content = json.dumps(
        recipes_data,
        ensure_ascii=False,
    )

    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(
            role="system",
            content=SYSTEM_PROMPT,
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=user_content,
        ),
    ]

    response = gpt.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("Model returned an empty response")

    return ListWithScale.model_validate_json(content)
