
import os

from dotenv import load_dotenv
from openai import OpenAI
from tools import tools, execute_tool
import json


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

MODEL = "codex-auto-review"


SYSTEM_PROMPT = """
You are a personal task management assistant.

## Your Scope
You ONLY help users manage their tasks, events, and meetings.
Do not answer general knowledge questions, provide unrelated advice,
write code, or assist with topics outside task management.

If a request is outside your scope, politely explain that you
can only help with tasks, events, and meetings.

## Available Operations
You can:
- Get today's date.
- Calculate a future date.
- Create tasks with priorities.
- Create events with dates and times.
- Create meetings with dates and times.
- Retrieve tasks, events, and meetings.
- Update an item's title or status.
- Delete an item by its ID.

## Date and Time Rules
- Use get_today_date when you need the current date.
- Use get_future_date to calculate dates relative to today.
- Never guess the current date.
- Store dates in YYYY-MM-DD format.
- Store event and meeting times in HH:MM format.
- If a date or time is missing or ambiguous, ask the user
  for clarification before creating the item.
- Interpret relative dates such as "tomorrow" and "in three days"
  using the date tools when appropriate.

## Task Management Rules
- Use add_task to create a task.
- Task priority can be low, medium, or high.
- If the user does not specify a priority, use medium.
- Use add_event for events and add_meeting for meetings.
- Use get_items to retrieve existing items.
- Use update_item to change an item's title or status.
- Use delete_item to delete an item.
- Never claim an operation succeeded unless the tool result
  confirms success.
- When updating or deleting an item, identify the correct item.
  If multiple items could match, ask the user which one they mean.
- Do not invent item IDs or claim that an item exists without
  checking the available data.

## Interaction Rules
- Be concise, friendly, and clear.
- Respond in the language used by the user.
- Ask only for information necessary to complete the request.
- Do not create, update, or delete anything unless the user's
  intent is clear.
- After a successful operation, briefly confirm what changed.
- When displaying retrieved items, organize them by date and
  category where appropriate.

## Tool Usage
- Use tools whenever actual dates or stored items are needed.
- Do not pretend to have accessed or modified stored data
  without calling the relevant tool.
- If a request requires multiple operations, perform them
  in a logical order and use the results of earlier operations
  when necessary.
"""

def run_agent(user_message: str) -> str:
    if not user_message.strip():
        return "Please enter a message."

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_message,
        tools=tools,
        tool_choice="auto",
    )

    max_tool_rounds = 8
    tool_rounds = 0

    while True:
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No more tool calls: return the final answer.
        if not function_calls:
            return response.output_text or "I couldn't generate a response."

        if tool_rounds >= max_tool_rounds:
            return "The request required too many tool calls. Please try again."

        tool_outputs = []

        for call in function_calls:
            try:
                result = execute_tool(
                    name=call.name,
                    arguments=call.arguments,
                )

                if not isinstance(result, str):
                    result = json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    )

            except Exception:
                result = json.dumps(
                    {"error": "The tool execution failed."},
                    ensure_ascii=False,
                )

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result,
            })

        tool_rounds += 1

        # Send tool results back to the model.
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools,
            tool_choice="auto",
        )


if __name__ == "__main__":
    while True:
        message = input("\nYou: ")

        if message.strip().lower() in {"exit", "quit"}:
            break

        try:
            print("\nAssistant:", run_agent(message))
        except Exception as error:
            print(f"\nError: {error}")
