import os
from ai.prompt import parse_prompt_file
from typing import TypedDict, List


class AIConfig(TypedDict):
    model: str
    max_tokens: int
    temperature: float


class Message(TypedDict):
    role: str
    content: str


class PromptFile(TypedDict):
    messages: List[Message]
    config: AIConfig


def get_api_key() -> str:
    api_key = os.getenv('OPENAI_API_KEY')

    # If the api key was not found, ask if from the user
    if not api_key:
        # Get the API key from th e use
        api_key = input(
            'OpenAI API key is missing, please enter your API key: ')

        if not api_key:
            print('API key was not provided!')
            return

    return api_key


def get_prompt_file(prompt_file_name: str, context: dict) -> PromptFile:
    prompt_file = parse_prompt_file(
        os.path.join(os.getcwd(), 'ai', 'prompts', prompt_file_name + '.yaml'),
        context)

    return prompt_file
