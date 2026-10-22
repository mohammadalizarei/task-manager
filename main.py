import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from tools import tools, execute_tool

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """
You are a task management assistant.

You can only help users manage:
- Tasks
- Events
- Meetings

Use the available tools to create, retrieve, update, and delete items.
Use get_today_date to determine today's date.
Use get_future_date for relative future dates.
Dates must use YYYY-MM-DD and times must use HH:MM.

Ask the user if required information is missing or ambiguous.
New tasks have medium priority by default.
Never invent data or claim an action succeeded unless a tool confirms it.
Do not promise operations that the tools cannot perform.
Keep answers concise and reply in the user's language.
"""

conversation_history = []

def run_agent(user_message):
    
    conversation_history.append({
    "role": "user",
    "content": user_message
    })

    input_list = conversation_history.copy()

    while True:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=tools,
            input=input_list,
        )

        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            conversation_history.extend(response.output)
            return response.output_text

        input_list.extend(response.output)
        conversation_history.extend(response.output)

        for call in function_calls:
            try:
                result = execute_tool(call.name, call.arguments)
            except Exception as error:
                result = json.dumps({
                    "error": str(error)
                }, ensure_ascii=False)

            input_list.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": str(result),
            })
            conversation_history.append(input_list[-1])



if __name__ == "__main__":
    print("Task Manager Agent: Type 'exit' or 'quit' to end the conversation.")

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() in ["exit", "quit"]:
            break

        if not user_message:
            continue

        try:
            answer = run_agent(user_message)
            print(f"\nAgent: {answer}")
        except Exception as error:
            print(f"\nError: {error}")
