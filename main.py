
import os

from dotenv import load_dotenv
from openai import OpenAI
from tools import tools, execute_tool


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def ask_agent(user_message: str):
    response = client.responses.create(
        model="YOUR_MODEL_NAME",
        input=user_message,
        tools=tools,
    )

    return response

