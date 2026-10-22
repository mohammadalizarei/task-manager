import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

DB_FILE = "database.json"

def get_today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

get_today_date_schema = {
    "type": "function",
    "name": "get_today_date",
    "description": "Returns the current date in YYYY-MM-DD format.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "strict": True
}

def get_future_date(days: int) -> str:
    target_date = datetime.now() + timedelta(days=days)
    return target_date.strftime("%Y-%m-%d")

get_future_date_schema = {
    "type": "function",
    "name": "get_future_date",
    "description": "Calculates and returns the date after a given number of days from today in YYYY-MM-DD format.",
    "parameters": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "The number of days to add to the current date."
            }
        },
        "required": ["days"],
        "additionalProperties": False
    },
    "strict": True
}

def add_task(date: str, title: str, priority: Optional[str] = None) -> str:
    if not priority:
        priority = "medium"

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    day_entry = next((item for item in data if item["date"] == date), None)
    if not day_entry:
        day_entry = {
            "date": date,
            "tasks": [],
            "events": [],
            "meetings": []
        }
        data.append(day_entry)

    new_task = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "priority": priority,
        "status": "pending"
    }

    day_entry["tasks"].append(new_task)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return json.dumps(new_task, ensure_ascii=False)


add_task_schema = {
    "type": "function",
    "name": "add_task",
    "description": "Adds a new task for a specific date with status set to pending.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date for the task in YYYY-MM-DD format."
            },
            "title": {
                "type": "string",
                "description": "The title of the task."
            },
            "priority": {
                "type": ["string", "null"],
                "enum": ["low", "medium", "high", None],
                "description": "The priority of the task. Defaults to medium if null."
            }
        },
        "required": ["date", "title", "priority"],
        "additionalProperties": False
    },
    "strict": True
}